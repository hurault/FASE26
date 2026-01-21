## This is the GitHub repository for the paper “Formally Correct Search for Interpretable DNFs”, accepted at FASE 2026.

The `Experiments` directory contains the source code and datasets used for comparing Random Forests with nested (k,k)-DNF models, while the `Why3` directory contains the files required to replay the proofs of correctness and completeness of the SAT encoding.
For more details, please refer to the `README` files present in each directory.

## A Getting Started

### Replay the experiments
1. Get the docker image, either via https://cloud.irit.fr/s/0G9YJD6db0mfDx2, or embedded in the Zenodo DOI.
2. Load the docker with `docker load -i fase_exp.tar`
3. Run the docker with `docker run --rm -it fase_exp bash`
4. Smoke test
`python3 main.py data/car.data 6 2 1 120`

shoud print
```text
--------------------------------- Random Forest max_depth = 2
Test Accuracy :  78.61 %
--------------------------------- Nested (k,k)-DNF with k = 2
Test Accuracy :  87.86 %
```
Be careful: since a timeout comes into play, depending on the machine’s performance, the percentage may be slightly different.

### Replay the proofs
1. Get the docker image, either via https://cloud.irit.fr/s/oXYNl0dxqZZpcb4, or embedded in the Zenodo DOI.
2. Load the docker with `docker load -i fase_why3.tar`
3. Run the docker with `docker run --rm -it fase_why3 bash`
4. You will then be able to run the `why3 replay encoding-ok` to replay the proof. 
If the replay is OK, you will see : `96/96 (replay OK)`
