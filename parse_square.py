import pandas as pd

square_data = os.path.join('..','input_data','unsorted','RAW AST data_ready to use','Sq AST 2018.sav')
df = pd.read_spss(square_data)

#Instead of iterating through each row we can melt this wide format data into long format data.

ast_data_square = pd.melt(df,id_vars=df.columns[0:5], value_vars=df.columns[5:-2],var_name='antibiotic', value_name='sensitivity')

ast_data_square = ast_data_square.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample
ast_data_square = ast_data_square.reset_index()
ast_data_square = ast_data_square[['index','sex','Age','Specimen','Organism','antibiotic','sensitivity']]

ast_data_square.columns = ['lab_id', 'sample_sex', 'sample_age', 'specimen', 'pathogen', 'antibiotic', 'sensitivity']

ast_data_square.to_csv(os.path.join('outdata','ast_data_square.csv'))
