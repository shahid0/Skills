#!/usr/bin/env python3
"""
compile_auditor.py - Assets and Interface Builder compilation auditor.
Compiles and audits asset catalogs (actool) and Interface Builder storyboards/XIBs (ibtool).
Parses warning/error plist outputs and produces formatted reports.
"""

import argparse
import json
import os
import plistlib
import re
import subprocess
import sys
import tempfile

DEFAULT_RULES = {
    "missing_images": {
        "severity": "error",
        "category": "asset",
        "keywords": ["not found", "missing", "does not exist", "unassigned child", "no image"]
    },
    "mismatched_dimensions": {
        "severity": "warning",
        "category": "asset",
        "keywords": ["dimension", "scale", "pixel", "size", "resolution", "idiom"]
    },
    "unsupported_format": {
        "severity": "error",
        "category": "asset",
        "keywords": ["unsupported format", "color space", "profile", "png", "jpeg"]
    },
    "misaligned_layout": {
        "severity": "warning",
        "category": "layout",
        "keywords": ["constraint", "frame for", "will be different", "ambiguous layout", "misaligned"]
    },
    "localization_warning": {
        "severity": "warning",
        "category": "localization",
        "keywords": ["localization", "not localized", "missing translation", "localizable"]
    },
    "compile_error": {
        "severity": "error",
        "category": "compilation",
        "keywords": ["failed to compile", "compilation error", "unable to resolve", "syntactic error"]
    }
}

SEVERITY_ORDER = {
    "info": 0,
    "warning": 1,
    "error": 2
}

