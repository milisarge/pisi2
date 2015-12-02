 
#!/usr/bin/python
import piksemel
import os
import os.path
import shutil

import glob
import pisi.version

MAX_PERMITTED = 2

class initramfs:

    path = None

    def __init__(self, path):
        self.path = path
        spl = path.split("/boot/initramfs-")[1]
        self.version = pisi.version.Version(spl.split(".img")[0])

    def __repr__(self):
        return '%s - %s' % (self.path, self.version)

    def getVersion(self):
        return self.version

def cleanupOldImages():
    images = glob.glob("/boot/initramfs-*.img")
    objs = list()
    for image in images:
        try:
            i = initramfs(image)
            objs.append(i)
        except Exception, e:
            continue
        
    simages = sorted(objs, key=initramfs.getVersion, reverse=True)

    if len(simages) > MAX_PERMITTED:
        death = simages[MAX_PERMITTED:]
        for kill in death:
            try:
                os.unlink(kill.path)
            except Exception, ex:
                print "Unable to remove stale initramfs: %s" % ex


def updateInitrd(filepath):
    parse = piksemel.parse(filepath)
    for xmlfile in parse.tags("File"):
        path = xmlfile.getTagData("Path")
        if not path.startswith("/"):
            path = "/%s" % path # Just in case
        if path.startswith("/lib/modules"):
            # Handle the proper case of modules
            version = path.split("/")[3]
            cmd = "/sbin/depmod %s" % version
            os.system(cmd)
            cmd = "dracut -N -f --kver %s" % version
            os.system(cmd)

            initname = "/boot/initramfs-%s.img" % version
            if os.path.exists("/boot/efi/pisi"):
                try:
                    shutil.copy(initname, "/boot/efi/pisi/initramfs")
                except Exception, e:
                    print("Failed to copy efi boot")

            if os.path.exists("/proc/cmdline") and not os.path.exists("/sys/firmware/efi"):
                os.system("/usr/sbin/update-grub")
            break


def setupPackage(metapath, filepath):
    cleanupOldImages()
    updateInitrd(filepath)


def postCleanupPackage(metapath, filepath):
    # TODO: Remove old initramfs!
    pass
