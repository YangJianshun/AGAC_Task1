import sys
import os
import json
import jieba
import argparse

parser = argparse.ArgumentParser(description = 'Convert json format to tab format')
parser.add_argument("indir", help="Input directory containing json format files")
parser.add_argument("outdir", help="Output directory")
parser.add_argument("-NoTriggerWords",action="store_true")

args=parser.parse_args()

indir,outdir=args.indir,args.outdir

def json2tab(filename,outfilename):
    F=open(filename,'r')
    info_json=F.read()
    F.close
    info = json.loads(info_json)
    #print(info.keys())
    words=[x for x in jieba.cut(info['text'])if not x in (' ','\t','\n')]
    #print(info['text'])
    for denotation in info['denotations']:
        #print(denotation['obj'],'\t',end='')
        begin=int(denotation['span']['begin'])
        end=int(denotation['span']['end'])
        #print(info['text'][begin:end])
    denotations=info['denotations']
    beg=0
    denotation_index=0
    in_denotation=False
    O=open(outfilename,'w')
    for word in words:
        word_pos=info['text'].index(word,beg)
        word_len=len(word)
        beg = word_pos+word_len
        label = 'O'
        if(not denotation_index>len(denotations)-1):
            if word_pos==denotations[denotation_index]['span']['begin']:
                label='B-'+denotations[denotation_index]['obj']
                in_denotation=True
            elif in_denotation==True:
                label='I-'+denotations[denotation_index]['obj']
            if word_pos+word_len==denotations[denotation_index]['span']['end']:
                if not word_pos==denotations[denotation_index]['span']['begin']:
                    label='E-'+denotations[denotation_index]['obj']
                denotation_index+=1
                in_denotation=False
        if args.NoTriggerWords: label='O'
        O.write("{}\t{}:{}:{}:{}\t{}\n".format(word,filename,'S1',word_pos,word_len,label))
        if word=='.':O.write("\n")
        #print("{}\t{}:{}:{}:{}\t{}".format(word,filename,'S1',word_pos,word_len,label))
    #print(info['denotations'])
    O.close()
#json2tab('PubMed-16371368.json','PubMed-16371368.tab')

infiles=os.listdir(indir)
if not os.path.exists(outdir): os.system('mkdir {}'.format(outdir))
for infile in infiles:
    infile=indir+'/' + infile
    outfile=infile.split('/')[-1]
    outfile=outfile.split('.')
    outfile[-1]='tab'
    outfile='.'.join(outfile)
    outfile=outdir+'/'+outfile
    json2tab(infile,outfile)

