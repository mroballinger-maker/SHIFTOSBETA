# SHIFT OS 1.0

A modern Debian 13 + KDE Plasma live desktop concept, themed with the SHIFT circle-and-double-chevron mark and dark teal/cyan/blue/violet gradients.

**Status:** build project in progress. The ISO has not yet been built or boot-tested. See the repository Actions workflow for generating an ISO.

## Target

- Debian 13 (Trixie), amd64
- KDE Plasma desktop and SDDM
- Dark SHIFT Ocean theme and custom wallpaper
- Calamares installer branding
- Hybrid ISO intended for virtual machines and USB installation

## Build

On Debian 13 amd64 with internet access and at least 25 GB free disk space, install `live-build debootstrap cpio apt-utils xorriso squashfs-tools grub-pc-bin grub-efi-amd64-bin mtools dosfstools python3 python3-pil ca-certificates`, then run `sudo ./build.sh`.

Alternatively, open **Actions → Build SHIFT OS ISO** and run the workflow. A successful run uploads the ISO and its SHA-256 checksum as an artifact for 14 days. This build is not considered ready for real-hardware installation until it succeeds and is tested in a VM.

## Safety

Test the ISO in a virtual machine first. Installing onto a physical disk can erase its contents; back up your data before installing. SHIFT OS is a Debian derivative, not a distribution built from scratch. All underlying software retains its own licences and trademarks.