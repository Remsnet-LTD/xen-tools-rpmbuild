%define kvmajor 3.14
%define kvminor 27
%define pkg_release 03
%define KRELEASE %{kvmajor}.%{kvminor}-%{release}.%{_target_cpu}

Name: kernel-xen
Version: %{kvmajor}.%{kvminor}
Release: %{pkg_release}.el%{rhel}xen
License: GPL
Group: System Environment/Kernel
URL: http://www.kernel.org
Packager: Horst venzke <horst.venzke@remsnet.de>
Summary: The Linux Kernel
Vendor: The Linux Community
Provides: kernel-xen = %{version}-%{release}
Provides: kernel = %{version}-%{release}
Requires: kernel-xen-firmware
BuildRequires: git bc
BuildRoot: %_topdir/BUILDROOT
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

Source0: linux-%{kvmajor}.%{kvminor}.tar.xz
Source1: config-%{kvmajor}.x86_64

#Patch0: xsa-90.patch

%description
The Linux Kernel, the operating system core itself

%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: glibc-kernheaders
Provides: glibc-kernheaders = 3.0-46
Provides: kernel-headers = %{version}-%{release}
Provides: kernel-xen-headers = %{version}-%{release}
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package firmware
Summary: Firmware files used by the Linux kernel
Group: Development/System
Provides: kernel-xen-firmware = %{version}-%{release}
Provides: kernel-firmware = %{version}-%{release}
Obsoletes: aic94xx-firmware atmel-firmware bfa-firmware ipw2100-firmware ipw2200-firmware
Obsoletes: ivtv-firmware iwl100-firmware iwl1000-firmware iwl3945-firmware iwl4965-firmware
Obsoletes: iwl5000-firmware iwl5150-firmware iwl6000-firmware iwl6000g2a-firmware iwl6000g2b-firmware
Obsoletes: iwl6050-firmware kernel-firmware libertas-usb8388-firmware netxen-firmware ql2100-firmware
Obsoletes: ql2200-firmware ql23xx-firmware ql2400-firmware ql2500-firmware rt61pci-firmware rt73usb-firmware
Obsoletes: zd1211-firmware
%description firmware
Kernel-firmware includes firmware files required for some devices to
operate.

%package devel
Summary: Development package for building kernel modules to match the kernel
Group: System Environment/Kernel
Provides: kernel-xen-devel = %{version}-%{release}
Provides: kernel-devel = %{version}-%{release}
%description devel
This package provides kernel headers and makefiles sufficient to build modules
against the kernel package.

%prep
%setup -q -n linux-%{kvmajor}.%{kvminor}

#%patch0 -p1

make mrproper
cat $RPM_SOURCE_DIR/config-%{kvmajor}.%{_target_cpu} >> .config

%build
perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}.%{_target_cpu}/" Makefile

make oldconfig
make %{?_smp_mflags} bzImage
make %{?_smp_mflags} modules

%install
rm -rf $RPM_BUILD_ROOT

## Create directory structure.
mkdir -p $RPM_BUILD_ROOT/boot
touch $RPM_BUILD_ROOT/boot/initramfs-%{KRELEASE}.img
mkdir -p $RPM_BUILD_ROOT/lib/modules
mkdir -p $RPM_BUILD_ROOT/lib/firmware
mkdir -p $RPM_BUILD_ROOT/usr

# Copy across all our modules.
make INSTALL_MOD_PATH=$RPM_BUILD_ROOT KBUILD_SRC= modules_install

# Create the firmware files for the kernel-xen-firmware package
make INSTALL_FW_PATH=$RPM_BUILD_ROOT/lib/firmware firmware_install

## Pull down all the firmware for kernel-xen-firmware package
echo "Cloning linux-firmware Git repo for kernel-xen-firmware package..."
## We can't use --depth=1 now because git.kernel.org dies when doing a shallow clone somewhere
## between 11th Jul and 27th July. Now we waste their bandwidth.
git clone --depth=1 git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
#git clone git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git

