# OpenSCAD Multi-Architecture Packages

[![Docker Build](https://img.shields.io/github/actions/workflow/status/gounthar/openscad/docker-build-matrix.yml?branch=multiplatform&logo=docker&label=docker%20build&style=plastic)](https://github.com/gounthar/openscad/actions/workflows/docker-build-matrix.yml)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-025E8C?logo=dependabot&style=plastic)](https://github.com/gounthar/openscad/network/updates)
[![Docker Hub](https://img.shields.io/docker/pulls/gounthar/openscad?logo=docker&style=plastic)](https://hub.docker.com/r/gounthar/openscad)
[![GitHub Release](https://img.shields.io/github/v/release/gounthar/openscad?logo=github&style=plastic)](https://github.com/gounthar/openscad/releases/latest)

Automated build and packaging infrastructure for [OpenSCAD](https://openscad.org/) with **multi-architecture support** (x86_64, aarch64, riscv64).

**Available as:**
- 📦 **APT packages** for Debian/Ubuntu
- 📦 **RPM packages** for Fedora/RHEL/Rocky/AlmaLinux
- 🐳 **Docker images** for containerized environments
- 📥 **GitHub Releases** for direct download

## Supported Architectures

All packages and Docker images support multiple architectures:

| Architecture | Description | Package Arch | Docker Platform |
|--------------|-------------|--------------|-----------------|
| x86_64/amd64 | Intel/AMD 64-bit | `amd64` / `x86_64` | `linux/amd64` |
| aarch64/arm64 | ARM 64-bit (Apple Silicon, Raspberry Pi 4+) | `arm64` / `aarch64` | `linux/arm64` |
| riscv64 | RISC-V 64-bit | `riscv64` | `linux/riscv64` |

## Installation

### Package Repositories (Recommended)

Pre-built packages are available for Debian/Ubuntu and Fedora/RHEL-based distributions with automatic updates.

#### Debian/Ubuntu (APT)

```bash
# Import GPG key
curl -fsSL https://github.com/gounthar/docker-for-riscv64/releases/download/gpg-key/gpg-public-key.asc | \
  sudo gpg --dearmor -o /usr/share/keyrings/openscad-archive-keyring.gpg

# Add repository
echo "deb [signed-by=/usr/share/keyrings/openscad-archive-keyring.gpg] https://gounthar.github.io/openscad stable main" | \
  sudo tee /etc/apt/sources.list.d/openscad.list

# Update and install
sudo apt-get update
sudo apt-get install openscad
```

**Supported Distributions:**
- Debian Trixie (13) and newer
- Ubuntu 24.04 LTS and newer

#### Fedora/RHEL/Rocky/AlmaLinux (DNF/YUM)

```bash
# Import GPG key
sudo rpm --import https://gounthar.github.io/openscad/rpm/RPM-GPG-KEY

# Add repository
sudo curl -L https://gounthar.github.io/openscad/rpm/openscad.repo \
  -o /etc/yum.repos.d/openscad.repo

# Install
sudo dnf install openscad
```

**Supported Distributions:**
- Fedora 39 and newer
- RHEL/Rocky/AlmaLinux 9 and newer

### GitHub Releases

Pre-built `.deb` and `.rpm` packages are available from [GitHub Releases](https://github.com/gounthar/openscad/releases) for manual installation.

```bash
# Debian/Ubuntu example (replace with your architecture)
wget https://github.com/gounthar/openscad/releases/latest/download/openscad_YYYY.MM.DD-1_amd64.deb
sudo apt install ./openscad_YYYY.MM.DD-1_amd64.deb

# Fedora/RHEL example (replace with your architecture)
wget https://github.com/gounthar/openscad/releases/latest/download/openscad-YYYY.MM.DD-1.x86_64.rpm
sudo dnf install ./openscad-YYYY.MM.DD-1.x86_64.rpm
```

**Version Format:** `YYYY.MM.DD.BUILD_NUMBER`
- Example: `2025.11.20.33-1` = November 20, 2025, build #33

### Docker Images

Multi-architecture Docker images are available for running OpenSCAD in containers.

```bash
# Pull the multi-arch image (automatically selects your architecture)
docker pull gounthar/openscad:latest

# Render a SCAD file to STL
docker run --rm -v $(pwd):/work gounthar/openscad:latest /work/model.scad -o /work/output.stl

# Or use GitHub Container Registry
docker pull ghcr.io/gounthar/openscad:latest
```

### Example Usage

```bash
# Render with options
docker run --rm -v $(pwd):/work gounthar/openscad:latest \
    /work/model.scad \
    -o /work/output.stl \
    -D 'quality=50'

# Get help
docker run --rm gounthar/openscad:latest --help
```

## Repository Structure

This repository contains **only build infrastructure** - no OpenSCAD source code.

### Source Tree

```
.
├── upstream/           # Git submodule → openscad/openscad
├── docker/             # Dockerfiles for multi-arch builds
├── debian/             # Debian package control files
├── rpm/                # RPM spec files
├── .github/workflows/  # CI/CD pipelines (build, package, release)
└── .updatecli/         # Automated dependency updates
```

The actual OpenSCAD source code is pulled from the [upstream repository](https://github.com/openscad/openscad) as a git submodule.

### Package Repositories (GitHub Pages)

Package repositories are hosted on GitHub Pages at `https://gounthar.github.io/openscad`:

**APT Repository:**
```
dists/stable/main/
├── binary-amd64/     # x86_64 .deb packages
├── binary-arm64/     # aarch64 .deb packages
└── binary-riscv64/   # RISC-V .deb packages
pool/main/            # Package pool
```

**RPM Repository:**
```
rpm/fedora/
├── x86_64/           # x86_64 .rpm packages + metadata
├── aarch64/          # aarch64 .rpm packages + metadata
└── riscv64/          # riscv64 .rpm packages + metadata
```

## Building Locally

### Prerequisites

- Docker with buildx support
- QEMU for cross-architecture builds (for arm64/riscv64)

### Clone and Build

```bash
# Clone with submodule
git clone --recurse-submodules https://github.com/gounthar/openscad.git
cd openscad

# Build for your current architecture
docker buildx build -f docker/Dockerfile -t openscad:local .

# Build multi-arch and push
docker buildx build \
    --platform linux/amd64,linux/arm64,linux/riscv64 \
    -f docker/Dockerfile \
    -t gounthar/openscad:latest \
    --push .
```

## Automated Build and Release

This repository uses fully automated CI/CD:

### Dependency Management
- **Dependabot**: Weekly updates for Docker base images and GitHub Actions
- **UpdateCLI**: Advanced dependency tracking for Debian base image versions
- **Auto-merge**: Minor/patch updates merged automatically after CI passes

### Build Pipeline
1. **Docker Images**: Multi-arch images built from Debian Trixie base
2. **Package Extraction**: Binaries and assets extracted from Docker images
3. **Package Creation**: `.deb` and `.rpm` packages built with proper dependencies
4. **Repository Updates**: APT and RPM repositories updated automatically
5. **GitHub Releases**: Tagged releases created with all package artifacts

### Release Schedule
- **Automated**: Every successful build creates a new release
- **Versioning**: `YYYY.MM.DD.BUILD_NUMBER` format
- **Cleanup**: Old packages automatically removed after 7 days

## What is OpenSCAD?

OpenSCAD is a software for creating solid 3D CAD objects. It is free software and available for Linux/UNIX, MS Windows and macOS.

Unlike most free software for creating 3D models, OpenSCAD focuses on the CAD aspects rather than the artistic aspects of 3D modeling. It's a 3D-compiler that reads script files describing objects and renders 3D models from them.

**Learn more:**
- [OpenSCAD Website](https://openscad.org/)
- [OpenSCAD Manual](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual)
- [Upstream Repository](https://github.com/openscad/openscad)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Areas of Interest

- **Package Testing**: Testing on various distributions and architectures
- **Documentation**: Improving installation guides and troubleshooting
- **Build Optimizations**: Reducing build times and image sizes
- **Additional Distributions**: Support for Arch, openSUSE, Alpine, etc.
- **Additional Architectures**: ARMv7, ppc64le, s390x support
- **Workflow Improvements**: CI/CD pipeline enhancements

## License

OpenSCAD is licensed under the GNU General Public License version 2 (GPL-2.0).

See [COPYING](COPYING) for details.
