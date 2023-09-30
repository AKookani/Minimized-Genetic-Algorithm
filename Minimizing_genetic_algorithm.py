"""
Created on Wed Jun 16 19:03:45 2021

@author: ali
"""
import numpy as np

def F1(X):
    T1 = (-20 * np.exp(-0.2 * (np.sqrt(np.sum(X**2,1) * 1./(np.size(X,1))))))
    T2 = np.exp(np.sum(np.cos(X*2*(np.pi)),1)*1./(np.size(X,1)))
    Out = T1-T2+20+(np.exp(1))
    return Out
def F2(X):
    T1 = X**2 
    T2 = -10 * np.cos(2 * (np.pi) * X) + 10
    Out = np.sum(T1 + T2, 1)
    return Out

n = 4
d = 5
dX = [-5.12, 5.12]
rX = max(dX) - min(dX)
nBit = (np.ceil (np.log2 (rX * 10**n))).astype(int)

popSize = 50 
pc = 0.25 
pm = 0.01
maxG = 1000   

bestF = np.inf
Pop = np.random.randint(2, size=(popSize, nBit * d))

Dec = np.zeros((popSize, d))
Dec_t = np.zeros((16,))

def bi2de(binary):
    output = 0
    for j in range(len(binary)):
        output += binary[(len(binary))-j-1,] * (2 ** j)
    return output

for g in range(maxG):
    for s in range(d):
        for i in range(popSize):
            Dec_t = Pop[i, (s - 1) * nBit + 1 : (s - 1) * nBit + nBit]
            Dec[i, s] = bi2de(Dec_t)
    
    X = min(dX) + Dec * rX / ((2 ** nBit) - 1)
    F = F2(X)
    M = min(F)
    I = np.where(F == M)
    if M < bestF:        
        bestF = M
        Xbest = X[I[0], :]
        bestG = g

    FI = (max(F) + min(F))-F
    P = FI / np.sum(FI)
    Q = np.cumsum (P)

    I = np.zeros(popSize, dtype=int)
    for c in range(popSize):
        I[c] = np.amin(np.where(Q>((np.random.randint(0, 1000))/1000)))

    Pop = Pop[I,:]
#Crossover           
    R = np.random.random(popSize)
    I = np.where(R <= pc)
    I = I[0]
    L = np.array(len(I), dtype=np.uint8)
    
    bitget = np.unpackbits(L)
    if bitget[len(bitget) - 1] == 1:
        I = np.append(I, np.random.randint(1, L, 1), axis=0)
        L = L + 1
        
    for c in range(1, 2, L):
        
        V1 = Pop[I[c],:]
        tempV1 = Pop[I[c],:]
        V2 = Pop[I[c+1],:]
        tempV2 = Pop[I[c+1],:]
        
        Mask = np.random.randint(2, size=(nBit*d))
        T = np.where(Mask==1)
        
        tempV1[T[0]] = V2[T[0]]
        tempV2[T[0]] = V1[T[0]]  
        V1[T[0]] = tempV2[T[0]]
        V2[T[0]] = tempV1[T[0]]  
        del tempV1
        del tempV2
        
        Pop[I[c],:] = V1        
        Pop[I[c+1],:] = V2       
        
        #Pop(I(c),:) = Mask.*V1+(1-Mask).*V2          
        #Pop(I(c+1),:) = Mask.*V2+(1-Mask).*V1
        
#Mutation       
    R = np.random.random([popSize, nBit*d])
    I = np.where(R<=pm)
    for ij in range(len(I[1])):
        for ji in range(len(I[0])):
            Pop[I[0][ji],I[1][ij]] = int(not(Pop[I[0][ji],I[1][ij]]))

print('The best Fitness is :') 
print(bestF) 
print('The best X is :')
print(Xbest)
print('The best answer is found in Generation # :')
print(bestG)