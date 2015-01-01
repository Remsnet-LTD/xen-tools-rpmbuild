#
#
#

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
#
# Build ocaml bits unless rpmbuild was run with --without ocaml
# or ocamlopt is missing (the xen makefile doesn't build ocaml bits if it isn't there)
%define with_ocaml  %{?_without_ocaml: 0} %{?!_without_ocaml: 1}
#
%define build_ocaml %(test -x %{_bindir}/ocamlopt && echo %{with_ocaml} || echo 0)
# build an efi boot image (where supported) unless rpmbuild was run with
# --without efi

%define build_efi %{?_without_efi: 0} %{?!_without_efi: 1}
# build xsm support unless rpmbuild was run with --without xsm
# or required packages are missing
%define with_xsm  %{?_without_xsm: 0} %{?!_without_xsm: 1}
%define build_xsm %(test -x %{_bindir}/checkpolicy && test -x %{_bindir}/m4 && echo %{with_xsm} || echo 0)

## Disable xsm policy
%define with_xsm 0

%define build_xsm 0

# xen only supports efi boot images on x86_64
%ifnarch x86_64
%define build_efi 0
%endif

# Disable efi on EL6 builds
%if 0%{?rhel} == 6
%define build_efi 0
%endif


## Set Xen version...
%define xen_major 4
%define xen_minor 4
%define xen_other 1
%define pkg_release 3.03

# Hypervisor ABI
%define hv_abi %{xen_major}.%{xen_minor}

Summary: Xen is a virtual machine monitor
Name:    xen44
Version: %{xen_major}.%{xen_minor}.%{xen_other}
Release: %{pkg_release}.el%{rhel}
Group:   Development/Libraries
License: GPLv2+ and LGPLv2+ and BSD
URL:     http://xen.org/
Source0: http://bits.xensource.com/oss-xen/release/%{version}/xen-%{version}.tar.gz
Source1: xen.modules
Source2: xen.logrotate
# used by stubdoms
Source10: lwip-1.3.0.tar.gz
Source11: newlib-1.16.0.tar.gz
Source12: zlib-1.2.3.tar.gz
Source13: pciutils-2.2.9.tar.bz2
Source14: grub-0.97.tar.gz
# init.d bits
Source20: init.xendomains
# sysconfig bits
Source30: sysconfig.xenstored
Source31: sysconfig.xenconsoled

Patch4: xen-dumpdir.patch
Patch5: xen-net-disable-iptables-on-bridge.patch

Patch28: pygrubfix.patch
Patch34: xend.catchbt.patch
Patch35: xend-pci-loop.patch

Patch50: xsa104.patch
Patch51: xsa105.patch
Patch52: xsa106.patch
Patch53: xsa107-4.4.patch
Patch54: xsa108.patch

Patch60: increase-logging.patch

BuildRoot: %{_tmppath}/xen-%{version}-%{release}-root
BuildRequires: transfig libidn-devel zlib-devel texi2html SDL-devel curl-devel
BuildRequires: libxml2-devel libxslt-devel
BuildRequires: libX11-devel python-devel ghostscript tetex-latex
BuildRequires: ncurses-devel gtk2-devel libaio-devel
BuildRequires: wget git
# for the docs
BuildRequires: perl texinfo graphviz

# so that the makefile knows to install udev rules
BuildRequires: udev
BuildRequires: libgudev1-devel

# we need some EPEL 7 packakes
# zum EPEL -Repository : http://mirror.de.leaseweb.net/epel/7/
# http://ftp.uma.es/mirror/epel/7/x86_64/e/epel-release-7-1.noarch.rpm
BuildRequires: epel-release

%ifnarch ia64
# so that x86_64 builds pick up glibc32 correctly
BuildRequires: glibc-devel glibc-devel
#
# uuid
BuildRequires: libuuid libuuid-devel
#
#  scsi/iscsi
BuildRequires: libiscsi libiscsi-devel lsscsi
BuildRequires: iscsi-initiator-utils-devel iscsi-initiator-utils
#
# for the VMX "bios"
BuildRequires: dev86
%endif