## Things are starting to get ugly trying to sync this git, plus firmware in the
## linux-firmware package, plus firmware in the kernel tarball itself.
## As such, we now obsolete kernel-firmware from EL6 and replace the lot.
## We don't overwrite firmware in the kernel tarball however...
cp -Rn linux-firmware/* $RPM_BUILD_ROOT/lib/firmware/

## Remove conflicts with microcode packages...
rm -fR $RPM_BUILD_ROOT/lib/firmware/amd-ucode/*

# Install kernel headers
make ARCH=x86 INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

# Do headers_check but don't die if it fails.
make ARCH=x86 INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_check \
     > hdrwarnings.txt || :
if grep -q exist hdrwarnings.txt; then
   sed s:^$RPM_BUILD_ROOT/usr/include/:: hdrwarnings.txt
   # Temporarily cause a build failure if header inconsistencies.
   # exit 1
fi

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) | xargs rm -f

# glibc provides scsi headers for itself, for now
rm -rf $RPM_BUILD_ROOT/usr/include/scsi
rm -f $RPM_BUILD_ROOT/usr/include/asm*/atomic.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/io.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/irq.h

# Manipulate the files how we want them.
cp arch/x86/boot/bzImage $RPM_BUILD_ROOT/boot/vmlinuz-%{KRELEASE}
cp System.map $RPM_BUILD_ROOT/boot/System.map-%{KRELEASE}
cp .config $RPM_BUILD_ROOT/boot/config-%{KRELEASE}
gzip -c9 < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-%{KRELEASE}.gz

# mark modules as executable so rpmbuild will strip their debugging symbols
find $RPM_BUILD_ROOT/lib/modules/%{KRELEASE} -name "*.ko" -type f | xargs chmod u+x

# remove files that will be auto generated by depmod at rpm -i time
rm -f $RPM_BUILD_ROOT/lib/modules/%{KRELEASE}/modules.*
rm -f $RPM_BUILD_ROOT/lib/modules/%{KRELEASE}/build
rm -f $RPM_BUILD_ROOT/lib/modules/%{KRELEASE}/source

## Gather up all the files we need for our devel package...
mkdir -p $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/
cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/
cp Module.symvers $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/
cp System.map $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/

# then drop all but the needed Makefiles/Kconfig files
rm -rf $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/Documentation
rm -rf $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/scripts
rm -rf $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/include

## Recopy stuff we probably do need.
cp .config $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/
cp -a scripts $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/
if [ -d arch/x86/scripts ]; then
        cp -a arch/x86/scripts $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/arch/x86 || :
