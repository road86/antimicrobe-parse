# Setup

To install conda environment for our parsing, run
```
conda env create -f amrenv.yml
conda activate amrenv
```

To finish configuration run `R` and execute

```
install.packages('dplyr')
```

# Testing

To use test data, run
```
AMR_TEST=test python clean.py
```

# Preparing antibiogram from messy data

## Parsing chevron files and create antibiogram
Create a symbolic link to our lab data to `../input_data`

Download latest revision of the lookup table chevron-lookup-table as an xls to that directory.

Run script
```
./run.sh
```
or just execute commands from there
