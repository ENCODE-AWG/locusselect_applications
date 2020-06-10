for rep in ENCFF321LTI.tsv ENCFF057BZW.tsv ENCFF570OXF.tsv
do
    
    python get_expression_for_gene_list_ENCODE.py -gene_list /mnt/lab_data2/annashch/locusselect_applications/coordinates/H1ESC_PROXY_FOR_WTC11/genes.txt \
	   -expression $rep \
	   -outf TPM_$rep &
done
