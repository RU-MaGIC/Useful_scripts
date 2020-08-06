import csv, os, glob, sys, json, requests
'''
A script for converting a file with ensemble IDs to more human readable gene symbol IDs. 
To start with, I manually downloaded the two backend sheets from biomart. Eventually I would love to have a function to allow it to pull new ones and such. TBD. 

To execute, import this and then:
ensemble_label('input_file_from_DEseq2','Output_Sample_ID','Genome of Interest ("mouse" or "human")')
'''

def db_build(genome):
    db_dict={}
    if genome=='human':
        with open('./ensembl_human.csv') as db:
            reader=csv.DictReader(db, delimiter=',')
            for row in reader:
                key=row['Gene stable ID']
                val=row['Gene name']
                db_dict[key]=val
            db.close()
        return db_dict
    elif genome=='mouse':
        with open('./ensembl_mouse.csv') as db:
            reader=csv.DictReader(db, delimiter=',')
            for row in reader:
                key=row['Gene stable ID']
                val=row['Gene name']
                db_dict[key]=val
            db.close()
        return db_dict
    else:
        print('Talk to designer- you arent using a standard genome')
        
def fetcher(db_dict, gene_in):
    names=[]
    names.append(db_dict[gene_in])
    return names

def ensemble_label(deseq,proj,genome):
    db=db_build(genome)
    with open(deseq) as chart:
        reader=csv.DictReader(chart, delimiter=',')
        headers=[]
        heads=reader.fieldnames
        for item in heads:
            headers.append(item)
        headers.append('GeneID')

        with open('./diffexpr-results_geneID'+proj+'.txt','w',newline='\n') as output:
            wr=csv.writer(output, quoting=csv.QUOTE_NONE, delimiter='\t')
            wr.writerow(headers)
            for row in reader:
                writelist=[]
                for field in reader.fieldnames:
                    writelist.append(str(row[field]))
                try:
                    geneid=fetcher(db,row['Gene'])
                except:
                    geneid=row['Gene']
                writelist.append(str(geneid).strip("[]'"))
                wr.writerow(writelist)
        output.close()
    chart.close()
    print('Gene IDS transcribed')           


