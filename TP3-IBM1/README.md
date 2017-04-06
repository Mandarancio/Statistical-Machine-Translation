# TP3 - IBM1
Martino Ferrari
## Project Structure
```
.
+-- core/               < folder containing all the functional code of the project
|   +-- em_ibm.py       < EM algorithm
|   +-- ibm1.py         < IBM Translation Model 1
|   +-- train.py        < training pipeline
+-- resources/          < folder containing the optional static translation tables
+-- test/               < folder containing the optional static translation tables
|   +-- myalignments    < output of main.py
+-- training/           < folder containing the training data set
+-- conf.json           < example of configuration (optional)
+-- main.py             < main script with all the required functinality
+-- generate_tables.py  < script to generate static translation table (optional)
```
## EM
### Performances

### Results

## IBM1
### Performances
### Results

## Overall Results

|Language|N training|N its|Precision|Recall|F1 Score|
|--------|---------:|----:|--------:|-----:|-------:|
|English → Spanish|50000|5|    0.596| 0.487|   0.536|
|English → Spanish|10000|5|    0.540| 0.441|   0.485|
|English → Spanish| 5000|5|    0.508| 0.415|   0.457|
|English → Spanish| 1000|5|    0.398| 0.325|   0.358|

