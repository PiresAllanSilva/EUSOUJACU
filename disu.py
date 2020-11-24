# This script writes the distance from 
# atom mol1///25/ha to atom mol1///26/ha
# out to the file "dist.txt"
# Simply change your selections to see different distances.
 
# import PyMOL's command namespace
from pymol import cmd
 
# open dist.txt for writing
f=open('dist.csv','w')

cys1=[5,10,11,21,29,30,36,43]
cys2=[5,10,11,21,29,30,36,43]
 
# calculate the distance and store it in dst
for i in cys1:
	for j in cys2:
		#if i==j: continue
		if j-i<4: continue 
		dst1=cmd.distance('tmp',str(i)+'/CA',str(j)+'/CA')
		dst2=cmd.distance('tmp',str(i)+'/CB',str(j)+'/CB')
# write the formatted value of the distance (dst)
# to the output file
#f.write("%8.3f\n"%dst)
#dst=cmd.distance('tmp','A/10/C','B/10/C')
		if dst1>10: continue
		if dst2>9: continue
		if dst2-dst1>1: continue
		out="Cys"+str(i)+"-Cys"+str(j)+";"+str(dst1)+";"+str(dst2)+";"+str(dst2-dst1)+"\n"
		f.write(out)
	#print(str(i))
	cys2.remove(i)
# close the output file.
f.close()
