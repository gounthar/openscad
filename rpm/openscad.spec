Name:           openscad
Version:        2025.11.19
Release:        1%{?dist}
Summary:        The Programmer's Solid 3D CAD Modeller

License:        GPL-2.0-or-later
URL:            https://openscad.org/

# Pre-built binary package - no source required
# Binaries extracted from Docker image

# Runtime dependencies for Fedora
Requires:       qt5-qtbase
Requires:       qt5-qtmultimedia
Requires:       qt5-qtsvg
Requires:       CGAL
Requires:       opencsg
Requires:       qscintilla-qt5
Requires:       freetype
Requires:       fontconfig
Requires:       harfbuzz
Requires:       glew
Requires:       gmp
Requires:       mpfr
Requires:       libzip
Requires:       double-conversion
Requires:       tbb
Requires:       boost-filesystem
Requires:       boost-regex
Requires:       boost-system
Requires:       lib3mf

Recommends:     openscad-MCAD

%description
OpenSCAD is a software for creating solid 3D CAD objects. It focuses on CAD
aspects rather than artistic ones.

OpenSCAD is not an interactive modeller. Instead it is something like a
3D-compiler that reads in a script file that describes the object and renders
the 3D model from this script. This gives the designer full control over the
modelling process and enables him to easily change any step in the modelling
process or make designs that are defined by configurable parameters.

This package contains pre-built binaries extracted from Docker images.

%prep
# No preparation needed - pre-built binaries

%build
# No build needed - pre-built binaries

%install
# Create necessary directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -d %{buildroot}%{_datadir}/metainfo
install -d %{buildroot}%{_datadir}/mime/packages
install -d %{buildroot}%{_datadir}/openscad

# Install binary
install -p -m 0755 %{_sourcedir}/openscad %{buildroot}%{_bindir}/openscad

# Install data files if present
if [ -d %{_sourcedir}/share ]; then
    # Copy specific data files
    cp -a %{_sourcedir}/share/applications %{buildroot}%{_datadir}/ 2>/dev/null || true
    cp -a %{_sourcedir}/share/icons %{buildroot}%{_datadir}/ 2>/dev/null || true
    cp -a %{_sourcedir}/share/metainfo %{buildroot}%{_datadir}/ 2>/dev/null || true
    cp -a %{_sourcedir}/share/mime %{buildroot}%{_datadir}/ 2>/dev/null || true
    # Create openscad directory (ownership claimed by package)
    # Do not copy any library files from Docker image
fi

%files
%{_bindir}/openscad
%{_datadir}/applications/openscad.desktop
%{_datadir}/icons/hicolor/*/apps/openscad.*
%{_datadir}/metainfo/org.openscad.OpenSCAD.appdata.xml
%{_datadir}/mime/packages/openscad.xml
%dir %{_datadir}/openscad/

%changelog
* Wed Nov 19 2025 Bruno Verachten <gounthar@gmail.com> - 2025.11.19-1
- Multi-architecture package from Docker image
- Supports x86_64, aarch64, and riscv64 architectures
