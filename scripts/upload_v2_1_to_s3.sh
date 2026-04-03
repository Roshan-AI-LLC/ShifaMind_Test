#!/usr/bin/env bash
# upload_v2_1_to_s3.sh
# Run this on your LOCAL Mac after downloading v2.1 files from Google Drive.
#
# ── Before running ────────────────────────────────────────────────────────────
# 1. Download these files from Google Drive to your Mac:
#
#    From: MyDrive/ShifaMind_v2.1/checkpoints/  → best checkpoint .pt file
#    From: MyDrive/ShifaMind_v2.1/analysis/     → concept_list_v2.1.json
#    From: MyDrive/ShifaMind_v2.1/analysis/     → top50_icd10_info_v2.1.json
#    From: MyDrive/ShifaMind_v2.1/thresholds/   → optimal_thresholds.json
#
# 2. Edit the four variables below to point to where you saved those files.
# 3. Make sure AWS CLI is configured (aws configure or IAM profile set).
# 4. Run: bash upload_v2_1_to_s3.sh
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

BUCKET="shifamind-models"
PREFIX="phase1"

# ── Edit these paths ──────────────────────────────────────────────────────────
CHECKPOINT_FILE="$HOME/Downloads/phase1_best.pt"        # v2.1 checkpoint
CONCEPT_LIST_FILE="$HOME/Downloads/concept_list_v2.1.json"
ICD10_INFO_FILE="$HOME/Downloads/top50_icd10_info_v2.1.json"
THRESHOLDS_FILE="$HOME/Downloads/optimal_thresholds.json"
# ─────────────────────────────────────────────────────────────────────────────

echo "Uploading ShifaMind v2.1 files to s3://$BUCKET/$PREFIX/"
echo ""

for f in "$CHECKPOINT_FILE" "$CONCEPT_LIST_FILE" "$ICD10_INFO_FILE" "$THRESHOLDS_FILE"; do
    if [ ! -f "$f" ]; then
        echo "ERROR: File not found: $f"
        echo "Edit the path variables at the top of this script."
        exit 1
    fi
done

echo "  [1/4] Checkpoint..."
aws s3 cp "$CHECKPOINT_FILE" "s3://$BUCKET/$PREFIX/phase1_best.pt"

echo "  [2/4] Concept list..."
aws s3 cp "$CONCEPT_LIST_FILE" "s3://$BUCKET/$PREFIX/concept_list.json"

echo "  [3/4] ICD-10 info..."
aws s3 cp "$ICD10_INFO_FILE" "s3://$BUCKET/$PREFIX/top50_icd10_info.json"

echo "  [4/4] Thresholds..."
aws s3 cp "$THRESHOLDS_FILE" "s3://$BUCKET/$PREFIX/optimal_thresholds.json"

echo ""
echo "Done! Verify with:"
echo "  aws s3 ls s3://$BUCKET/$PREFIX/"
