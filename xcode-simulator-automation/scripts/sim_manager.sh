#!/bin/bash
# sim_manager.sh - Simulator Automation Helper Script
# Wraps simctl commands for booting, installation, launching, push notifications, coordinates, and screen recording.

set -euo pipefail

# Print usage information
usage() {
    cat <<EOF
Usage: $(basename "$0") <command> [arguments]

Commands:
  boot <device>
      Boot a simulator and wait for it to be fully booted.
      Example: $(basename "$0") boot "iPhone 15"

  install <device> <app_path>
      Install an app (.app bundle) on the simulator.
      Example: $(basename "$0") install booted ./build/Build/Products/Debug-iphonesimulator/MyApp.app

  launch <device> <bundle_id> [args...]
      Launch an application by identifier.
      Example: $(basename "$0") launch booted com.example.myapp

  terminate <device> <bundle_id>
      Terminate a running application by identifier.
      Example: $(basename "$0") terminate booted com.example.myapp

  push <device> <bundle_id> <payload_path>
      Send a mock push notification using a JSON payload.
      Example: $(basename "$0") push booted com.example.myapp notification.json

  location <device> set <latitude> <longitude>
      Override GPS coordinates.
      Example: $(basename "$0") location booted set 37.7749 -122.4194

  record <device> <output_mp4_path> [duration_seconds]
      Record simulator screen video as MP4.
      If duration is specified, records for that many seconds and exits.
      Otherwise, records until SIGINT (Ctrl+C) is received.
      Example: $(basename "$0") record booted output.mp4 10

EOF
    exit 1
}

# Ensure simctl is available
check_dependencies() {
    if ! command -v xcrun &>/dev/null; then
        echo "Error: xcrun not found. Xcode Command Line Tools must be installed." >&2
        exit 1
    fi
}

