import sys
import os
import json
import argparse

parser = argparse.ArgumentParser(description = 'Convert tab format to json format')
parser.add_argument("infile", help="Input tab file")
parser.add_argument("outdir", help="Output directory")

args=parser.parse_args()
if not os.path.exists(args.outdir): os.system("mkdir {}".format(args.outdir))

info={}
F=open(args.infile,'r')
for line in F:
    line=line.strip('\n')
    if line=='': continue
    lines=line.split('\t')
    jsonfile_and_pos,obj=lines[1],lines[3]
    if obj=='O': continue
    jsonfile,paragraph,start,length=jsonfile_and_pos.split(':')
    #print(jsonfile,start,length,obj)
    start=int(start);length=int(length)
    info.setdefault(jsonfile,[])
    info[jsonfile].append((start,start+length,obj))
F.close()
for jsonfile in info.keys():
    #print(jsonfile)
    denotations_new=[]
    i=1
    for obj_pos in info[jsonfile]:
        if(obj_pos[2].startswith('B-')):
            denotations_new.append({"id":"T{}".format(i),"span":{"begin":obj_pos[0],"end":obj_pos[1]},"obj":obj_pos[2][2:]})
            i+=1
        else:
            denotations_new[-1]["span"]["end"]=obj_pos[1]
    
    json_content=json.loads( open(jsonfile,'r').read() )
    json_content.pop('relations')
    json_content['denotations']=denotations_new
    json_str=json.dumps(json_content)
    #print('-------')
    #print(json_str)
    #print('-------')
    outfile=args.outdir+'/'+jsonfile.split('/')[-1]
    #print(outfile)
    #print('-------')
    O=open(outfile,'w')
    O.write(json_str)
    O.close()


