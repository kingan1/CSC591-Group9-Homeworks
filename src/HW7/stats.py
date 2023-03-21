import math
import random

def RX(t,s) :
    t = sorted(t)
    return {"name":s or "", 
            "rank":0, 
            "n":len(t), 
            "show":"", 
            "has":t} 

def mid(t):
    t= t.get("has", t)
    n = len(t)//2
    return (t[n] +t[n+1])/2 if len(t)%2==0 else t[n+1]

def div(t):
    t= t.get("has", t)
    return (t[ len(t)*9//10 ] - t[ len(t)*1//10 ])/2.56

def merge(rx1,rx2) :
    rx3 = RX([], rx1['name'])
    for _,t in enumerate([rx1['has'],rx2['has']]):
        for _,x in enumerate(t): 
            rx3['has'].append(x)
    rx3['has'] = sorted(rx3['has'])
    rx3['n'] = len(rx3['has'])
    return rx3

def samples(t,n=0):
    u= []
    n = n or len(t)
    for i in range(n): 
        u.append(t[random.randrange(len(t))]) 
    return u

def gaussian(mu,sd): #  #--> n; return a sample from a Gaussian with mean `mu` and sd `sd`
    mu,sd = mu or 0, sd or 1
    sq,pi,log,cos,r = math.sqrt,math.pi,math.log,math.cos,random.random
    return  mu + sd * sq(-2*log(r())) * cos(2*pi*r())