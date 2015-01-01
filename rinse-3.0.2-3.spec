# Remsnet Spec file for package rinse
#
# Copyright (c) 1995-2008 Remsnet Netzwerk Service OhG , D-73630 Remshalden
# Copyright (c) 2008-2015 Remsnet Consullting & Internet Services LTD , D-40476 Duesseldorf

# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via  https://github.com/remsnet/xen-tools-rpmbuild

%define clustername     generic
%define name            rinse
%define pkg_version     3.0.2
%define pkg_release     03

Summary: Packaged up rinse
Name: %{name}
Version: %{pkg_version}
Release:%{pkg_release}.el%{rhel}
License: GPLv2
Group: System Tools
Source0: %{name}-%{version}.tar.gz
Packager:       Horst Venzke <horst.venzke@remsnet.de>

Vendor: http://xen-tools.org/software/rinse/
URL: http://collab-maint.alioth.debian.org/rinse/%{name}-%{version}.tar.gz
Requires: wget
#
#perl/cpan depend stuff  to install perl LWP::UserAgent ( not exist in EPEL7 )
Requires: perl-CPAN
Requires: perl-libwww-perl
Requires: perl-Time-HiRes perl-local-lib perl-homedir perl-Encode-Locale
#
BuildRoot: %{_tmppath}/%{name}-%{pkg_version}-%{pkg_release}.el%{rhel}-root

%description
rinse-%{pkg_version} - this is a vanilla install

The rinse tool was born out of a frustration with the currently available
solutions for installing minimal copies of RPM-based distributions.

The need to perform simple chroot() installations of other distributions
is not common, but the ability to do such a thing is very useful when
it comes to testing new tools, and working towards the creation of new
Xen guests.

%prep

%setup -c %{name}


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
bash  echo y;echo o conf prerequisites_policy follow;echo o conf commit|cpan


%post

%preun

%postun


%files
%defattr(-,root,root)
%defattr(0644,root,root,0755)
%{_sysconfdir}/bash_completion.d/rinse
#
%{_sysconfdir}/rinse/centos-7.packages
%{_sysconfdir}/rinse/fedora-10.packages
%{_sysconfdir}/rinse/fedora-12.packages
%{_sysconfdir}/rinse/fedora-13.packages
%{_sysconfdir}/rinse/fedora-14.packages
%{_sysconfdir}/rinse/fedora-15.packages
%{_sysconfdir}/rinse/fedora-16.packages
%{_sysconfdir}/rinse/fedora-17.packages
%{_sysconfdir}/rinse/fedora-18.packages
%{_sysconfdir}/rinse/fedora-19.packages
%{_sysconfdir}/rinse/fedora-7.packages
%{_sysconfdir}/rinse/fedora-8.packages
%{_sysconfdir}/rinse/fedora-9.packages
%{_sysconfdir}/rinse/opensuse-10.1.packages
%{_sysconfdir}/rinse/opensuse-10.2.packages
%{_sysconfdir}/rinse/opensuse-10.3.packages
%{_sysconfdir}/rinse/opensuse-11.0.packages
%{_sysconfdir}/rinse/opensuse-11.1.packages
%{_sysconfdir}/rinse/opensuse-11.2.packages
%{_sysconfdir}/rinse/opensuse-11.3.packages
%{_sysconfdir}/rinse/opensuse-12.1.packages
%{_sysconfdir}/rinse/opensuse-12.3.packages
%{_sysconfdir}/rinse/opensuse-13.1.packages
%{_sysconfdir}/rinse/centos-4.packages
%{_sysconfdir}/rinse/centos-5.packages
%{_sysconfdir}/rinse/centos-6.packages
%{_sysconfdir}/rinse/fedora-core-4.packages
%{_sysconfdir}/rinse/fedora-core-5.packages
%{_sysconfdir}/rinse/fedora-core-6.packages
%{_sysconfdir}/rinse/rhel-5.packages
%config(missingok,noreplace) %{_sysconfdir}/rinse/rinse.conf
%{_sysconfdir}/rinse/slc-5.packages
%{_sysconfdir}/rinse/slc-6.packages
%{_mandir}/man8/%{name}*

%defattr(755,root,root,0755)
/usr/lib/rinse/centos-4/post-install.sh
/usr/lib/rinse/centos-5/post-install.sh
/usr/lib/rinse/centos-6/post-install.sh
/usr/lib/rinse/centos-7/post-install.sh
/usr/lib/rinse/common/10-resolv.conf.sh
/usr/lib/rinse/common/15-mount-proc.sh
/usr/lib/rinse/common/20-dev-zero.sh
/usr/lib/rinse/fedora-10/post-install.sh
/usr/lib/rinse/fedora-12/post-install.sh
/usr/lib/rinse/fedora-13/post-install.sh
/usr/lib/rinse/fedora-14/post-install.sh
/usr/lib/rinse/fedora-15/post-install.sh
/usr/lib/rinse/fedora-16/post-install.sh
/usr/lib/rinse/fedora-18/post-install.sh
/usr/lib/rinse/fedora-19/post-install.sh
/usr/lib/rinse/fedora-7/post-install.sh
/usr/lib/rinse/fedora-8/post-install.sh
/usr/lib/rinse/fedora-9/post-install.sh
/usr/lib/rinse/fedora-core-4/post-install.sh
/usr/lib/rinse/fedora-core-5/post-install.sh
/usr/lib/rinse/fedora-core-6/post-install.sh
/usr/lib/rinse/opensuse-10.1/post-install.sh
/usr/lib/rinse/opensuse-10.2/post-install.sh
/usr/lib/rinse/opensuse-10.3/post-install.sh
/usr/lib/rinse/opensuse-11.0/post-install.sh
/usr/lib/rinse/opensuse-11.1/post-install.sh
/usr/lib/rinse/opensuse-11.2/post-install.sh
/usr/lib/rinse/opensuse-11.3/post-install.sh
/usr/lib/rinse/opensuse-12.1/post-install.sh
/usr/lib/rinse/opensuse-12.3/post-install.sh
/usr/lib/rinse/opensuse-13.1/post-install.sh
/usr/lib/rinse/rhel-5/post-install.sh
/usr/lib/rinse/slc-5/post-install.sh
/usr/lib/rinse/slc-6/post-install.sh

%{_sbindir}/rinse


%changelog
* Thu Jan 1 2015 - Remsnet LTD support <support@remsnet.de> -r 3.0.2-02
- update to rinse 3.0.2
- updated rise project download ( now at debian )
- added cpan & perl depend install stuff
- added cpan autoconfig at %pre to be able install missing stuff
* Fri Mar 14 2014 support@remsnet.de - r 2.02-02
- rebuild release 2.0.1
