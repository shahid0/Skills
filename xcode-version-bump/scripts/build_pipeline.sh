#!/bin/bash
# build_pipeline.sh - Xcode build, version bump, archive, and export pipeline

set -euo pipefail

# Default values
WORKSPACE=""
PROJECT=""
SCHEME=""
CONFIG="Release"
BUMP_TYPE="none"
MARKETING_VERSION=""
EXPORT_OPTIONS=""
OUTPUT_DIR="./build/output"
DRY_RUN=false

# Print usage instructions
usage() {
    cat <<EOF
Usage: $(basename "$0") [options]

Options:
  -w, --workspace <path>           Path to the .xcworkspace file
  -p, --project <path>             Path to the .xcodeproj file (alternative to -w)
  -s, --scheme <name>              Xcode scheme to build (required)
  -c, --config <name>              Xcode build configuration (default: Release)
  -b, --bump-type <type>           Bump type: 'build', 'marketing', 'both', or 'none' (default: none)
  -m, --marketing-version <ver>    New marketing version (required if bump-type is 'marketing' or 'both')
  -e, --export-options <path>      Path to ExportOptions.plist (required for IPA export)
  -o, --output-dir <path>          Output directory for final IPA (default: ./build/output)
  -d, --dry-run                    Verify configurations and print commands without executing them
  -h, --help                       Show this help message
EOF
    exit 1
}

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        -w|--workspace)
            WORKSPACE="$2"
            shift 2
            ;;
        -p|--project)
            PROJECT="$2"
            shift 2
            ;;
        -s|--scheme)
            SCHEME="$2"
            shift 2
            ;;
        -c|--config)
            CONFIG="$2"
            shift 2
            ;;
        -b|--bump-type)
            BUMP_TYPE="$2"
            shift 2
            ;;
        -m|--marketing-version)
            MARKETING_VERSION="$2"
            shift 2
            ;;
        -e|--export-options)
            EXPORT_OPTIONS="$2"
            shift 2
            ;;
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Error: Unknown option: $1"
            usage
            ;;
    esac
done

echo "=== Xcode Build & Version Bump Pipeline ==="

# Check tool availability
if ! command -v xcodebuild &> /dev/null; then
    echo "Error: xcodebuild command not found. Xcode is required to run this script."
    exit 1
fi

if ! command -v agvtool &> /dev/null; then
    echo "Error: agvtool command not found. Xcode Command Line Tools are required to run this script."
    exit 1
fi

# Validations
if [[ -z "$SCHEME" ]]; then
    echo "Error: Scheme (-s, --scheme) is required."
    exit 1
fi

if [[ -n "$WORKSPACE" && -n "$PROJECT" ]]; then
    echo "Error: Specify either workspace (-w) or project (-p), not both."
    exit 1
fi

# Auto-detection if neither workspace nor project is specified
if [[ -z "$WORKSPACE" && -z "$PROJECT" ]]; then
    echo "No workspace or project specified. Searching current directory..."
    workspaces=(*.xcworkspace)
    projects=(*.xcodeproj)
    if [[ -e "${workspaces[0]}" ]]; then
        WORKSPACE="${workspaces[0]}"
        echo "Auto-detected workspace: $WORKSPACE"
    elif [[ -e "${projects[0]}" ]]; then
        PROJECT="${projects[0]}"
        echo "Auto-detected project: $PROJECT"
    else
        echo "Error: No workspace or project specified, and none found in the current directory."
        exit 1
    fi
fi

# Determine project directory and command arguments
if [[ -n "$WORKSPACE" ]]; then
    if [[ ! -e "$WORKSPACE" ]]; then
        echo "Error: Workspace does not exist: $WORKSPACE"
        exit 1
    fi
    PROJ_DIR=$(dirname "$WORKSPACE")
    TARGET_ARG="-workspace $WORKSPACE"
else
    if [[ ! -e "$PROJECT" ]]; then
        echo "Error: Project does not exist: $PROJECT"
        exit 1
    fi
    PROJ_DIR=$(dirname "$PROJECT")
    TARGET_ARG="-project $PROJECT"
fi

if [[ -z "$EXPORT_OPTIONS" ]]; then
    echo "Error: ExportOptions.plist (-e, --export-options) is required."
    exit 1
fi

if [[ ! -f "$EXPORT_OPTIONS" ]]; then
    echo "Error: ExportOptions.plist file not found: $EXPORT_OPTIONS"
    exit 1
fi

if [[ "$BUMP_TYPE" == "marketing" || "$BUMP_TYPE" == "both" ]]; then
    if [[ -z "$MARKETING_VERSION" ]]; then
        echo "Error: Marketing version (-m) is required when bump-type is '$BUMP_TYPE'."
        exit 1
    fi
