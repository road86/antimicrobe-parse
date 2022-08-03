import pandas as pd
import re

ast_data = pd.read_csv('outdata/ast_data_chevron.csv')

#clean all starting with "growth of.."
growth = re.compile('growth.*?Of',re.IGNORECASE)
ast_data['pathogen'] = ast_data['pathogen'].astype(str).apply(lambda x: re.sub(growth,'',x))

#general cleaning of post and prefixes and leading spaces
ast_data['pathogen'] = ast_data['pathogen'].apply(lambda x: x.removesuffix(' l').rstrip('.').removesuffix('spp').lstrip().rstrip().lower().replace('. ','.').replace('.','. '))

ast_data['pathogen'] = ast_data['pathogen'].astype(str).apply(lambda x: re.sub(" +", " ", x)) # remove multiple spaces

#order alphabe
las_pat = sorted(list(ast_data['pathogen'].unique()))
pd.Series(las).to_csv('chevpat.csv')

#####
## Antibiotics
####


ast_data['antibiotic'] = ast_data['antibiotic'].astype(str).apply(lambda x: re.sub(" +", " ", x)) # remove multiple spaces

ast_data['antibiotic'] = ast_data['antibiotic'].apply(lambda x: x.replace(' /','/').replace('/ ','/').lstrip().rstrip().lower())

las_anti = sorted(list(ast_data['antibiotic'].unique()))
pd.Series(las).to_csv('chevantbio.csv')


#####
## Specimen
####

las_spec = sorted(list(ast_data['specimen'].unique()))
pd.Series(las).to_csv('chev_specimen.csv')
