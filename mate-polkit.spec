#
# Conditional build:
%bcond_without	appindicator	# application indicators support

%define	gtk3_ver	3.22.0
Summary:	Integrates polkit authentication for MATE desktop
Summary(pl.UTF-8):	Integracja uwierzytelniania polkit ze środowiskiem MATE
Name:		mate-polkit
Version:	1.28.1
Release:	1
License:	LGPL v2+
Group:		X11/Applications
Source0:	https://pub.mate-desktop.org/releases/1.28/%{name}-%{version}.tar.xz
# Source0-md5:	4cb48a238219a894b24e5395b75aac90
URL:		https://wiki.mate-desktop.org/mate-desktop/components/mate-polkit/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gobject-introspection-devel >= 0.6.2
BuildRequires:	gtk+3-devel >= %{gtk3_ver}
BuildRequires:	gtk-doc >= 1.3
%if %{with appindicator}
BuildRequires:	libayatana-appindicator-gtk3-devel >= 0.0.13
%endif
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	mate-common
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.97
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
# needed for gobject-introspection support (Gtk-3.0.gir -> Gdk-3.0.gir -> cairo-1.0.gir, which requires libcairo-gobject.so)
BuildRequires:	cairo-gobject-devel
Requires:	glib2 >= 1:2.50.0
Requires:	gtk+3 >= %{gtk3_ver}
Requires:	polkit-libs >= 0.97
%if %{with appindicator}
Requires:	libayatana-appindicator-gtk3 >= 0.0.13
%endif
Obsoletes:	mate-polkit-devel < 1.20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE polkit integrates polkit with the MATE Desktop environment. MATE
polkit is a fork of GNOME polkit.

%description -l pl.UTF-8
Integracja uwierzytelniania polkit ze środowiskiem MATE. MATE polkit
to odgałęzienie pakietu GNOME polkit.

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
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{frp,ie,ku_IQ,ur_PK}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libexecdir}/polkit-mate-authentication-agent-1
%{_sysconfdir}/xdg/autostart/polkit-mate-authentication-agent-1.desktop
