#!/bin/bash

run_dataset() {
    dataset_train=$1
    dataset_test=$2
    attr_count=$3

    for k in {2..7}; do
        if [ "$k" -eq 7 ]; then
            timeout=180
        else
            timeout=120
        fi

        for class_target in 1 0; do
            echo "====================================================="
            echo "Running: $dataset_train / k=$k / class=$class_target / timeout=$timeout"
            echo "====================================================="

            if [ "$dataset_test" = "NONE" ]; then
                python3 main.py "$dataset_train" $attr_count "$k" "$class_target" "$timeout"
            else
                python3 main.py "$dataset_train" "$dataset_test" $attr_count "$k" "$class_target" "$timeout"
            fi
        done
    done
}

# ------------------------------
#   DATASETS
# ------------------------------

# balance-scale
run_dataset "data/balance-scale.data" "NONE" 4
# car
run_dataset "data/car.data" "NONE" 6
# kr-vs-kp
run_dataset "data/kr-vs-kp.data" "NONE" 36
# monks
run_dataset "data/monks-1.train" "data/monks-1.test" 6
run_dataset "data/monks-2.train" "data/monks-2.test" 6
run_dataset "data/monks-3.train" "data/monks-3.test" 6
# SPECT
run_dataset "data/SPECT.train" "data/SPECT.test" 22
# tic-tac-toe
run_dataset "data/tic-tac-toe.data" "NONE" 9