BuildRequires: gettext
BuildRequires: gnutls-devel
BuildRequires: openssl-devel
# For ioemu PCI passthrough
BuildRequires: pciutils-devel

# Several tools now use uuid
%if 0%{?rhel} == 5
Requires: e4fsprogs
BuildRequires: e4fsprogs e4fsprogs-devel
%endif

%if 0%{?rhel} == 6
Requires: libuuid
BuildRequires: libuuid-devel
%endif

%if 0%{?rhel} == 7
Requires: libuuid
BuildRequires: libuuid-devel
%endif

%ifarch x86_64
Requires: /lib64/libuuid.so.1
%endif

%ifarch i386
Requires: /lib/libuuid.so.1
%endif


# iasl needed to build hvmloader
BuildRequires: iasl
# modern compressed kernels
BuildRequires: bzip2-devel xz-devel
# libfsimage
BuildRequires: e2fsprogs-devel
# tools now require yajl
BuildRequires: yajl-devel

%if %with_xsm
# xsm policy file needs needs checkpolicy and m4
BuildRequires: checkpolicy m4
BuildRequires: epel-release-7-5
%endif

Requires: yajl
Requires: bridge-utils
Requires: python-lxml
Requires: udev >= 059
# Not strictly a dependency, but kpartx is by far the most useful tool right
# now for accessing domU data from within a dom0 so bring it in when the user
# installs xen.
Requires: kpartx
Requires: chkconfig
ExclusiveArch: %{ix86} x86_64 ia64
#ExclusiveArch: %{ix86} x86_64 ia64 noarch

%if %with_ocaml
BuildRequires: ocaml-runtime ocaml-findlib
BuildRequires: ocaml-libvirt-devel ocaml-findlib-devel
%endif

# efi image needs an ld that has -mi386pep option
%if %build_efi
BuildRequires: mingw64-binutils
BuildRequires: mingw64-glib2
%endif

## List the required xen packages here - including version numbers
Requires: xen44-doc = %{version}-%{release}
Requires: xen44-hypervisor = %{version}-%{release}
Requires: xen44-libs = %{version}-%{release}
Requires: xen44-licenses = %{version}-%{release}
Requires: xen44-runtime = %{version}-%{release}
Requires: xen44-qemu = %{version}-%{release}

Conflicts: xen
Obsoletes: xen >= 4.4

%description
This package contains the command line tools needed to manage
virtual machines running under the Xen hypervisor

%package libs
Summary: Libraries for Xen tools
Group: Development/Libraries
Requires(pre): /sbin/ldconfig
Requires(post): /sbin/ldconfig
Requires: xen44 = %{version}-%{release}
Requires: xen44-licenses = %{version}-%{release}
Requires: yajl
Conflicts: xen-libs
Obsoletes: xen-libs >= 4.4

%description libs
This package contains the libraries needed to run applications
which manage Xen virtual machines.


%package runtime
Summary: Core Xen runtime environment
Group: Development/Libraries
Requires: /usr/bin/qemu-img
# Ensure we at least have a suitable kernel installed, though we can't
# force user to actually boot it.
Requires: xen44-hypervisor-abi = %{hv_abi}
Requires: xen44 = %{version}-%{release}
Requires: xen44-libs = %{version}-%{release}
Requires: kpartx python-lxml yajl bridge-utils
Conflicts: xen-runtime
Obsoletes: xen-runtime => 4.4

%description runtime
This package contains the runtime programs and daemons which
form the core Xen userspace environment.


%package hypervisor
Summary: Libraries for Xen tools
Group: Development/Libraries
Requires: xen44 = %{version}-%{release}
Provides: xen44-hypervisor-abi = %{hv_abi}
Requires: libXext yajl mesa-libGL qemu-img SDL
Conflicts: xen-hypervisor
Obsoletes: xen-hypervisor >= 4.4

