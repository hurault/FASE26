## Project Structure

- `data/`
Directory containing the datasets used by the program.  
**Important:** Each data file must have the **class label in the first column**.

- `wcnf/`
Directory where temporary files are stored. These files contain the clauses sent to the MaxSAT solver.

- `to_dnf.py`
Module responsible for generating clauses (conversion to DNF).

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

## Usage of main.py

The program accepts **5 or 6 parameters**:

1. **Dataset path**  
   - Can be one or two files depending if the testing an training dataset are split.  
   - If only one file is provided, the script will automatically split it.

2. **Number of features (`number_F`)**  
   - Number of dataset features to consider.  
   - **Warning:** Must match the actual number of features in the dataset.

3. **Timeout**  
   - Maximum solving time for the MaxSAT solver.  
   - **Important:** The timeout can significantly impact the solver’s results.

4. **k parameter**  
   - Must be **greater than 2**.

5. **Target class**  
   - Class to predict: **0 or 1**.

Result : the accuracies of a Random Forest (max_depth = k) and a nested (k, k)-DNF trained on the dataset.

## Replay the FASE 2026 paper results

Please note that the results of the experiments may vary when executed on different machines with different hardware resources. This variability is due to the use of a MaxSAT solver with a timeout, which can lead to different outcomes depending on available computational resources. The results reported in the paper were obtained on a Dell Inc. Precision 3591 with 32 GiB of RAM and Intel® Core™ Ultra 7 165H × 22, running Ubuntu 24.04.3 LTS (64 bits). Hence, you may need to extend the timeout beyond the value we used to achieve the same or better results.

To replay the experiments with the same parameters as in the paper, run the script **./replay_exp.sh**.
The experiments can also be run by specifying a timeout using the -t option, for example **./replay_exp.sh -t 200**.
All experiments, with the paper configuration, take around 2h30 on the computer described previously.

## Docker
A docker is available here : https://filesender.renater.fr/?s=download&token=6cc997f7-2958-4731-92c8-3f8ce4022297

Load the docker with `docker load -i fase_exp.tar`

Run the docker with `docker run --rm -it fase_exp bash`

you will then be able to run the `docker run --rm -it fase_why3 bash` or the `main.py` file like explained above.
