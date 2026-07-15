#!/usr/bin/env python3
"""
xcresult_parser.py
Runs xcodebuild test suites, extracts test failure details, exports attachments/screenshots,
and produces a consolidated JSON report suitable for LLM self-healing context.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from urllib.parse import urlparse, parse_qs


def pre_parse_config() -> str | None:
    """Pre-parse to determine if a config file is supplied."""
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--config", type=str, default=None)
    pre_args, _ = pre_parser.parse_known_args()
    return pre_args.config


def main() -> int:
    # 1. Load config if specified, otherwise fall back to relative default config path
    config_path = pre_parse_config()
    if config_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "..", "resources", "test_options.json")

    defaults = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                defaults = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load configuration from {config_path}: {e}", file=sys.stderr)

    # 2. Main Argument Parser
    parser = argparse.ArgumentParser(
        description="Run Xcode tests and parse test failures and attachments from .xcresult bundles."
    )
    parser.add_argument("--config", type=str, default=None, help="Path to config JSON file.")
    parser.add_argument("--workspace", type=str, default=defaults.get("workspace"), help="Path to .xcworkspace.")
    parser.add_argument("--project", type=str, default=defaults.get("project"), help="Path to .xcodeproj.")
    parser.add_argument("--scheme", type=str, default=defaults.get("scheme"), help="Scheme name to test.")
    parser.add_argument(
        "--destination",
        type=str,
        default=defaults.get("destination", "platform=iOS Simulator,name=iPhone 15"),
        help="Target destination for testing."
    )
    parser.add_argument(
        "--result-bundle-path",
        type=str,
        default=defaults.get("result_bundle_path", "./build/TestResults.xcresult"),
        help="Path where .xcresult bundle should be written."
    )
    parser.add_argument(
        "--output-report",
        type=str,
        default=defaults.get("output_report", "./build/test_report.json"),
        help="JSON file path where parsed results will be saved."
    )
    parser.add_argument(
        "--export-attachments-dir",
        type=str,
        default=defaults.get("export_attachments_dir", "./build/Attachments"),
        help="Directory where test failure attachments will be exported."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        default=defaults.get("clean", False),
        help="Whether to perform a clean before testing."
    )
    parser.add_argument(
        "--only-failures",
        action="store_true",
        default=defaults.get("only_failures", True),
        help="Only export attachments for failed tests."
    )
    parser.add_argument(
        "xcodebuild_args",
        nargs=argparse.REMAINDER,
        help="Arbitrary extra arguments to forward to xcodebuild."
    )

    args = parser.parse_args()

    # 3. Build & Run xcodebuild command
    xcode_cmd = ["xcodebuild", "test"]
    if args.workspace:
        xcode_cmd.extend(["-workspace", args.workspace])
    elif args.project:
        xcode_cmd.extend(["-project", args.project])

    if args.scheme:
        xcode_cmd.extend(["-scheme", args.scheme])

    if args.destination:
        xcode_cmd.extend(["-destination", args.destination])

    if args.result_bundle_path:
        rb_path = os.path.abspath(args.result_bundle_path)
        # Xcodebuild fails if resultBundlePath already exists; clean it first
        if os.path.exists(rb_path):
            print(f"Cleaning existing result bundle at {rb_path}...")
            if os.path.isdir(rb_path):
                shutil.rmtree(rb_path)
            else:
                os.remove(rb_path)
        xcode_cmd.extend(["-resultBundlePath", rb_path])

    if args.clean:
        xcode_cmd.append("clean")

    if args.xcodebuild_args:
        # Filter out potential double hyphen issues if remainder gets parsed weirdly
        extra_args = [a for a in args.xcodebuild_args if a != "--"]
        xcode_cmd.extend(extra_args)

    print(f"Executing: {' '.join(xcode_cmd)}")
    sys.stdout.flush()

    # Launch tests
    test_proc = subprocess.run(xcode_cmd)
    exit_code = test_proc.returncode

    # 4. Parse Results
    failures = []
    summary_stats = {
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "skipped_tests": 0
    }
    status = "passed"
    error_msg = None

    result_bundle = os.path.abspath(args.result_bundle_path)
    if os.path.exists(result_bundle):
        try:
            # A. Query object graph for issues
            get_cmd = ["xcrun", "xcresulttool", "get", "--format", "json", "--path", result_bundle]
            get_proc = subprocess.run(get_cmd, capture_output=True, text=True, check=True)
            data = json.loads(get_proc.stdout)

            # Pull failure summaries
            raw_failures = []
            
            # Root level issues
            root_issues = data.get("issues", {})
            raw_failures.extend(root_issues.get("testFailureSummaries", {}).get("_values", []))

            # Action level issues
            actions = data.get("actions", {}).get("_values", [])
            for action in actions:
                action_res = action.get("actionResult", {})
                action_issues = action_res.get("issues", {})
                raw_failures.extend(action_issues.get("testFailureSummaries", {}).get("_values", []))

            # Deduplicate failures
            seen = set()
            for fail in raw_failures:
                test_case_name = fail.get("testCaseName", {}).get("_value")
                message = fail.get("message", {}).get("_value")
                
                doc_loc = fail.get("documentLocationInCreatingWorkspace", {})
                url = doc_loc.get("url", {}).get("_value")

                fail_key = (test_case_name, message, url)
                if fail_key in seen:
                    continue
                seen.add(fail_key)

                # Parse URL for file and line number
                file_path = None
                line_number = None
                if url:
                    try:
                        parsed_url = urlparse(url)
                        file_path = parsed_url.path
                        if parsed_url.fragment:
                            fragment_params = parse_qs(parsed_url.fragment)
                            # Convert 0-indexed URLs to 1-indexed editor lines
                            if "StartingLineNumber" in fragment_params:
                                line_number = int(fragment_params["StartingLineNumber"][0]) + 1
                            elif "EndingLineNumber" in fragment_params:
                                line_number = int(fragment_params["EndingLineNumber"][0]) + 1
                            elif "LineNumber" in fragment_params:
                                line_number = int(fragment_params["LineNumber"][0])
                    except Exception:
                        pass

                failures.append({
                    "test_case_name": test_case_name,
                    "message": message,
                    "file_path": file_path,
                    "line_number": line_number,
                    "url": url,
                    "screenshots": []
                })

            # B. Get summary counts
            sum_cmd = ["xcrun", "xcresulttool", "get", "test-results", "summary", "--path", result_bundle]
            sum_proc = subprocess.run(sum_cmd, capture_output=True, text=True)
            if sum_proc.returncode == 0:
                try:
                    summary_data = json.loads(sum_proc.stdout)
                    summary_stats["total_tests"] = summary_data.get("totalTestCount", 0)
                    summary_stats["passed_tests"] = summary_data.get("passedTests", 0)
                    summary_stats["failed_tests"] = summary_data.get("failedTests", 0)
                    summary_stats["skipped_tests"] = summary_data.get("skippedTests", 0)
                except Exception:
                    pass
            else:
                summary_stats["failed_tests"] = len(failures)
                summary_stats["total_tests"] = len(failures)

            if summary_stats["failed_tests"] > 0 or len(failures) > 0:
                status = "failed"

            # C. Export screenshots and map them
            if args.export_attachments_dir:
                export_dir = os.path.abspath(args.export_attachments_dir)
                os.makedirs(export_dir, exist_ok=True)
                
                manifest_path = os.path.join(export_dir, "manifest.json")
                if os.path.exists(manifest_path):
                    os.remove(manifest_path)

                export_cmd = [
                    "xcrun", "xcresulttool", "export", "attachments",
                    "--path", result_bundle,
                    "--output-path", export_dir
                ]
                if args.only_failures:
                    export_cmd.append("--only-failures")

                subprocess.run(export_cmd, capture_output=True, text=True)

                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, "r") as f:
                            attachments_data = json.load(f)

                        for test_detail in attachments_data:
                            test_id = test_detail.get("testIdentifier")
                            test_id_url = test_detail.get("testIdentifierURL")
                            attachments = test_detail.get("attachments", [])

                            for fail in failures:
                                match = False
                                if test_id and fail["test_case_name"]:
                                    norm_test_id = test_id.replace("/", ".").replace("()", "")
                                    norm_fail_name = fail["test_case_name"].replace("()", "")
                                    if norm_test_id == norm_fail_name or norm_test_id in norm_fail_name or norm_fail_name in norm_test_id:
                                        match = True

                                if not match and test_id_url and fail["url"]:
                                    if test_id_url in fail["url"]:
                                        match = True

                                if match:
                                    for att in attachments:
                                        if not args.only_failures or att.get("isAssociatedWithFailure"):
                                            file_name = att.get("exportedFileName")
                                            full_path = os.path.abspath(os.path.join(export_dir, file_name))
                                            fail["screenshots"].append({
                                                "file_name": file_name,
                                                "path": full_path,
                                                "name": att.get("suggestedHumanReadableName"),
                                                "device_name": att.get("deviceName"),
                                                "device_id": att.get("deviceId")
                                            })
                    except Exception as e:
                        print(f"Warning: Failed to parse attachments manifest.json: {e}", file=sys.stderr)

        except Exception as e:
            status = "build_error"
            error_msg = f"Failed parsing result bundle: {e}"
    else:
        status = "build_error"
        error_msg = f"Result bundle not found at: {result_bundle}. Xcodebuild compilation may have failed."

    # 5. Output Report
    report = {
        "status": status,
        "summary": summary_stats,
        "failures": failures,
        "xcodebuild_exit_code": exit_code,
        "error_message": error_msg
    }

    if args.output_report:
        report_output = os.path.abspath(args.output_report)
        report_dir = os.path.dirname(report_output)
        if report_dir:
            os.makedirs(report_dir, exist_ok=True)
        try:
            with open(report_output, "w") as f:
                json.dump(report, f, indent=2)
            print(f"Report written to: {report_output}")
        except Exception as e:
            print(f"Error: Failed to write report file: {e}", file=sys.stderr)

    # 6. Display CLI summary
    print("\n" + "=" * 60)
    print(f"TEST SUITE STATUS: {status.upper()}")
    print("=" * 60)
    print(f"Total Tests:   {summary_stats['total_tests']}")
    print(f"Passed:        {summary_stats['passed_tests']}")
    print(f"Failed:        {summary_stats['failed_tests']}")
    print(f"Skipped:       {summary_stats['skipped_tests']}")
    if error_msg:
        print(f"Error:         {error_msg}")
    
    if failures:
        print("\nFailing Tests Details:")
        for i, fail in enumerate(failures, 1):
            print(f"  {i}. {fail['test_case_name']}")
            print(f"     Location:   {fail['file_path']}:{fail['line_number']}")
            print(f"     Message:    {fail['message']}")
            if fail["screenshots"]:
                print(f"     Screenshots ({len(fail['screenshots'])}):")
                for s in fail["screenshots"]:
                    print(f"       - {s['file_name']} [{s['name']}] ({s['device_name']})")
    print("=" * 60 + "\n")

    return 0 if status == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
