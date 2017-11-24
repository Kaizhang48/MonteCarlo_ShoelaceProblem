# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import random
from pandas import DataFrame
import matplotlib.pyplot as plt

class End:
    def __init__(self,rowindex=np.nan,p=np.nan,sd=np.nan,chsrange=np.nan):
        self.owner=rowindex
        self.prob=p
        self.side=sd
        self.to_be_chosen=chsrange
        self.choose=0
        
class Shoelace:
    def __init__(self,slindex,p,l):
        self.index=slindex
        self.r_end=End(slindex,p,'right',np.nan)
        self.l_end=End(slindex,p,'left',np.nan)
        self.length=l
        self.component=[slindex]
        
class Box:
    def __init__(self,numofsl,l):
        self.content=list(range(numofsl))
        self.contentofindex=list(range(numofsl))
        self.loopcontent=[]
        for i in range(numofsl):
            self.content[i]=Shoelace(i,np.nan,l)
            self.contentofindex[i]=i
        
        self.numofloop=0
        self.numofshoelace=numofsl
        
    def get_shoelace_pos(self,idx):
        return self.contentofindex.index(idx)
        
    def remove_sl(self,idx):
        pos=self.get_shoelace_pos(idx)
        del self.content[pos]
        del self.contentofindex[pos]
        self.numofshoelace-=1
           
    def update_numofloop(self):
        self.numofloop=len(self.loopcontent)
        
    def update_numofshoelace(self):
        self.numofshoelace=len(self.content)
        
    def end2shoelace(self,end):
        pos=self.get_shoelace_pos(end.owner)
        return self.content[pos]


def sum_f(box,f):
    output2=0.0
    for shoelace in box.content:
        if shoelace.r_end.choose==0:
            output2+=f(shoelace.length)
        if shoelace.l_end.choose==0:
            output2+=f(shoelace.length)
    return output2
            
def impose_prob (box,f):
    F=sum_f(box,f)
    end_index=0.0
    for i in range(len(box.content)):
        shoelace=box.content[i]
        if shoelace.r_end.choose==0:
            p=f(shoelace.length)/F
            shoelace.r_end.prob=p
            shoelace.r_end.to_be_chosen=[end_index,end_index+p]
            end_index+=p
        else:
            shoelace.r_end.prob=np.nan
            shoelace.r_end.to_be_chosen=[0,0]
            
        if shoelace.l_end.choose==0:
            p=f(shoelace.length)/F
            shoelace.l_end.prob=p
            shoelace.l_end.to_be_chosen=[end_index,end_index+p]
            end_index+=p
        else:
            shoelace.l_end.prob=np.nan
            shoelace.l_end.to_be_chosen=[0,0]
        
def choose_or_not(rnd,end):
    if end.choose==0:
        if rnd>end.to_be_chosen[0] and rnd<=end.to_be_chosen[1]:
            return 1
        else:
            return 0
    else:
        return 0
    
def grab(box):
    rnd=random.random()
    for shoelace in box.content:
        if choose_or_not(rnd,shoelace.r_end):
            shoelace.r_end.choose=1
            return shoelace.r_end
        elif choose_or_not(rnd,shoelace.l_end):
            shoelace.l_end.choose=1
            return shoelace.l_end

def standard_answer(n):
    num=0.0
    for i in range(1,2*n,2):
        num+=1.0/i
    return num
    
def print_shoelace_info(shoelace):
    print ('The index of this shoelace is: ', shoelace.index)
    print ('the length of this shoelace is: ',shoelace.length)
    print ('components of this shoelace is: ',shoelace.component)
    print ('the info of its right end is below:')
    print ('choose or not: ', shoelace.r_end.choose)
    print ('the probability of of this end to be chosen is: ', shoelace.r_end.prob)
    print ('the range of this ned to be chosen is: ', shoelace.r_end.to_be_chosen)
    print ('the info of its left end is below:')
    print ('choose or not: ', shoelace.l_end.choose)
    print ('the probability of of this end to be chosen is: ', shoelace.l_end.prob)
    print ('the range of this end to be chosen is: ', shoelace.l_end.to_be_chosen)
    print ('= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ')

