import pandas as pd
import re
import os

#read in ast data parsed from various providers.
ast_data = pd.read_csv(os.path.join('outdata','ast_data_chevron.csv'))


#clean all starting with "growth of.."
growth = re.compile('growth.*?Of',re.IGNORECASE)
ast_data['pathogen'] = ast_data['pathogen'].astype(str).apply(lambda x: re.sub(growth,'',x))

#general cleaning of post and prefixes and leading spaces
ast_data['pathogen'] = ast_data['pathogen'].apply(lambda x: x.removesuffix(' l').rstrip('.').removesuffix('spp').lstrip().rstrip().lower().replace('. ','.').replace('.','. '))

ast_data['pathogen'] = ast_data['pathogen'].astype(str).apply(lambda x: re.sub(" +", " ", x)) # remove multiple spaces

#order alphabe
las_pat = sorted(list(ast_data['pathogen'].unique()))
pd.Series(las_pat).to_csv(os.path.join('outdata','chevpat.csv'))


#####
## Antibiotics
####


ast_data['antibiotic'] = ast_data['antibiotic'].astype(str).apply(lambda x: re.sub(" +", " ", x)) # remove multiple spaces

ast_data['antibiotic'] = ast_data['antibiotic'].apply(lambda x: x.replace(' /','/').replace('/ ','/').lstrip().rstrip().lower().lstrip('/').rstrip('/').lstrip('('))

las_anti = sorted(list(ast_data['antibiotic'].unique()))
pd.Series(las_anti).to_csv(os.path.join('outdata','chevanti.csv'))

###
##R S I
#####

ast_data['result'] = ast_data['result'].astype(str).apply(lambda x: x.lstrip().rstrip().rstrip('/').rstrip('*').lstrip('*').lower()) # remove multiple spaces

las_res = sorted(list(ast_data['result'].unique()))
pd.Series(las_res).to_csv(os.path.join('outdata','chevres.csv'))


#####
## Specimen
####

ast_data['specimen'] = ast_data['specimen'].astype(str).apply(lambda x: re.sub(" +", " ", x)) # remove multiple spaces

ast_data['specimen'] = ast_data['specimen'].apply(lambda x: x.replace(' /','/').replace('/ ','/').lstrip().rstrip().lower().lstrip('/').rstrip('/').lstrip('('))


las_spec = sorted(list(ast_data['specimen'].unique()))
pd.Series(las_spec).to_csv(os.path.join('outdata','chev_specimen.csv'))

# ast_data.to_csv(os.path.join('outdata','ast_data_chevron_to_clean.csv'))

#########
#######
#### Use lookup table to fix all the different spellings
##
#


correction_fields = ['pathogen','antibiotic','result','specimen','specimen_category']
lookup_table = pd.read_excel(os.path.join('..','input_data','chevron-lookup-tables.xlsx'),sheet_name=correction_fields)

for cfield in correction_fields[:-1]: #corrections to fields
    lookup_table[cfield]['spelling'] = lookup_table[cfield]['spelling'].apply(lambda x: x.lower())
    cfield_rep = lookup_table[cfield].set_index('spelling')['correct'].dropna().apply(lambda x: x.lower()).to_dict()
    data_assigned_mask = ast_data[cfield].isin(cfield_rep.keys())
    missing_cfield = ast_data[~data_assigned_mask]
    missing_keys_for = ast_data[~data_assigned_mask][cfield].unique()
    print(f'The following {cfield} keys are missing')
    print(missing_keys_for)
    ast_data = ast_data[data_assigned_mask]
    ast_data[cfield] = ast_data[cfield].replace(cfield_rep)
    print(len(ast_data))


las_spec_clean = sorted(list(ast_data['specimen'].unique()))
pd.Series(las_spec_clean).to_csv(os.path.join('outdata','specimens_unique.csv'))

try:
    lookup_table['specimen_category']['category'] = lookup_table['specimen_category']['category'].apply(lambda x: x.lower())
except:
 print('if the following line breaks it would be because some of the speciment on the list have no specimen_category')

specimen_category_rep = lookup_table['specimen_category'].set_index('specimen')['category'].dropna().apply(lambda x: x.lower()).to_dict()

data_assigned_mask = ast_data['specimen'].isin(specimen_category_rep.keys())

missing_specimen_category = ast_data[~data_assigned_mask]

print(f'The following specimen_category keys are missing')
print(missing_specimen_category)
ast_data = ast_data[data_assigned_mask]

ast_data['specimen_category'] = ast_data['specimen'].replace(specimen_category_rep)

ast_data.to_csv(os.path.join('outdata','ast_data_chevron_clean.csv'))
