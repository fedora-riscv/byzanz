Summary: A desktop recorder
Name: byzanz
Version: 0.1.0
Release: 1%{?dist}
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

Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

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
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=%{buildroot} install
%find_lang byzanz

%clean
rm -rf %{buildroot}

%pre
if [ $1 -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    if [ -f %{_sysconfdir}/gconf/schemas/byzanz.schemas ]; then
        gconftool-2 --makefile-uninstall-rule \
          %{_sysconfdir}/gconf/schemas/byzanz.schemas >/dev/null || :
        killall -HUP gconfd-2 || :
    fi
fi

%preun
if [ $1 -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/byzanz.schemas > /dev/null || :
    killall -HUP gconfd-2 || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/byzanz.schemas > /dev/null || :
killall -HUP gconfd-2 || :

%files -f byzanz.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS

%{_sysconfdir}/gconf/schemas/byzanz.schemas
%{_bindir}/byzanz-record
%{_libdir}/bonobo/servers/ByzanzApplet.server
%{_libexecdir}/byzanz-applet
%{_datadir}/gnome-2.0/ui/byzanzapplet.xml
%{_datadir}/icons/hicolor/24x24/apps/byzanz-record-area.png
%{_datadir}/icons/hicolor/24x24/apps/byzanz-record-screen.png
%{_datadir}/icons/hicolor/24x24/apps/byzanz-record-window.png

%changelog
* Thu Jan 26 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.0-1
- Update to 0.1.0
- Add scriptlet for installing GConf schema.

* Thu Jan 19 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-3
- Bump release.

* Fri Jan 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1
- Initial build.

