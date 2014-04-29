rinse, xen-shell, xen-tools, rpmstrap, debootstrap, fakerooot

=====

RPMbuild project for:

- rinse ( http://www.steve.org.uk/Software/rinse/)
- xen-shell ( http://xen-tools.org/software/xen-tools/ )
- xen-tools ( http://xen-tools.org/software/xen-tools/ )
- rpmstrap ( https://github.com/blipvert/rpmstrap )
- debootstrap ( https://wiki.debian.org/de/Debootstrap )
- fakerooot ( https://wiki.debian.org/FakeRoot )


When it comes that you do scripted automated minimal OS provisioning & installation, 
the tools rinse with xen-tools been one of  the  tools for that.

Most OS depend tools require an GUI  / Xterm .
most of them , i.e  autoyast , satelite-server , yast-vm, yast-dirinstall, fai and some more
are allmost overkill  for AUTOMATED simple minimalistic imageing. 

rinse & xen-tools  don´t require X11 or VNC at all.

On Xen together with the latest xen-tools , this makes the admin live simpler.


usage see  Web-references :
http://wiki.centos.org/HowTos/Xen/Xen4QuickStart<br>
http://blog.xen.org/index.php/2012/08/31/xen-tools-a-straightforward-vm-provisioninginstallation-tool/<p>

http://www.raskas.be/blog/howtos/centos-base-image/<br>
http://forum.slicehost.com/index.php?p=/discussion/690/howto-install-centos-5-to-a-slice/p1<br>
http://www.steve.org.uk/Software/rinse/<br>
http://manpages.debian.org/cgi-bin/man.cgi?query=xen-create-image&apropos=0&sektion=0&manpath=Debian+6.0+squeeze&format=html&locale=en<br>
http://grantmcwilliams.com/item/538-centos-6-virtual-machine-64-bit-installation-on-xen<br>
http://wejn.org/stuff/how-to-boot-via-pygrub-on-lenny.html#6f318909c4c3e7e3364d1ecd26143baf<br>
http://wiki.centos.org/TipsAndTricks/CreateNewInitrd<br>


Depend Software :

- phyton 
- coreutils
- perl => 5.8
- some CPAN perl modules ( install from rpm or CPAN )
     perl(Config::IniFiles)
     perl (Text::Template)
     perl(Text::Template)
     perl(Config::IniFiles)
     perl(Expect) perl(Expect::Simple)
     perl(Getopt::Long)
     perl(LWP::UserAgent)
     perl(Pod::Usage)
     perl(File::Basename)
     perl(File::Find)
     perl(File::Path)

- sharutils
- libacl
- glibc
- makedev
