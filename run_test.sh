set -e
AMR_TEST=test python clean.py
R < amr_preprocess.r --no-save
python prepare_matrix.py
