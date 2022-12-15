import pandas as pd
import re
import os
import uuid

def clean(ast_data, summary=False, animal=False):
    #clean all starting with "growth of.."
    growth = re.compile('growth.*?Of', re.IGNORECASE)
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
    if not summary:
        ast_data['sensitivity'] = ast_data['sensitivity'].astype(str).apply(lambda x: x.lstrip().rstrip().rstrip('/').rstrip('*').lstrip('*').lower()) # remove multiple spaces

        las_res = sorted(list(ast_data['sensitivity'].unique()))
        pd.Series(las_res).to_csv(os.path.join('outdata','all_res_spelling.csv'))


    #####
    ## Specimen
    ####
    if not animal:
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


    correction_fields = ['pathogen','antibiotic','sensitivity','specimen','specimen_category']
    lookup_table = pd.read_excel(os.path.join('..','input_data','lookup-tables.xlsx'),sheet_name=correction_fields)

    assigned_masks_total = pd.Series(True,ast_data.index)
    # for cfield in ['pathogen']: #corrections to fields
    for cfield in correction_fields[:-1]: #corrections to fields
        if summary and cfield=="sensitivity":
            continue # skip fixing sensitivity
        if animal and cfield=="specimen":
            continue # skip fixing specimen for animals
        print('##############################')
        print(cfield)
        print('##############################')
        lookup_table[cfield] = lookup_table[cfield].dropna(subset=['spelling'])
        lookup_table[cfield]['spelling'] = lookup_table[cfield]['spelling'].apply(lambda x: str(x).lower())
        cfield_rep = lookup_table[cfield].set_index('spelling')['correct'].apply(lambda x: x.lower() if type(x)==str else x).to_dict()

        data_assigned_mask = ast_data[cfield].isin(cfield_rep.keys())
        print('records with data keys')
        print(data_assigned_mask.sum())

        missing_keys_for = ast_data[~data_assigned_mask][cfield].unique()
        print(f'The following {cfield} keys are missing')
        print(missing_keys_for)
        pd.Series(missing_keys_for).to_csv(os.path.join('outdata',f'missing_{cfield}_spelling.csv'))

        ast_data[cfield] = ast_data[cfield].replace(cfield_rep)

        data_nan = (~ast_data[cfield].isna())

        print('records with not a nan')
        print(data_nan.sum())

        data_assigned_mask_no_nan = data_assigned_mask & data_nan

        print('records with data keys and not a nan')
        print(data_assigned_mask_no_nan.sum())

        print('excluded data by provider')
        print(ast_data[(~data_assigned_mask_no_nan)].groupby('provider').count()['location'])


        assigned_masks_total=(data_assigned_mask_no_nan) & (assigned_masks_total)
        print(assigned_masks_total.sum())

    print('##############################')
    print('removing keys')
    print('##############################')


    print(assigned_masks_total.value_counts())

    misme = ast_data[~assigned_masks_total]

    misme.to_csv(os.path.join('outdata','data_skipped.csv'))
    print('Amount of data skipped is:')
    print(len(ast_data[~assigned_masks_total]))
    print('excluded data by provider')
    print(misme.groupby('provider').count()['location'])

    ast_data_preclean = ast_data[assigned_masks_total]


    print('included data by provider')
    print(ast_data_preclean.groupby('provider').count()['location'])

    if not summary:
        print('number of isolates (by provider)')
        print(ast_data_preclean.groupby(['provider'])['amr_uuid'].nunique())

    if not animal:
        las_spec_clean = sorted(list(ast_data_preclean['specimen'].unique()))
        pd.Series(las_spec_clean).to_csv(os.path.join('outdata','specimens_unique.csv'))

        print('##############################')
        print('Setting specimen category')
        print('##############################')

        try:
            lookup_table['specimen_category']['category'] = lookup_table['specimen_category']['category'].apply(lambda x: x.lower())
        except:
            print('if the following line breaks it would be because some of the speciment on the list have no specimen_category')

        specimen_category_rep = lookup_table['specimen_category'].set_index('specimen')['category'].dropna().apply(lambda x: x.lower()).to_dict()

        data_assigned_mask_speccat = ast_data_preclean['specimen'].isin(specimen_category_rep.keys())

        missing_specimen_category = ast_data_preclean[~data_assigned_mask_speccat]

        print(f'The following specimen_category keys are missing')
        print(missing_specimen_category['specimen'].unique())
        ast_data_preclean = ast_data_preclean[data_assigned_mask_speccat]

        ast_data_preclean['specimen_category'] = ast_data_preclean['specimen'].replace(specimen_category_rep)

    return ast_data_preclean
