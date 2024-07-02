import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import statistics

"""
0 = no Roll
1 = Crit Rate
2 = Crit Dmg
3 = Atk%
4 = Flat Atk
5 = ER
6 = Basic Atk
7 = Heavy Atk
8 = Skill
9 = Ult
10 = Flat Hp
11 = Hp%
12 = Flat Def
13 = Def%
"""


number_of_cycles = 10000


must_have_substats = [1,2,3]
great_substats = [5, 8]
bad_substats = [10,11,12,13]
max_bad_stats = 0



class Echo:
    
    def __init__(self):
        self.substats = [0,0,0,0,0]
        self.number_of_must = 0
        self.number_of_great = 0
        self.number_of_good = 0
        self.bad_stats = max_bad_stats
    
    
class Single_cycle:
        
    def __init__(self):
        
        self.echos = [Echo()]
        self.exp_needed = 0
        self.tuner_needed = 0
        self.golden_goose = 0
        self.great_echos = 0
        self.good_echos = 0
    
    
class Total_cycles:
    
    exp_list = []
    tuner_list = []
    echos_until_GG = []
    total_great = []
    total_good = []
    cycle = [Single_cycle() for i in range(number_of_cycles)]
    
    
def roll_substat(echo: Echo):
    x = random.randint(1,13)
    while x in echo.substats:
        x = random.randint(1,13)
    return x
    

def get_exp_used(i):
    if i == 0:
        exp = 4400
    elif i == 1:
        exp = 16500
    elif i == 2:
        exp = 39600
    elif i == 3:
        exp = 79100
    elif i == 4:
        exp = 142600    
    else :
        exp = 0    
    return exp
    
    
total = Total_cycles()

for this_cycle in total.cycle:
    for echo in this_cycle.echos:
        
        i=0
        for substat in echo.substats:
            
            x = roll_substat(echo)
            echo.substats[i] = x
            
            if x in must_have_substats:
                echo.number_of_must += 1
            elif x in great_substats:
                echo.number_of_great += 1
            elif x not in bad_substats:    
                echo.number_of_good += 1
            elif x in bad_substats and echo.bad_stats > 0:
                echo.bad_stats -= 1
            else :
                this_cycle.tuner_needed += (i+1)*10*0.7
                this_cycle.exp_needed += get_exp_used(i)*0.25
                break
            
            
            
            if i == 4 :
                if  len(must_have_substats) == echo.number_of_must and 5 - echo.number_of_must - echo.number_of_great - max_bad_stats <= 0:
                    this_cycle.golden_goose = 1
                    this_cycle.tuner_needed += 50
                    this_cycle.exp_needed += get_exp_used(i)
                    
                    break
                elif  len(must_have_substats) == echo.number_of_must and echo.number_of_great > 0:
                    this_cycle.great_echos += 1
                    this_cycle.tuner_needed += 50
                    this_cycle.exp_needed += get_exp_used(i)
                    break
                elif  len(must_have_substats) == echo.number_of_must and echo.number_of_good > 0:
                    this_cycle.good_echos += 1
                    this_cycle.tuner_needed += 50
                    this_cycle.exp_needed += get_exp_used(i)
                    break
                
            if 5 - (i+1) < len(must_have_substats) - echo.number_of_must:
                this_cycle.tuner_needed += (i+1)*10*0.7
                this_cycle.exp_needed += get_exp_used(i)*0.25
                break    
            i += 1
            
            
        if this_cycle.golden_goose == 1:
            break            
        else:    
            this_cycle.echos.append(Echo())
            
    total.echos_until_GG.append(len(this_cycle.echos))   
    total.total_great.append(this_cycle.great_echos)             
    total.total_good.append(this_cycle.good_echos)  
    total.tuner_list.append(this_cycle.tuner_needed)
    total.exp_list.append(this_cycle.exp_needed)                   
    
   


plt.hist(total.echos_until_GG, weights=np.ones(len(total.echos_until_GG)) / len(total.echos_until_GG), bins=30, edgecolor="black")
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()

aver_GG = statistics.fmean(total.echos_until_GG)
aver_great = statistics.fmean(total.total_great)
aver_good = statistics.fmean(total.total_good)
aver_tuner = statistics.fmean(total.tuner_list)
aver_exp = statistics.fmean(total.exp_list)

print("Average to GG: " + str(aver_GG) + " Higest: " + str(max(total.echos_until_GG)))
print("Average Great: " + str(aver_great))
print("Average Good: " + str(aver_good))
print("Average Tuner: " + str(aver_tuner) + " / " + str(aver_tuner/80) + " Days (" +  str(aver_tuner/120)+ ")")
print("Average Exp: " + str(aver_exp) + " / " + str(aver_exp/88000) + " Days")