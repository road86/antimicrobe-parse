import pandas as pd
import os

indata_summary = pd.read_csv(os.path.join("outdata","ast_data_animal_clean.csv"))
prov='animal'
loc='any'

list_of_versions = list()
lv = {'provider':prov, 'location':loc}
list_of_versions.append(lv)
print(f'Processing {prov} at {loc}')
preped_frames = []
preped_noiso_frames = []

indata_summary['specimen_category']=pd.Series("animal",index=indata_summary.index)
prepdata3 = indata_summary.groupby(['specimen_category','pathogen','antibiotic']).sum()[['sensitive_isolates','isolates_number']].reset_index()
prep_sum = prepdata3[['specimen_category', 'pathogen', 'antibiotic', 'sensitive_isolates','isolates_number']]
prep_sum.columns = ['specimen_category', 'pathogen', 'antibiotic', 'sensitive_isolates', 'total']
preped_frames.append(prep_sum)

prepnoiso_sum = indata_summary[['specimen_category','pathogen','isolates_number']].drop_duplicates()

prepnoiso_sum.columns = ['specimen_category', 'pathogen', 'number_of_isolates']
preped_noiso_frames.append(prepnoiso_sum)

prep_both = pd.concat(preped_frames)

prep_both = prep_both.groupby(['specimen_category','pathogen','antibiotic']).sum()[['sensitive_isolates','total']].reset_index()
prep_both['sensitivity'] = prep_both.apply(lambda x: x['sensitive_isolates']/x['total'],axis=1)
prep_both.to_csv(os.path.join('outdata',f'pre-processed-{prov}-{loc}.csv'))

prep_both_niso = pd.concat(preped_noiso_frames)
prep_both_niso.to_csv(os.path.join('outdata',f'number-of-isolates-{prov}-{loc}.csv'))

pd.DataFrame.from_records(list_of_versions).to_csv(os.path.join('outdata','list_of_versions.csv'))
