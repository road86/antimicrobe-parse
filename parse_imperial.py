import pandas as pd
import os

for year in ['21','22']:
    imperial_data = os.path.join('..','input_data','unsorted','AST data_ready to use',f'Imperial Hospital, Chattogram_20{year}.xlsx')

    # imperial_data = os.path.join('..','input_data','unsorted','RAW AST data_ready to use','Imperial Hospital, Chattogram_2022.xlsx')

    #we are reading sheets with individual data for each specimen
    dfs = pd.read_excel(imperial_data, sheet_name=[4,5,6,7,8,9,10,13,14,15])
    list_of_dfs = []

    for sheet_id in dfs.keys():
        df = dfs[sheet_id]
        organism_f = df.columns[7]
        date_f = df.columns[1]
        specimen_f = df.columns[6]
        df = df.dropna(subset=[organism_f, date_f, specimen_f])
        ast_data_part = pd.melt(df,id_vars=df.columns[0:9], value_vars=df.columns[9:],var_name='antibiotic', value_name='sensitivity')

        print(ast_data_part[organism_f].unique())
        ast_data_part.columns = ['index', 'sample_date','lab_id','sample_age', 'sample_sex', 'unit', 'specimen', 'pathogen', 'enzyme','antibiotic', 'sensitivity']
        ast_data_part = ast_data_part[['lab_id', 'sample_date','sample_age', 'sample_sex', 'specimen', 'pathogen', 'antibiotic', 'sensitivity']]


        list_of_dfs.append(ast_data_part)

    ast_data = pd.concat(list_of_dfs)

ast_data = ast_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample
    ### here

ast_data['location']=pd.Series('chittagong',index=ast_data.index)
ast_data['provider']=pd.Series('imperial',index=ast_data.index)

ast_data.to_csv(os.path.join('outdata',f'ast_data_imperial.csv'))
