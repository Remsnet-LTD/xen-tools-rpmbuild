# Remsnet Spec file for package xen-shell
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

Name:           xen-shell
Version:        1.9
Release:        2
Summary:        Scripts used to create new Xen domains

Group:          Applications/Emulators
License:        GPLv2 or Artistic
URL:            http://xen-tools.org/software/xen-tools/
Source0:        http://xen-tools.org/software/xen-tools/xen-shell-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
Patch:          %{name}.Makefile.patch

BuildArch:      noarch
Requires:       perl
Requires:       perl(File::Basename)
Requires:       perl(File::Find)
Requires:       perl(File::Path)
Requires:       xen
AutoReqProv:    no

%description
xen-tools is a collection of simple perl scripts which allow you to
easily create new guest Xen domains.
source : https://github.com/craigw/xen-shell

%prep
%setup -q
%patch -p0 -F 10


%build
test "%{buildroot}" != "/" && %__rm -rf "%{buildroot}"

mkdir -p  "%{buildroot}"
make clean
make makemanpages


%install

mkdir -p -m 755 %{buildroot}/%{_mandir}/man1
install -m 644  man/xen-shell.man %{buildroot}/%{_mandir}/man1/%{name}.1
install -m 644  man/xen-add-user.man %{buildroot}/%{_mandir}/man1/xen-add-user.1
install -m 644  man/xen-login-shell.man %{buildroot}/%{_mandir}/man1/xen-login-shell.1
install -m 644  man/xm-reimage.man %{buildroot}/%{_mandir}/man1/xm-reimage.1
gzip -f -9 %{buildroot}/%{_mandir}/man1/%{name}.1
gzip -f -9 %{buildroot}/%{_mandir}/man1/xen-add-user.1
gzip -f -9 %{buildroot}/%{_mandir}/man1/xen-login-shell.1
gzip -f -9 %{buildroot}/%{_mandir}/man1/xm-reimage.1


mkdir -p -m 755 %{buildroot}/%{_bindir}
install -m 755 bin/xm-reimage %{buildroot}/%{_bindir}/xm-reimage
install -m 755 bin/xen-login-shell  %{buildroot}/%{_bindir}/xen-login-shell
install -m 755 bin/xen-shell        %{buildroot}/%{_bindir}/xen-shell


mkdir -p -m 755 %{buildroot}/%{_sysconfdir}/%{name}
install -m 644 misc/xen-shell.conf %{buildroot}/%{_sysconfdir}/%{name}/xen-shell.conf
install -m 644 misc/_screenrc %{buildroot}/%{_sysconfdir}/%{name}/screenrc


mkdir -p -m 755 %{buildroot}/%{_sysconfdir}/bash_completion.d
install -m 644 misc/xen-shell %{buildroot}/%{_sysconfdir}/bash_completion.d/xen-shell

%pre
if [ ! -d /etc/xen-shell ]; then mkdir /etc/xen-shell ; fi
if [ ! -d /etc/bash_completion.d ]; then mkdir /etc/bash_completion.d/ ; fi


%clean
test "%{buildroot}" != "/" && %__rm -rf "%{buildroot}"


%files
%defattr(755,root,root,755)
%_bindir/xm-reimage
%_bindir/xen-login-shell
%_bindir/xen-shell


%defattr(644,root,root,755)
%doc README BUGS

%dir %_sysconfdir/%{name}
%{_sysconfdir}/%{name}/xen-shell.conf
%{_sysconfdir}/%{name}/screenrc
%{_sysconfdir}/bash_completion.d/xen-shell
%_mandir/man1/*

%changelog
* Fri Mar 14 2014 support@remsnet.de -r2
- rebuild release 1.9

