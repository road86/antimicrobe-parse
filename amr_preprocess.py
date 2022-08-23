import pandas as pd
import os

indata = pd.read_csv(os.path.join("outdata","ast_data_clean.csv"))
indata_summary = pd.read_csv(os.path.join("outdata","ast_data_summary_clean.csv"))
#I suggest that we do not use summary data at all until we verify its quality by seeing input data and their calculations https://github.com/road86/project-amr/issues/19
indata_summary = indata_summary.iloc[0:0]


providers = list(indata['provider'].unique()) + list(indata_summary['provider'].unique())
locations = list(indata['location'].unique()) + list(indata_summary['location'].unique())

masks = dict()
masks_summary = dict()

for prov in providers:
    masks[(prov,'bgd')] = (indata['provider']==prov)
    masks_summary[(prov,'bgd')] = (indata_summary['provider']==prov)

for loc in locations:
    masks[('all',loc)] = (indata['location']==loc)
    masks_summary[('all',loc)] = (indata_summary['location']==loc)

masks[('all','bgd')] = pd.Series(True,indata.index)
masks_summary[('all','bgd')] = pd.Series(True,indata.index)

list_of_versions = []

for maskey in masks.keys():
    cleaneddata = indata[masks[maskey]]
    cleaneddata_summary = indata_summary[masks_summary[maskey]]

    prov = maskey[0]
    loc = maskey[1]
    lv = {'provider':prov, 'location':loc}
    list_of_versions.append(lv)
    print(f'Processing {prov} at {loc}')
    preped_frames = []
    preped_noiso_frames = []

    if len(cleaneddata)!=0:
        prepdata = cleaneddata.groupby(['specimen_category', 'pathogen','antibiotic','sensitivity'])['amr_uuid'].count().reset_index()
        prepdata2 = pd.pivot(prepdata, index=['specimen_category','pathogen','antibiotic'], columns='sensitivity', values='amr_uuid').reset_index()

        prepdata2.columns = list(prepdata2.columns[:3]) + [ 'count_' + x for x in prepdata2.columns[3:]]

        prepdata2 = prepdata2.fillna(0)
        prepdata2['total'] = prepdata2[list(prepdata2.columns[3:])].sum(axis=1)
        prep_ind = prepdata2[['specimen_category', 'pathogen', 'antibiotic', 'count_s', 'total']]
        prep_ind.columns = ['specimen_category', 'pathogen', 'antibiotic', 'sensitive_isolates', 'total']
        preped_frames.append(prep_ind)

        prepnoiso_ind= cleaneddata.groupby(['specimen_category', 'pathogen'])['amr_uuid'].nunique().reset_index()
        prepnoiso_ind.columns = ['specimen_category', 'pathogen', 'number_of_isolates']
        preped_noiso_frames.append(prepnoiso_ind)

    if len(cleaneddata_summary)!=0:
        prepdata3 = cleaneddata_summary.groupby(['specimen_category','pathogen','antibiotic']).sum()[['sensitive_isolates','isolates_number']].reset_index()
        prep_sum = prepdata3[['specimen_category', 'pathogen', 'antibiotic', 'sensitive_isolates','isolates_number']]
        prep_sum.columns = ['specimen_category', 'pathogen', 'antibiotic', 'sensitive_isolates', 'total']
        preped_frames.append(prep_sum)

        prepnoiso_sum = cleaneddata_summary[['specimen_category','pathogen','isolates_number']].drop_duplicates()

        prepnoiso_sum.columns = ['specimen_category', 'pathogen', 'number_of_isolates']
        preped_noiso_frames.append(prepnoiso_sum)

    prep_both = pd.concat(preped_frames)

    prep_both = prep_both.groupby(['specimen_category','pathogen','antibiotic']).sum()[['sensitive_isolates','total']].reset_index()
    prep_both['sensitivity'] = prep_both.apply(lambda x: x['sensitive_isolates']/x['total'],axis=1)
    prep_both.to_csv(os.path.join('outdata',f'pre-processed-{prov}-{loc}.csv'))

    prep_both_niso = pd.concat(preped_noiso_frames)
    prep_both_niso.to_csv(os.path.join('outdata',f'number-of-isolates-{prov}-{loc}.csv'))


sens0iso = (prepdata2['count_s']==0).sum()
totiso = len(prepdata2['count_s'])
perc_sens0iso = sens0iso/totiso
print(f'There are {sens0iso} antibiotic/pathogen pairs with 0 sensitive AST results, which is {perc_sens0iso:.2f} of all pairs')

pd.DataFrame.from_records(list_of_versions).to_csv(os.path.join('outdata','list_of_versions.csv'))
