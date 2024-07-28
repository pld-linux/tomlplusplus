#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	TOML config file parser and serializer for C++17
Name:		tomlplusplus
Version:	3.4.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/marzer/tomlplusplus/releases
Source0:	https://github.com/marzer/tomlplusplus/archive/v%{version}/%{name}-v%{version}.tar.gz
# Source0-md5:	c1f32ced14311fe949b9ce7cc3f7a867
URL:		https://marzer.github.io/tomlplusplus/
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	meson >= 0.61.0
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TOML config file parser and serializer for C++17.

%package devel
Summary:	Header files for tomlplusplus
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:8

%description devel
Header files for tomlplusplus.

%package static
Summary:	Static tomlplusplus libraries
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tomlplusplus libraries.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md CONTRIBUTING.md LICENSE README.md
%attr(755,root,root) %{_libdir}/libtomlplusplus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtomlplusplus.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtomlplusplus.so
%{_includedir}/toml++
%{_libdir}/cmake/tomlplusplus
%{_pkgconfigdir}/tomlplusplus.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtomlplusplus.a
%endif
