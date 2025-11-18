Name:           openscad
Version:        2024.11.18
Release:        1%{?dist}
Summary:        The Programmers Solid 3D CAD Modeller

# Upstream commit for this build
%global commit 63150dbbae53b2c8dbd75143a57409e60c1eb404
%global shortcommit %(c=%{commit}; echo ${c:0:7})

License:        GPL-2.0-or-later
URL:            https://openscad.org/
Source0:        https://github.com/openscad/openscad/archive/%{commit}/openscad-%{shortcommit}.tar.gz

BuildRequires:  cmake >= 3.5
BuildRequires:  gcc-c++
BuildRequires:  qt5-qtbase-devel >= 5.4
BuildRequires:  CGAL-devel >= 5.4
BuildRequires:  opencsg-devel >= 1.3.0
BuildRequires:  qscintilla-qt5-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  freetype-devel
BuildRequires:  fontconfig-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  eigen3-devel
BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel
BuildRequires:  libzip-devel
BuildRequires:  cairo-devel
BuildRequires:  lib3mf-devel
BuildRequires:  libspnav-devel
BuildRequires:  qt5-qtgamepad-devel
BuildRequires:  bison >= 2.4
BuildRequires:  flex >= 2.5.35
BuildRequires:  glew-devel >= 1.5.4
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  python3
BuildRequires:  boost-regex-devel >= 1.61.0
BuildRequires:  boost-system-devel >= 1.61.0
BuildRequires:  boost-filesystem-devel >= 1.61.0
BuildRequires:  pkgconf
BuildRequires:  ImageMagick
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-dri-drivers
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  double-conversion-devel
BuildRequires:  git

Requires:       qt5-qtbase
Requires:       CGAL
Requires:       opencsg
Requires:       qscintilla-qt5

Recommends:     openscad-MCAD

%description
OpenSCAD is a software for creating solid 3D CAD objects. It focuses on CAD
aspects rather than artistic ones.

OpenSCAD is not an interactive modeller. Instead it is something like a
3D-compiler that reads in a script file that describes the object and renders
the 3D model from this script. This gives the designer full control over the
modelling process and enables him to easily change any step in the modelling
process or make designs that are defined by configurable parameters.

This package provides multi-architecture builds (x86_64, aarch64, riscv64).

%prep
%autosetup -n openscad-%{commit}

%build
%cmake -DEXPERIMENTAL=1 -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

# Remove bundled libraries
rm -rf %{buildroot}%{_datadir}/openscad/libraries
rm -rf %{buildroot}%{_datadir}/openscad/fonts

%files
%license COPYING
%doc README.md RELEASE_NOTES.md
%{_bindir}/openscad
%{_datadir}/applications/openscad.desktop
%{_datadir}/icons/hicolor/*/apps/openscad.*
%{_datadir}/metainfo/org.openscad.OpenSCAD.appdata.xml
%{_datadir}/mime/packages/openscad.xml
%{_datadir}/openscad/

%changelog
* Mon Nov 18 2024 Bruno Verachten <gounthar@gmail.com> - 2024.11.18-1
- Initial multi-architecture package build
- Built from upstream commit 63150dbb
- Supports x86_64, aarch64, and riscv64 architectures
- Uses CMake build system with experimental features enabled
