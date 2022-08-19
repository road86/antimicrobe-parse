import pandas as pd
import os

indata = pd.read_csv(os.path.join("outdata","ast_data_clean.csv"))

providers = list(indata['provider'].unique())
locations = list(indata['location'].unique())

masks = dict()

for prov in providers:
    masks[(prov,'bgd')] = (indata['provider']==prov)

for loc in locations:
    masks[('all',loc)] = (indata['location']==loc)

masks[('all','bgd')] = pd.Series(True,indata.index)

list_of_versions = []

for maskey in masks.keys():
    cleaneddata = indata[masks[maskey]]
    prov = maskey[0]
    loc = maskey[1]
    lv = {'provider':prov, 'location':loc}
    list_of_versions.append(lv)

    prepdata = cleaneddata.groupby(['specimen_category', 'pathogen','antibiotic','sensitivity'])['amr_uuid'].count().reset_index()
    prepdata2 = pd.pivot(prepdata, index=['specimen_category','pathogen','antibiotic'], columns='sensitivity', values='amr_uuid').reset_index()

    prepdata2.columns = list(prepdata2.columns[:3]) + [ 'count_' + x for x in prepdata2.columns[3:]]

    prepdata2 = prepdata2.fillna(0)
    prepdata2['total'] = prepdata2[list(prepdata2.columns[3:])].sum(axis=1)
    prepdata2['sensitivity'] = prepdata2.apply(lambda x: x['count_s']/x['total'],axis=1)

    prepdata2.to_csv(os.path.join('outdata',f'pre-processed-{prov}-{loc}.csv'))


    prepnoiso= cleaneddata.groupby(['specimen_category', 'pathogen'])['amr_uuid'].nunique().reset_index()
    prepnoiso.columns = ['specimen_category', 'pathogen', 'number_of_isolates']
    prepnoiso.to_csv(os.path.join('outdata',f'number-of-isolates-{prov}-{loc}.csv'))

pd.DataFrame.from_records(list_of_versions).to_csv(os.path.join('outdata','list_of_versions.csv'))
