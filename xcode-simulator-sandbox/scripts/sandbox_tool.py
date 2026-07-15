#!/usr/bin/env python3
import argparse
import json
import os
import plistlib
import sqlite3
import subprocess
import sys
from typing import Any, Dict, List, Optional

DEFAULT_DEVICE = "booted"

def get_app_container(bundle_id: str, device: str = DEFAULT_DEVICE, container_type: str = "data") -> str:
    """Resolve the simulator container path for a bundle ID using simctl."""
    try:
        cmd = ["xcrun", "simctl", "get_app_container", device, bundle_id, container_type]
        output = subprocess.check_output(cmd, stderr=subprocess.PIPE).decode("utf-8").strip()
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to get container path for '{bundle_id}' on device '{device}'.", file=sys.stderr)
        print(e.stderr.decode("utf-8").strip(), file=sys.stderr)
        sys.exit(1)

def resolve_path(path: Optional[str], bundle_id: Optional[str], device: str = DEFAULT_DEVICE, container_type: str = "data") -> str:
    """Resolve a path which might be relative to an app's container."""
    if not bundle_id:
        if not path:
            print("Error: No path provided.", file=sys.stderr)
            sys.exit(1)
        return os.path.abspath(path)
    
    container_base = get_app_container(bundle_id, device, container_type)
    if not path:
        return container_base
    
    return os.path.join(container_base, path)

def find_preferences_plist(bundle_id: str, device: str = DEFAULT_DEVICE, custom_path: Optional[str] = None) -> str:
    """Find preference plist for bundle ID, allowing custom relative path."""
    if custom_path:
        return resolve_path(custom_path, bundle_id, device, "data")
    container = get_app_container(bundle_id, device, "data")
    return os.path.join(container, "Library", "Preferences", f"{bundle_id}.plist")

def cmd_container_path(args):
    path = get_app_container(args.bundle_id, args.device, args.type)
    print(path)

