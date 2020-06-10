import argparse
import pandas as pd

def parse_args():
    parser=argparse.ArgumentParser(description="use gencode annotation to get gene coordinates; add flanks of specified length with a stride of specific size")
    parser.add_argument("-gene_list")
    parser.add_argument("-gencode_gtf",default="/mnt/data/annotations/gencode/GRCh37/gencode.v32lift37.annotation.gtf.gz")
    parser.add_argument("-expression")
    parser.add_argument("-outf")
    return parser.parse_args()

def main():
    args=parse_args()
    #get genes of interest
    genes=open(args.gene_list,'r').read().strip().split('\n')
    gene_dict={} 
    for gene in genes:
        gene_dict[gene]=1
    expression=pd.read_csv(args.expression,header=0,sep='\t')
    expression_dict={}
    for index,row in expression.iterrows():
        gid=row['gene_id'].split('.')[0]
        val=row['TPM']
        expression_dict[gid]=val
    gtf=pd.read_csv(args.gencode_gtf,header=None,sep='\t',skiprows=5)
    gtf=gtf[gtf[2]=='gene']
    outf=open(args.outf,'w')
    outf.write('Gene\tGeneID\tTPM\n')
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
                cur_expression=expression_dict[gene_id]
            except:
                cur_expression="NA"
            outf.write(gene_name+'\t'+gene_id+'\t'+str(cur_expression)+'\n')
    outf.close()
    
                    
    
if __name__=="__main__":
    main() 
