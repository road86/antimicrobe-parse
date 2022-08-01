from striprtf.striprtf import rtf_to_text
import re
import pandas as pd
import datetime
import uuid

def get_pat_or_spe(pat_or_spe,text):

    spe_opts = ['Specimen', 'Sample']
    if pat_or_spe=='spe':
        for spe_opt in spe_opts:
            str_pat, r_pat, r_ant_pat = get_report_val(spe_opt,text)
            if len(str_pat) == 1:
                return re.sub(r_ant_pat,'',str_pat[0]).replace("\n","").lstrip().rstrip()

    pat_opts = ['Bacteria isolated', 'Culture']
    if pat_or_spe=='pat':
        for pat_opt in pat_opts:
            str_pat, r_pat, r_ant_pat = get_report_val(pat_opt,text)
            if len(str_pat) == 1:
                return re.sub(r_ant_pat,'',str_pat[0]).replace("Growth Of","").replace("Growth of","").replace("\n","").lstrip().rstrip()

def get_report_val(arg_name, text):
    r_pat = re.compile(f'{arg_name}.*?:.*?\n',re.IGNORECASE)
    r_ant_pat = re.compile(f'{arg_name}.*?:',re.IGNORECASE)
    pat_res = re.findall(r_pat,text)
    return pat_res, r_pat, r_ant_pat

def strip_fname(fname):
    fsp = fname.split('.')[0].split('^')
    date = datetime.datetime.strptime(fsp[0], '%Y%m%d')
    sex = fsp[1]
    age = fsp[2].split('Y')[0]
    return date, sex, age

megagigalist = []
fileslocs1 = '/Users/mix/dodon/praca/AMR/data/21-chittagong-chevron/July to September, 2021'
fileslocs='/Users/mix/dodon/praca/AMR/data/20-chittagong-chevron/Chevron Results 20201226'
fileslocs2 = '/Users/mix/dodon/praca/AMR/data/21-chittagong-chevron/March to June, 2021'

allfileslocs = []
allfileslocs.append(fileslocs)
allfileslocs.append(fileslocs1)
allfileslocs.append(fileslocs2)

