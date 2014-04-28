# Remsnet Spec file for package :debootstrap
#
# Copyright (c) 1995-2008 Remsnet Netzwerk Service OhG , D-73630 Remshalden
# Copyright (c) 2008-2014 Remsnet Consullting & Internet Services LTD , D-40476 Duesseldorf

# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://github.com/remsnet/xen-tools

Name:           debootstrap
Version:        1.0.59
Release:        4
Summary:        Debian GNU/Linux bootstrapper
Packager:       Horst Venzke <horst.venzke@remsnet.de>
Group:          System Environment/Base
License:        MIT
URL:            https://wiki.debian.org/de/Debootstrap
Source0:        http://ftp.debian.org/debian/pool/main/d/debootstrap/debootstrap_%{version}.tar.xz
Patch0:         debootstrap-devices.patch
Patch1:         debootstrap-perms.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       coreutils, gettext, wget, tar, gzip, binutils, gnupg
Requires:       fakeroot
Requires:       makedev
Provides:       debootstrap

BuildRequires:  coreutils
BuildRequires:  fakeroot

%if 0%{?fedora_version} ||  0%{?rhel_version} || 0%{?centos_version}
BuildRequires:   MAKEDEV
%endif

%if 0%{?suse_version} || 0%{?sles_version}
BuildRequires:  makedev
%endif


%description
debootstrap is used to create a Debian base system from scratch, without
requiring the availability of dpkg or apt.  It does this by downloading
.deb files from a mirror site, and carefully unpacking them into a
directory which can eventually be chrooted into.

This might be often useful coupled with virtualization techniques to run
Debian GNU/Linux guest system.


%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
# in Makefile, path is hardcoded, modify it to take rpm macros into account
sed -i -e 's;/usr/sbin;%{_sbindir};' Makefile

# _smp_mflags would make no sense at all
fakeroot make


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/debootstrap/scripts/
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 0644 debootstrap.8 $RPM_BUILD_ROOT%{_mandir}/man8
make install DESTDIR=$RPM_BUILD_ROOT \
       VERSION="%{version}-%{release}" \
       DSDIR=$RPM_BUILD_ROOT%{_datadir}/debootstrap
# substitute the rpm macro path
sed -i -e 's;/usr/share;%{_datadir};' $RPM_BUILD_ROOT%{_sbindir}/debootstrap
# correct the debootstrap script timestamp
touch -r debootstrap  $RPM_BUILD_ROOT%{_sbindir}/debootstrap


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_datadir}/debootstrap
%{_sbindir}/debootstrap
%{_mandir}/man8/debootstrap.8*
%doc debian/changelog debian/copyright README


%changelog
* Mon Apr 28 2014 support@remsnet.de 1.0.59-r4
- Bump to 1.0.59 release
- smal rpmbuild fixes
- update BuildRequires , Requires

* Sun Mar 31 2013 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.47-1
- new upstream release:
  + properly decrypt InRelease file if available