def print_end_info(end):
    print ('this end is the',end.side,' of shoelace ',end.owner)
    print ('the probability to choose it is: ',end.prob)
    print ('the range of this end to be chosen is: ',end.to_be_chosen)
def print_box_info(box):
    print ('this box has ',box.numofshoelace,' shoelaces')
    print ('so far it has', box.numofloop,' loops and they are')
    print (box.loopcontent)
    print ("Every shoelaces' info is below: ")
    for shoelace in box.content:
        print_shoelace_info (shoelace)
    print ('============================================================================')

def newgame(numofshoelace,length,prob_function,f):
    box=Box(numofshoelace,length)
    prob_function(box,f)
    while box.numofshoelace>1:
        grab_end1=grab(box)
#         print_end_info(grab_end1)
        prob_function(box,f)
#         print ('grab2 start')
        grab_end2=grab(box)
#         print_end_info(grab_end2)
#         print_box_info(box)
#         print ('___________________________________________________________')
        if grab_end1.owner==grab_end2.owner:
#             print (grab_end1.owner,' and ',grab_end1.owner,'form a loop!')
            s1=box.end2shoelace(grab_end1)
            s2=box.end2shoelace(grab_end2)
            if s1.component!=s2.component:
                s1.component.extend(s2.component)
            box.loopcontent.append(s1.component)
            box.update_numofloop()
            box.remove_sl(grab_end1.owner)
            prob_function(box,f)
#             print_box_info(box)
        else :
#             print ('no loop!')
#             print (grab_end1.owner,' and ',grab_end2.owner,'form a line!')
            s1=box.end2shoelace(grab_end1)
            s2=box.end2shoelace(grab_end2)
            s1.component.extend(s2.component)
            s1.length+=s2.length
            box.remove_sl(s2.index)
            s1.r_end.choose=0
            s1.l_end.choose=0
            prob_function(box,f)
#             print_box_info(box)
    if box.numofshoelace==1:
#         print ('finally')
        box.loopcontent.append(box.content[0].component)
        box.update_numofloop()
        box.remove_sl(box.content[0].index)
#         print_box_info(box)
    return box.numofloop

def f(x):
    return x

def f1(x):
    return x**2

def f2(x):
    return 1

def f3(x):
    return np.power(2.0,x)

def newsimulation (box_cap,length,times,prob_function,f):
    num=0.0
    for i in range(times):
        num+=newgame(box_cap,length,prob_function,f)
    sim_answer=num/times
    return sim_answer
#=========================================================================================
if __name__=='__main__':
    sim=[0,1]
    sim1=[0,1]
    sim2=[0,1]
    sim3=[0,1]
    std=[0,1]
    times=100000
    length=1.0
    maximum=10
    for i in range(2,maximum+1):
        output=newsimulation (i,length,times,impose_prob,f)
        output1=newsimulation (i,length,times,impose_prob,f1)
        output2=newsimulation (i,length,times,impose_prob,f2)
        output3=newsimulation (i,length,times,impose_prob,f3)
        sim.append(output)
        sim1.append(output1)
        sim2.append(output2)
        sim3.append(output3)
        std.append(standard_answer(i))
    x_range=[0,1]
    x_range.extend(range(2,maximum+1))
    result=DataFrame([sim,sim1,std,sim2,sim3],columns=x_range,index=['f(x)=x','f(x)=x^2','f(x)=1 solution','f(x)=1 simulation','f(x)=2^x'])
    result.T.plot(style={'f(x)=x':'-','f(x)=x^2':'-','f(x)=1 solution': '--','f(x)=1 simulation':'-','f(x)=2^x':'-'},figsize=(10,7.5))
    plt.show()
