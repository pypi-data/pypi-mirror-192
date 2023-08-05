# multiPrime

`multiPrime is an error-tolerant primer design tool for broad-spectrum pathogens detection. 
It proposes a solution for the minimum degeneracy degenerate primer design with error (MD-EDPD).` 

## 1. Install

> pip

```
pip3 install multiPrime
```

+ `pip` `python >=3.9`



## 2. Usage

```
$ multiPrime -h 
multiPrime -i input -o output
           Options: { -l [18] -n [4] -d [10] -v [1] -g [0.2,0.7] -f [0.8] -c [4] -p [10] -a [4] }

Options:
-h, --help            show this help message and exit
-i INPUT, --input=INPUT
                      Input file: multi-alignment output (muscle or others).
-l PLEN, --plen=PLEN  Length of primer. Default: 18.
-n DNUM, --dnum=DNUM  Number of degenerate. Default: 4.
-d DEGENERACY, --degeneracy=DEGENERACY
                      degeneracy of primer. Default: 10.
-v VARIATION, --variation=VARIATION
                      Max mismatch number of primer. Default: 1.
-e ENTROPY, --entropy=ENTROPY
                      Entropy is actually a measure of disorder. This parameter is used to judge whether the 
                      window is conservation. Entropy of primer-length window. Default: 3.6.
-g GC, --gc=GC        Filter primers by GC content. Default [0.2,0.7].
-s SIZE, --size=SIZE  Filter primers by mini PRODUCT size. Default 100.
-f FRACTION, --fraction=FRACTION
                      Filter primers by match fraction. Default: 0.8.
-c COORDINATE, --coordinate=COORDINATE
                      Mismatch index is not allowed to locate in start or
                      stop. otherwise, it won't be regard as the mis-
                      coverage. With this param, you can control the index
                      of Y-distance (number=variation and position of mismatch) when calculate
                      coverage with error.Default: 4.
-p PROC, --proc=PROC  Number of process to launch. Default: 20.
-a AWAY, --away=AWAY  Filter hairpin structure, which means distance of the
                      minimal paired bases. Default: 4. Example:(number of
                      X) AGCT[XXXX]AGCT. Primers should not have
                      complementary sequences (no consecutive 4 bp
                      complementarities),otherwise the primers themselves
                      will fold into hairpin structure.
-o OUT, --out=OUT     Output file: candidate primers. e.g.
                      [*].candidate.primers.txt.
```

Parameters：

| Parameters      | Description                                                                                                                                                                                                                                                                              |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -i/--input      | Input file: Result of multi-alignment. (muscle, mafft or others)                                                                                                                                                                                                                         |
| -l/--plen       | Length of primer. Default: 18                                                                                                                                                                                                                                                            |
| -n/--dnum       | Number of degenerate. Default: 4.                                                                                                                                                                                                                                                        |
| -v/--variation  | Max mismatch number of primer. Default: 1.                                                                                                                                                                                                                                               |
| -e/--entropy    | Entropy is actually a measure of disorder. This parameter is used to judge whether the window is conservation. Entropy of primer-length window. Default: 3.6.                                                                                                                            |
| -g/--gc         | Filter primers by GC content. Default [0.2,0.7].                                                                                                                                                                                                                                         |
| -s/--size       | Number of degenerate. Default: 4.                                                                                                                                                                                                                                                        |
| -f/--fraction   | Filter primers by match fraction (Coverage with errors). Default: 0.8.                                                                                                                                                                                                                   |
| -c/--coordinate | Mismatch index is not allowed to locate in start or stop. otherwise, it won't be regard as the mis-coverage. With this param, you can control the index of Y-distance (number=variation and position of mismatch) when calculate coverage with error.Default: 4.                         |
| -p/--proc       | Number of process to launch. Default: 20.                                                                                                                                                                                                                                                |
| -a/--away       | Filter hairpin structure, which means distance of the minimal paired bases. Default: 4. Example:(number of X) AGCT[XXXX]AGCT. Primers should not have complementary sequences (no consecutive 4 bp complementarities),otherwise the primers themselves will fold into hairpin structure. |
| -o/--out        | Output file: candidate primers. e.g.  [*].candidate.primers.txt.                                                                                                                                                                                                                         |

## 3. Results

Three output files：

+ `output`：Information of primer.
+ `output.gap_seq_id_json`: Positions and non-contained sequences caused by errors (number of errors are greater than threshold).
+ `output.non_coverage_seq_id_json`: Positions and non-contained sequences.



## 4. test dir

```
multiPrime/example
```

