"trrust_analysis.py"
import pandas as pd
import numpy as np

###
# Depends upon TransSyncW and SIGNET
###

def read_trrust_db(db_file):
    trrust_data = pd.read_table(db_file ,header=None)
    trrust_data.columns =['Gene', 'Target', 'Action', 'Refrence']
    return trrust_data.drop(['Refrence'],axis = 1)

def combine_transync_outputs(cores_file, marker_file, target_genes_file):
    transync = pd.read_table(cores_file)
    transync.rename(columns = {'core':'Type'}, inplace = True)
    transynm = pd.read_table(marker_file)
    transynm.insert(3, 'Type', 'marker')
    transync_genes = pd.concat([transync, transynm])
    transync_genes.to_csv(target_genes_file)
    return transync_genes

def reform_signet_output(signet_out_file, signet_unique_genes_file):
    signet = pd.read_csv(signet_out_file)
    tf = signet['V1']
    tg = signet['V2']
    signet_data = pd.concat([tf,tg])
    signet_unique_genes = pd.DataFrame((signet_data.unique()),columns=['Gene'])
    signet_unique_genes.to_csv(signet_unique_genes_file,index=False)
    return pd.DataFrame(signet_data,columns=['Gene'])


def analyse(trust_db, transync_combined, signet_reformed, artefacts_path): 
    trrust_transsynw_gene_match=trust_db[trust_db['Gene'].isin(transync_combined['Gene'])]
    trrust_transsynw_gene_match['Source']='TranSyn'
    trrust_transsynw_target_match=trust_db[trust_db['Target'].isin(transync_combined['Gene'])]
    trrust_transsynw_target_match['Source']='TranSyn'

    trrust_signet_gene_match=trust_db[trust_db['Gene'].isin(signet_reformed['Gene'])]
    trrust_signet_gene_match['Source']='SIGNET'
    trrust_signet_target_match=trust_db[trust_db['Target'].isin(signet_reformed['Gene'])]
    trrust_signet_target_match['Source']='SIGNET'
    
    trrust_analysis = [trrust_transsynw_gene_match,trrust_transsynw_target_match,trrust_signet_gene_match,trrust_signet_target_match]
    tdata = pd.concat(trrust_analysis)
    tdata.to_csv(artefacts_path + "/trrust_analysis.csv", index=False)
    return tdata

def trrust_analysis(trust_db_file, artefacts_path):
    print("RUNNING TRRUST_analysis with params", trust_db_file, artefacts_path)

    cores_file= artefacts_path+"/TransSynW/cores.tsv"
    markers_file = artefacts_path+"/TransSynW/markers.tsv"
    signet_file = artefacts_path+"/Signet/copaired2.csv"
    target_genes_file = artefacts_path+"/Trrust_Analysis/transync_genes.csv"
    signet_unique_genes_file = artefacts_path+"/Trrust_Analysis/signet_unique_gene_list.csv"
    

    return analyse(read_trrust_db(trust_db_file),
    combine_transync_outputs(cores_file, markers_file, target_genes_file),
    reform_signet_output(signet_file,signet_unique_genes_file), artefacts_path)