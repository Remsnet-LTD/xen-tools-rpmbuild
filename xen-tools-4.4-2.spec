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
Release:        2
Summary:        Scripts used to create new Xen domains

Group:          Applications/Emulators
License:        GPLv2 or Artistic
URL:            http://xen-tools.org/software/xen-tools/
Source0:        http://xen-tools.org/software/xen-tools/xen-tools-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       perl perl-Text-Template perl-Config-IniFiles perl-Expect
AutoReqProv:    no

%description
xen-tools is a collection of simple perl scripts which allow you to
easily create new guest Xen domains.

%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


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


%doc

%defattr(755,root,root,755)
%{_bindir}/xen-*
%{_bindir}/xt-*



%changelog
* Fri Mar 14 2014 support@remsnet.de -r2
- rebuild release 4.4