fi

if [[ "$BUMP_TYPE" != "build" && "$BUMP_TYPE" != "marketing" && "$BUMP_TYPE" != "both" && "$BUMP_TYPE" != "none" ]]; then
    echo "Error: Invalid bump-type '$BUMP_TYPE'. Allowed values: build, marketing, both, none."
    exit 1
fi

# Verify Apple Generic Versioning
echo "Verifying Apple Generic Versioning build settings..."
versioning_system=$(xcodebuild -showBuildSettings $TARGET_ARG -scheme "$SCHEME" -configuration "$CONFIG" 2>/dev/null | grep -E "VERSIONING_SYSTEM" | awk -F '=' '{print $2}' | tr -d '[:space:]' || true)

if [[ -z "$versioning_system" ]]; then
    echo "Warning: Could not verify VERSIONING_SYSTEM from build settings. Please check manually."
elif [[ "$versioning_system" != "apple-generic" ]]; then
    echo "Error: Apple Generic Versioning is not enabled. VERSIONING_SYSTEM is currently set to '$versioning_system'."
    echo "Please configure 'Versioning System' (VERSIONING_SYSTEM) to 'Apple Generic' in Xcode."
    exit 1
else
    echo "Verified: Apple Generic Versioning is enabled."
fi

# Run version bumps
bump_versions() {
    local original_dir
    original_dir=$(pwd)
    echo "Navigating to project directory: $PROJ_DIR"
    cd "$PROJ_DIR"

    local xcodeproj_count
    xcodeproj_count=$(ls -1d *.xcodeproj 2>/dev/null | wc -l)
    if [[ $xcodeproj_count -eq 0 ]]; then
        echo "Error: agvtool requires to be run in a directory containing an .xcodeproj file. None found in $PROJ_DIR."
        cd "$original_dir"
        exit 1
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY RUN] Version bumps would be executed:"
        if [[ "$BUMP_TYPE" == "build" || "$BUMP_TYPE" == "both" ]]; then
            echo "  - Increment build version (agvtool bump)"
        fi
        if [[ "$BUMP_TYPE" == "marketing" || "$BUMP_TYPE" == "both" ]]; then
            echo "  - Update marketing version to $MARKETING_VERSION (agvtool new-marketing-version $MARKETING_VERSION)"
        fi
    else
        if [[ "$BUMP_TYPE" == "build" || "$BUMP_TYPE" == "both" ]]; then
            echo "Running: agvtool bump"
            agvtool bump
        fi
        if [[ "$BUMP_TYPE" == "marketing" || "$BUMP_TYPE" == "both" ]]; then
            echo "Running: agvtool new-marketing-version $MARKETING_VERSION"
            agvtool new-marketing-version "$MARKETING_VERSION"
        fi
    fi

    cd "$original_dir"
}

if [[ "$BUMP_TYPE" != "none" ]]; then
    bump_versions
fi

# Prepare Output Directory
if [[ "$DRY_RUN" == "false" ]]; then
    mkdir -p "$OUTPUT_DIR"
fi

# Run xcodebuild archive
ARCHIVE_PATH="$OUTPUT_DIR/$SCHEME.xcarchive"
echo "Creating compilation archive..."
if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] Archive command:"
    echo "  xcodebuild archive $TARGET_ARG -scheme \"$SCHEME\" -configuration \"$CONFIG\" -archivePath \"$ARCHIVE_PATH\""
else
    xcodebuild archive \
      $TARGET_ARG \
      -scheme "$SCHEME" \
      -configuration "$CONFIG" \
      -archivePath "$ARCHIVE_PATH"
fi

# Run xcodebuild exportArchive
echo "Exporting signed IPA package..."
if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] Export command:"
    echo "  xcodebuild -exportArchive -archivePath \"$ARCHIVE_PATH\" -exportOptionsPlist \"$EXPORT_OPTIONS\" -exportPath \"$OUTPUT_DIR\""
else
    xcodebuild -exportArchive \
      -archivePath "$ARCHIVE_PATH" \
      -exportOptionsPlist "$EXPORT_OPTIONS" \
      -exportPath "$OUTPUT_DIR"
fi

# Completion logs
if [[ "$DRY_RUN" == "true" ]]; then
    echo "=== [DRY RUN] Build pipeline simulation complete ==="
else
    echo "=== Build pipeline completed successfully ==="
    echo "Archive: $ARCHIVE_PATH"
    echo "Export Output: $OUTPUT_DIR"
fi