# Main entrypoint
main() {
    check_dependencies

    if [[ $# -lt 1 ]]; then
        usage
    fi

    local command="$1"
    shift

    case "$command" in
        boot)
            if [[ $# -lt 1 ]]; then
                echo "Error: 'boot' requires a device identifier." >&2
                usage
            fi
            local device="$1"
            echo "Booting device '$device' and waiting for completion..."
            # bootstatus with -b boots the simulator if it isn't booted, and waits
            xcrun simctl bootstatus "$device" -b
            echo "Device '$device' is booted and ready."
            ;;

        install)
            if [[ $# -lt 2 ]]; then
                echo "Error: 'install' requires a device and app path." >&2
                usage
            fi
            local device="$1"
            local app_path="$2"
            echo "Installing '$app_path' on device '$device'..."
            xcrun simctl install "$device" "$app_path"
            echo "Installation completed."
            ;;

        launch)
            if [[ $# -lt 2 ]]; then
                echo "Error: 'launch' requires a device and bundle identifier." >&2
                usage
            fi
            local device="$1"
            local bundle_id="$2"
            shift 2
            echo "Launching '$bundle_id' on device '$device'..."
            xcrun simctl launch "$device" "$bundle_id" "$@"
            ;;

        terminate)
            if [[ $# -lt 2 ]]; then
                echo "Error: 'terminate' requires a device and bundle identifier." >&2
                usage
            fi
            local device="$1"
            local bundle_id="$2"
            echo "Terminating '$bundle_id' on device '$device'..."
            xcrun simctl terminate "$device" "$bundle_id"
            ;;

        push)
            if [[ $# -lt 3 ]]; then
                echo "Error: 'push' requires a device, bundle identifier, and JSON payload path." >&2
                usage
            fi
            local device="$1"
            local bundle_id="$2"
            local payload="$3"
            if [[ ! -f "$payload" ]]; then
                echo "Error: Payload file '$payload' does not exist." >&2
                exit 1
            fi
            echo "Sending push notification to '$bundle_id' on device '$device' using '$payload'..."
            xcrun simctl push "$device" "$bundle_id" "$payload"
            ;;

        location)
            if [[ $# -lt 2 ]]; then
                echo "Error: 'location' requires a device and location parameters." >&2
                usage
            fi
            local device="$1"
            shift
            local action="$1"
            
            if [[ "$action" == "set" ]]; then
                if [[ $# -lt 3 ]]; then
                    echo "Error: 'location set' requires latitude and longitude." >&2
                    usage
                fi
                local lat="$2"
                local lon="$3"
                echo "Setting GPS coordinates on device '$device' to $lat, $lon..."
                xcrun simctl location "$device" set "${lat},${lon}"
            elif [[ "$action" == "clear" || "$action" == "list" ]]; then
                xcrun simctl location "$device" "$action"
            else
                if [[ $# -eq 2 ]]; then
                    local lat="$action"
                    local lon="$2"
                    echo "Setting GPS coordinates on device '$device' to $lat, $lon..."
                    xcrun simctl location "$device" set "${lat},${lon}"
                else
                    echo "Error: Invalid location action or parameters." >&2
                    usage
                fi
            fi
            ;;

        record)
            if [[ $# -lt 2 ]]; then
                echo "Error: 'record' requires a device and output MP4 path." >&2
                usage
            fi
            local device="$1"
            local output_path="$2"
            local duration="${3:-}"
            
            # Check if output file directory is writable
            local output_dir
            output_dir=$(dirname "$output_path")
            if [[ ! -d "$output_dir" ]]; then
                echo "Error: Directory '$output_dir' does not exist." >&2
                exit 1
            fi

            # Determine recording mode
            local ffmpeg_available=0
            if command -v ffmpeg &>/dev/null; then
                ffmpeg_available=1
            fi

            # If output is .mp4 and ffmpeg is available, we record to a temp .mov and convert
            local actual_output="$output_path"
            local temp_mov=""
            if [[ "$output_path" == *.mp4 && $ffmpeg_available -eq 1 ]]; then
                temp_mov=$(mktemp "./sim_record_XXXXXX.mov")
                actual_output="$temp_mov"
            fi

            echo "Starting screen recording on device '$device'..."
            if [[ -n "$duration" ]]; then
                if ! [[ "$duration" =~ ^[0-9]+$ ]]; then
                    echo "Error: Duration must be a positive integer." >&2
                    exit 1
                fi
                echo "Recording will run for $duration seconds."
                
                # Start recording in background
                xcrun simctl io "$device" recordVideo --force "$actual_output" &
                local pid=$!
                
                # Wait for the recording to actually start
                sleep 1
                
                echo "Recording..."
                sleep "$duration"
                
                echo "Stopping recording..."
                kill -2 "$pid" 2>/dev/null || true
                wait "$pid" 2>/dev/null || true
            else
                echo "Press Ctrl+C to stop recording..."
                
                # Start recording in background and trap SIGINT
                xcrun simctl io "$device" recordVideo --force "$actual_output" &
                local pid=$!
                
                trap 'echo -e "\nStopping recording..."; kill -2 $pid 2>/dev/null || true; wait $pid 2>/dev/null || true' SIGINT
                
                # Wait for background process to complete
                wait "$pid" 2>/dev/null || true
                trap - SIGINT
            fi

            # Handle conversion if needed
            if [[ -n "$temp_mov" && -f "$temp_mov" ]]; then
                echo "Converting recording to MP4 format using ffmpeg..."
                if ffmpeg -y -i "$temp_mov" -c:v libx264 -pix_fmt yuv420p "$output_path" &>/dev/null; then
                    echo "Video saved to '$output_path'"
                else
                    echo "Error: ffmpeg conversion failed. Copying raw recording instead." >&2
                    cp "$temp_mov" "$output_path"
                fi
                rm -f "$temp_mov"
            else
                echo "Video saved to '$output_path'"
            fi
            ;;

        *)
            echo "Error: Unknown command '$command'." >&2
            usage
            ;;
    esac
}

main "$@"
