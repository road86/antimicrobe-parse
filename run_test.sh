set -e
echo 'AMR_TEST=test python clean.py'
AMR_TEST=test python clean.py
echo 'R < amr_preprocess.r --no-save'
R < amr_preprocess.r --no-save
echo 'python prepare_matrix.py'
python prepare_matrix.py
