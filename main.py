import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt # https://docs.python.org/3/library/datetime.html
import json
import os
import csv

print("""
                                                                                  $$\           
                                                                                  $$ |          
 $$$$$$\   $$$$$$$\  $$$$$$\  $$$$$$$\   $$$$$$\  $$$$$$\$$$$\   $$$$$$$\$$$$$$\  $$ | $$$$$$$\ 
$$  __$$\ $$  _____|$$  __$$\ $$  __$$\ $$  __$$\ $$  _$$  _$$\ $$  _____\____$$\ $$ |$$  _____|
$$$$$$$$ |$$ /      $$ /  $$ |$$ |  $$ |$$ /  $$ |$$ / $$ / $$ |$$ /     $$$$$$$ |$$ |$$ /      
$$   ____|$$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ | $$ | $$ |$$ |    $$  __$$ |$$ |$$ |      
\$$$$$$$\ \$$$$$$$\ \$$$$$$  |$$ |  $$ |\$$$$$$  |$$ | $$ | $$ |\$$$$$$$\$$$$$$$ |$$ |\$$$$$$$\ 
 \_______| \_______| \______/ \__|  \__| \______/ \__| \__| \__| \_______\_______|\__| \_______|
""")

calcHist = []
sessionFilepath = ""
historyFilepath = ""

def addHist(op, initial_value, parameters, result):
    histEntry = {
        "timestamp": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        "op": op,
        "initial_value": initial_value,
        "parameters": parameters,
        "result": result
    }
    calcHist.append(histEntry)

def saveSesh(money):
    session_data = {
        "money": money,
        "history": calcHist,
        "timestamp": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open("file.txt", "w") as f:
        f.write("Created using write mode.")

def showHist():
    if not calcHist:
        print("\nNo history.\n")
        return
    
    print("\n-----------------------")
    for i, histEntry in enumerate(calcHist, 1):
        print(f"{i}. {histEntry['timestamp']} - {histEntry['op']}")
        print(f"  init: ${histEntry['initial_value']}")
        print(f"  param: ${histEntry['parameters']}")
        print(f"  result: ${histEntry['result']}\n")

money = float(input("\nHow much money do you have?\n"))

while True:
    command = input("\nWhat do you want to do?\n").lower()
    time = np.arange(0, 10.1, 0.1)
    initial_money = money
    
    if(command == "help"):
        print("All commands: add, subtract, multiply, divide, interest, decay, compound, continuous, break-even, new, exit")
    
    elif(command == "add"):
        value = float(input("\nHow much?\n"))
        money += value

        addHist("add", initial_money, {"added: value"}, money)
        print(f"${round(money, 2)}")

    elif(command == "subtract"):
        value = float(input("\nHow much?\n"))
        
        money -= value
        addHist("sub", initial_money, {"sub: value", money})
        print(f"${round(money, 2)}")

    elif(command == "multiply"):
        value = float(input("\nHow much?\n"))
        
        money *= value  
        addHist(initial_money, {"multiplied by": value}, money)
        print(f"${round(money, 2)}")
        
    elif(command == "divide"):
        value = float(input("\nHow much?\n"))
        if value == 0:
            print("err: cannot divide by 0\n")
        else:
            money /= value
            addHist(initial_money, {"divided by:": value}, money)
            print(f"${round(money, 2)}")
    
    elif(command == "compound"):
        rate = float(input("\nWhat is your annual compounded interest rate?\n"))
        periods = int(input("\nHow many times is your interest compounded in a year?\n"))
        years = int(input("\nFor how many years?\n"))
        time = np.arange(0, years + 1/periods, 1/periods)
        growth = money * np.power((1 + rate / periods), (time * periods))
        print(f"${round(money * np.power(1 + rate / periods, time[-1] * periods), 2)}")
        addHist("compound")
        plt.plot(time, growth)
        plt.show()

    elif(command == "interest"):
        rate = float(input("\nWhat is the annual interest rate?\n"))
        growth = money * np.power(1 + rate, time)
        print(f"${round(money * np.power((1 + rate), time[-1]), 2)}")
        plt.plot(time, growth)
        plt.show()

    elif(command == "decay"):
        rate = float(input("\nWhat is the annual decay rate?\n"))
        growth = money * np.power(1 + rate, -time)
        print(f"${round(money * np.power((1 + rate), -time[-1]), 2)}")
        plt.plot(time, growth)
        plt.show()
    
    elif(command == "continuous"):
        rate = float(input("\nWhat is your annual continuous interest rate?\n"))
        years = int(input("\nFor how many years?\n"))
        time = np.arange(0, years + 0.1, 0.1)
        growth = money * np.exp(rate * time)
        print(f"${round(money * np.exp(rate * time[-1]), 2)}")
        plt.plot(time, growth)
        plt.show()

    elif(command == "break-even"):
        money2 = float(input("\nWhat is the starting value of the second slope?\n"))
        rate1 = float(input("\nWhat is the rate of the first slope?\n"))
        rate2 = float(input("\nWhat is the rate of the second slope?\n"))
        
        if(rate2 == rate1):
            print('None')
            
        else:
            equation1 = money + rate1 * time
            equation2 = money2 + rate2 * time
            point = (money - money2)/(rate2 - rate1)
            print(str(round(point, 2)) + ", " + str(round(point * rate1), 2))
            plt.plot(time, equation1)
            plt.plot(time, equation2)
            plt.show()
    
    elif(command == "new"):
        money = float(input("\nHow much money do you have?\n"))
        addHist("new", initial_money, {"changed: value"}, money)

    elif(command == "exit"):
        addHist("exited.")
        break
    
    else:
        print('err: invalid')
    
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
