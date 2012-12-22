Summary:	Integrates polkit authentication for MATE desktop
Name:		mate-polkit
Version:	1.5.0
Release:	1
License:	LGPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	5639bec0c7667b5be9bbf2bac2931b31
URL:		http://mate-desktop.org/
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+2-devel
BuildRequires:	mate-common
BuildRequires:	polkit-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
# needed for gobject-introspection support somehow,
# https://bugzilla.redhat.com/show_bug.cgi?id=847419#c17 asserts this is a bug (elsewhere)
# but I'm not entirely sure -- rex
BuildRequires:	cairo-gobject-devel
#Provides:	PolicyKit-authentication-agent
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Integrates polkit with the MATE Desktop environment

%package devel
Summary:	Integrates polkit with the MATE Desktop environment
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development libraries for mate-polkit

%prep
%setup -q

%build
NOCONFIGURE=1 ./autogen.sh --disable-static
%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libpolkit-gtk-mate-1.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
# yes, license really is LGPLv2+, despite included COPYING is about GPL, poke upstreamo
# to include COPYING.LIB here instead  -- rex
%doc AUTHORS COPYING README
%{_sysconfdir}/xdg/autostart/polkit-mate-authentication-agent-1.desktop
%attr(755,root,root) %{_libdir}/libpolkit-gtk-mate-1.so.*.*.*
%ghost %{_libdir}/libpolkit-gtk-mate-1.so.0
%{_libdir}/girepository-1.0/PolkitGtkMate-1.0.typelib
%{_libexecdir}/polkit-mate-authentication-agent-1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libpolkit-gtk-mate-1.so
%{_pkgconfigdir}/polkit-gtk-mate-1.pc
%{_includedir}/polkit-gtk-mate-1
%{_datadir}/gir-1.0/PolkitGtkMate-1.0.gir
