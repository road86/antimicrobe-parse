import pandas as pd
import uuid
from openpyxl.styles import PatternFill
from openpyxl.styles import Alignment
import numpy as np

def mper(val):
    return str(round(100*val))+'%'

#threshold of number of isolates tested for given antibiotic out of total number of isolates of this bacteria. If it is below the threshold we are not showing a result
thresh=0.02

prepo = pd.read_csv('pre-processed.csv')
noi = pd.read_csv('number_of_isolates.csv')

# rawsummary = pd.merge(prepo,noi, on = ['specimen_category','pathogen'])
# easier to use to dfs for noi and rest of the data
rawsummary = prepo[['specimen_category', 'pathogen', 'antibiotic', 'total', 'sensitivity']]


#  ######
#    ##
#    ##
#    ##
#    ##
#  ######
#
#  Calculate antibiogram
#


with pd.ExcelWriter("amb.xlsx", engine="openpyxl") as writer:
    for specimen_type in prepo['specimen_category'].unique():
        print(specimen_type)
        df = rawsummary[rawsummary['specimen_category']==specimen_type]
        df_n = noi[noi['specimen_category']==specimen_type]
        df_n = df_n.sort_values(by=['number_of_isolates'], ascending = False)
        df_n = df_n.set_index('pathogen')

        amb_matrix_perc = pd.pivot(df, index='antibiotic', columns='pathogen', values='sensitivity')
        amb_matrix_tot = pd.pivot(df, index='antibiotic', columns='pathogen', values='total')

        new_row = dict()
        full_amb_list = []

        total_n_iso = df_n['number_of_isolates'].sum()
        new_row[('total','--')] = total_n_iso

        for pat, niso in df_n.iterrows():
            new_row[(pat,'n')] = niso['number_of_isolates']
            new_row[(pat,'%')] = mper(niso['number_of_isolates'] / total_n_iso)


        new_row[('overall sensitivity','%')] = '--'
        full_amb_list.append(new_row)
        tots_row = new_row

        for (antibio, aperc), (_, atot) in zip(amb_matrix_perc.iterrows(), amb_matrix_tot.iterrows()):
            new_row = dict()
            new_row[('total','--')] = atot.sum()
            oversense = 0
            for pat, _ in df_n.iterrows():
                if np.isnan(atot[pat]):
                    new_row[(pat,'n')] = 0
                    new_row[(pat,'%')] = '--'
                else:
                    #if number of isolates tested on this antibiotic i less than some percentage  of total number of isolates we will not report sensitivity
                    new_row[(pat,'n')] = atot[pat]
                    if (atot[pat] / tots_row[(pat,'n')]) < thresh:
                        new_row[(pat,'%')] = '--'
                    else:
                        new_row[(pat,'%')] = mper(aperc[pat])
                    n_times_per = atot[pat] * aperc[pat]
                    oversense = oversense + n_times_per
            new_row['overall sensitivity','%'] = mper(oversense/atot.sum())
            full_amb_list.append(new_row)

        full_amb_index = ['Total number of isolates'] + list(amb_matrix_perc.index)

        full_amb = pd.DataFrame.from_records(full_amb_list,index=full_amb_index)

        new_columns = pd.MultiIndex.from_tuples(full_amb.columns, names=['Pathogen', 'number of isolates and sensitivity'])
        full_amb.columns = new_columns
        full_amb.to_excel(writer,sheet_name=specimen_type)
        # Set backgrund colors depending on cell values
        worksheet = writer.sheets[specimen_type]


#  ######   ######  ######
#    ##       ##      ##
#    ##       ##      ##
#    ##       ##      ##
#    ##       ##      ##
#  ######   ######  ######
#
#  formatting
#
        heading_size = 3 #I'm not setting it up anywhere it is for some reason longer than I'd want

        worksheet.row_dimensions[1].height = 150

        worksheet.column_dimensions[worksheet.cell(row=3,column=1).column_letter].width = 40
        for ccc in range(2,len(full_amb.columns)+2):
            if ccc%2:
                worksheet.column_dimensions[worksheet.cell(row=3,column=ccc).column_letter].width = 5
            else:
                worksheet.column_dimensions[worksheet.cell(row=3,column=ccc).column_letter].width = 5
            worksheet.cell(row=1,column=ccc).alignment = Alignment(textRotation=70)
            for rrr in range(heading_size+1,heading_size+1+len(full_amb)):
                worksheet.cell(row=rrr,column=ccc).alignment = Alignment(vertical='center')
                worksheet.cell(row=rrr,column=ccc).alignment = Alignment(horizontal='center')

        # worksheet.column_dimensions[worksheet.cell(row=3,column=len(full_amb.columns)+1).column_letter].width = 20
        # worksheet.column_dimensions[worksheet.cell(row=3,column=len(full_amb.columns)).column_letter].width = 20

        #starting after first entry which is pathogen wide totals
        for rrr in range(heading_size+2,heading_size+1+len(full_amb)):
            for ccc in list(range(4,len(full_amb.columns)+1,2))+[len(full_amb.columns)+1]:
                value_str = worksheet.cell(row=rrr,column=ccc).value
                if value_str == '--':
                    worksheet.cell(row=rrr,column=ccc).fill = PatternFill("solid", start_color=('ededed'))
                else:
                    value = int(value_str.rstrip('%'))
                    worksheet.cell(row=rrr,column=ccc).fill = PatternFill("solid", start_color=('d62d20' if value < 50 else 'ed6f00' if value < 75 else 'eee600' if value < 90 else 'a0e040'))

        for ccc in range(1,len(full_amb.columns)+2):
            worksheet.cell(row=4,column=ccc).fill = PatternFill("solid", start_color='6495ed')
        worksheet.delete_rows(3,1)
