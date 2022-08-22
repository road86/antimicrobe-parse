import uuid
import re
import pandas as pd
import os

nourish_data = os.path.join('..','input_data', 'unsorted', 'Animal Health data', 'Antibiotic Sensitivity Report@ 20.08.22.xlsx')


df1 = pd.read_excel(nourish_data, sheet_name = 'E.Coli', skiprows = 3, nrows= 25, header = [4])
df2 = pd.read_excel(nourish_data, sheet_name = 'Staphylococcus', skiprows = 3, nrows= 23, header = [4])
df3 = pd.read_excel(nourish_data, sheet_name = 'Pseudomonas', skiprows = 3, nrows= 25, header = [4])

##checking
datacheck = 'check' # folder to store script checks
df1.to_csv(f'{datacheck}/nourish1.csv') #checking if skiprows and header give the desired result
df2.to_csv(f'{datacheck}/nourish2.csv')
df3.to_csv(f'{datacheck}/nourish3.csv')
##################

ast_poultry = pd.melt(df1,id_vars=df1.columns[0:6], value_vars=df1.columns[6:-2],var_name='antibiotic', value_name='sensitivity')

ast_poultry = ast_poultry.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample
ast_poultry = ast_poultry.reset_index()
ast_poultry = ast_poultry[['index','Organism', 'Isolates_number' ,'antibiotic','sensitivity']]

ast_poultry.columns = ['pathogen', 'isolates' ,'antibiotic', 'sensitivity']

