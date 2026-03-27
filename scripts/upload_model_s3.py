"""
upload_model_s3.py — Upload Phase 1 model weights and thresholds to S3.

Usage:
    AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... \\
    S3_BUCKET=shifamind-models \\
    python scripts/upload_model_s3.py \\
        --weights path/to/phase1_best.pt \\
        --thresholds path/to/optimal_thresholds.json

The script uploads to:
    s3://<S3_BUCKET>/phase1/phase1_best.pt
    s3://<S3_BUCKET>/phase1/optimal_thresholds.json
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.environ.get("S3_BUCKET", "shifamind-models")
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def upload_file(s3_client, local_path: Path, bucket: str, key: str) -> None:
    size_mb = local_path.stat().st_size / (1024 ** 2)
    print(f"  Uploading {local_path.name} ({size_mb:.1f} MB) → s3://{bucket}/{key}")

    s3_client.upload_file(
        str(local_path),
        bucket,
        key,
        ExtraArgs={"ServerSideEncryption": "AES256"},
        Callback=ProgressBar(local_path.stat().st_size),
    )
    print()  # newline after progress bar


class ProgressBar:
    def __init__(self, total: int):
        self.total = total
        self.seen = 0

    def __call__(self, bytes_amount: int):
        self.seen += bytes_amount
        pct = self.seen * 100 / self.total if self.total else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"\r  [{bar}] {pct:.1f}%", end="", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Upload ShifaMind Phase 1 model to S3")
    parser.add_argument("--weights", required=True, help="Path to phase1_best.pt")
    parser.add_argument("--thresholds", required=True, help="Path to optimal_thresholds.json")
    parser.add_argument("--bucket", default=S3_BUCKET, help="S3 bucket name")
    parser.add_argument("--prefix", default="phase1", help="S3 key prefix")
    parser.add_argument("--region", default=AWS_REGION, help="AWS region")
    args = parser.parse_args()

    weights_path = Path(args.weights)
    thresholds_path = Path(args.thresholds)

    if not weights_path.exists():
        print(f"Error: weights file not found: {weights_path}")
        sys.exit(1)
    if not thresholds_path.exists():
        print(f"Error: thresholds file not found: {thresholds_path}")
        sys.exit(1)

    try:
        import boto3
    except ImportError:
        print("Error: boto3 not installed. Run: pip install boto3")
        sys.exit(1)

    s3 = boto3.client("s3", region_name=args.region)

    print(f"Uploading to s3://{args.bucket}/{args.prefix}/\n")
    upload_file(s3, weights_path, args.bucket, f"{args.prefix}/phase1_best.pt")
    upload_file(s3, thresholds_path, args.bucket, f"{args.prefix}/optimal_thresholds.json")

    print("\nUpload complete.")
    print(f"  S3_MODEL_KEY={args.prefix}/phase1_best.pt")
    print(f"  S3_THRESHOLDS_KEY={args.prefix}/optimal_thresholds.json")


if __name__ == "__main__":
    main()
