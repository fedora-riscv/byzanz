%global git 64ab7a13975247647cb4043e0144097eb2fa12b7
Summary: A desktop recorder
Name: byzanz
Version: 0.3
Release: 0.6%{?dist}
License: GPLv3+
Group: Applications/Multimedia
URL: http://git.gnome.org/browse/byzanz/
#Source0: http://download.gnome.org/sources/%{name}/0.2/%{name}-%{version}.tar.bz2
# git archive --format=tar --prefix=byzanz-%{git}/ %{git} | xz > byzanz-%{git}
Source0: byzanz-%{git}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gnome-common
BuildRequires: cairo-devel >= 1.8.10
BuildRequires: gtk2-devel >= 2.17.10
BuildRequires: libXdamage-devel >= 1.0
BuildRequires: glib2-devel >= 2.6.0
BuildRequires: gnome-panel-devel >= 2.91.91
BuildRequires: gstreamer-devel >= 0.10.24
BuildRequires: gstreamer-plugins-base-devel >= 0.10.24
BuildRequires: gettext-devel
BuildRequires: intltool
BuildRequires: perl(XML::Parser)
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake

Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

Patch0: 0001-Deal-with-various-deprecations.patch

%description
Byzanz is a desktop recorder striving for ease of use. It can record to 
GIF images, Ogg Theora video - optionally with sound - and other formats.
A GNOME panel applet and a command-line recording tool are included.

%prep
%setup -q -n byzanz-%{git}
%patch0 -p1

%build
./autogen.sh
CFLAGS="%optflags -Wno-deprecated-declarations"
%configure
make

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
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files -f byzanz.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS

%{_sysconfdir}/gconf/schemas/byzanz.schemas
%{_bindir}/byzanz-playback
%{_bindir}/byzanz-record
%{_libexecdir}/byzanz-applet
%{_datadir}/dbus-1/services/org.gnome.panel.applet.ByzanzAppletFactory.service
%{_datadir}/gnome-2.0/ui/byzanzapplet.xml
%{_datadir}/gnome-panel/4.0/applets/org.gnome.ByzanzApplet.panel-applet
%{_datadir}/icons/hicolor/*/apps/byzanz-record-area.*
%{_datadir}/icons/hicolor/*/apps/byzanz-record-desktop.*
%{_datadir}/icons/hicolor/*/apps/byzanz-record-window.*
%{_mandir}/man1/byzanz-playback.1*
%{_mandir}/man1/byzanz-record.1*

%changelog
* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 Matthias Clasen <mclasen@redhat.com> - 0.3-0.4
- Deal with deprecations

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.3-0.3
- Rebuild for new libpng

* Fri Jun 24 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.3-0.2
- Update git snapshot (translation updates only)

* Wed Mar 23 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.3-0.1
- Update to prerelease of 0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 13 2010 Benjamin Otte <otte@redhat.com> - 0.2.2-1
- Update to 0.2.2

* Mon Feb 22 2010 Benjamin Otte <otte@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.1-6
- Rebuild for GCC 4.3

* Fri Aug 24 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.1-5
- Update license tag.

* Mon Aug 28 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.1-4
- BR perl(XML::Parser)

* Mon Aug 28 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.1-3
- Bump release and rebuild.

* Wed Jun 14 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.1-2
- Add gettext-devel BR

* Mon May 29 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.1-1
- Update to 1.1.1.

* Mon Feb 20 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.0-6
- Bump for another rebuild.

* Mon Feb 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.0-5
- Previous build failed, try without %%{_smp_mflags}.

* Mon Feb 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.0-4
- Bump release again.

* Mon Feb 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.0-3
- Bump release and rebuild for new gcc4.1 and glibc.

* Thu Jan 26 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.0-2
- Add post and postun scripts to update the GTK+ icon cache.

* Thu Jan 26 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.1.0-1
- Update to 0.1.0
- Add scriptlet for installing GConf schema.

* Thu Jan 19 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-3
- Bump release.

* Fri Jan 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1
- Initial build.

