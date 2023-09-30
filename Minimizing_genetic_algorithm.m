tic
clc; 
clear;   

n = 4; 
d = 5; 
dX = [-5.12, 5.12]; 
rX = range(dX); 
nBit = ceil (log2 (rX*10^n));   

popSize = 50; 
pc = 0.25; 
pm = 0.01; 
maxG = 1000;   

bestF = inf; 
Pop = randi ([0,1],popSize,nBit*d); 

for g = 1 : maxG          
    for s = 1 : d         
        Dec(:,s) = bi2de (Pop(:,(s-1)*nBit+1:(s-1)*nBit+nBit));     
    end
    
    X = min(dX) + Dec * rX /(2^nBit-1);          
    F = F2(X);          
    [M,I] = min(F);          
    if M < bestF         
        bestF = M;         
        Xbest = X(I,:);        
        bestG = g;     
    end
    
    FI = (max(F) + min(F))-F;     
    P = FI / sum(FI);     
    Q = cumsum (P);           
    
    I =[];     
    for c = 1 : popSize         
        I(c) = min (find(Q>rand));     
    end
    
    Pop = Pop(I,:);
% Crossover           
    R = rand (1,popSize);     
    I = find (R<=pc);     
    L = length (I);          
    
    if bitget (L,1)==1         
        I(L+1) = I(randi([1,L],1));         
        L = L+1;     
    end
    
    for c = 1 : 2 : L                          
        
        V1 = Pop(I(c),:);         
        V2 = Pop(I(c+1),:);                  
        
        Mask = randi ([0,1],1,nBit*d);         
        T = find (Mask==1);                  
        
        [V1(T),V2(T)] = deal (V2(T),V1(T));                   
        
        Pop(I(c),:) = V1;         
        Pop(I(c+1),:) = V2;                        
        
        % Pop(I(c),:) = Mask.*V1+(1-Mask).*V2;          
        % Pop(I(c+1),:) = Mask.*V2+(1-Mask).*V1]; 
    end 
    
% Mutation       
    R = rand (popSize,nBit*d);     
    I = find (R<=pm);     
    Pop(I) = not(Pop(I));      
end 
disp ('The best Fitness is :'); 
disp (bestF); disp ('The best X is :'); 
disp (Xbest); disp ('The best answer is found in Generation # :'); 
disp (bestG); 
toc 
function[Out] = F1(X)
T1 = -20*exp(-0.2*(sqrt(sum(X.^2,2)*1./size(X,2)))); 
T2 = exp(sum(cos(X*2*pi),2)*1./size(X,2)); 
Out = T1-T2+20+exp(1);
end
function [Out] = F2(X)
T1 = X.^2; T2 = -10*cos(2*pi*X)+10; 
Out = sum(T1+T2,2);
end
function [Out] = F3(X)
T1 = 1/4000*sum(X.^2,2); 
I = 1:1:size(X,2); 
T2 = -prod(cos (X./repmat(sqrt(I),size(X,1),1)),2)+1; 
Out = T1+T2; 
end
function [Out] = F4(X)
Out = sum(cumsum(X,2).^2,2); 
end