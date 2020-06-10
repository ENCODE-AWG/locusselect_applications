import argparse
import pandas as pd

def parse_args():
    parser=argparse.ArgumentParser(description="use gencode annotation to get gene coordinates; add flanks of specified length with a stride of specific size")
    parser.add_argument("-gene_list")
    parser.add_argument("-gencode_gtf",default="/mnt/data/annotations/gencode/GRCh37/gencode.v32lift37.annotation.gtf.gz")
    parser.add_argument("-expression",default="rna.seq.results.txt")
    parser.add_argument("-out_suffix")
    return parser.parse_args()

def main():
    args=parse_args()
    #get genes of interest
    genes=open(args.gene_list,'r').read().strip().split('\n')
    gene_dict={} 
    for gene in genes:
        gene_dict[gene]=1
    expression=open(args.expression,'r').read().strip().split('\n')
    expression_dict={}
    for line in expression[1::]:
        tokens=line.split('\t')
        gid=tokens[0]
        val=tokens[1::]
        expression_dict[gid]=val
    print(str(expression_dict))
    gtf=pd.read_csv(args.gencode_gtf,header=None,sep='\t',skiprows=5)
    gtf=gtf[gtf[2]=='gene']
    outf=open('expression_for_target_gene_set_H1ESC_WTC11.txt','w')
    outf.write('Gene\tGeneID\tExcitatory\n')
    print("loaded gtf:"+str(gtf.shape))
    for index,row in gtf.iterrows():
        keep=False
        gene_info=[i.strip() for i in row[8].split(';')]
        for entry in gene_info:
            if entry.startswith('gene_id'):
                gene_id=entry.split('"')[1].split('.')[0] 
            if entry.startswith('gene_name'):
                gene_name=entry.split('"')[1].upper() 
                if gene_name in gene_dict:
                    keep=True
        if keep is True:
            try:
                cur_expression=expression_dict[gene_id][0]
            except:
                cur_expression="NA"
            outf.write(gene_name+'\t'+gene_id+'\t'+str(cur_expression)+'\n')
    outf.close()
    
                    
    
if __name__=="__main__":
    main() 
