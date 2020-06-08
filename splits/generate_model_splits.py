import argparse
import pandas as pd
chrom_to_split={'chr1':0,
                'chr2':1,
                'chr19':1,
                'chr3':2,
                'chr20':2,
                'chr6':3,
                'chr13':3,
                'chr22':3,
                'chr5':4,
                'chr16':4,
                'chrY':4,
                'chr4':5,
                'chr15':5,
                'chr21':5,
                'chr7':6,
                'chr14':6,
                'chr18':6,
                'chr11':7,
                'chr17':7,
                'chrX':7,
                'chr9':8,
                'chr12':8,
                'chr8':9,
                'chr10':9}
import argparse
def parse_args():
    parser=argparse.ArgumentParser(description="split bed file by folds")
    parser.add_argument("-input")
    parser.add_argument("-output")
    return parser.parse_args()

def main():
    args=parse_args()
    data=pd.read_csv(args.input,header=None,sep='\t')
    nsplits=10
    splits={}
    for i in range(nsplits):
        splits[i]=open(args.output+'.'+str(i),'w')
        print("create output files")
    for index,row in data.iterrows():
        chrom=row[0]
        cur_split=chrom_to_split[chrom]
        splits[cur_split].write('\t'.join([str(j) for j in row])+'\n')
    for split in splits:
        splits[split].close()
        

    
if __name__=="__main__":
    main()
    

