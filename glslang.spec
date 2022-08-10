#
# spec file for package glslang
#
# Copyright (c) 2022 openEuler
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.



%define lname libglslang11
Name:           glslang
Version:        11.8.0
Release:        2
Summary:        OpenGL and OpenGL ES shader front end and validator
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++
URL:            https://www.khronos.org/opengles/sdk/tools/Reference-Compiler/
#Git-URL:	https://github.com/KhronosGroup/glslang
Source:         https://github.com/KhronosGroup/glslang/archive/%version.tar.gz
Source3:        baselibs.conf
Patch0:         0001-build-set-SOVERSION-on-all-libraries.patch
BuildRequires:  bison
BuildRequires:  cmake >= 2.8
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  ninja-build

%description
glslang is a compiler front end for the OpenGL ES and OpenGL shading
languages. It implements a strict interpretation of the
specifications for these languages.

%package -n %lname
Summary:        OpenGL and OpenGL ES shader front end implementation
Group:          System/Libraries

%description -n %lname
glslang is a compiler front end for the OpenGL ES and OpenGL shading
languages. It implements a strict interpretation of the
specifications for these languages.

%package devel
Summary:        OpenGL and OpenGL ES shader front end and validator
Group:          Development/Libraries/C and C++
Requires:       %lname = %version

%description devel
glslang is a compiler front end for the OpenGL ES and OpenGL shading
languages. It implements a strict interpretation of the
specifications for these languages.

spirv-remap is a utility to improve compression of SPIR-V binary
files via entropy reduction, plus optional stripping of debug
information and load/store optimization. It transforms SPIR-V to
SPIR-V, remapping IDs. The resulting modules have an increased ID
range (IDs are not as tightly packed around zero), but will compress
better when multiple modules are compressed together, since
compressor's dictionary can find better cross module commonality.

%prep
%autosetup -p1

%build
%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects
# Refactor: Build twice and deliver both shared and static ones.
%cmake -B build-shared \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX=/usr \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=ON
%ninja_build -C build-shared

%cmake -B build-static \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX=/usr \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF
%ninja_build -C build-static

%install
# Install for both shared and static.
%global _lto_cflags %{_lto_cflags} -ffat-lto-objects
%ninja_install -C build-shared
%ninja_install -C build-static
b="%buildroot"
# Remove .a file breaks 3rd party apps expectations -- jchzhou
# 3rd party programs use -lOGLCompiler (because pristine glslang ships .a files),
# so satisfy them under our shared build.
ln -s libglslang.so "$b/%{_libdir}/libOGLCompiler.so"
ln -s libglslang.so "$b/%{_libdir}/libOSDependent.so"
%fdupes %{buildroot}/%{_prefix}

%post   -n %lname -p /sbin/ldconfig
%postun -n %lname -p /sbin/ldconfig

%files -n %lname
%_libdir/*.so.11*

%files devel
%_bindir/gls*
%_bindir/spirv*
%_libdir/cmake/
%_libdir/*resource*.so
%_libdir/libHLSL.so
%_libdir/libOGLCompiler.so
%_libdir/libOSDependent.so
%_libdir/libSPIRV.so
%_libdir/libSPVRemapper.so
%_libdir/libglslang.so
%{_libdir}/libHLSL.a
%{_libdir}/libOGLCompiler.a
%{_libdir}/libOSDependent.a
%{_libdir}/libSPIRV.a
%{_libdir}/libSPVRemapper.a
%{_libdir}/libglslang.a
%{_libdir}/libGenericCodeGen.a
%{_libdir}/libMachineIndependent.a
%{_libdir}/libglslang-default-resource-limits.a
%_includedir/*

%changelog
* Tue Aug 09 2022 Jchzhou <jchzhou@outlook.com> 11.8.0-2
- Add .a files back to meet 3rd party apps' expectations
- build/install with ninja macros

* Fri Apr 15 2022 Jingwiw <ixoote@gmail.com> 11.8.0-1
- init from openSUSE
  author: openSUSE
  url: https://build.opensuse.org/package/view_file/openSUSE:Factory:RISCV/glslang
  changes: https://build.opensuse.org/package/view_file/openSUSE:Factory:RISCV/glslang/glslang.changes