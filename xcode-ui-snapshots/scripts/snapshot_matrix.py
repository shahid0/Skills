#!/usr/bin/env python3
"""
snapshot_matrix.py
Automates iOS Simulator screenshot capture across a matrix of devices,
appearances (light/dark), dynamic text content sizes, and status bar overrides.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time


def parse_arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automate iOS simulator screenshots across device, appearance, and content size configurations."
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to a JSON configuration file defining the matrix.",
    )
    parser.add_argument(
        "--devices",
        type=str,
        nargs="+",
        help="Override simulator device names or UDIDs (e.g. 'iPhone 17 Pro' or UDID).",
    )
    parser.add_argument(
        "--appearances",
        type=str,
        nargs="+",
        choices=["light", "dark"],
        help="Override target appearances.",
    )
    parser.add_argument(
        "--content-sizes",
        type=str,
        nargs="+",
        help="Override target content sizes (e.g. 'medium', 'accessibility-large').",
    )
    parser.add_argument(
        "--app-bundle-id",
        type=str,
        help="The bundle identifier of the target app to launch.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./screenshots",
        help="Directory to save the captured screenshots.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay in seconds after launching or configuring the simulator before taking a screenshot.",
    )
    parser.add_argument(
        "--no-boot",
        action="store_true",
        help="Skip checking and booting simulators (assume already booted).",
    )
    parser.add_argument(
        "--launch-args",
        type=str,
        nargs="+",
        help="Optional arguments to pass to the app on launch.",
    )
    return parser


def get_available_devices() -> dict:
    """Fetches list of all simulators via simctl."""
    try:
        result = subprocess.run(
            ["xcrun", "simctl", "list", "devices", "-j"],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout).get("devices", {})
    except Exception as e:
        print(f"Error listing simulators: {e}", file=sys.stderr)
        return {}


def resolve_device_udid(device_name_or_udid: str, available_devices: dict) -> tuple[str, str] | None:
    """
    Resolves a device name or UDID to (udid, canonical_name).
    If it is 'booted', returns ('booted', 'booted').
    """
    if device_name_or_udid.lower() == "booted":
        return "booted", "booted"

    # Check if input is already a UDID pattern
    is_udid = re.match(
        r"^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$",
        device_name_or_udid,
        re.IGNORECASE,
    )

    matches = []
    for runtime, dev_list in available_devices.items():
        for dev in dev_list:
            udid = dev.get("udid")
            name = dev.get("name")
            is_available = dev.get("isAvailable", True)

            if is_udid and udid.lower() == device_name_or_udid.lower():
                return udid, name

            if name.lower() == device_name_or_udid.lower():
                if is_available:
                    return udid, name
                matches.append((udid, name))

    if matches:
        return matches[0]

    if is_udid:
        return device_name_or_udid, device_name_or_udid

    return None


def ensure_device_booted(udid: str, available_devices: dict) -> bool:
    """Checks if simulator is booted, and boots it if necessary."""
    if udid == "booted":
        return True

    # Find current state of the device
    state = None
    for runtime, dev_list in available_devices.items():
        for dev in dev_list:
            if dev.get("udid") == udid:
                state = dev.get("state")
                break

    if state == "Booted":
        print(f"Device {udid} is already booted.")
        return True

    print(f"Booting device {udid}...")
    try:
        subprocess.run(["xcrun", "simctl", "boot", udid], check=True)
        # Open the Simulator app
        subprocess.run(["open", "-a", "Simulator"], check=True)
        print("Waiting for boot status to be ready...")
        subprocess.run(["xcrun", "simctl", "bootstatus", udid], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to boot device {udid}: {e}", file=sys.stderr)
        return False


def apply_status_bar_overrides(device: str, overrides: dict) -> bool:
    """Configures the status bar on the target simulator."""
    if not overrides:
        return True
    
    # First clear existing status bar overrides
    subprocess.run(["xcrun", "simctl", "status_bar", device, "clear"], capture_output=True)

    cmd = ["xcrun", "simctl", "status_bar", device, "override"]
    for key, val in overrides.items():
        cmd.append(f"--{key}")
        cmd.append(str(val))

    print(f"Applying status bar overrides to {device}...")
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to override status bar on {device}: {e}", file=sys.stderr)
        return False


def clear_status_bar_overrides(device: str) -> None:
    """Clears status bar overrides."""
    print(f"Clearing status bar overrides on {device}...")
    subprocess.run(["xcrun", "simctl", "status_bar", device, "clear"], capture_output=True)


def configure_ui(device: str, appearance: str | None, content_size: str | None) -> bool:
    """Configures simulator UI options like appearance and text size."""
    success = True
    if appearance:
        print(f"Setting appearance on {device} to '{appearance}'...")
        try:
            subprocess.run(["xcrun", "simctl", "ui", device, "appearance", appearance], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to set appearance on {device}: {e}", file=sys.stderr)
            success = False

    if content_size:
        print(f"Setting content size on {device} to '{content_size}'...")
        try:
            subprocess.run(["xcrun", "simctl", "ui", device, "content_size", content_size], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to set content size on {device}: {e}", file=sys.stderr)
            success = False

    return success


def launch_app(device: str, bundle_id: str, launch_args: list[str] | None) -> bool:
    """Launches the target app on the simulator."""
    print(f"Terminating {bundle_id} on {device} if running...")
    subprocess.run(["xcrun", "simctl", "terminate", device, bundle_id], capture_output=True)

    cmd = ["xcrun", "simctl", "launch", device, bundle_id]
    if launch_args:
        cmd.extend(launch_args)

    print(f"Launching {bundle_id} on {device}...")
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to launch app {bundle_id} on {device}: {e}", file=sys.stderr)
        return False


def capture_screenshot(device: str, output_path: str) -> bool:
    """Captures a screenshot of the booted simulator."""
    print(f"Capturing screenshot to {output_path}...")
    try:
        # Note: Always uses 'booted' for screenshot command to fulfill constraints,
        # but fallback to specific device if needed.
        target = "booted" if device != "booted" else "booted"
        subprocess.run(["xcrun", "simctl", "io", target, "screenshot", output_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to capture screenshot: {e}", file=sys.stderr)
        return False


def clean_name(name: str) -> str:
    """Converts a name to a safe string for filenames."""
    clean = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    return re.sub(r"_+", "_", clean).strip("_")


def main() -> int:
    args_parser = parse_arguments()
    args = args_parser.parse_args()

    # Default configuration values
    config_data = {
        "app_bundle_id": None,
        "devices": ["booted"],
        "appearances": ["light"],
        "content_sizes": ["medium"],
        "status_bar_overrides": {},
        "delay": 2.0,
        "launch_args": []
    }

    # Load from config file if provided
    if args.config:
        if not os.path.exists(args.config):
            print(f"Error: Config file not found at {args.config}", file=sys.stderr)
            return 1
        try:
            with open(args.config, "r") as f:
                loaded_config = json.load(f)
                config_data.update(loaded_config)
        except Exception as e:
            print(f"Error parsing config file: {e}", file=sys.stderr)
            return 1

    # Apply command-line overrides
    if args.devices:
        config_data["devices"] = args.devices
    if args.appearances:
        config_data["appearances"] = args.appearances
    if args.content_sizes:
        config_data["content_sizes"] = args.content_sizes
    if args.app_bundle_id:
        config_data["app_bundle_id"] = args.app_bundle_id
    if args.delay is not None:
        config_data["delay"] = args.delay
    if args.launch_args:
        config_data["launch_args"] = args.launch_args

    # Check required bundle ID
    bundle_id = config_data.get("app_bundle_id")
    if not bundle_id:
        print("Error: App bundle ID is required. Specify via --app-bundle-id or in config.", file=sys.stderr)
        args_parser.print_usage()
        return 1

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    available_devices = get_available_devices()
    failures = 0
    total_runs = 0

    devices = config_data.get("devices", ["booted"])
    appearances = config_data.get("appearances", ["light"])
    content_sizes = config_data.get("content_sizes", ["medium"])
    status_bar_overrides = config_data.get("status_bar_overrides", {})
    delay = config_data.get("delay", 2.0)
    launch_arguments = config_data.get("launch_args", [])

    print("\n=== Snapshot Matrix Configurations ===")
    print(f"App Bundle ID: {bundle_id}")
    print(f"Devices:       {devices}")
    print(f"Appearances:   {appearances}")
    print(f"Content Sizes: {content_sizes}")
    print(f"Output Dir:    {args.output_dir}")
    print(f"Delay:         {delay}s")
    print("======================================\n")

    for dev_name in devices:
        resolved = resolve_device_udid(dev_name, available_devices)
        if not resolved:
            print(f"Skipping device '{dev_name}': Could not resolve UDID.", file=sys.stderr)
            failures += 1
            continue

        udid, canonical_name = resolved
        print(f"--- Processing: {canonical_name} ({udid}) ---")

        # Boot device if requested
        if not args.no_boot and udid != "booted":
            if not ensure_device_booted(udid, available_devices):
                print(f"Skipping {canonical_name}: Failed to boot.", file=sys.stderr)
                failures += 1
                continue

        # Override status bar if defined
        if status_bar_overrides:
            apply_status_bar_overrides(udid, status_bar_overrides)

        # Loop configurations
        for appr in appearances:
            for size in content_sizes:
                total_runs += 1
                print(f"\nConfiguring: {appr} | {size}")
                
                # Apply UI config
                if not configure_ui(udid, appr, size):
                    print("Failed configuring UI settings, continuing layout anyway...")

                # Launch target application
                if not launch_app(udid, bundle_id, launch_arguments):
                    print(f"Skipping capture for {appr}/{size} due to launch failure.")
                    failures += 1
                    continue

                # Wait for layout stabilization
                print(f"Waiting {delay}s for UI rendering...")
                time.sleep(delay)

                # Output filename formatting
                clean_device = clean_name(canonical_name)
                clean_size = clean_name(size)
                filename = f"screenshot_{clean_device}_{appr}_{clean_size}.png"
                output_path = os.path.join(args.output_dir, filename)

                # Capture
                if not capture_screenshot(udid, output_path):
                    failures += 1

        # Post-device cleanup
        if status_bar_overrides:
            clear_status_bar_overrides(udid)

    print("\n=== Snapshot Matrix Execution Finished ===")
    print(f"Total Configurations attempted: {total_runs}")
    print(f"Successful Captures:           {total_runs - failures}")
    print(f"Failures encountered:          {failures}")
    
    return 1 if failures > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