%description hypervisor
This package contains the Xen hypervisor


%package doc
Summary: Xen documentation
Group: Documentation
#BuildArch: noarch
Requires: xen44 = %{version}-%{release}
Conflicts: xen-doc
Obsoletes: xen-doc => 4.4

%description doc
This package contains the Xen documentation.


%package qemu
Summary: Xen qemu files
Group: Development/Libraries
Requires: xen44 = %{version}-%{release}
Conflicts: xen-qemu
Obsoletes: xen-qemu => 4.4

%description qemu
This package contains the Xen qemu files.


%package devel
Summary: Development libraries for Xen tools
Group: Development/Libraries
Requires: xen44-libs = %{version}-%{release}
Conflicts: xen-devel
Obsoletes: xen-devel => 4.4

%description devel
This package contains what's needed to develop applications
which manage Xen virtual machines.


%package licenses
Summary: License files from Xen source
Group: Documentation
Requires: xen44 = %{version}-%{release}
Conflicts: xen-licenses
Obsoletes: xen-licenses => 4.4

%description licenses
This package contains the license files from the source used
to build the xen packages.


%if %build_ocaml
%package ocaml
Summary: Ocaml libraries for Xen tools
Group: Development/Libraries
Requires: ocaml-runtime, xen44-libs = %{version}-%{release}

%description ocaml
This package contains libraries for ocaml tools to manage Xen
virtual machines.


%package ocaml-devel
Summary: Ocaml development libraries for Xen tools
Group: Development/Libraries
Requires: xen44-ocaml = %{version}-%{release}

%description ocaml-devel
This package contains libraries for developing ocaml tools to
manage Xen virtual machines.
%endif


%prep
%setup -q -n xen-%{version}
%patch4 -p1
%patch5 -p1

%patch28 -p1
%patch34 -p1
%patch35 -p1

%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1

%patch60 -p1

# stubdom sources
cp -v %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} stubdom

#---------------------------------------------------------------------------------------------------
%build

%if !%build_ocaml
%define ocaml_flags OCAML_TOOLS=n
%endif
%if %build_efi
%define efi_flags LD_EFI=/usr/x86_64-w64-mingw32/bin/ld
mkdir -p dist/install/boot/efi/efi/fedora
%endif

#------------------
export XEN_VENDORVERSION="-%{release}"
export XEN_TARGET_ARCH=x86_64
export XEN_PYTHON_NATIVE_INSTALL=1
export CFLAGS="$RPM_OPT_FLAGS"
#
./configure --prefix=%{_prefix} --libdir=%{_libdir}

make  %{?_smp_mflags} %{?efi_flags} prefix=/usr dist-xen

#------------------

make %{?_smp_mflags} %{?ocaml_flags} prefix=/usr dist-tools
make                 prefix=/usr dist-docs
unset CFLAGS
#------------------

make %{?ocaml_flags} dist-stubdom

#---------------------------------------------------------------------------------------------------
%install
rm -rf %{buildroot}
%if %build_ocaml
mkdir -p %{buildroot}%{_libdir}/ocaml/stublibs
%endif
%if %build_efi
mkdir -p %{buildroot}/boot/efi/efi/fedora
%endif

make XEN_PYTHON_NATIVE_INSTALL=1 DESTDIR=%{buildroot} %{?efi_flags}  prefix=/usr install-xen
make XEN_PYTHON_NATIVE_INSTALL=1 DESTDIR=%{buildroot} %{?ocaml_flags} prefix=/usr install-tools
make XEN_PYTHON_NATIVE_INSTALL=1 DESTDIR=%{buildroot} prefix=/usr install-docs
make XEN_PYTHON_NATIVE_INSTALL=1 DESTDIR=%{buildroot} %{?ocaml_flags} prefix=/usr install-stubdom

