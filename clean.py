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
pd.Series(las_pat).to_csv('chevpat.csv')




#####
## Antibiotics
####


ast_data['antibiotic'] = ast_data['antibiotic'].astype(str).apply(lambda x: re.sub(" +", " ", x)) # remove multiple spaces

ast_data['antibiotic'] = ast_data['antibiotic'].apply(lambda x: x.replace(' /','/').replace('/ ','/').lstrip().rstrip().lower().lstrip('/').rstrip('/').lstrip('('))

las_anti = sorted(list(ast_data['antibiotic'].unique()))
pd.Series(las_anti).to_csv('chevantbio.csv')


###
##R S I
#####

ast_data['result'] = ast_data['result'].astype(str).apply(lambda x: x.lstrip().rstrip().rstrip('/').rstrip('*').lstrip('*').upper()) # remove multiple spaces

las_res = sorted(list(ast_data['result'].unique()))
pd.Series(las_res).to_csv('chevres.csv')


#####
## Specimen
####

las_spec = sorted(list(ast_data['specimen'].unique()))
pd.Series(las_spec).to_csv('chev_specimen.csv')

ast_data.to_csv('outdata/ast_data_chevron_to_clean.csv')

#########
#######
#### Use lookup table to fix all the different spellings
##
#


lookup_table = pd.read_excel('../input_data/chevron-lookup-tables.xlsx',sheet_name=['pathogen','antibiotic','result','specimen'])

pathogen_rep = lookup_table['pathogen'].set_index('spelling')['correct'].dropna().apply(lambda x: x.lower()).to_dict()
missing_pathogen = ast_data[~ast_data['pathogen'].isin(pathogen_rep.keys())]
ast_data = ast_data[ast_data['pathogen'].isin(pathogen_rep.keys())]
ast_data['pathogen'] = ast_data['pathogen'].replace(pathogen_rep)


antibiotic_rep = lookup_table['antibiotic'].set_index('spelling')['correct'].dropna().apply(lambda x: x.lower()).to_dict()
missing_antibiotic = ast_data[~ast_data['antibiotic'].isin(antibiotic_rep.keys())]
ast_data = ast_data[ast_data['antibiotic'].isin(antibiotic_rep.keys())]
ast_data['antibiotic'] = ast_data['antibiotic'].replace(antibiotic_rep)


result_rep = lookup_table['result'].set_index('spelling')['correct'].dropna().apply(lambda x: x.upper()).to_dict() ##R/S/I to avoid confusion we keep it upper letter
missing_result = ast_data[~ast_data['result'].isin(result_rep.keys())]
ast_data = ast_data[ast_data['result'].isin(result_rep.keys())]
ast_data['result'] = ast_data['result'].replace(result_rep)


specimen_rep = lookup_table['specimen'].set_index('spelling')['correct'].dropna().apply(lambda x: x.lower()).to_dict()
missing_specimen = ast_data[~ast_data['specimen'].isin(specimen_rep.keys())]
ast_data = ast_data[ast_data['specimen'].isin(specimen_rep.keys())]
ast_data['specimen'] = ast_data['specimen'].replace(specimen_rep)

lookup_table['specimen']['correct'] = lookup_table['specimen']['correct'].apply(lambda x: x.lower())

specimen_category_rep = lookup_table['specimen'].set_index('correct')['specimen_category'].dropna().apply(lambda x: x.lower()).to_dict()

missing_specimen_category = ast_data[~ast_data['specimen'].isin(specimen_category_rep.keys())]
ast_data = ast_data[ast_data['specimen'].isin(specimen_category_rep.keys())]

ast_data['specimen_category'] = ast_data['specimen'].replace(specimen_category_rep)

ast_data.to_csv('outdata/ast_data_chevron_clean.csv')
