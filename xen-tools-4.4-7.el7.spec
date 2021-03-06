# Remsnet Spec file for package xen-tools
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

Name:           xen-tools
Version:        4.4
Release:        7.el%{rhel}
Summary:        Scripts used to create new Xen domains
Packager:       Horst Venzke <horst.venzke@remsnet.de>
Group:          Applications/Emulators
License:        GPLv2 or Artistic
URL:            https://github.com/remsnet/xen-tools
Source0:        http://xen-tools.org/software/xen-tools/xen-tools-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       xen44 => 4.4
Requires:       rpmstrap
Requires:       rinse > 3.0.0
Requires:       python >= 2.7.0
Requires:       bash
Requires:       coreutils

#perl/cpan depend stuff  to install perl LWP::UserAgent ( not exist in EPEL7 )
Requires:       perl >= 5.8.0
Requires:       perl-CPAN
Requires:       perl-libwww-perl
Requires:       perl-Time-HiRes perl-local-lib perl-homedir perl-Encode-Locale
Requires:       perl-Text-Template
Requires:       perl-Config-IniFiles
Requires:       perl-Expect
Requires:       perl-Env
Requires:       perl-File-Which
Requires:       perl-File-Slurp
Requires:       perl-Term-UI
Requires:       perl-IPC-Cmd
Requires:       perl-Pod-Usage
Requires:       perl-Getopt-Long
Requires:       perl(LWP::UserAgent)
Requires:       perl(File::Basename)
Requires:       perl(File::Find)
Requires:       perl(File::Path)
##Requires:       perl(Expect::Simple)
##Requires:       perl(Data::Validate:URI)
#
#--hash_method
Requires:       perl(Digest::SHA)
Requires:       perl(Digest::MD5)
#
AutoReqProv:    no
Provides:       xen-tools

%description
xen-tools is a collection of simple perl scripts which allow you to
easily create new guest Xen domains.

Once installed and configured you can create a new Xen instance in a matter of minutes. Each new Xen domain will be complete with:

    All networking details setup, with either multiple static IP addresses or DHCP.
    An installation of OpenSSH.
    An arbitary set of partitions.

Your new instance will be completed by having the user accounts from your guest system copied over, and you may optionally boot the image as soon as it has been created.

Installation Methods:

Mutiple installation methods are supported to increase your choices. You can choose to:

    Install via debootstrap
    Install via rinse
    Copy a previously created image.
    Untar an archive of a pristine image

Frequently asked questions and frequently anticipated questions see http://xen-tools.org/software/xen-tools/faq.html

Example Usage see http://xen-tools.org/software/xen-tools/examples.html


%prep
%setup -q


%build
test "%{buildroot}" != "/" && %__rm -rf "%{buildroot}"

%install
make install prefix=$RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/*
%{_sysconfdir}/bash_completion.d/*
%{_sysconfdir}/initramfs-tools/conf.d/%{name}

%{_mandir}/man8/xen-*
%{_mandir}/man8/xt-*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*


%defattr(755,root,root,755)
%{_datadir}/perl5/Xen/Tools/Common.pm


%defattr(755,root,root,755)
%{_bindir}/xen-*
%{_bindir}/xt-*

%defattr(644,root,root,755)
%doc AUTHORS ChangeLog *.markdown LICENSE ChangeLog misc/README
%doc examples misc partitions

%pre

test -f /etc/modprobe.d/loop.local || echo 'options loop max_loop=255' > /etc/modprobe.d/loop.local

%post

for i in $(seq 8 255) ;  do mknod /dev/loop$i b 7 $i ;done
chmod 664 /dev/loop*
chown 0.disk /dev/loop*

%clean
test "%{buildroot}" != "/" && %__rm -rf "%{buildroot}"



%changelog
* Thu Jan 1 2015 - Remsnet LTD support <support@remsnet.de> -r 3.0.2-02
- centos7 build
* Sat Jul  5 2014 support@remsnet.de -r6
- add perl Digest-SHA, Digest-MD5

* Tue May 27 2014 support@remsnet.de -r5
- added centos 6.5 support, completed rewrite the centos6.0 hooks
- forked xen-tools https://github.com/remsnet/xen-tools ,
- xen-tool patches provited by private email to xen-tools to current maintainer Axel beckert.

* Mon Apr 28 2014 support@remsnet.de -r4
- updated Requires perl modules
- added Requires xen, bash,
- coreutils - mknod required
- added %pre with generate /etc/modprobe.d/loop.local
- added %post with generate 255 loop dev nodes
- added %clean
- replaced buildroot cleanup with test "%{buildroot}" != "/" && %__rm -rf "%{buildroot}"
- updated %doc

* Fri Mar 14 2014 support@remsnet.de -r2
- rebuild release 4.4
