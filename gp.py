import random
import numpy as np
import copy
import math

class node:
    def __init__(self,nodevalue):
        self.nodevalue = nodevalue
        self.right = None
        self.left = None
        self.MSE = None

    def __lt__(self, other):
        return self.MSE < other.MSE

def print_tree(root):
    if root is None:
        return 
    if root.left is None and root.right is None:
        if root.nodevalue == 'x':
            return 'x'
        else:
            return root.nodevalue
  
    LeftSum = print_tree(root.left) 
    if root.nodevalue in ['+','-','*','/','**']:
        RightSum = print_tree(root.right)
        return '(' + str(LeftSum)+str(root.nodevalue)+str(RightSum)+')'
    else :
        return str(root.nodevalue)+'(' + str(LeftSum) + ')' 


def combine_trees(choice_tree_1 , choice_tree_2):
    temp = copy.deepcopy(choice_tree_1)
    while(True):
        if temp.left.nodevalue == 'x':
            temp.left = choice_tree_2
            return temp
        else:
            temp = temp.left

def mutation(tree,Operators,Operands,numtree):
    treenodes = list()
    treenodes.append(tree)
    for i in range(len(treenodes)>0) :
        probability = round(random.random() , 3)
        node_of_tree = treenodes[i]
        if probability > 0.1:
            if node_of_tree.left != None and node_of_tree.right != None:
                treenodes.append(node_of_tree.left)
                treenodes.append(node_of_tree.right)
            else:
                return
        else:
            if node_of_tree.nodevalue in Operators:
                    if node_of_tree.nodevalue == 'cos' or node_of_tree.nodevalue == 'sin':
                        node_of_tree.nodevalue = random.choice(Operators)
                        node_of_tree.right.nodevalue = random.choice(Operands)
                        return
                    else:
                        node_of_tree.nodevalue = random.choice(Operators)
                        return
            elif node_of_tree.nodevalue in Operands:
                node_of_tree.nodevalue = random.choice(Operands)
                return           
        if i==numtree:
            return
        
def calculate_tree(tree , x_entr):
    pridict_y = list()
    tree_function = str(print_tree(tree))
    for point_x in x_entr:
        res=0
        try:
            tree_function = tree_function.replace('x' , str(point_x))
            res = eval(tree_function)
        except:
            pass
        pridict_y.append(res)
    return pridict_y

def find_best_trees(tree , x , y):
    pridict_y = calculate_tree(tree , x)
    summation = 0
    for i in range (0,len(y)):
        difference = y[i] - pridict_y[i]
        squared_difference = difference**2
        summation = summation + squared_difference
    MSE = summation/len(y)
    return MSE/10

# x o y dar khod tabe asli
x = list()
# baze az 1 ta 10 ba fasele 0.2
temp = -10.1
for i in range(100):
    temp = temp + 0.2
    temp = round(temp , 1)
    x.append(temp)
y = list()
for i in range(100):
    # y.append(x[i]+2)
    # y.append(x[i]*math.sin(x[i]+1))
    # y.append(2*math.sin(x[i]) + i*3)
    y.append(-1*x[i]+3)

#tolid jamiat avalie random
number_population_trees = 100
operators = ['*' , '/' , '+' , '-' , '**' , 'math.sin' , 'math.cos']
operands = [1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 'x']
first_population_trees = list()
for i in range(number_population_trees):
    operatorTMP = random.choice(operators)
    operandTMP = random.choice(operands)
    # print(operandTMP)
    parent = node(operatorTMP)
    parent.left = node('x')
    if operatorTMP == 'sin' or operatorTMP == 'cos':
        parent.right = node(None)
    else:
        parent.right = node(operandTMP)
    #agar khod tabe bod hazf mishe va yeki dige sakhte mishe
    if operatorTMP == '+' and operandTMP == '2':
        del parent
        i -= 1
    first_population_trees.append(parent)


#GP
population_befor = list() #nasli ke alan hastim
population_befor = copy.deepcopy(first_population_trees)

population_after = list() #entekhabi haye nasle badi
population_after = copy.deepcopy(first_population_trees)

generation_number = 100
number_trees_combined = 50
numtree_mutation = 1
best_mse_in_generation = list()
generation=0
best_MSE=100000000
best_gen=generation_number
for generation in range(generation_number):
    # population_after = copy.deepcopy(population_befor)
    numtree_mutation = numtree_mutation+2
    delindx = list()
    for j in range(int(number_trees_combined/2)):
        choisen_tree_1 = random.choice(population_befor)
        choisen_tree_2 = random.choice(population_befor)
        population_after.append(combine_trees(choisen_tree_1 , choisen_tree_2))
        population_after.append(combine_trees(choisen_tree_2 , choisen_tree_1))
        if j==int(number_trees_combined/2)-1:# delete derakht moshabeh
            for a in range(len(population_after)):
                for s in range(len(population_after)):
                    if population_after[a].MSE == population_after[s].MSE and a != s:
                        delindx.append(a)
            delindx = [*set(delindx)]
            if len(delindx) < int(number_trees_combined/2) + number_population_trees:
                j = j- int(int(number_trees_combined/2)/3) 

    for indximprtnt in range(len(delindx)):
        population_befor.append(population_after[delindx[indximprtnt]])
    for k in range(len(delindx)):
        population_after.append(population_befor[k])


    # population_befor.clear()
    for tree in population_after:
        mutation(tree,operators,operands,numtree_mutation)

    for tree in population_after:
        try:
            tree.MSE = round(find_best_trees(tree , x , y) , 8)
        except:
            tree.MSE = 1000000000

    population_befor.clear()
    population_after.sort()
    population_befor=population_after[:number_population_trees]
    population_after.clear()
    population_after=population_befor[:number_population_trees]
    
    if best_MSE > population_befor[0].MSE:
        best_tree = population_befor[0]
        best_MSE = population_befor[0].MSE
        best_gen = generation
    if population_befor[0].MSE < 1:
        break

# print("\n\n\nbest function")
# print(print_tree(population_befor[0]))
# print("MSE = "+str(population_befor[0].MSE))
# print("\n")
# print("Best tree")
# print(print_tree(best_tree))
# print("Best mse = "+str(best_MSE))
# print("Best generation = "+str(best_gen+1))

population_befor.reverse()
for i in range(len(population_befor)):
    print(print_tree(population_befor[i]))
    print("MSE = "+str(population_befor[i].MSE))
print("\n")
print("Best tree")
print(print_tree(best_tree))
print("Best mse = "+str(best_MSE))
print("Best generation = "+str(best_gen+1))