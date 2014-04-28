# Remsnet Spec file for package for rpmstrap
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


Summary: Bootstraps rpm-based systems
Name: rpmstrap
Version: 0.5.2
Release: 4
License: GPL
Group: Development/Tools
URL:    https://github.com/blipvert/rpmstrap
Source: https://github.com/blipvert/rpmstrap/archive/rpmstrap-%{version}.tar.bz2
Vendor: Sam Hart <_sam_@-progeny-.'com'>
Packager: Horst Venzke <horst.venzke@remsnet.de>
Requires: phyton => 2.5
Provides: rpmstrap

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

#Buildarch: noarch

%description
rpmstrap is a tool for bootstrapping a basic RPM-based system. It is inspired
by debootstrap, and allows you to build chroots and basic systems from RPM
sources.

%prep
%setup

%build

%install
%{__rm} -rf %{buildroot}
DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}/rpmstrap" ./install.sh
%{__ln_s} -f %{_libdir}/rpmstrap/tools/compstool.py %{buildroot}%{_bindir}/compstool.py
%{__ln_s} -f %{_libdir}/rpmstrap/tools/progress_bar.py %{buildroot}%{_bindir}/progress_bar.py
%{__ln_s} -f %{_libdir}/rpmstrap/tools/rpm_get-arch.py %{buildroot}%{_bindir}/rpm_get-arch.py
%{__ln_s} -f %{_libdir}/rpmstrap/tools/rpm_get-update.py %{buildroot}%{_bindir}/rpm_get-update.py
%{__ln_s} -f %{_libdir}/rpmstrap/tools/rpm_migrate.sh %{buildroot}%{_bindir}/rpm_migrate.sh
%{__ln_s} -f %{_libdir}/rpmstrap/tools/rpm_refiner.py %{buildroot}%{_bindir}/rpm_refiner.py
%{__ln_s} -f %{_libdir}/rpmstrap/tools/rpm_solver.py %{buildroot}%{_bindir}/rpm_solver.py
%{__ln_s} -f %{_libdir}/rpmstrap/tools/rpmdiff.py %{buildroot}%{_bindir}/rpmdiff.py
%{__ln_s} -f %{_libdir}/rpmstrap/tools/rpmdiff_lib.py %{buildroot}%{_bindir}/rpmdiff_lib.py
%{__ln_s} -f %{_libdir}/rpmstrap/tools/suite_upgrader.py %{buildroot}%{_bindir}/suite_upgrader.py

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_bindir}/compstool.py
%{_bindir}/progress_bar.py
%{_bindir}/rpm_get-arch.py
%{_bindir}/rpm_get-update.py
%{_bindir}/rpm_migrate.sh
%{_bindir}/rpm_refiner.py
%{_bindir}/rpm_solver.py
%{_bindir}/rpmdiff.py
%{_bindir}/rpmdiff_lib.py
%{_bindir}/rpmstrap
%{_bindir}/suite_upgrader.py
%{_libdir}/rpmstrap/

%doc CHANGES LICENSE README TODO
%_datadir/doc/%{name}-%{version}/CHANGES
%_datadir/doc/%{name}-%{version}/LICENSE
%_datadir/doc/%{name}-%{version}/README
%_datadir/doc/%{name}-%{version}/README.tools
%_datadir/doc/%{name}-%{version}/TODO
%_datadir/doc/%{name}-%{version}/rpmstrap-api-doc.txt


%changelog
* Fri Mar 14 2014 support@remsnet.de -r3
- rebuild release 0.5.2 on opensuse & centos 6.5
- smal rpmbuild fixes

* Wed Sep 14 2010 Sam Hart <sam@progeny.com>
- Bump to 0.5.2 release on centos 5.3
- moved to  https://github.com/blipvert/rpmstrap

* Wed Sep 14 2005 Sam Hart <sam@progeny.com>
- Bump to 0.5.1 release
* Thu Sep 8 2005 Jacob Boswell <jacob@privateroot.com>
- Initial build.

