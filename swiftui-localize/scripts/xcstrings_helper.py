#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile


def run_command(cmd, description):
    """Runs a shell command and returns the stdout. Raises subprocess.CalledProcessError on failure."""
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}:", file=sys.stderr)
        print("Command:", " ".join(cmd), file=sys.stderr)
        print("Exit Code:", e.returncode, file=sys.stderr)
        print("Stdout:", e.stdout, file=sys.stderr)
        print("Stderr:", e.stderr, file=sys.stderr)
        raise e


def check_variations_translated(variations):
    """Recursively checks if all variation stringUnits are translated and have values."""
    if not isinstance(variations, dict):
        return False
    string_units = []

    def traverse(d):
        if not isinstance(d, dict):
            return
        if "stringUnit" in d:
            string_units.append(d["stringUnit"])
        else:
            for k, v in d.items():
                traverse(v)

    traverse(variations)
    if not string_units:
        return False
    return all(
        isinstance(u, dict)
        and u.get("state") == "translated"
        and u.get("value") is not None
        for u in string_units
    )


def is_key_translated(entry, locale):
    """Returns True if the string catalog entry is fully translated for the specified locale."""
    if not isinstance(entry, dict):
        return False
    localizations = entry.get("localizations", {})
    if locale not in localizations:
        return False

    locale_data = localizations[locale]
    if not isinstance(locale_data, dict):
        return False

    # Check for simple string unit
    if "stringUnit" in locale_data:
        unit = locale_data["stringUnit"]
        if (
            isinstance(unit, dict)
            and unit.get("state") == "translated"
            and unit.get("value") is not None
        ):
            return True
        return False

    # Check for variations (plurals, devices, etc.)
    if "variations" in locale_data:
        return check_variations_translated(locale_data["variations"])

    return False


def cmd_extract(args):
    """Runs xcrun xcstringstool extract to pull localizable strings into an .xcstrings file."""
    xcstrings_path = os.path.abspath(args.xcstrings_path)
    output_dir = os.path.dirname(xcstrings_path) or "."
    table_name = os.path.splitext(os.path.basename(xcstrings_path))[0]

    # Pre-create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # If the file does not exist, initialize it with a basic template to prevent issues
    if not os.path.exists(xcstrings_path):
        initial_json = {
            "sourceLanguage": args.source_language,
            "strings": {},
            "version": "1.0",
        }
        with open(xcstrings_path, "w", encoding="utf-8") as f:
            json.dump(initial_json, f, indent=2)

    # Build xcstringstool command
    cmd = ["xcrun", "xcstringstool", "extract"]

    # Source files/directories
    for src in args.source_files:
        cmd.append(os.path.abspath(src))

    cmd.extend(
        [
            "--output-directory",
            output_dir,
            "--output-format",
            "xcstrings",
            "--table",
            table_name,
        ]
    )

    if args.append:
        cmd.append("--append")

    if args.swiftui:
        cmd.append("--SwiftUI")

    if args.modern:
        cmd.append("--modern-localizable-strings")

    if args.legacy:
        cmd.append("--legacy-localizable-strings")

    print(f"Running extract command: {' '.join(cmd)}")
    run_command(cmd, "strings extraction")
    print(f"Strings successfully extracted and merged into {xcstrings_path}")