def load_plist(path: str) -> dict:
    if not os.path.exists(path):
        print(f"Error: Plist file does not exist at '{path}'", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, "rb") as f:
            return plistlib.load(f)
    except Exception as e:
        print(f"Error: Failed to read plist at '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def save_plist(path: str, data: dict):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            plistlib.dump(data, f, fmt=plistlib.FMT_BINARY)
        print(f"Successfully saved plist to '{path}'")
    except Exception as e:
        print(f"Error: Failed to write plist to '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def get_plist_path_from_args(args) -> str:
    if args.bundle_id:
        return find_preferences_plist(args.bundle_id, args.device, args.path)
    elif args.path:
        return resolve_path(args.path, None)
    else:
        print("Error: Either --path (-p) or --bundle-id (-b) must be provided.", file=sys.stderr)
        sys.exit(1)

def cmd_plist_print(args):
    path = get_plist_path_from_args(args)
    data = load_plist(path)
    print(json.dumps(data, indent=2, default=str))

def cmd_plist_get(args):
    path = get_plist_path_from_args(args)
    data = load_plist(path)
    if args.key not in data:
        print(f"Error: Key '{args.key}' not found in plist.", file=sys.stderr)
        sys.exit(1)
    
    val = data[args.key]
    if isinstance(val, (dict, list)):
        print(json.dumps(val, indent=2, default=str))
    else:
        print(val)

def cmd_plist_set(args):
    path = get_plist_path_from_args(args)
    if os.path.exists(path):
        data = load_plist(path)
    else:
        data = {}
    
    val_str = args.value
    if args.type == "string":
        value = val_str
    elif args.type == "int":
        try:
            value = int(val_str)
        except ValueError:
            print(f"Error: Value '{val_str}' is not a valid integer.", file=sys.stderr)
            sys.exit(1)
    elif args.type == "float":
        try:
            value = float(val_str)
        except ValueError:
            print(f"Error: Value '{val_str}' is not a valid float.", file=sys.stderr)
            sys.exit(1)
    elif args.type == "bool":
        if val_str.lower() in ("true", "1", "yes"):
            value = True
        elif val_str.lower() in ("false", "0", "no"):
            value = False
        else:
            print(f"Error: Value '{val_str}' is not a valid boolean.", file=sys.stderr)
            sys.exit(1)
    elif args.type == "json":
        try:
            value = json.loads(val_str)
        except json.JSONDecodeError as e:
            print(f"Error: Value '{val_str}' is not valid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Auto-detect type
        if val_str.lower() in ("true", "yes"):
            value = True
        elif val_str.lower() in ("false", "no"):
            value = False
        elif val_str.isdigit():
            value = int(val_str)
        else:
            try:
                value = float(val_str)
            except ValueError:
                value = val_str
    
    data[args.key] = value
    save_plist(path, data)

def cmd_plist_delete(args):
    path = get_plist_path_from_args(args)
    data = load_plist(path)
    if args.key in data:
        del data[args.key]
        save_plist(path, data)
    else:
        print(f"Warning: Key '{args.key}' not found in plist. No action taken.")

def get_sqlite_conn(path: str) -> sqlite3.Connection:
    if not os.path.exists(path):
        print(f"Error: SQLite database file does not exist at '{path}'", file=sys.stderr)
        sys.exit(1)
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error: Failed to connect to SQLite database at '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def print_table_format(rows: List[sqlite3.Row]):
    if not rows:
        print("No results.")
        return
    keys = rows[0].keys()
    widths = {k: len(k) for k in keys}
    for row in rows:
        for k in keys:
            val_str = str(row[k]) if row[k] is not None else "NULL"
            widths[k] = max(widths[k], len(val_str))
    
    header = " | ".join(f"{k:<{widths[k]}}" for k in keys)
    separator = "-+-".join("-" * widths[k] for k in keys)
    print(header)
    print(separator)
    for row in rows:
        print(" | ".join(f"{(str(row[k]) if row[k] is not None else 'NULL'):<{widths[k]}}" for k in keys))

def cmd_sqlite_tables(args):
    path = resolve_path(args.path, args.bundle_id, args.device)
    conn = get_sqlite_conn(path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    rows = cursor.fetchall()
    conn.close()
    
    for r in rows:
        print(r['name'])

def cmd_sqlite_schema(args):
    path = resolve_path(args.path, args.bundle_id, args.device)
    conn = get_sqlite_conn(path)
    cursor = conn.cursor()
    if args.table:
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (args.table,))
    else:
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    rows = cursor.fetchall()
    conn.close()
    
    for r in rows:
        if r['sql']:
            print(r['sql'] + ";\n")

def cmd_sqlite_query(args):
    path = resolve_path(args.path, args.bundle_id, args.device)
    conn = get_sqlite_conn(path)
    cursor = conn.cursor()
    try:
        cursor.execute(args.sql)
        if args.sql.strip().lower().startswith(("select", "pragma", "explain")):
            rows = cursor.fetchall()
            if args.format == "json":
                results = [dict(r) for r in rows]
                print(json.dumps(results, indent=2, default=str))
            else:
                print_table_format(rows)
        else:
            conn.commit()
            print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
    except Exception as e:
        print(f"Error: Query failed: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()

def cmd_sqlite_dump(args):
    path = resolve_path(args.path, args.bundle_id, args.device)
    conn = get_sqlite_conn(path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {args.table};")
        rows = cursor.fetchall()
        if args.format == "json":
            results = [dict(r) for r in rows]
            print(json.dumps(results, indent=2, default=str))
        else:
            print_table_format(rows)
    except Exception as e:
        print(f"Error: Failed to dump table '{args.table}': {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(
        description="Inspect and modify files (plists and SQLite DBs) in iOS Simulator app sandboxes."
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")
    
    # 1. Container Path
    parser_path = subparsers.add_parser("container-path", help="Get the path to the app's container on simulator")
    parser_path.add_argument("bundle_id", help="App Bundle ID")
    parser_path.add_argument("--device", default=DEFAULT_DEVICE, help=f"Simulator device (default: {DEFAULT_DEVICE})")
    parser_path.add_argument("--type", default="data", choices=["data", "app", "groups", "all"], help="Container type (default: data)")
    parser_path.set_defaults(func=cmd_container_path)
    
    # Plist Shared Parser
    plist_parent = argparse.ArgumentParser(add_help=False)
    plist_parent.add_argument("--path", "-p", help="Path to plist file (relative to container if -b/--bundle-id is provided)")
    plist_parent.add_argument("--bundle-id", "-b", help="App Bundle ID (will locate preferences plist automatically)")
    plist_parent.add_argument("--device", default=DEFAULT_DEVICE, help=f"Simulator device (default: {DEFAULT_DEVICE})")
    
    # 2. Plist Parser
    parser_plist = subparsers.add_parser("plist", help="Inspect or edit plist files")
    plist_subparsers = parser_plist.add_subparsers(dest="plist_command", required=True, help="Plist actions")
    
    plist_print = plist_subparsers.add_parser("print", parents=[plist_parent], help="Print plist contents as JSON")
    plist_print.set_defaults(func=cmd_plist_print)
    
    plist_get = plist_subparsers.add_parser("get", parents=[plist_parent], help="Get a single value from plist")
    plist_get.add_argument("key", help="Plist key to retrieve")
    plist_get.set_defaults(func=cmd_plist_get)
    
    plist_set = plist_subparsers.add_parser("set", parents=[plist_parent], help="Set a single value in plist")
    plist_set.add_argument("key", help="Plist key to set")
    plist_set.add_argument("value", help="Value to set")
    plist_set.add_argument("--type", choices=["string", "int", "float", "bool", "json", "auto"], default="auto", help="Value type (default: auto)")
    plist_set.set_defaults(func=cmd_plist_set)
    
    plist_del = plist_subparsers.add_parser("delete", parents=[plist_parent], help="Delete a key from plist")
    plist_del.add_argument("key", help="Key to delete")
    plist_del.set_defaults(func=cmd_plist_delete)
    
    # SQLite Shared Parser
    sqlite_parent = argparse.ArgumentParser(add_help=False)
    sqlite_parent.add_argument("--path", "-p", required=True, help="Path to SQLite database file (relative to container if -b/--bundle-id is provided)")
    sqlite_parent.add_argument("--bundle-id", "-b", help="App Bundle ID")
    sqlite_parent.add_argument("--device", default=DEFAULT_DEVICE, help=f"Simulator device (default: {DEFAULT_DEVICE})")
    
    # 3. SQLite Parser
    parser_sqlite = subparsers.add_parser("sqlite", help="Inspect or query SQLite databases")
    sqlite_subparsers = parser_sqlite.add_subparsers(dest="sqlite_command", required=True, help="SQLite actions")
    
    sqlite_tables = sqlite_subparsers.add_parser("tables", parents=[sqlite_parent], help="List all tables in the database")
    sqlite_tables.set_defaults(func=cmd_sqlite_tables)
    
    sqlite_schema = sqlite_subparsers.add_parser("schema", parents=[sqlite_parent], help="Print schema of database or specific table")
    sqlite_schema.add_argument("table", nargs="?", help="Specific table schema to dump (optional)")
    sqlite_schema.set_defaults(func=cmd_sqlite_schema)
    
    sqlite_query = sqlite_subparsers.add_parser("query", parents=[sqlite_parent], help="Run a raw SQL query")
    sqlite_query.add_argument("sql", help="SQL statement to execute")
    sqlite_query.add_argument("--format", choices=["table", "json"], default="table", help="Output format (default: table)")
    sqlite_query.set_defaults(func=cmd_sqlite_query)
    
    sqlite_dump = sqlite_subparsers.add_parser("dump", parents=[sqlite_parent], help="Dump all rows from a table")
    sqlite_dump.add_argument("table", help="Table name")
    sqlite_dump.add_argument("--format", choices=["table", "json"], default="table", help="Output format (default: table)")
    sqlite_dump.set_defaults(func=cmd_sqlite_dump)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
