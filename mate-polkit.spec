#
# Conditional build:
%bcond_without	appindicator	# application indicators support
%bcond_with	gtk3		# use GTK+ 3.x instead of 2.x

%define	gtk2_ver	2:2.24.0
%define	gtk3_ver	3.0.0
Summary:	Integrates polkit authentication for MATE desktop
Summary(pl.UTF-8):	Integracja uwierzytelniania polkit ze środowiskiem MATE
Name:		mate-polkit
Version:	1.14.0
Release:	1
License:	LGPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.14/%{name}-%{version}.tar.xz
# Source0-md5:	1259f8b245917ecfb22fc9d8ff309d2c
URL:		http://wiki.mate-desktop.org/mate-polkit
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-tools >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gobject-introspection-devel >= 0.6.2
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= %{gtk2_ver}}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= %{gtk3_ver}}
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	intltool >= 0.35.0
%if %{with appindicator}
%{!?with_gtk3:BuildRequires:	libappindicator-gtk2-devel >= 0.0.13}
%{?with_gtk3:BuildRequires:	libappindicator-gtk3-devel >= 0.0.13}
%endif
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	mate-common
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.97
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
# needed for gobject-introspection support (Gtk-2.0.gir -> Gdk-2.0.gir -> cairo-1.0.gir, which requires libcairo-gobject.so)
BuildRequires:	cairo-gobject-devel
Requires:	glib2 >= 1:2.36.0
%{!?with_gtk3:Requires:	gtk+2 >= %{gtk2_ver}}
%{?with_gtk3:Requires:	gtk+3 >= %{gtk3_ver}}
Requires:	polkit-libs >= 0.97
%if %{with appindicator}
%{!?with_gtk3:Requires:	libappindicator-gtk2 >= 0.0.13}
%{?with_gtk3:Requires:	libappindicator-gtk3 >= 0.0.13}
%endif
#Provides:	PolicyKit-authentication-agent
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE polkit integrates polkit with the MATE Desktop environment. MATE
polkit is a fork of GNOME polkit.

%description -l pl.UTF-8
Integracja uwierzytelniania polkit ze środowiskiem MATE. MATE polkit
to odgałęzienie pakietu GNOME polkit.

%package devel
Summary:	Development files for mate-polkit library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki mate-polkit
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36.0
%{!?with_gtk3:Requires:	gtk+2-devel >= %{gtk2_ver}}
%{?with_gtk3:Requires:	gtk+3-devel >= %{gtk3_ver}}
Requires:	polkit-devel >= 0.97

%description devel
Development files for mate-polkit library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki mate-polkit.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_appindicator:--disable-appindicator} \
	--disable-silent-rules \
	--disable-static \
	%{?with_gtk3:--with-gtk=3.0}

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libpolkit-gtk-mate-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolkit-gtk-mate-1.so.0
%{_libdir}/girepository-1.0/PolkitGtkMate-1.0.typelib
%attr(755,root,root) %{_libexecdir}/polkit-mate-authentication-agent-1
%{_sysconfdir}/xdg/autostart/polkit-mate-authentication-agent-1.desktop

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpolkit-gtk-mate-1.so
%{_includedir}/polkit-gtk-mate-1
%{_datadir}/gir-1.0/PolkitGtkMate-1.0.gir
%{_pkgconfigdir}/polkit-gtk-mate-1.pc
