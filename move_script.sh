#!/usr/bin/env bash
# 🚀 Eidosian File Mover v2.0 🚀
# -----------------------------------------------------------
# This script organizes your repository by moving all files
# and directories into a designated subdirectory, with robust
# idempotence and safety checks to prevent accidental data loss.
# -----------------------------------------------------------
# 🌟 AUTHOR: The Eidosian Engineer
# 🌟 DATE: $(date)
# 🌟 LICENSE: MIT | Open Source Eidosian Excellence
# -----------------------------------------------------------

# ⚠️ STRICT ERROR HANDLING ⚠️
set -euo pipefail

# 📝 CONFIGURATION VARIABLES 📝
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$REPO_ROOT/ollama_toolkit"
LOG_FILE="$REPO_ROOT/file_move_$(date +%Y%m%d_%H%M%S).log"
EXCLUDED_ITEMS=(
    # Git and repo structure
    ".git" "ollama_toolkit" "$(basename "${BASH_SOURCE[0]}")" ".gitignore" "README.md"
    # Package configuration
    "pyproject.toml" "setup.py" "setup.cfg" "MANIFEST.in" "LICENSE" 
    # Documentation
    ".readthedocs.yaml" "docs" "rtd_tutorial.md" "eidosian_principles.md"
    # Development tools and scripts
    "build_docs.sh" "publish_to_pypi.sh" "publish.py" "development.sh"
    "init_repo.sh" "update_parent_gitignore.sh"
    # Build artifacts and cache
    "dist" "ollama_toolkit.egg-info" ".pytest_cache" ".vscode" "wheelhouse"
    # Tests and examples
    "tests" "examples"
    # Credentials and configs
    ".pypirc"
    # Generated log files
    "file_move_*.log"
)

# 🧰 UTILITY FUNCTIONS 🧰
log() {
    local message="$1"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo -e "[$timestamp] $message" | tee -a "$LOG_FILE"
}

confirm() {
    local prompt="$1"
    read -p "❓ $prompt [y/N]: " response
    [[ "${response,,}" =~ ^(yes|y)$ ]]
}

# 🔍 START WITH VALIDATION & CHECKS 🔍
log "🔥😈 Eidos: Beginning file organization ritual... 🔥😈"
log "📂 Repository root: $REPO_ROOT"
log "🎯 Target directory: $TARGET_DIR"

# Ensure we don't operate on a non-repo directory
if [[ ! -d "$REPO_ROOT/.git" ]]; then
    log "⚠️ WARNING: This doesn't appear to be a git repository root. Proceed with caution."
    if ! confirm "Continue anyway?"; then
        log "🛑 Operation aborted by user."
        exit 0
    fi
fi

# Create target folder if it doesn't exist
if [[ ! -d "$TARGET_DIR" ]]; then
    log "📁 Creating target directory: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
else
    log "📁 Target directory already exists: $TARGET_DIR"
fi

# 📋 INVENTORY PHASE 📋
log "📊 Analyzing repository contents..."
items_to_move=()
shopt -s dotglob nullglob

for item in "$REPO_ROOT"/*; do
    basename_item="$(basename "$item")"
    
    # Skip excluded items (with glob pattern support for log files)
    skip=false
    for excluded in "${EXCLUDED_ITEMS[@]}"; do
        # Handle glob patterns
        if [[ "$excluded" == *"*"* ]]; then
            if [[ "$basename_item" == ${excluded} ]]; then
                skip=true
                break
            fi
        # Regular exact matching
        elif [[ "$basename_item" == "$excluded" ]]; then
            skip=true
            break
        fi
    done
    
    if [[ "$skip" == true ]]; then
        log "⏩ Skipping excluded item: $basename_item"
        continue
    fi
    
    # Check if the item already exists in target directory (for idempotence)
    if [[ -e "$TARGET_DIR/$basename_item" ]]; then
        log "⚠️ Item already exists in target: $basename_item (will be skipped)"
        continue
    fi
    
    items_to_move+=("$item")
done

# 🚦 CONFIRMATION PHASE 🚦
if [[ ${#items_to_move[@]} -eq 0 ]]; then
    log "✅ Nothing to move! The operation is idempotent and has already been completed."
    exit 0
fi

log "🔍 Found ${#items_to_move[@]} items to move:"
for item in "${items_to_move[@]}"; do
    log "   - $(basename "$item")"
done

if ! confirm "Ready to move these ${#items_to_move[@]} items to $TARGET_DIR?"; then
    log "🛑 Operation aborted by user."
    exit 0
fi

# 🚚 EXECUTION PHASE 🚚
log "🚀 Beginning file movement operation..."
success_count=0
error_count=0

for item in "${items_to_move[@]}"; do
    basename_item="$(basename "$item")"
    log "📦 Moving: $basename_item"
    
    if mv "$item" "$TARGET_DIR/"; then
        log "✅ Successfully moved: $basename_item"
        ((success_count++))
    else
        log "❌ Failed to move: $basename_item"
        ((error_count++))
    fi
done

# 📊 SUMMARY PHASE 📊
log "🎉 Operation complete!"
log "📊 Summary: $success_count items moved successfully, $error_count errors"
log "📂 All specified files have been moved into $TARGET_DIR"

if [[ $error_count -gt 0 ]]; then
    log "⚠️ Some errors occurred. Check the log file for details: $LOG_FILE"
    exit 1
fi

log "🔥😈 Eidos: File organization ritual completed successfully! 🔥😈"