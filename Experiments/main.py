from to_dnf import to_nested_dnf_WCNF, to_nested_dnf_MaxSAT, find_paths, find_examples_paths,dnf_formula, calcul_accuracy
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

def main():

    maxsat_path = "./NuWLS-c-IBR-2024/bin/NuWLS-c-IBR_static" # Update the path to NuWLS MaxSAT
    timeout = 120
    class_target = 1
    k = 5
    # Reading the data
    number_F = 6 # number of features
    features = [f'F{i}' for i in range(0,(number_F))]
    class_name = 'c'
    train_data =  pd.read_csv("./data/monks-1.train",sep=' ',header=None, names=["c"] + features + ['del'],skipinitialspace=True) 
    test_data =  pd.read_csv("./data/monks-1.test",sep=' ',header=None, names= ["c"] + features + ['del'],skipinitialspace=True) 
    del train_data['del']
    del test_data['del']
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
    main()