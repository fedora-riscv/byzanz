Summary: A desktop recorder
Name: byzanz
Version: 0.0.3
Release: 3%{?dist}
License: GPL
Group: Applications/Multimedia
URL: http://www.freedesktop.org/~company/byzanz/
Source0: http://www.freedesktop.org/~company/byzanz/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gtk2-devel >= 2.6.0
BuildRequires: libXdamage-devel >= 1.0
BuildRequires: glib2-devel >= 2.6.0
BuildRequires: gnome-panel-devel >= 2.10.0
BuildRequires: gnome-vfs2-devel >= 2.12.0
BuildRequires: libgnomeui-devel >= 2.12.0

%description
Byzanz is a desktop recorder. Just like Istanbul. But it doesn't
record to Ogg Theora, but to GIF.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
%find_lang byzanz

%clean
rm -rf %{buildroot}

%files -f byzanz.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS

%{_bindir}/byzanz-record
%{_libdir}/bonobo/servers/ByzanzApplet.server
%{_libexecdir}/byzanz-applet

%changelog
* Thu Jan 19 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-3
- Bump release.

* Fri Jan 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1
- Initial build.