for cfilelocs in allfileslocs:
    fileslist = os.listdir(cfilelocs)

    outputloc = "outdata"
    os.makedirs(outputloc, exist_ok=True)

    for fnl in fileslist:
        if not 'rtf' in fnl:
            continue
        if fnl.startswith('.'):
            continue

        cf = os.path.join(cfilelocs,fnl)
        # print(fnl)

        sample_date, sample_sex, sample_age = strip_fname(fnl)

        with open(cf, 'r') as file:
            rtftext = file.read()

        cleantext = rtf_to_text(rtftext, errors="ignore")
        #print(cleantext)
        #test parameters, tabs
        p = re.compile('\\t+')
        ct0 = re.sub(p,'',cleantext)

        #correct new lines
        nl = re.compile('\\n')
        ct1 = re.sub(nl,'\n',ct0)

        #double-named antibiotics
        nlb = re.compile('/\\n')
        ct2 = re.sub(nlb,'/',ct1)

        #read specimen
        #read bacteria
        specimen = get_pat_or_spe('spe',ct2)
        pathogen = get_pat_or_spe('pat',ct2)

        # print(sample_date)
        # print(sample_sex)
        # print(sample_age)
        # print(specimen)
        # print(pathogen)
        #read table

        nontab = re.compile('Microbiology.*?Anti',re.DOTALL | re.IGNORECASE)
        ctt0 = re.sub(nontab,'Anti',ct2)

        #######
        #lil hackS
        if ctt0.lower().find('micro') == 0: #preamble not removed
            nontab = re.compile('Microbiology.*?Susceptibility Information:',re.DOTALL | re.IGNORECASE)
            ctt0 = re.sub(nontab,'Antimicrobial,MIC,Interpretation,Antimicrobial,MIC,Interpretation\n',ctt0)


        if ctt0.lower().find('mic method') == 0: #preamble not removed
            nontab = re.compile('MIC Method.*?Antimicrobial',re.DOTALL | re.IGNORECASE)
            ctt0 = re.sub(nontab,'Antimicrobial',ctt0)

        if ctt0.lower().find('test: ') == 0: #preamble not removed
            nontab = re.compile('Test:.*?Antibiotics',re.DOTALL | re.IGNORECASE)
            ctt0 = re.sub(nontab,'Antibiotics',ctt0)

        #random messups in machine output?
        randmess = re.compile('InterpretRation')
        ctt0 = re.sub(randmess,'Interpretation',ctt0)

        ## hacks among hacks
        ########
        tabend = re.compile('S = Sen.*?\\n',re.DOTALL)
        ctt1 = re.sub(tabend,'',ctt0)

        tabend_more = re.compile('\\n\(Legend: ',re.DOTALL)
        ctt2 = re.sub(tabend_more,'',ctt1)

        tabtocsv = re.compile('\|')
        ctt3 = re.sub(tabtocsv,',',ctt2).lstrip() ##prevent first column name starting with white spaces

        #clean up some MIC name
        micmess = re.compile('MIC \(.*?\)')
        ctt = re.sub(micmess,'MIC',ctt3).lstrip()

        textfile = open(os.path.join(outputloc,f'{fn}.csv'), "w")
        a = textfile.write(ctt)
        textfile.close()

        df = pd.read_csv(os.path.join(outputloc,f'{fn}.csv'))
        df.columns = [e.lstrip().rstrip() for e in df.columns]

        import_uuid = str(uuid.uuid4())

        if df.columns[0]=='Antimicrobial':
            for iii, rrr in df.iterrows():
                if 'MIC' in df.columns:
                    mic0 = rrr['MIC']
                    mic1 = rrr['MIC.1']
                else:
                    mic0 = 'N/A'
                    mic1 = 'N/A'

                new_df = {
                    'import_uuid':import_uuid,
                    'input_file_name':fnl,
                    'sample_date':sample_date,
                    'sample_sex':sample_sex,
                    'sample_age':sample_age,
                    'pathogen':pathogen,
                    'specimen':specimen,
                    'antibiotic':rrr['Antimicrobial'],
                    'mic':mic0,
                    'result':rrr['Interpretation']
                }
                megagigalist.append(new_df)
                if not 'Antimicrobial.1' in df.columns:
                    continue
                new_df = {
                    'import_uuid':import_uuid,
                    'input_file_name':fnl,
                    'sample_date':sample_date,
                    'sample_sex':sample_sex,
                    'sample_age':sample_age,
                    'pathogen':pathogen,
                    'specimen':specimen,
                    'antibiotic':rrr['Antimicrobial.1'],
                    'mic':mic1,
                    'result':rrr['Interpretation.1']
                }
                megagigalist.append(new_df)
        elif 'Antibiotics' in df.columns[0]:
            for iii, rrr in df.iterrows():
                new_df = {
                    'import_uuid':import_uuid,
                    'input_file_name':fnl,
                    'sample_date':sample_date,
                    'sample_sex':sample_sex,
                    'sample_age':sample_age,
                    'pathogen':pathogen,
                    'specimen':specimen,
                    'antibiotic':rrr['Antibiotics'],
                    'result':rrr['Sensitivity']
                }
                megagigalist.append(new_df)
                if not 'Antibiotics.1' in df.columns:
                    continue
                new_df = {
                    'import_uuid':import_uuid,
                    'input_file_name':fnl,
                    'sample_date':sample_date,
                    'sample_sex':sample_sex,
                    'sample_age':sample_age,
                    'pathogen':pathogen,
                    'specimen':specimen,
                    'antibiotic':rrr['Antibiotics.1'],
                    'result':rrr['Sensitivity.1']
                }
                megagigalist.append(new_df)
        else:
            print('ERROR')

ast_data = pd.DataFrame.from_records(megagigalist)
ast_data.to_csv('ast_data.csv')
