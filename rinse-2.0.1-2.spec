# Remsnet Spec file for package rinse
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

# Please submit bugfixes or comments via  https://github.com/remsnet/xen-tools

%define clustername     generic
%define rinserev        2.0.1
%define pversion        2.0.1
%define prelease        2

Summary: Packaged up rinse
Name: rinse
Version: %{pversion}
Release: %{prelease}
License: GPLv2
Group: System Tools
Source0: rinse-%{version}.tar.gz
Packager: Jimmy Tang <jtang@tchpc.tcd.ie>

Vendor: http://xen-tools.org/software/rinse
URL: http://xen-tools.org/software/rinse
Requires: wget
#BuildArch: %{arch}
BuildRoot: %{_tmppath}/%{name}-root

%description
rinse-%{rinserev} - this is a vanilla install

The rinse tool was born out of a frustration with the currently available
solutions for installing minimal copies of RPM-based distributions.

The need to perform simple chroot() installations of other distributions
is not common, but the ability to do such a thing is very useful when
it comes to testing new tools, and working towards the creation of new
Xen guests.

%prep
%setup -c

# do a build just in case if something needs to be compiled
%build
%{__make} -C "%{_builddir}/%{name}-%{version}/%{name}-%{version}"

%install
%{__make} -C "%{_builddir}/%{name}-%{version}/%{name}-%{version}" \
        PREFIX=${RPM_BUILD_ROOT} \
        install

%clean
%{__rm} -rf %{buildroot}


%pre

%post

%preun

%postun


%files
%defattr(-,root,root)
%defattr(0644,root,root,0755)
%{_sysconfdir}/bash_completion.d/rinse
%{_sysconfdir}/rinse/centos-4.packages
%{_sysconfdir}/rinse/centos-5.packages
%{_sysconfdir}/rinse/centos-6.packages
 %{_sysconfdir}/rinse/fedora-core-10.packages
%{_sysconfdir}/rinse/fedora-core-4.packages
%{_sysconfdir}/rinse/fedora-core-5.packages
%{_sysconfdir}/rinse/fedora-core-6.packages
%{_sysconfdir}/rinse/fedora-core-7.packages
%{_sysconfdir}/rinse/fedora-core-8.packages
%{_sysconfdir}/rinse/fedora-core-9.packages
%{_sysconfdir}/rinse/opensuse-10.1.packages
%{_sysconfdir}/rinse/opensuse-10.2.packages
%{_sysconfdir}/rinse/opensuse-10.3.packages
%{_sysconfdir}/rinse/opensuse-11.0.packages
%{_sysconfdir}/rinse/opensuse-11.1.packages
%{_sysconfdir}/rinse/opensuse-12.1.packages
%{_sysconfdir}/rinse/rhel-5.packages
%config(missingok,noreplace) %{_sysconfdir}/rinse/rinse.conf
%{_sysconfdir}/rinse/slc-5.packages
%{_sysconfdir}/rinse/slc-6.packages
%{_libdir}/rinse/centos-4/post-install.sh
%{_libdir}/rinse/centos-5/post-install.sh
%{_libdir}/rinse/centos-6/post-install.sh
%{_libdir}/rinse/common/10-resolv.conf.sh
%{_libdir}/rinse/common/15-mount-proc.sh
%{_libdir}/rinse/common/20-dev-zero.sh
%{_libdir}/rinse/fedora-core-10/post-install.sh
%{_libdir}/rinse/fedora-core-4/post-install.sh
%{_libdir}/rinse/fedora-core-5/post-install.sh
%{_libdir}/rinse/fedora-core-6/post-install.sh
%{_libdir}/rinse/fedora-core-7/post-install.sh
%{_libdir}/rinse/fedora-core-8/post-install.sh
%{_libdir}/rinse/fedora-core-9/post-install.sh
%{_libdir}/rinse/opensuse-10.1/post-install.sh
%{_libdir}/rinse/opensuse-10.2/post-install.sh
%{_libdir}/rinse/opensuse-10.3/post-install.sh
%{_libdir}/rinse/opensuse-11.0/post-install.sh
%{_libdir}/rinse/opensuse-11.1/post-install.sh
%{_libdir}/rinse/opensuse-12.1/post-install.sh
%{_libdir}/rinse/rhel-5/post-install.sh
%{_libdir}/rinse/slc-5/post-install.sh
%{_libdir}/rinse/slc-6/post-install.sh
%{_sbindir}/rinse
%{_mandir}/man8/%{name}*


%changelog
* Fri Mar 14 2014 support@remsnet.de
- rebuild release 2.0.1