def cmd_list_missing(args):
    """Finds and lists keys in the .xcstrings catalog missing translations for a locale."""
    xcstrings_path = os.path.abspath(args.xcstrings_path)
    if not os.path.exists(xcstrings_path):
        print(f"Error: Catalog file not found at {xcstrings_path}", file=sys.stderr)
        sys.exit(1)

    with open(xcstrings_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    source_lang = catalog.get("sourceLanguage", "en")
    strings = catalog.get("strings", {})

    missing_keys = []
    for key, entry in strings.items():
        if not is_key_translated(entry, args.locale):
            comment = entry.get("comment", "")
            missing_keys.append({"key": key, "comment": comment})

    # Output JSON or list format
    if args.json:
        output_data = {
            "sourceLanguage": source_lang,
            "targetLanguage": args.locale,
            "missingCount": len(missing_keys),
            "missing": missing_keys,
        }
        print(json.dumps(output_data, indent=2, ensure_ascii=False))
    else:
        print(
            f"Found {len(missing_keys)} missing translation(s) for locale '{args.locale}':"
        )
        for i, item in enumerate(missing_keys, start=1):
            comment_str = f" // Comment: {item['comment']}" if item["comment"] else ""
            print(f"{i}. Key: \"{item['key']}\"{comment_str}")


def cmd_merge(args):
    """Merges translated strings back into the .xcstrings catalog."""
    xcstrings_path = os.path.abspath(args.xcstrings_path)
    if not os.path.exists(xcstrings_path):
        print(f"Error: Catalog file not found at {xcstrings_path}", file=sys.stderr)
        sys.exit(1)

    # Resolve translations
    translations_raw = args.translations.strip()
    if os.path.exists(translations_raw):
        with open(translations_raw, "r", encoding="utf-8") as f:
            translations = json.load(f)
    else:
        try:
            translations = json.loads(translations_raw)
        except json.JSONDecodeError as e:
            print(
                f"Error: translations must be a path to a JSON file or a valid JSON string. Error: {e}",
                file=sys.stderr,
            )
            sys.exit(1)

    if not isinstance(translations, dict):
        print(
            "Error: Translations JSON must be a dictionary/object of keys to values.",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(xcstrings_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    if "strings" not in catalog:
        catalog["strings"] = {}

    merged_count = 0
    for key, value in translations.items():
        if key not in catalog["strings"]:
            catalog["strings"][key] = {"extractionState": "manual"}

        entry = catalog["strings"][key]
        if "localizations" not in entry:
            entry["localizations"] = {}

        locale_dict = entry["localizations"]

        if isinstance(value, str):
            locale_dict[args.locale] = {
                "stringUnit": {"state": "translated", "value": value}
            }
            merged_count += 1
        elif isinstance(value, dict):
            # Allow structured merging for plurals/variations
            locale_dict[args.locale] = value
            merged_count += 1
        else:
            print(
                f"Warning: Skipping key '{key}' because translation value type '{type(value).__name__}' is invalid.",
                file=sys.stderr,
            )

    with open(xcstrings_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(
        f"Successfully merged {merged_count} translation(s) for locale '{args.locale}' into {xcstrings_path}."
    )


def cmd_compile(args):
    """Compiles the .xcstrings file using xcrun xcstringstool compile to verify correctness."""
    xcstrings_path = os.path.abspath(args.xcstrings_path)
    if not os.path.exists(xcstrings_path):
        print(f"Error: Catalog file not found at {xcstrings_path}", file=sys.stderr)
        sys.exit(1)

    # Use specified output directory or a temporary one
    output_dir = args.output_dir
    is_temp = False
    if not output_dir:
        temp_dir = tempfile.TemporaryDirectory()
        output_dir = temp_dir.name
        is_temp = True
    else:
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "xcrun",
        "xcstringstool",
        "compile",
        xcstrings_path,
        "--output-directory",
        output_dir,
    ]
    if args.dry_run:
        cmd.append("--dry-run")

    print(f"Compiling catalog: {xcstrings_path}")
    try:
        run_command(cmd, "catalog compilation")
        print("Verification: Catalog compiled successfully with no syntax or structure errors.")
    finally:
        if is_temp:
            temp_dir.cleanup()


def main():
    parser = argparse.ArgumentParser(
        description="Helper utility for managing SwiftUI String Catalogs (.xcstrings) via xcstringstool."
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Subcommand to execute"
    )

    # Subcommand: extract
    parser_extract = subparsers.add_parser(
        "extract", help="Extract strings from SwiftUI/Swift source code files"
    )
    parser_extract.add_argument(
        "-s",
        "--source-files",
        nargs="+",
        required=True,
        help="Paths to Swift source files or folders to extract from",
    )
    parser_extract.add_argument(
        "-x",
        "--xcstrings-path",
        required=True,
        help="Path to the target .xcstrings file",
    )
    parser_extract.add_argument(
        "--source-language",
        default="en",
        help="Source language of the catalog if creating a new one (default: en)",
    )
    parser_extract.add_argument(
        "--no-append",
        action="store_false",
        dest="append",
        help="Overwrite existing strings instead of appending them",
    )
    parser_extract.add_argument(
        "--no-swiftui",
        action="store_false",
        dest="swiftui",
        help="Disable extraction from SwiftUI APIs",
    )
    parser_extract.add_argument(
        "--no-modern",
        action="store_false",
        dest="modern",
        help="Disable modern localized string extraction (e.g. String(localized:))",
    )
    parser_extract.add_argument(
        "--no-legacy",
        action="store_false",
        dest="legacy",
        help="Disable legacy genstrings-style extraction (e.g. NSLocalizedString)",
    )

    # Subcommand: list-missing
    parser_list = subparsers.add_parser(
        "list-missing", help="List keys that are missing translations for a locale"
    )
    parser_list.add_argument(
        "-x",
        "--xcstrings-path",
        required=True,
        help="Path to the target .xcstrings file",
    )
    parser_list.add_argument(
        "-l",
        "--locale",
        required=True,
        help="Target locale/language code (e.g. es, fr, de)",
    )
    parser_list.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )

    # Subcommand: merge
    parser_merge = subparsers.add_parser(
        "merge", help="Merge translated strings back into the .xcstrings file"
    )
    parser_merge.add_argument(
        "-x",
        "--xcstrings-path",
        required=True,
        help="Path to the target .xcstrings file",
    )
    parser_merge.add_argument(
        "-l",
        "--locale",
        required=True,
        help="Target locale/language code (e.g. es, fr, de)",
    )
    parser_merge.add_argument(
        "-t",
        "--translations",
        required=True,
        help="JSON string or path to a JSON file containing key-value translation mappings",
    )

    # Subcommand: compile
    parser_compile = subparsers.add_parser(
        "compile", help="Compile and verify the .xcstrings file"
    )
    parser_compile.add_argument(
        "-x",
        "--xcstrings-path",
        required=True,
        help="Path to the target .xcstrings file",
    )
    parser_compile.add_argument(
        "-o",
        "--output-dir",
        help="Optional directory to output build products to (defaults to a temp folder)",
    )
    parser_compile.add_argument(
        "--dry-run",
        action="store_true",
        help="List compilation output paths without writing files to disk",
    )

    args = parser.parse_args()

    if args.command == "extract":
        cmd_extract(args)
    elif args.command == "list-missing":
        cmd_list_missing(args)
    elif args.command == "merge":
        cmd_merge(args)
    elif args.command == "compile":
        cmd_compile(args)


if __name__ == "__main__":
    main()
