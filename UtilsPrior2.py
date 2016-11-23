def sketch(entities,matrix):
    S=len(entities)
    from graphviz import Digraph
    dot = Digraph()
    for i in range(0,len(entities)):
        dot.node(entities[i])
    for i in range(0,S):
        for j in range(0,S):
            if (matrix[i,j])==1:
                dot.edge(entities[i],entities[j])
    return dot

######################################################


def Grouping(S):
    import numpy as np
    CC=np.random.choice(range(1,S))   # Number of CCs
    Group=[]
    Groupinitial=[]
    for i in range(0,CC):
        Group.append([])
        Groupinitial.append([])


    flag=1
    while flag==1:
    
        for i in range(0,S):
            g=np.random.choice(range(0,CC))

            Group[g].append(i)
    
  
        if min([len(i) for i in Group])!=0:
            flag=0
        else:
            Groupinitial=[]
            for i in range(0,CC):
                Groupinitial.append([])
            Group=Groupinitial
    return Group

######################################################

def Distribution(Lmin,Lmax,Lambda):
    import numpy as np
    flag=0
    while flag==0:
        x=np.random.poisson(lam=Lambda)
        
        if x>=Lmin and x <= Lmax:
            flag=1
            
        if Lmax==0:
            x=0
        
    return x
######################################################      
        
def GenGraph(Nodes_CC,Lambda):
    import numpy as np
    import networkx as nx

    Lmin=min(1,len(Nodes_CC))
    Lmax=len(Nodes_CC)-1
    flag=0
    if len(Nodes_CC)==1:
        D=[0]
    
    while len(Nodes_CC)!=1 and flag==0:
    
        D=[Distribution(Lmin,Lmax,Lambda) for i in range(0,len(Nodes_CC))]
        if nx.is_valid_degree_sequence(D, method='eg') ==True:
        # eg:Erdős-Gallai      hh:  Havel-Hakimi
            flag=1
    
    return D 


    #####################################################
def GenEdges(S,Group,Lambda):
    import networkx as nx
    import random
    import numpy as np

    Dtotal=[]

    CC=len(Group)
    Edges=[]
    for i in range(0,CC):
        Nodes_CC=Group[i]
        D=GenGraph(Nodes_CC,Lambda)
        Dtotal.append(D)
        G = nx.random_degree_sequence_graph(D,  tries=100)
    
        mapping={}
        for i in range(0,len(Nodes_CC)):
            mapping[i]=Nodes_CC[i]
        H=nx.relabel_nodes(G,mapping)
        for item in H.edges():
            Edges.append(item)
        G=0

    #print(Edges)


    Adj=np.zeros([S,S])
    for i in Edges:
        j=i[0]
        k=i[1]
        if random.randint(0, 1)==0:
            Adj[j,k]=1
        else:
            Adj[k,j]=1
    
    return(Adj,Dtotal,CC)

#####################################################

def Calc_prior2(CC,Dtotal, Lambda):
    from scipy.stats import poisson
    import numpy as np
    
    eta=.5
    a=np.exp(-eta * CC)

    P=1
    for i in Dtotal:
        for j in i:
            P=P * poisson.pmf(j, mu=Lambda, loc=0)

    return (a**eta) * (P**(1-eta))   