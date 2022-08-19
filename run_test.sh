set -e
echo 'AMR_TEST=test python clean.py'
AMR_TEST=test python clean.py
echo 'python amr_preprocess.py'
python amr_preprocess.py
echo 'python prepare_matrix.py'
python prepare_matrix.py
