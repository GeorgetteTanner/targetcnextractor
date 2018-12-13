#! /usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse

parser = argparse.ArgumentParser(description="Get the total, or allele specific, copy number of the mid-point of target regions from a copy number profile")
parser.add_argument('-t', '--targets', dest='targets', help='Target regions BED file (with header in first line)')
parser.add_argument('-c', '--cnfile', dest='cnfile', help='Copy number file (with header in first line) in format:chromosome \t start \t end \t total cn \t allele A cn (optional) \t allele B cn (optional)')
parser.add_argument('-o', '--output', dest='output', help='Output file directory and name')

args = parser.parse_args()

cndata={}
with open(args.cnfile,'r') as file:
    heading=file.readline()
    for line in file:
        l=line.split()
        if l[0] not in cndata:
            cndata[l[0]]=[]
        cndata[l[0]].append(l[1:])    

tdata=[]
with open(args.targets,'r') as file:
    next(file)
    for line in file:
        l=line.split()
        tdata.append([l[0],round((int(l[2])-int(l[1]))/2)+1,0])

tcns=[]        
for t in tdata:
    for region in cndata[t[0]]:
        if int(t[1])>=int(region[0]) and int(t[1])<=int(region[1]):
            tcns.append([t[0],t[1],region[2:]])
            break
        
with open(args.output,'w+') as file:
    file.write(heading)
    if len(tcns[0][2])==1:
        for t in tcns:
            file.write(str(t[0])+'\t'+str(t[1])+'\t'+str(t[2][0])+'\n')
    elif len(tcns[0][2])==3:        
        for t in tcns:
            file.write(str(t[0])+'\t'+str(t[1])+'\t'+str(t[2][0])+'\t'+str(t[2][1])+'\t'+str(t[2][2])+'\n')
    else:
        print('ERROR')