%if %build_efi
mv %{buildroot}/boot/efi/efi %{buildroot}/boot/efi/EFI
%endif
%if %build_xsm
# policy file should be in /boot/flask
mkdir %{buildroot}/boot/flask
mv %{buildroot}/boot/xenpolicy.* %{buildroot}/boot/flask
%else
rm -f %{buildroot}/boot/xenpolicy.*
%endif

############ debug packaging: list files ############

find %{buildroot} -print | xargs ls -ld | sed -e 's|.*%{buildroot}||' > f1.list

############ kill unwanted stuff ############

# stubdom: newlib
rm -rf %{buildroot}/usr/*-xen-elf

# hypervisor symlinks
rm -rf %{buildroot}/boot/xen-4.0.gz
rm -rf %{buildroot}/boot/xen-4.gz

# silly doc dir fun
rm -rf %{buildroot}%{_datadir}/doc/xen
rm -rf %{buildroot}%{_datadir}/doc/qemu

# Pointless helper
rm -f %{buildroot}%{_sbindir}/xen-python-path

# qemu stuff (unused or available from upstream)
rm -rf %{buildroot}/usr/share/xen/man
rm -rf %{buildroot}/usr/bin/qemu-*-xen
ln -s qemu-img %{buildroot}/%{_bindir}/qemu-img-xen
ln -s qemu-img %{buildroot}/%{_bindir}/qemu-nbd-xen
#for file in bios.bin openbios-sparc32 openbios-sparc64 ppc_rom.bin \
#         pxe-e1000.bin pxe-ne2k_pci.bin pxe-pcnet.bin pxe-rtl8139.bin \
#         vgabios.bin vgabios-cirrus.bin video.x openbios-ppc bamboo.dtb
#do
#       rm -f %{buildroot}/%{_datadir}/xen/qemu/$file
#done

# README's not intended for end users
rm -f %{buildroot}/%{_sysconfdir}/xen/README*

# standard gnu info files
rm -rf %{buildroot}/usr/info

# adhere to Static Library Packaging Guidelines
rm -rf %{buildroot}/%{_libdir}/*.a

##%if %build_efi
### clean up extra efi files
##rm -rf %{buildroot}/%{_libdir}/efi
##%endif

############ fixup files in /etc ############

# udev
#rm -rf %{buildroot}/etc/udev/rules.d/xen*.rules
#mv %{buildroot}/etc/udev/xen*.rules %{buildroot}/etc/udev/rules.d

# modules
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/modules
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/modules/xen.modules

# logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/xen

# init scripts
install -m 755 %{SOURCE20} %{buildroot}%{_sysconfdir}/rc.d/init.d/xendomains

# sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE30} %{buildroot}%{_sysconfdir}/sysconfig/xenstored
install -m 644 %{SOURCE31} %{buildroot}%{_sysconfdir}/sysconfig/xenconsoled

############ create dirs in /var ############
mkdir -p %{buildroot}%{_localstatedir}/lib/xen/xend-db/domain
mkdir -p %{buildroot}%{_localstatedir}/lib/xen/xend-db/vnet
mkdir -p %{buildroot}%{_localstatedir}/lib/xen/xend-db/migrate
mkdir -p %{buildroot}%{_localstatedir}/lib/xen/images
mkdir -p %{buildroot}%{_localstatedir}/log/xen/console

############ create symlink for x86_64 for compatibility with 3.4 ############

%if "%{_libdir}" != "/usr/lib"
ln -s %{_libdir}/xen/bin/libxl-save-helper %{buildroot}/usr/lib/xen/bin/libxl-save-helper
%endif

############ debug packaging: list files ############

find %{buildroot} -print | xargs ls -ld | sed -e 's|.*%{buildroot}||' > f2.list
diff -u f1.list f2.list || true

############ assemble license files ############

mkdir licensedir
# avoid licensedir to avoid recursion, also stubdom/ioemu and dist
# which are copies of files elsewhere
find . -path licensedir -prune -o -path stubdom/ioemu -prune -o \
  -path dist -prune -o -name COPYING -o -name LICENSE | while read file; do
  mkdir -p licensedir/`dirname $file`
  install -m 644 $file licensedir/$file
done

############ all done now ############

%post runtime
/sbin/chkconfig --add xencommons
/sbin/chkconfig --add xendomains
/sbin/chkconfig --add xen-watchdog

%preun runtime
if [ $1 = 0 ]; then
  /sbin/chkconfig --del xencommons
  /sbin/chkconfig --del xendomains
  /sbin/chkconfig --del xen-watchdog
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post hypervisor
if [ $1 = 1 -a -f /sbin/grub2-mkconfig -a -f /boot/grub2/grub.cfg ]; then
  /sbin/grub2-mkconfig -o /boot/grub2/grub.cfg
fi

%postun hypervisor
if [ -f /sbin/grub2-mkconfig -a -f /boot/grub2/grub.cfg ]; then
  /sbin/grub2-mkconfig -o /boot/grub2/grub.cfg
fi

%clean
rm -rf %{buildroot}

# Base package only contains XenD/xm python stuff
#files -f xen-xm.lang
%files
%defattr(-,root,root)
%doc COPYING README
%{_bindir}/xencons
%{python_sitearch}/xen
%if 0%{?rhel} >= 6
%{python_sitearch}/xen-*.egg-info
%endif

# Guest autostart links
%dir %attr(0700,root,root) %{_sysconfdir}/xen/auto
# Autostart of guests
%config(noreplace) %{_sysconfdir}/sysconfig/xendomains

# Persistent state for XenD
%dir %{_localstatedir}/lib/xen/xend-db/
%dir %{_localstatedir}/lib/xen/xend-db/domain
%dir %{_localstatedir}/lib/xen/xend-db/migrate
%dir %{_localstatedir}/lib/xen/xend-db/vnet

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/fs

# All runtime stuff except for XenD/xm python stuff
%files runtime
%defattr(-,root,root)
# Hotplug rules
%config(noreplace) %{_sysconfdir}/udev/rules.d/*

%dir %attr(0700,root,root) %{_sysconfdir}/xen
%dir %attr(0700,root,root) %{_sysconfdir}/xen/scripts/
%config %attr(0700,root,root) %{_sysconfdir}/xen/scripts/*

%{_sysconfdir}/rc.d/init.d/xen-watchdog
%{_sysconfdir}/rc.d/init.d/xencommons
%{_sysconfdir}/rc.d/init.d/xendomains
%{_sysconfdir}/bash_completion.d/xl.sh

%config(noreplace) %{_sysconfdir}/sysconfig/xenstored
%config(noreplace) %{_sysconfdir}/sysconfig/xenconsoled
%config(noreplace) %{_sysconfdir}/sysconfig/xencommons
%config(noreplace) %{_sysconfdir}/xen/xl.conf
%config(noreplace) %{_sysconfdir}/xen/cpupool
%config(noreplace) %{_sysconfdir}/xen/xlexample*

# Auto-load xen backend drivers
%attr(0755,root,root) %{_sysconfdir}/sysconfig/modules/xen.modules

# Rotate console log files
%config(noreplace) %{_sysconfdir}/logrotate.d/xen

# Programs run by other programs
%dir %{_libdir}/xen
%dir %{_libdir}/xen/bin
%attr(0700,root,root) %{_libdir}/xen/bin/*
# QEMU runtime files
%dir %{_datadir}/xen/qemu
%dir %{_datadir}/xen/qemu/keymaps
%{_datadir}/xen/qemu/keymaps/*

# man pages
%{_mandir}/man1/xentop.1*
%{_mandir}/man1/xentrace_format.1*
%{_mandir}/man8/xentrace.8*
%{_mandir}/man1/xl.1*
%{_mandir}/man5/xl.cfg.5*
%{_mandir}/man5/xl.conf.5*
%{_mandir}/man5/xlcpupool.cfg.5*

%{python_sitearch}/fsimage.so
%{python_sitearch}/grub
%if 0%{?rhel} >= 6
%{python_sitearch}/pygrub-*.egg-info
%endif

# The firmware
%ifnarch ia64
# Avoid owning /usr/lib twice on i386
%if "%{_libdir}" != "/usr/lib"
%dir /usr/lib/xen
%dir /usr/lib/xen/bin
/usr/lib/xen/bin/stubdom-dm
/usr/lib/xen/bin/qemu-dm
/usr/lib/xen/bin/libxl-save-helper
/usr/lib/xen/bin/stubdompath.sh
/usr/lib/xen/bin/xenpaging
%endif
%dir /usr/lib/xen/boot
# HVM loader is always in /usr/lib regardless of multilib
/usr/lib/xen/boot/hvmloader
/usr/lib/xen/boot/ioemu-stubdom.gz
/usr/lib/xen/boot/xenstore-stubdom.gz
/usr/lib/xen/boot/pv-grub*.gz
%endif
# General Xen state
%dir %{_localstatedir}/lib/xen
%dir %{_localstatedir}/lib/xen/dump
%dir %{_localstatedir}/lib/xen/images
# Xenstore persistent state
%dir %{_localstatedir}/lib/xenstored
# Xenstore runtime state
%ghost %{_localstatedir}/run/xenstored

# All xenstore CLI tools
%{_bindir}/qemu-*-xen
%{_bindir}/xenstore
%{_bindir}/xenstore-*
%{_bindir}/pygrub
%{_bindir}/xentrace*
%{_bindir}/remus
%{_sbindir}/tapdisk*
%if %build_xsm
# XSM
%{_sbindir}/flask-*
%{_sbindir}/xsview
%endif
# Disk utils
%{_sbindir}/qcow-create
%{_sbindir}/qcow2raw
%{_sbindir}/img2qcow
# Misc stuff
%{_bindir}/xen-detect
%{_bindir}/xencov_split
%{_sbindir}/gdbsx
%{_sbindir}/gtrace*
%{_sbindir}/kdd
%{_sbindir}/lock-util
%{_sbindir}/tap-ctl
%{_sbindir}/td-util
%{_sbindir}/vhd-*
%{_sbindir}/xen-bugtool
%{_sbindir}/xen-hptool
%{_sbindir}/xen-hvmcrash
%{_sbindir}/xen-hvmctx
%{_sbindir}/xen-mfndump
%{_sbindir}/xen-tmem-list-parse
%{_sbindir}/xenconsoled
%{_sbindir}/xenlockprof
%{_sbindir}/xenmon.py*
%{_sbindir}/xentop
%{_sbindir}/xentrace_setmask
%{_sbindir}/xenbaked
%{_sbindir}/xenstored
%{_sbindir}/xenpm
%{_sbindir}/xenpmd
%{_sbindir}/xenperf
%{_sbindir}/xenwatchdogd
%{_sbindir}/xl
%{_sbindir}/xencov
%{_sbindir}/xen-lowmemd
%{_sbindir}/xen-ringwatch

# Xen logfiles
%dir %attr(0700,root,root) %{_localstatedir}/log/xen
# Guest/HV console logs
%dir %attr(0700,root,root) %{_localstatedir}/log/xen/console

%files hypervisor
%defattr(-,root,root)
/boot/xen-syms-*
/boot/xen-*.gz
/boot/xen.gz

##%if %build_efi
##/boot/efi/EFI/fedora/*.efi
##%endif

%if %build_xsm
%dir %attr(0755,root,root) /boot/flask
/boot/flask/xenpolicy.*
%endif

%files doc
%defattr(-,root,root)
%doc docs/misc/
%doc dist/install/usr/share/doc/xen/html
%{_mandir}/man1/xenstore-chmod.1.gz
%{_mandir}/man1/xenstore-ls.1.gz
%{_mandir}/man1/xenstore.1.gz
%{_mandir}/man1/xm.1.gz
%{_mandir}/man5/xend-config.sxp.5.gz
%{_mandir}/man5/xmdomain.cfg.5.gz

%files qemu
%defattr(-,root,root)
/usr/etc/qemu/target-x86_64.conf
/usr/lib/xen/bin/qemu-img
/usr/lib/xen/bin/qemu-io
/usr/lib/xen/bin/qemu-nbd
/usr/lib/xen/bin/qemu-system-i386
/usr/libexec/qemu-bridge-helper
/usr/share/qemu-xen/qemu/*
/usr/share/xen/qemu/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%dir %{_includedir}/xen
%{_includedir}/xen/*
%dir %{_includedir}/xenstore-compat
%{_includedir}/xenstore-compat/*
%{_libdir}/*.so

%files licenses
%defattr(-,root,root)
%doc licensedir/*

%if %build_ocaml
%files ocaml
%defattr(-,root,root)
%{_libdir}/ocaml/xen*
%exclude %{_libdir}/ocaml/xen*/*.a
%exclude %{_libdir}/ocaml/xen*/*.cmxa
%exclude %{_libdir}/ocaml/xen*/*.cmx
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner
%{_sbindir}/oxenstored
%config(noreplace) %{_sysconfdir}/xen/oxenstored.conf

