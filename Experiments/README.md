## Project Structure

- `data/`
Directory containing the datasets used in the experiments. The first column of each file is the class label.

- `wcnf/`
Directory containing the WCNF file used by the MaxSAT solver.

- `to_dnf.py`
The source code of the project.

- `main.py`
Main script of the project.

- `Dockerfile`
File used to build the Docker image and listing the dependencies.

- `replay_exp.sh`
Replay the experiments of the paper

## Dependencies
In addition to Python with the libraries NumPy, pandas, scikit-learn, and SymPy, the program requires a MaxSAT solver.

The MaxSAT solver used is **NuWLS-c-IBR**  
Documentation: https://maxsat-evaluations.github.io/2024/descriptions.html

The path to the solver must be set in the `maxsat_path` variable in the `main.py` file.

## Usage

The program accepts **5 or 6 parameters**, depending on whether the dataset is provided as a single file or as separate training and test files :

```
python3 main.py <data_file> <nb_features> <k> <class_target> <timeout>
```
```
python3 main.py <train_file> <test_file> <nb_features> <k> <class_target> <timeout>
```

- **Important :** The timeout represents the maximum solving time for the MaxSAT solver and can significantly impact its results.

- **Output :** The accuracies of a Random Forest (max_depth = k) and a Nested (k,k)-DNF trained on the dataset.

## Replay the FASE 2026 paper results

Please note that the results of the experiments may vary when executed on different machines with different hardware resources. This variability is due to the use of a MaxSAT solver with a timeout, which can lead to different outcomes depending on available computational resources. The results reported in the paper were obtained on a Dell Inc. Precision 3591 with 32 GiB of RAM and Intel® Core™ Ultra 7 165H × 22, running Ubuntu 24.04.3 LTS (64 bits). Hence, you may need to extend the timeout beyond the value we used to achieve the same or better results.

To replay the experiments (table 4 of the paper) with the same parameters as in the paper, run the script **./replay_exp.sh**.
The experiments can also be run by specifying a timeout using the -t option, for example **./replay_exp.sh -t 200**.
All experiments, with the paper configuration, take around 2h30 on the computer described previously.

## Docker
A docker is available here : https://filesender.renater.fr/?s=download&token=6cc997f7-2958-4731-92c8-3f8ce4022297

Load the docker with `docker load -i fase_exp.tar`

Run the docker with `docker run --rm -it fase_exp bash`

you will then be able to run the `./replay_exp.sh` script or the `main.py` file like explained above.
