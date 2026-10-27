#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ "$(id -u)" -ne 0 ]; then
  echo "Run as root: sudo ./build.sh" >&2
  exit 1
fi
for tool in lb python3; do
  command -v "$tool" >/dev/null 2>&1 || { echo "Missing $tool; install live-build python3 python3-pil." >&2; exit 1; }
done
python3 -c 'from PIL import Image, ImageDraw' >/dev/null 2>&1 || { echo "Missing Pillow; install python3-pil." >&2; exit 1; }
echo "Generating SHIFT OS branding..."
python3 tools/generate_branding.py
echo "Configuring Debian 13 live-build..."
./auto/config
echo "Building SHIFT OS ISO (network access and 25 GB free disk space recommended)..."
lb build
iso_file=""
for candidate in live-image-amd64.hybrid.iso live-image-amd64.iso; do
  if [ -f "$candidate" ]; then iso_file="$candidate"; break; fi
done
if [ -z "$iso_file" ]; then
  echo "Build finished but no expected ISO was found." >&2
  exit 2
fi
cp -f "$iso_file" SHIFT-OS-1.0-amd64.iso
sha256sum SHIFT-OS-1.0-amd64.iso > SHIFT-OS-1.0-amd64.iso.sha256
echo "ISO: $(pwd)/SHIFT-OS-1.0-amd64.iso"
cat SHIFT-OS-1.0-amd64.iso.sha256