%files ocaml-devel
%defattr(-,root,root)
%{_libdir}/ocaml/xen*/*.a
%{_libdir}/ocaml/xen*/*.cmxa
%{_libdir}/ocaml/xen*/*.cmx
%endif

%changelog
* Thu Oct 23 2014 Steven Haigh <netwiz@crc.id.au> - 4.4.1-3.1
- Increase logging on DomU creation to debug pv-grub issues
        See: http://lists.xen.org/archives/html/xen-devel/2014-10/msg02546.html

* Tue Oct 07 2014 Steven Haigh <netwiz@crc.id.au> - 4.4.1-3
- Fix scriptlets on package install/uninstall for initscripts - bug #32
- Fix error message printed on empty /etc/xen/auto/ path - bug #31

* Wed Oct 01 2014 Steven Haigh <netwiz@crc.id.au> - 4.4.1-2
- XSA-104 (CVE-2014-7154) Race condition in HVMOP_track_dirty_vram
- XSA-105 (CVE-2014-7155) Missing privilege level checks in x86 HLT, LGDT, LIDT, and LMSW emulation
- XSA-106 (CVE-2014-7156) Missing privilege level checks in x86 emulation of software interrupts
- XSA-107 (CVE-2014-6268) Mishandling of uninitialised FIFO-based event channel control blocks
- XSA-108 (CVE-2014-7188) Improper MSR range used for x2APIC emulation

* Wed Sep 03 2014 Steven Haigh <netwiz@crc.id.au> - 4.4.1-1
- Update to upstream xen 4.4.1

* Wed Aug 06 2014 Steven Haigh <netwiz@crc.id.au> - 4.4.0-0.4
- Attempt to use qemu from upstream vs EL6

* Sat Jul 19 2014 Steven Haigh <netwiz@crc.id.au> - 4.4.0-0.3
- XSA-100 (CVE-2014-4021) Hypervisor heap contents leaked to guests

* Fri Jun 06 2014 Steven Haigh <netwiz@crc.id.au> - 4.4.0-0.2
- Rebase for Xen 4.4.0 release
- XSA-89 (CVE-2014-2599) x86: enforce preemption in HVM_set_mem_access / p2m_set_mem_access()
- XSA-92 (CVE-2014-3124) x86/HVM: restrict HVMOP_set_mem_type
- XSA-96 (CVE-2014-3967,CVE-2014-3968) x86/HVM: eliminate vulnerabilities from hvm_inject_msi()
