import os
import sys

dosya=sys.argv[1]

os.system("service dbus start")
os.system("pisi -y up")
os.system("pisi ar lxqtkay https://github.com/ayhanyalcinsoy/Pisicik/raw/master/Desktop/lxqt/pisi-index.xml.xz")
os.system("pisi ar contribkay https://github.com/pisilinux/contrib/raw/master/pisi-index.xml.xz")
os.system("pisi -y it cmake")
with open(dosya) as fp:
	for line in fp:
		paket=line.strip()
		os.system("pisi -y bi "+paket+" --ignore-safety")
		os.system("pisi -y it *.pisi")
		#os.system("pisi -y hs -t 78")
		print paket,"derlendi" 