fi
if [ -f arch/x86/*lds ]; then
        cp -a arch/x86/*lds $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/arch/x86/ || :
fi
rm -f $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/scripts/*.o
rm -f $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/scripts/*/*.o
if [ -d arch/x86/include ]; then
        cp -a --parents arch/x86/include $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/
fi
mkdir -p $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/include
cd include
cp -a acpi asm-generic clocksource config crypto drm generated keys linux math-emu media memory misc net pcmcia ras rdma rxrpc scsi sound target trace uapi video xen $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/include

# Make sure the Makefile and version.h have a matching timestamp so that
# external modules can be built
touch -r $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/Makefile $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/include/linux/version.h
touch -r $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/.config $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/include/linux/autoconf.h
# Copy .config to include/config/auto.conf so "make prepare" is unnecessary.
cp $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/.config $RPM_BUILD_ROOT/usr/src/kernels/%{KRELEASE}/include/config/auto.conf

# Create links to kernel source....
ln -s /usr/src/kernels/%{KRELEASE} $RPM_BUILD_ROOT/lib/modules/%{KRELEASE}/build
ln -s /usr/src/kernels/%{KRELEASE} $RPM_BUILD_ROOT/lib/modules/%{KRELEASE}/source

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Add kernel-xen to the list of packages that allow multiple installs
# so we don't nuke working kernels on an upgrade. That would be bad.
if ! grep -q installonlypkgs /etc/yum.conf; then
        sed -i --follow-symlinks 's/\[main]/[main]\ninstallonlypkgs=kernel kernel-xen kernel-smp kernel-bigmem kernel-enterprise kernel-debug/g' /etc/yum.conf
        echo "Added kernel-xen to 'installonlypkgs' line in /etc/yum.conf!"
fi

if [ -x /sbin/new-kernel-pkg ]
then
%if 0%{?rhel} == 5
        /sbin/new-kernel-pkg --package kernel --mkinitrd --depmod --install %{KRELEASE} || exit $?
%endif
%if 0%{?rhel} == 6
        /sbin/new-kernel-pkg --package kernel --mkinitrd --dracut --depmod --make-default --install %{KRELEASE} || exit $?
%endif
%if 0%{?rhel} == 7
        /sbin/new-kernel-pkg --package kernel --mkinitrd --dracut --depmod --make-default --install %{KRELEASE} || exit $?
%endif

        ## Check that xen.gz exits, if so, add hypervisor lines, if not, assume we're a DomU or bare metal install.
        if [ -h "/boot/xen.gz" ]; then
                GRUB_CONF=$(readlink -n -e /etc/grub.conf 2>/dev/null)
                if [ -z $GRUB_CONF ]; then
                        if [ -f "/boot/grub/grub.conf" ]; then
                                GRUB_CONF="/boot/grub/grub.conf"
                        else
                                echo "No valid grub.conf found. You'll need to fix this manually!"
                        fi
                else
                        HYPERVISOR=`grep -m1 xen.gz $GRUB_CONF`
                        if [[ -z $HYPERVISOR ]]; then
                                ## We haven't found an existing hypervisor. Find where xen.gz is and add the defaults.
                                echo "No existing Xen install found. Using defaults."

                                ## Look for /boot partition, otherwise assume relative to /
                                if `grep -q "/boot" /proc/mounts`; then
                                        XEN_GZ="/xen.gz"
                                else
                                        XEN_GZ="/boot/xen.gz"
                                fi
                                HYPERVISOR="    kernel $XEN_GZ dom0_mem=1024M cpufreq=xen dom0_max_vcpus=1 dom0_vcpus_pin"
                        fi
                        KERNEL=`grep -m1 vmlinuz-%{KRELEASE} $GRUB_CONF`
                        INITRAMFS=`grep -m1 initramfs-%{KRELEASE} $GRUB_CONF`
                        if [[ -z "$KERNEL" || -z "$INITRAMFS" ]]; then
                                echo "ERROR: Something unexpected was found in /etc/grub.conf. Please edit manually."
                        else
                                KERNEL_NEW=$( echo "$KERNEL" | sed 's|kernel|module|' )
                                INITRAMFS_NEW=$( echo "$INITRAMFS" | sed 's|initrd|module|' )
                                sed -i --follow-symlinks "s|$KERNEL|$HYPERVISOR\n$KERNEL_NEW|" $GRUB_CONF
                                sed -i --follow-symlinks "s|$INITRAMFS|$INITRAMFS_NEW|" $GRUB_CONF
                        fi
                fi
        fi
fi

if [ -x /sbin/weak-modules ]
then
        /sbin/weak-modules --add-kernel %{KRELEASE} || exit $?
fi

%preun
if [ -x /sbin/new-kernel-pkg ]
then
        /sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{KRELEASE} || exit $?
fi
if [ -x /sbin/weak-modules ]
then
        /sbin/weak-modules --remove-kernel %{KRELEASE} || exit $?
fi

%files
%defattr (-, root, root)
%dir /lib/modules
/lib/modules/%{KRELEASE}
/boot/vmlinuz-%{KRELEASE}
/boot/System.map-%{KRELEASE}
/boot/config-%{KRELEASE}
/boot/symvers-%{KRELEASE}.gz
%if 0%{?rhel} == 5
/boot/initrd-%{KRELEASE}.img
%endif
%if 0%{?rhel} == 6
/boot/initramfs-%{KRELEASE}.img
%endif
%if 0%{?rhel} == 7
/boot/initramfs-%{KRELEASE}.img
%endif


%files headers
%defattr(-,root,root)
/usr/include/*

%files firmware
%defattr(-,root,root)
/lib/firmware/*

%files devel
%defattr(-,root,root)
/usr/src/kernels/%{KRELEASE}/*
/usr/src/kernels/%{KRELEASE}/.config

%changelog
* Wed Dec 31 2014  Horst Venzke <support@remsnet.de> - r3.14.27.el7-02
- rpmbuild on centos7
- added some %if 0%{?rhel} == 7

* Wed Dec 17 2014 Steven Haigh <netwiz@crc.id.au> - 3.14.27-1
- Update to upstream 3.14.27
