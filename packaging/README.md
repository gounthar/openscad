# Packaging

This directory contains packaging specifications for creating distribution-specific packages for multiple architectures.

## Supported Architectures

- **amd64** (x86_64) - GitHub-hosted runners
- **arm64** (aarch64) - Self-hosted runners required
- **riscv64** - Self-hosted runners required

## Package Formats

### Debian/Ubuntu (`packaging/debian/`)

Contains complete Debian packaging files:

- `control` - Package metadata and dependencies
- `rules` - Build rules using CMake
- `changelog` - Package version history
- `copyright` - License information
- `openscad.install` - Installation file list

**Build locally:**

```bash
# Install build dependencies
sudo apt-get install build-essential debhelper devscripts cmake \
    qtbase5-dev libcgal-dev libopencsg-dev libqscintilla2-qt5-dev \
    # ... (see control file for full list)

# Copy packaging to upstream source
cp -r packaging/debian upstream/debian

# Build package
cd upstream
dpkg-buildpackage -us -uc -b

# Packages will be in parent directory
ls ../*.deb
```

### Fedora/RHEL (`packaging/fedora/`)

Contains RPM spec file:

- `openscad.spec` - Complete RPM specification

**Build locally:**

```bash
# Install build dependencies
sudo dnf builddep packaging/fedora/openscad.spec

# Build RPM
rpmbuild -bb packaging/fedora/openscad.spec
```

## GitHub Actions Workflow

The `.github/workflows/build-packages.yml` workflow builds packages automatically:

### Triggers

- **Push to multiplatform branch** - When packaging files change
- **Pull requests** - When packaging files are modified
- **Manual dispatch** - Via GitHub Actions UI

### Architecture Strategy

| Architecture | Runner Type | Expected Build Time |
|-------------|-------------|---------------------|
| amd64 | GitHub-hosted (ubuntu-latest) | ~30-40 minutes |
| arm64 | Self-hosted | ~40-60 minutes |
| riscv64 | Self-hosted | ~1-2 hours |

### Self-Hosted Runner Setup

For arm64 and riscv64 builds, you need to set up self-hosted runners with these labels:

**arm64 runner:**
```yaml
runs-on: [self-hosted, linux, arm64]
```

**riscv64 runner:**
```yaml
runs-on: [self-hosted, linux, riscv64]
```

#### Prerequisites for Self-Hosted Runners

1. **Debian Trixie** or **Ubuntu 24.04+** (for recent CGAL and dependencies)
2. **Build tools**: `build-essential`, `cmake`, `git`
3. **OpenSCAD dependencies**: Qt5, CGAL, Boost, etc.
4. **GitHub Actions runner**: [github-act-runner](https://github.com/ChristopherHX/github-act-runner) for riscv64

#### Runner Registration

```bash
# For official GitHub runner (amd64/arm64)
./config.sh --url https://github.com/gounthar/openscad \
    --token YOUR_TOKEN \
    --name your-runner-name \
    --labels self-hosted,linux,arm64

# For github-act-runner (riscv64)
./github-act-runner configure \
    --url https://github.com/gounthar/openscad \
    --token YOUR_TOKEN \
    --name bananapi-f3-runner \
    --labels self-hosted,linux,riscv64
```

### Running Manually

```bash
# Trigger workflow
gh workflow run build-packages.yml

# Watch progress
gh run watch
```

## Memory Requirements

OpenSCAD builds are memory-intensive. Each compilation process can use 2-3GB of RAM. The build rules automatically limit parallelism based on available memory:

- **4GB RAM**: ~1 parallel job
- **8GB RAM**: ~2-3 parallel jobs
- **16GB RAM**: ~5-6 parallel jobs

## Dependencies

### Debian/Ubuntu Package Names

Key build dependencies (see `debian/control` for full list):

- `cmake` (>= 3.5)
- `qtbase5-dev` (>= 5.4)
- `libcgal-dev` (>= 5.4)
- `libopencsg-dev` (>= 1.3.0)
- `libboost-dev` (>= 1.61.0)
- `libqscintilla2-qt5-dev`
- `libeigen3-dev`
- `libgmp-dev`, `libmpfr-dev`
- `bison`, `flex`

### Fedora/RHEL Package Names

See `fedora/openscad.spec` for equivalent package names.

## Contributing

### Adding Support for Other Distributions

1. Create a new subdirectory (e.g., `packaging/arch/`)
2. Add the distribution-specific packaging files
3. Update the GitHub workflow to include new build jobs
4. Document the build process in this README

### Updating Dependencies

When upstream OpenSCAD updates dependencies:

1. Update `debian/control` Build-Depends
2. Update `fedora/openscad.spec` BuildRequires
3. Test builds on all architectures

## References

- [OpenSCAD Build Documentation](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Building_on_Linux/UNIX)
- [Debian Packaging Guide](https://www.debian.org/doc/manuals/debmake-doc/)
- [RPM Packaging Guide](https://rpm-packaging-guide.github.io/)
- [GitHub Self-Hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners)
