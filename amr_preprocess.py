import pandas as pd
import os

cleaneddata = pd.read_csv(os.path.join("outdata","ast_data_clean.csv"))

prepdata = cleaneddata.groupby(['specimen_category', 'pathogen','antibiotic','sensitivity'])['amr_uuid'].count().reset_index()
prepdata2 = pd.pivot(prepdata, index=['specimen_category','pathogen','antibiotic'], columns='sensitivity', values='amr_uuid').reset_index()

prepdata2.columns=['specimen_category', 'pathogen', 'antibiotic', 'count_i', 'count_r', 'count_s']
prepdata2 = prepdata2.fillna(0)
prepdata2['total'] = prepdata2[['count_r','count_s','count_i']].sum(axis=1)
prepdata2['sensitivity'] = prepdata2.apply(lambda x: x['count_s']/x['total'],axis=1)

prepdata2.to_csv('pre-processed.csv')


prepnoiso= cleaneddata.groupby(['specimen_category', 'pathogen'])['amr_uuid'].nunique().reset_index()
prepnoiso.columns = ['specimen_category', 'pathogen', 'number_of_isolates']
prepnoiso.to_csv('number_of_isolates.csv')
