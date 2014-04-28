# Remsnet Spec file for package fakeroot
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



Name: fakeroot
Group: Development/Languages
Version: 1.20
Release: 3
License: GPL
Summary: Gives a fake root environment
Autoreqprov: on
URL:    https://wiki.debian.org/FakeRoot
Source0:  http://ftp.debian.org/debian/pool/main/f/%{name}/%{name}_%{version}.orig.tar.bz2
BuildRoot:%{_tmppath}/%{name}-%{version}-build
# build essentials
BuildRequires: sharutils
BuildRequires: coreutils
BuildRequires: libacl-devel
BuildRequires: glibc-devel
Requires: sharutils
Requires: libacl
Requires: coreutils

%description
fakeroot runs a command in an environment were it appears to have root
privileges for file manipulation. This is useful for allowing users to
create archives (tar, ar, .deb etc.) with files in them with root
permissions/ownership. Without fakeroot one would have to have root
privileges to create the constituent files of the archives with the
correct permissions and ownership, and then pack them up, or one would
have to construct the archives directly, without using the archiver.

fakeroot works by replacing the file manipulation library functions
(chmod(), stat() etc.) by ones that simulate the effect the real
library functions would have had, had the user really been root. These
wrapper functions are in a shared library libfakeroot.so*, which is
loaded through the LD_PRELOAD mechanism of the dynamic loader.

This package is intended to enable something like:
dpkg-buildpackage -rfakeroot
i.e. to remove the need to become root for a package build.
This is done by setting LD_PRELOAD to libfakeroot.so,
which provides wrappers around getuid, chown, chmod, mknod,
stat, and so on, thereby creating a fake root environment.

fakeroot requires SYSV IPC or TCP to operate.

%prep
%setup -q -n %{name}-%{version}

%build
unset POSIXLY_CORRECT
mkdir obj-sysv obj-tcp
(
    cd obj-sysv
    CFLAGS="$RPM_OPT_FLAGS" ../configure --prefix=/usr --mandir=/usr/share/man \
        --libdir=%_libdir --program-suffix=-sysv --disable-static
    make
    )
(
    cd obj-tcp
    CFLAGS="$RPM_OPT_FLAGS" ../configure --prefix=/usr \
        --mandir=/usr/share/man --libdir=%_libdir --with-ipc=tcp \
        --program-suffix=-tcp --disable-static
    make
    )

%install
unset POSIXLY_CORRECT
make -C obj-tcp DESTDIR="$RPM_BUILD_ROOT" install
mv $RPM_BUILD_ROOT/%_libdir/libfakeroot-0.so \
    $RPM_BUILD_ROOT/%_libdir/libfakeroot-tcp.so
make -C obj-sysv DESTDIR="$RPM_BUILD_ROOT" install
mv $RPM_BUILD_ROOT/%_libdir/libfakeroot-0.so \
    $RPM_BUILD_ROOT/%_libdir/libfakeroot-sysv.so
cd $RPM_BUILD_ROOT/%_libdir

# cleanup
rm $RPM_BUILD_ROOT/%_libdir/libfakeroot.*a
rm $RPM_BUILD_ROOT/%_libdir/libfakeroot.so
#rm -fr $RPM_BUILD_ROOT/%{_mandir}/es
#rm -fr $RPM_BUILD_ROOT/%{_mandir}/fr
#rm -fr $RPM_BUILD_ROOT/%{_mandir}/sv
#rm -fr $RPM_BUILD_ROOT/%{_mandir}/nl
gzip -9 $RPM_BUILD_ROOT/%{_mandir}/man?/*.?

#ln -fs $RPM_BUILD_ROOT/usr/bin/fakeroot-sysv $RPM_BUILD_ROOT/usr/bin/fakeroot
#ln -fs $RPM_BUILD_ROOT/usr/bin/faked-sys $RPM_BUILD_ROOT/usr/bin/faked
cd  $RPM_BUILD_ROOT/usr/bin/
        ln -s fakeroot-sysv fakeroot
        ln -s faked-sysv faked
cd



%files -n fakeroot
%defattr(0755,root,root,0755)
/usr/bin/faked
/usr/bin/fakeroot
/usr/bin/faked-sysv
/usr/bin/faked-tcp
/usr/bin/fakeroot-sysv
/usr/bin/fakeroot-tcp
%_libdir/libfakeroot-sysv.so
%_libdir/libfakeroot-tcp.so

%defattr(644,root,root,755)
%doc AUTHORS BUGS COPYING DEBUG INSTALL README
%_mandir/nl/man1/fakeroot-*
%_mandir/nl/man1/faked-*
%_mandir/sv/man1/faked-*
%_mandir/sv/man1/fakeroot-*
%_mandir/fr/man1/fakeroot-*
%_mandir/fr/man1/faked-*
%_mandir/es/man1/faked-*
%_mandir/es/man1/fakeroot-*
%_mandir/de/man1/faked-*
%_mandir/de/man1/fakeroot-*
%_mandir/man1/faked-*
%_mandir/man1/fakeroot-*


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Apr 28 2014 support@remsnet.de 1.20-r4
- bumped to v1.20