def load_rules(config_path):
    """Loads rules from config path, fallback to DEFAULT_RULES if not found."""
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                return config_data.get("rules", DEFAULT_RULES)
        except Exception as e:
            print(f"Warning: Failed to load config from {config_path}: {e}. Using default rules.", file=sys.stderr)
    
    # Try loading from default relative path if config_path not provided
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_config = os.path.join(script_dir, "..", "resources", "lint_rules.json")
    if os.path.exists(default_config):
        try:
            with open(default_config, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                return config_data.get("rules", DEFAULT_RULES)
        except Exception:
            pass

    return DEFAULT_RULES

def map_issue(description, file_path, default_severity, rules):
    """Maps a warning/error message to a category and severity based on rules."""
    desc_lower = description.lower()
    matched_rule = None
    
    for _, rule_val in rules.items():
        keywords = rule_val.get("keywords", [])
        if any(kw in desc_lower for kw in keywords):
            matched_rule = rule_val
            break
            
    if matched_rule:
        severity = matched_rule.get("severity", default_severity)
        category = matched_rule.get("category", "general")
    else:
        severity = default_severity
        category = "general"
        
    return {
        "description": description,
        "file": file_path,
        "severity": severity,
        "category": category
    }

def parse_plist_output(output_bytes):
    """Parses XML plist from command output bytes."""
    if not output_bytes:
        return None
    try:
        return plistlib.loads(output_bytes)
    except Exception:
        # Fallback: Extract XML plist block if surrounded by non-XML output
        match = re.search(b'(<\\?xml.*?</plist>)', output_bytes, re.DOTALL)
        if match:
            try:
                return plistlib.loads(match.group(1))
            except Exception:
                pass
    return None

def extract_issues_from_plist(plist_dict, file_path, rules):
    """Extracts warnings, errors, and notices from actool/ibtool plist output."""
    issues = []
    
    # Keys mapping plist outputs to default severities
    key_mappings = {
        # Errors
        "com.apple.actool.document.errors": "error",
        "com.apple.actool.errors": "error",
        "com.apple.ibtool.document.errors": "error",
        "com.apple.ibtool.errors": "error",
        
        # Warnings
        "com.apple.actool.document.warnings": "warning",
        "com.apple.actool.warnings": "warning",
        "com.apple.ibtool.document.warnings": "warning",
        "com.apple.ibtool.warnings": "warning",
        
        # Notices
        "com.apple.actool.document.notices": "info",
        "com.apple.actool.notices": "info",
        "com.apple.ibtool.document.notices": "info",
        "com.apple.ibtool.notices": "info",
    }
    
    if not isinstance(plist_dict, dict):
        return issues
        
    for plist_key, default_severity in key_mappings.items():
        items = plist_dict.get(plist_key, [])
        if not isinstance(items, list):
            continue
            
        for item in items:
            if isinstance(item, dict):
                description = item.get("description") or item.get("message")
                item_file = item.get("file") or item.get("document") or file_path
                if not description:
                    continue
                issues.append(map_issue(description, item_file, default_severity, rules))
            elif isinstance(item, str):
                issues.append(map_issue(item, file_path, default_severity, rules))
                
    return issues

def audit_asset_catalog(asset_path, output_dir, platform, min_target, app_icon, rules):
    """Compiles and audits an asset catalog (.xcassets) using actool."""
    issues = []
    if not os.path.exists(asset_path):
        issues.append(map_issue(f"Asset catalog path does not exist: {asset_path}", asset_path, "error", rules))
        return issues

    cmd = [
        "xcrun", "actool", asset_path,
        "--compile", output_dir,
        "--platform", platform,
        "--minimum-deployment-target", min_target,
        "--output-format", "xml1",
        "--errors", "--warnings", "--notices"
    ]
    
    if app_icon:
        cmd.extend(["--app-icon", app_icon])

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        # actool prints plist format on stdout
        plist_dict = parse_plist_output(result.stdout)
        if plist_dict:
            issues.extend(extract_issues_from_plist(plist_dict, asset_path, rules))
        else:
            if result.returncode != 0:
                err_msg = result.stderr.decode("utf-8", errors="replace").strip()
                if not err_msg:
                    err_msg = result.stdout.decode("utf-8", errors="replace").strip() or f"Tool exited with code {result.returncode}"
                issues.append(map_issue(f"actool compilation failed: {err_msg}", asset_path, "error", rules))
    except Exception as e:
        issues.append(map_issue(f"Failed to execute actool: {str(e)}", asset_path, "error", rules))
        
    return issues

def audit_storyboard_or_xib(file_path, output_dir, platform, min_target, rules):
    """Audits a storyboard or XIB file using ibtool."""
    issues = []
    if not os.path.exists(file_path):
        issues.append(map_issue(f"Storyboard/XIB file path does not exist: {file_path}", file_path, "error", rules))
        return issues

    base, ext = os.path.splitext(os.path.basename(file_path))
    if ext == ".storyboard":
        out_file = os.path.join(output_dir, f"{base}.storyboardc")
    else:
        out_file = os.path.join(output_dir, f"{base}.nib")

    cmd = [
        "xcrun", "ibtool", file_path,
        "--compile", out_file,
        "--target-device", "iphone" if platform in ["iphoneos", "iphonesimulator"] else "ipad",
        "--minimum-deployment-target", min_target,
        "--output-format", "xml1",
        "--errors", "--warnings", "--notices"
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        # ibtool prints plist format on stdout
        plist_dict = parse_plist_output(result.stdout)
        if plist_dict:
            issues.extend(extract_issues_from_plist(plist_dict, file_path, rules))
        else:
            if result.returncode != 0:
                err_msg = result.stderr.decode("utf-8", errors="replace").strip()
                if not err_msg:
                    err_msg = result.stdout.decode("utf-8", errors="replace").strip() or f"Tool exited with code {result.returncode}"
                issues.append(map_issue(f"ibtool compilation failed: {err_msg}", file_path, "error", rules))
    except Exception as e:
        issues.append(map_issue(f"Failed to execute ibtool: {str(e)}", file_path, "error", rules))

    # Optional second-pass check: check for localized strings issues if plist extraction works
    return issues

def find_files_by_ext(dir_path, extensions):
    """Recursively search for files with specified extensions."""
    found_files = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                found_files.append(os.path.join(root, file))
    return found_files

def generate_text_report(issues, min_severity):
    """Generates a user-friendly and Xcode-compatible console report."""
    filtered_issues = [i for i in issues if SEVERITY_ORDER.get(i["severity"], 0) >= SEVERITY_ORDER.get(min_severity, 0)]
    
    if not filtered_issues:
        print("🎉 No lint issues found matching target severity threshold!")
        return 0

    counts = {"error": 0, "warning": 0, "info": 0}
    for issue in filtered_issues:
        sev = issue["severity"]
        counts[sev] = counts.get(sev, 0) + 1
        
        # Xcode friendly format: path:line: severity: message
        # Default line is 1 as compilation/asset errors apply to the whole file.
        sev_tag = "error" if sev == "error" else ("warning" if sev == "warning" else "note")
        print(f"{issue['file']}:1: {sev_tag}: [{issue['category']}] {issue['description']}")
        
    print(f"\n📈 Audit Summary: Errors: {counts['error']} | Warnings: {counts['warning']} | Notices: {counts['info']}")
    return counts["error"] + counts["warning"]

def generate_json_report(issues, min_severity):
    """Generates a JSON dump of issues."""
    filtered_issues = [i for i in issues if SEVERITY_ORDER.get(i["severity"], 0) >= SEVERITY_ORDER.get(min_severity, 0)]
    
    counts = {"error": 0, "warning": 0, "info": 0, "total": len(filtered_issues)}
    for issue in filtered_issues:
        sev = issue["severity"]
        counts[sev] = counts.get(sev, 0) + 1

    report = {
        "summary": counts,
        "issues": filtered_issues
    }
    
    print(json.dumps(report, indent=2))
    return counts["error"] + counts["warning"]

def generate_markdown_report(issues, min_severity):
    """Generates a Markdown format table report."""
    filtered_issues = [i for i in issues if SEVERITY_ORDER.get(i["severity"], 0) >= SEVERITY_ORDER.get(min_severity, 0)]
    
    severity_icons = {
        "error": "🔴 Error",
        "warning": "🟡 Warning",
        "info": "🔵 Info"
    }

    print("# Asset and Layout Lint Report\n")
    
    if not filtered_issues:
        print("🎉 No issues found matching threshold.")
        return 0

    print("| Severity | Category | File | Description |")
    print("| :--- | :--- | :--- | :--- |")
    
    counts = {"error": 0, "warning": 0, "info": 0}
    for issue in filtered_issues:
        sev = issue["severity"]
        counts[sev] = counts.get(sev, 0) + 1
        
        icon = severity_icons.get(sev, sev.upper())
        escaped_desc = issue['description'].replace("|", "\\|").replace("\n", " ")
        print(f"| {icon} | {issue['category']} | `{os.path.basename(issue['file'])}` | {escaped_desc} |")
        
    print("\n## Summary")
    print(f"- **Errors**: {counts['error']}")
    print(f"- **Warnings**: {counts['warning']}")
    print(f"- **Info/Notices**: {counts['info']}")
    print(f"- **Total Issues**: {len(filtered_issues)}")
    
    return counts["error"] + counts["warning"]

def main():
    parser = argparse.ArgumentParser(
        description="Compile and audit asset catalogs (actool) and Interface Builder storyboards (ibtool) for warnings and errors."
    )
    parser.add_argument(
        "--assets",
        nargs="+",
        help="Paths to asset catalogs (.xcassets) to audit."
    )
    parser.add_argument(
        "--storyboards",
        nargs="+",
        help="Paths to storyboard (.storyboard) or XIB (.xib) files or directories containing them."
    )
    parser.add_argument(
        "--platform",
        default="iphoneos",
        help="Target platform for compilation (e.g., iphoneos, iphonesimulator, macosx). Default: iphoneos"
    )
    parser.add_argument(
        "--minimum-deployment-target",
        default="14.0",
        help="Minimum deployment target version. Default: 14.0"
    )
    parser.add_argument(
        "--app-icon",
        help="Name of the app icon set to compile/verify (optional)."
    )
    parser.add_argument(
        "--config",
        help="Path to lint rules JSON configuration file."
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format of the audit report. Default: text"
    )
    parser.add_argument(
        "--severity",
        choices=["info", "warning", "error"],
        default="info",
        help="Minimum severity level to include in the report. Default: info"
    )
    parser.add_argument(
        "--output-dir",
        help="Custom output directory for compiled artifacts. If not provided, a temporary directory is used."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail (exit code 1) if any warnings or errors matching the severity threshold are found."
    )
    
    args = parser.parse_args()
    
    # Check that at least one audit type is specified
    if not args.assets and not args.storyboards:
        parser.print_help()
        sys.exit(0)
        
    rules = load_rules(args.config)
    issues = []
    
    # Establish compile output folder
    temp_dir_obj = None
    if args.output_dir:
        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)
    else:
        temp_dir_obj = tempfile.TemporaryDirectory()
        output_dir = temp_dir_obj.name

    try:
        # Audit Asset Catalogs
        if args.assets:
            for asset_path in args.assets:
                issues.extend(
                    audit_asset_catalog(
                        asset_path,
                        output_dir,
                        args.platform,
                        args.minimum_deployment_target,
                        args.app_icon,
                        rules
                    )
                )
                
        # Audit Storyboards & XIBs
        if args.storyboards:
            resolved_storyboards = []
            for path in args.storyboards:
                if os.path.isdir(path):
                    resolved_storyboards.extend(find_files_by_ext(path, [".storyboard", ".xib"]))
                else:
                    resolved_storyboards.append(path)
                    
            for file_path in resolved_storyboards:
                issues.extend(
                    audit_storyboard_or_xib(
                        file_path,
                        output_dir,
                        args.platform,
                        args.minimum_deployment_target,
                        rules
                    )
                )
    finally:
        if temp_dir_obj:
            try:
                temp_dir_obj.cleanup()
            except Exception:
                pass
                
    # Report output
    total_relevant_issues = 0
    if args.format == "json":
        total_relevant_issues = generate_json_report(issues, args.severity)
    elif args.format == "markdown":
        total_relevant_issues = generate_markdown_report(issues, args.severity)
    else:
        total_relevant_issues = generate_text_report(issues, args.severity)
        
    if args.strict and total_relevant_issues > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
