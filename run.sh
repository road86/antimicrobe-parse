set -e
echo 'python parse_chevron.py'
python parse_chevron.py
echo 'python parse_epic.py'
python parse_epic.py
echo 'python parse_square.py'
python parse_square.py
echo 'python parse_imperial.py'
python parse_imperial.py
echo 'python parse_khulna-mc.py'
python parse_khulna-mc.py
echo 'python parse_adhumic.py'
python parse_adhumic.py
echo 'python parse_birdem.py'
python parse_birdem.py
echo './run_summary_parse.sh'
./run_summary_parse.sh
echo 'python compile_summary.py'
python compile_summary.py
echo 'python compile_individual.py'
python compile_individual.py
echo 'python amr_preprocess.py'
python amr_preprocess.py
echo 'python prepare_matrix.py'
python prepare_matrix.py
echo 'Done!'
