set -e
python parse_summary_poultry-BARC.py
python parse_poultry-aftab.py
python parse_poultry-nourish.py
python compile_animal.py
python animal_preprocess.py
python prepare_matrix.py
