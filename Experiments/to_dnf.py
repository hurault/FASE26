import numpy as np
import pandas as pd
import itertools
from sklearn.tree import _tree
import subprocess
from multiprocessing import Pool
from sympy import symbols, simplify
from sympy.logic.boolalg import And, Or

# Returns the wcnf written to a file (./wcnf/wcnf_file.wcnf)
def to_nested_dnf_WCNF(features,tab_terms,k_prime,k,train_data,class_name,class_target) :
    n = len(tab_terms)
    m = len(features)
    data_size = len(train_data)
    count = 0
    top = data_size + 1
    file = "./wcnf/wcnf_file.wcnf"
    with open(file, 'w+') as f :
        f.write("p wcnf                                                                               \n") 
        # Soft clauses (trying to maximize the accuracy)
        xe = k_prime*k*m + 1
        e_class_target = train_data.index[train_data[class_name].values == class_target].tolist() 
        e_class_other = train_data.index[train_data[class_name].values == (1-class_target)].tolist()
        for x in e_class_target :
             f.write(f"1 {xe+x} 0\n")
        for x in e_class_other :
            f.write(f"1 {-(xe+x)} 0\n")

        # Each element of the matrix has at least one literal  
        clauses = []
        for i in range(k_prime*k):
            c = list(range(i*m+1,i*m+m+1))
            f.write(f"{top} {' '.join(map(str, c))} 0\n")
            clauses.append(c)

        # Each element of the matrix has at most one literal       
        for i in range(k_prime*k):
            for x, y in itertools.combinations(clauses[i], 2):
                f.write(f"{top} {-x} {-y} 0\n")
        
        xm = xe + data_size
        # Determining which terms covered each example
        for e in range(data_size):
            mask = tab_terms['e_covered'].map(lambda s: e in s)
            t_covered_e = tab_terms.index[mask]
            if not t_covered_e.empty :
                c = []
                for x in t_covered_e :
                    f.write(f"{top} {-(xm+x)} {xe+e} 0\n")
                    c.append(xm+x)
                    count = count +1
                c = c + [-(xe+e)]
                f.write(f"{top} {' '.join(map(str, c))} 0\n")   
                count = count +1
            else :
                f.write(f"{top} {-(xe+e)} 0\n")
                count = count +1
        
        xr = xm + n
        for ind, row in tab_terms.iterrows():
            # Rp,i,j+1 -> Rp,i,j (Nested)
            for i in range(k_prime):
                for j in range(k-1):
                    f.write(f"{top} {-(xr+i*k+j+1)} {xr+i*k+j} 0\n")
                     
            xt = xr + k_prime*k
            # Tp,i,j,l <=> Xi,j,l and Rp,i,j
            for index in range(m) : 
                c=[]
                for i in range(k_prime):
                    for j in range(k):
                        l = (i*k+j)*m+index
                        c = c+[xt+l]
                        ri = xr+i*k+j
                        f.write(f"{top} {-(xt+l)} {l+1} 0\n")
                        f.write(f"{top} {-(xt+l)} {ri} 0\n")
                        f.write(f"{top} {-ri} {-(l+1)} {xt+l} 0\n")
                        
                key, value = next(iter(features[index].items()))
                #if the literal is in the term (and the term is taken in the DNF)
                if key in row['term'] and row['term'][key] == value:
                    c = c+[-(xm+ind)]
                    f.write(f"{top} {' '.join(map(str, c))} 0\n")    
                    count = count +1
                else : 
                    for x in c :
                        f.write(f"{top} {-x} {-(xm+ind)} 0\n")
                        count = count +1
            
            xr = xt + k_prime*k*m
        count = count + data_size + k_prime*k * (1 + (m*(m-1)//2) + 3*m*n) + k_prime*(k-1)*n
        nb_variables = xr-1
        header = f"p wcnf {nb_variables} {count} {top}"
        f.seek(0)
        f.write(header.ljust(85)+"\n") 
    return file,xm

# Returns the Matrix and the DNF
# Execute the MaxSAT solver with a timeout and capture its output 
def to_nested_dnf_MaxSAT(file,xm,maxsat_path,features,tab_terms,k_prime,k,timeout_sec) :
    cmd = f"timeout {timeout_sec} {maxsat_path} {file}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout.splitlines()
    model = None
    found = False
    #Filter the line that start with "v" (i.e the model)
    for line in range(1, len(output)):
        if output[line].startswith("v"):
            model = [int(b) for b in output[line][2:]]
    #Construct the matrix
    matrix = pd.DataFrame([[{} for _ in range(k)] for _ in range(k_prime)])
    n = len(tab_terms)
    m = len(features)
    if model != None : 
        found = True
        for p in range(0,k_prime*k): 
            for index,l in enumerate(model[p*m:p*m+m]) :
                if l > 0 :
                    i = p // k
                    j = p % k 
                    matrix.at[i,j] = features[index]
        #Update the terms_table : Identifiying the terms taken in the final DNF
        mask = [model[xm+p-1]>0 for p in range(n)]
        tab_terms = tab_terms[mask]
    return found,tab_terms,matrix

# Returns the list of paths to the target_class
# Each path has a dictionary structure where the key is (feature_id, operator (<= or >) ) and the value is the threshold
def find_paths(tree,class_target):
    def find(node, path):
        paths = []
        if tree.feature[node] == _tree.TREE_UNDEFINED:
            if tree.value[node].argmax() == class_target :
                return [path]
            else:
                return []  
        # Trace both left and right branches
        left_child = tree.children_left[node]
        right_child = tree.children_right[node]
        feature_id = int(tree.feature[node])
        threshold = float(tree.threshold[node])
        keyi = (feature_id,'<=')
        if keyi not in path or ( path[keyi] > threshold) :
            pathi = path.copy()
            pathi[keyi] = threshold
            paths.extend(find(left_child,pathi))
        else :
            paths.extend(find(left_child, path))                     
        keyg = (feature_id,'>')
        if keyg not in path or ( path[keyg] < threshold) :
            pathg = path.copy()
            pathg[keyg] = threshold
            paths.extend(find(right_child, pathg))
        else :     
            paths.extend(find(right_child, path))                      
        return paths
    # Start from the root node (node 0)
    return find(0, {})  


def find_examples_path(path) :
    mask = np.ones(sizeG, dtype=bool)
    for (feature, operator), threshold in path.items() :
        mask &= dataG[f'F{feature}'].values <= threshold if operator == '<=' else dataG[f'F{feature}'].values > threshold
    return [path,set(dataG.index[mask])]
dataG = None
sizeG = None
def init_pool(data_arg):
    global dataG
    global sizeG
    dataG = data_arg
    sizeG = len(data_arg)
# Returns a table : For each path : e_covered : the list of examples (IDs) that the path covered
# Parallelized using multiprocessing (using Pool : data parallelism = distributing the input data across processes)
def find_examples_paths(paths,train_data):
    with Pool(initializer=init_pool, initargs=(train_data,)) as pool:
        results = pool.map(find_examples_path,paths)   
    tab_terms = pd.DataFrame(results, columns= ['term','e_covered']) 
    return tab_terms

# Returns the DNF formula, along with the number of terms in it
def dnf_formula(tab_terms) :
    fs=[]
    for t in tab_terms['term']:
        ts = []
        for (index, op), val in t.items():
            f = symbols(f'F{index}')
            if op == '>':
                ts.append(f > val)
            else :
                ts.append(f <= val)
        fs.append(And(*ts))
    formula = Or(*fs)
    num_terms = len(formula.args) if formula.func.__name__ == "Or" else 1
    return formula,num_terms

# Returns the accuracy    
def calcul_accuracy (formula,data,number_F,class_name,class_target):
    v=0
    if class_target == 1 :
        for i, row in data.iterrows():
            values = {symbols(f'F{j}'): data.loc[i, f'F{j}'] for j in range(number_F)}
            if int(bool(simplify(formula.subs(values)))) == data.loc[i,class_name] :
                v = v+1
    else :
        for i, row in data.iterrows():
            values = {symbols(f'F{j}'): data.loc[i, f'F{j}'] for j in range(number_F)}
            if int(bool(simplify(formula.subs(values)))) == (1- data.loc[i,class_name]):
                v = v+1
    return (v / len(data))*100