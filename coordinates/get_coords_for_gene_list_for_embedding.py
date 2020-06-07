import argparse
import pandas as pd

def parse_args():
    parser=argparse.ArgumentParser(description="use gencode annotation to get gene coordinates; add flanks of specified length with a stride of specific size")
    parser.add_argument("-gene_list")
    parser.add_argument("-gencode_gtf",default="/mnt/data/annotations/gencode/GRCh37/gencode.v32lift37.annotation.gtf.gz")
    parser.add_argument("-window_size",type=int,default=250)
    parser.add_argument("-interval_left_flank",type=int,default=1000000)
    parser.add_argument("-interval_right_flank",type=int,default=1000000)
    parser.add_argument("-out_suffix")
    return parser.parse_args()

def main():
    args=parse_args()
    #get genes of interest
    genes=open(args.gene_list,'r').read().strip().split('\n')
    gene_dict={} 
    for gene in genes:
        gene_dict[gene]=1
        
    gtf=pd.read_csv(args.gencode_gtf,header=None,sep='\t',skiprows=5)
    gtf=gtf[gtf[2]=='gene']
    print("loaded gtf:"+str(gtf.shape))
    for index,row in gtf.iterrows():
        gene_info=[i.strip() for i in row[8].split(';')]
        for entry in gene_info:
            if entry.startswith('gene_name'):
                gene_name=entry.split('"')[1].upper() 
                if gene_name in gene_dict:
                    print(gene_name)
                    gene_chrom=row[0]
                    gene_start=row[3]
                    gene_end=row[4]
                    gene_strand=row[6]
                    if gene_strand=="-":
                        anchor=gene_end
                    else:
                        anchor=gene_start
                    first_bin=args.window_size*(anchor//args.window_size)-args.interval_left_flank
                    last_bin=args.window_size*(anchor//args.window_size)+args.interval_right_flank
                    bin_start=list(range(first_bin,last_bin,args.window_size))
                    bin_end=list(range(first_bin+args.window_size,last_bin+args.window_size,args.window_size))
                    outf=open(gene_name+"."+args.out_suffix,'w')
                    for i in range(len(bin_start)):
                        outf.write(gene_chrom+'\t'+str(bin_start[i])+'\t'+str(bin_end[i])+'\t'+gene_name+'\t'+'0'+'\t'+gene_strand+'\t'+'.\t.\t.\t'+str(int(args.window_size/2))+'\n')
                    outf.close()
                    
                    
    
if __name__=="__main__":
    main() 
