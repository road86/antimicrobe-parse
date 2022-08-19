set -e
echo 'python parse_chevron.py'
python parse_chevron.py
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
echo 'python clean.py'
python clean.py
echo 'python amr_preprocess.py'
python amr_preprocess.py
echo 'python prepare_matrix.py'
python prepare_matrix.py
echo 'Done!'
