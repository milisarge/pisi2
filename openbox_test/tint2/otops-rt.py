import os


#os.sytem("pisi -y bi --ignore-safety")
os.sytem("pisi -y it pisilinux-dev-tools")
os.sytem("pisi it *.pisi")
os.system("checkelf -x -s -n -m *.pisi > missing.txt")

mdeps=[]
with open('missing.txt') as fp:
	kilit=1
	for line in fp:
		line=line.strip()
		if kilit==0:
			mdeps.append(line)
		if line=="--------------------":
			kilit=0
print mdeps	


with open('pspec.xml') as fp2:
	yenixml=""
	for line in fp2:
		line=line.strip()
		yenixml+=line+"\n"
		if line=="<RuntimeDependencies>":
			depsek=""
			for dep in mdeps:
				depsek+="<Dependency>"+dep+"</Dependency>"+"\n"
			yenixml+=depsek+"\n"
open("ypspec.xml","w").write(yenixml)
