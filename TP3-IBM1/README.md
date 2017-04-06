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
|   +-- test.align.es	< gold file for translation es -> en (inversed index)
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

|Language|# Training|# Its|Precision|Recall|F1 Score| Time|
|--------|---------:|----:|--------:|-----:|-------:|----:|
|English → Spanish|50000|5|    0.596| 0.487|   0.536| 292s|
|English → Spanish|20000|5|    0.575| 0.470|   0.517| 137s|
|English → Spanish|10000|5|    0.540| 0.441|   0.485|  68s|
|English → Spanish|10000|4|    0.538| 0.440|   0.484|  54s|
|English → Spanish|10000|3|    0.537| 0.439|   0.483|  42s|
|English → Spanish|10000|2|    0.534| 0.437|   0.481|  29s|
|English → Spanish|10000|1|    0.418| 0.342|   0.376|  16s|
|English → Spanish| 5000|5|    0.508| 0.415|   0.457|  34s|
|English → Spanish| 1000|5|    0.398| 0.325|   0.358|   7s|


|Language|# Training|# Its|Precision|Recall|F1 Score| Time|
|--------|---------:|----:|--------:|-----:|-------:|----:|
|Spanish → English|10000|5|    0.499| 0.446|   0.470|  67s|
|Spanish → English| 5000|5|    0.468| 0.418|   0.442|  33s|
|Spanish → English| 1000|5|    0.373| 0.334|   0.352|   8s|
