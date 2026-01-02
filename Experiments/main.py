from to_dnf import to_nested_dnf_WCNF, to_nested_dnf_MaxSAT, find_paths, find_examples_paths,dnf_formula, calcul_accuracy
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import sys

def main(args):
    maxsat_path = "./NuWLS-c-IBR/bin/NuWLS-c-IBR_static" # Update the path to NuWLS MaxSAT
    if len(args) == 5:
        # Reading the data
        data_file = args[0]
        number_F = int(args[1])
        features = [f'F{i}' for i in range(0,(number_F))]
        class_name = 'c'
        data = pd.read_csv(data_file,sep=' ',header=None, names=["c"] + features) 
        train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
        train_data = train_data.reset_index(drop=True)
        test_data = test_data.reset_index(drop=True)
        k = int(args[2])
        class_target = int(args[3])
        timeout = int(args[4])
    elif len(args) == 6:
        # Reading the data
        train_data_file = args[0]
        test_data_file = args[1]
        number_F = int(args[2])
        features = [f'F{i}' for i in range(0,(number_F))]
        class_name = 'c'
        train_data = pd.read_csv(train_data_file,sep=' ',header=None, names=["c"] + features) 
        test_data = pd.read_csv(test_data_file,sep=' ',header=None, names= ["c"] + features)  
        k = int(args[3])
        class_target = int(args[4])
        timeout = int(args[5])
    else :    
        print("The main program requires 5 or 6 arguments : \n"
        "1. If you have a single data file:\n"
        "   python3 main.py <data_file> <nb_features> <k> <class_target> <timeout> \n"
        "   Example : python3 main.py data/car.data 6 2 1 120\n"
        "2. If you have separate train and test files:\n"
        "   python3 main.py <train_file> <test_file> <nb_features> <k> <class_target> <timeout>\n"
        "   Example : python3 main.py data/monks-1.train data/monks-1.test 6 2 1 120\n")
        sys.exit(1)
    Xdata = train_data[features] 
    Ydata = train_data[class_name]
    Xdata_test = test_data[features] 
    Ydata_test = test_data[class_name]
    all_paths = []
    taken = set()
    taken_feature = set()
    features = []
    for i in range (2,k+1) : 
        rf = RandomForestClassifier(n_estimators=10*i,max_depth=i,random_state=42) 
        rf.fit(Xdata, Ydata)
        #Find all Paths to target class for each tree in the forest
        for i,tree in enumerate(rf.estimators_) :
            paths = find_paths(tree.tree_,class_target)
            for p in paths :
                t = tuple(sorted(p.items()))
                if t not in taken :
                    taken.add(t)
                    all_paths.append(p)
                    for key,v in p.items() : 
                        if (key,v) not in taken_feature :
                            taken_feature.add((key,v))
                            features.append({key: v})
    print('--------------------------------- Random Forest max_depth =',k)
    y_test_pred = rf.predict(Xdata_test)
    rf_acc_test = accuracy_score(Ydata_test,y_test_pred)
    print("Test Accuracy : ",round(rf_acc_test * 100, 2), "%")
    #Find the examples covered by each path
    tab_terms = find_examples_paths(all_paths,train_data)
    #Find the Nested (k,k)-DNF
    if (len(tab_terms) != 0) :
        print('--------------------------------- Nested (k,k)-DNF with k =',k)
        #file_path : path to the wcnf file (./wcnf/wcnf_file.wcnf)
        file_path,xm = to_nested_dnf_WCNF(features,tab_terms,k,k,train_data,class_name,class_target)
        found, tab_terms, matrix = to_nested_dnf_MaxSAT(file_path,xm,maxsat_path,features,tab_terms,k,k,timeout)
        if found : 
            formula,num_terms = dnf_formula(tab_terms)
            #print("DNF Formula : ",formula)  
            print("Test Accuracy : ", round(calcul_accuracy(formula,test_data,number_F,class_name,class_target),2), "%")
        else :
            print("Model not found")

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)