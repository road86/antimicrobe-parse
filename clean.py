import pandas as pd
import re
import os
import uuid

#read in ast data parsed from various providers.
preprocessed_files = ['ast_data_chevron.csv','ast_data_birdem.csv','ast_data_adhumic.csv','ast_data_square.csv','ast_data_imperial.csv','ast_data_khulna-mc.csv']
indata_dir = 'outdata'

if os.getenv('AMR_TEST') == 'test':
    preprocessed_files = ['ast_data_test.csv']
    indata_dir = 'test'

list_of_dfs = []
for ppf in preprocessed_files:
    ast_data_part = pd.read_csv(os.path.join(indata_dir,ppf))
    list_of_dfs.append(ast_data_part)

ast_data = pd.concat(list_of_dfs)


#clean all starting with "growth of.."
growth = re.compile('growth.*?Of',re.IGNORECASE)
ast_data['pathogen'] = ast_data['pathogen'].astype(str).apply(lambda x: re.sub(growth,'',x))

#general cleaning of post and prefixes and leading spaces
ast_data['pathogen'] = ast_data['pathogen'].apply(lambda x: x.removesuffix(' l').rstrip('.').removesuffix('spp').lstrip().rstrip().lower().replace('. ','.').replace('.','. '))

ast_data['pathogen'] = ast_data['pathogen'].astype(str).apply(lambda x: re.sub(" +", " ", x)) # remove multiple spaces

#order alphabe
las_pat = sorted(list(ast_data['pathogen'].unique()))
pd.Series(las_pat).to_csv(os.path.join('outdata','all_pat_spelling.csv'))


#####
## Antibiotics
####


ast_data['antibiotic'] = ast_data['antibiotic'].astype(str).apply(lambda x: re.sub(" +", " ", x)) # remove multiple spaces

ast_data['antibiotic'] = ast_data['antibiotic'].apply(lambda x: x.replace(' /','/').replace('/ ','/').lstrip().rstrip().lower().lstrip('/').rstrip('/').lstrip('('))

las_anti = sorted(list(ast_data['antibiotic'].unique()))
pd.Series(las_anti).to_csv(os.path.join('outdata','all_anti_spelling.csv'))

###
##R S I
#####

ast_data['result'] = ast_data['result'].astype(str).apply(lambda x: x.lstrip().rstrip().rstrip('/').rstrip('*').lstrip('*').lower()) # remove multiple spaces

las_res = sorted(list(ast_data['result'].unique()))
pd.Series(las_res).to_csv(os.path.join('outdata','all_res_spelling.csv'))


#####
## Specimen
####

ast_data['specimen'] = ast_data['specimen'].astype(str).apply(lambda x: re.sub(" +", " ", x)) # remove multiple spaces

ast_data['specimen'] = ast_data['specimen'].apply(lambda x: x.replace(' /','/').replace('/ ','/').lstrip().rstrip().lower().lstrip('/').rstrip('/').lstrip('('))


las_spec = sorted(list(ast_data['specimen'].unique()))
pd.Series(las_spec).to_csv(os.path.join('outdata','all_specimen_spelling.csv'))

# ast_data.to_csv(os.path.join('outdata','ast_data_chevron_to_clean.csv'))

#########
#######
#### Use lookup table to fix all the different spellings
##
#


correction_fields = ['pathogen','antibiotic','result','specimen','specimen_category']
lookup_table = pd.read_excel(os.path.join('..','input_data','lookup-tables.xlsx'),sheet_name=correction_fields)

assigned_masks_total = pd.Series(True,ast_data.index)
for cfield in correction_fields[:-1]: #corrections to fields
    lookup_table[cfield] = lookup_table[cfield].dropna(subset=['correct'])
    lookup_table[cfield]['spelling'] = lookup_table[cfield]['spelling'].apply(lambda x: x.lower())
    cfield_rep = lookup_table[cfield].set_index('spelling')['correct'].dropna().apply(lambda x: x.lower()).to_dict()
    data_assigned_mask = ast_data[cfield].isin(cfield_rep.keys())
    missing_cfield = ast_data[~data_assigned_mask]
    missing_keys_for = ast_data[~data_assigned_mask][cfield].unique()
    print(f'The following {cfield} keys are missing')
    print(missing_keys_for)

    missing_spellings_to_csv = sorted(missing_keys_for)
    pd.Series(missing_spellings_to_csv).to_csv(os.path.join('outdata',f'missing_{cfield}_spelling.csv'))

    assigned_masks_total=(data_assigned_mask) & (assigned_masks_total)

    ast_data[cfield] = ast_data[cfield].replace(cfield_rep)
    print(len(ast_data))


print(assigned_masks_total.value_counts())
ast_data = ast_data[assigned_masks_total]

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

ast_data['amr_uuid'] = [uuid.uuid4() for _ in range(len(ast_data.index))]
ast_data.to_csv(os.path.join('outdata','ast_data_clean.csv'))
