import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt # https://docs.python.org/3/library/datetime.html
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

money = 0
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

def showHist():
    if not calcHist:
        print("\nNo history.\n")
        return

    print("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    for i, histEntry in enumerate(calcHist, 1):
        print(f"{i}. {histEntry['timestamp']} - {histEntry['op']}")
        print(f"  init: ${histEntry['initial_value']}")
        print(f"  param: ${histEntry['parameters']}")
        print(f"  result: ${histEntry['result']}\n")

def exportHistToCSV(filename="calc_history.csv"):
    if not calcHist:
        print("\nNo history to export.\n")
        return
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'operation', 'initial_value', 'parameters', 'result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in calcHist:
            writer.writerow({
                'timestamp': entry['timestamp'],
                'operation': entry['op'],
                'initial_value': entry['initial_value'],
                'parameters': str(entry['parameters']),
                'result': entry['result']
            })
    print(f"\nHistory exported to {filename}\n")

def importHistFromCSV(filename="calc_history.csv"):
    global calcHist
    global money
    if not os.path.exists(filename):
        print(f"\nFile {filename} not found.\n")
        return
    
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            imported_hist = []
            
            for row in reader:
                # Convert parameters string back to dict
                try:
                    parameters = eval(row['parameters'])
                except:
                    parameters = {}
                
                entry = {
                    'timestamp': row['timestamp'],
                    'op': row['operation'],
                    'initial_value': float(row['initial_value']),
                    'parameters': parameters,
                    'result': row['result']
                }
                money = float(row['result'])
                imported_hist.append(entry)
            
            calcHist.extend(imported_hist)
            print(f"\nImported {len(imported_hist)} history entries from {filename}\n")
    
    except Exception as e:
        print(f"\nError importing CSV: {e}\n")

money = float(input("\nHow much money do you have?\n"))

while True:
    command = input("\nWhat do you want to do?\n").lower()
    time = np.arange(0, 10.1, 0.1)
    initial_money = money

    if(command == "help"):
        print("All commands: add, subtract, multiply, divide, interest, decay, compound, continuous, break-even, new, showhist, export, import, recent, exit")

    elif(command == "add"):
        value = float(input("\nHow much?\n"))
        money += value

        addHist("add", initial_money, {"added": value}, money)
        print(f"${round(money, 2)}")

    elif(command == "subtract"):
        value = float(input("\nHow much?\n"))

        money -= value
        addHist("subtract", initial_money, {"subtracted": value}, money)
        print(f"${round(money, 2)}")

    elif(command == "multiply"):
        value = float(input("\nHow much?\n"))

        money *= value  
        addHist("multiply", initial_money, {"multiplied by": value}, money)
        print(f"${round(money, 2)}")

    elif(command == "divide"):
        value = float(input("\nHow much?\n"))
        if value == 0:
            print("err: cannot divide by 0\n")
        else:
            money /= value
            addHist("divide", initial_money, {"divided by": value}, money)
            print(f"${round(money, 2)}")

    elif(command == "compound"):
        rate = float(input("\nWhat is your annual compounded interest rate?\n"))
        periods = int(input("\nHow many times is your interest compounded in a year?\n"))
        years = int(input("\nFor how many years?\n"))
        time = np.arange(0, years + 1/periods, 1/periods)
        growth = money * np.power((1 + rate / periods), (time * periods))
        money = round(money * np.power(1 + rate / periods, time[-1] * periods), 2)
        print(f"${money}")
        addHist("compound:", initial_money, {
            "rate": rate, "periods:": periods, "years": years
        }, money)
        plt.plot(time, growth)
        plt.show()

    elif(command == "interest"):
        rate = float(input("\nWhat is the annual interest rate?\n"))
        years = int(input("\nFor how many years?\n"))
        time = np.arange(0, years + 0.1, 0.1)
        growth = money * np.power(1 + rate, time)
        money = round(money * np.power((1 + rate), time[-1]), 2)
        print(f"${money}")
        addHist("interest", initial_money, {"rate": rate, "years": years}, money)
        plt.plot(time, growth)
        plt.show()

    elif(command == "decay"):
        rate = float(input("\nWhat is the annual decay rate?\n"))
        years = int(input("\nFor how many years?"))
        time = np.arange(0, years + 0.1, 0.1)
        decay = money * np.power(1 - rate, time)
        money = round(money * np.power((1 - rate), time[-1]), 2)
        print(f"${money}")
        addHist("decay", initial_money, {"rate": rate, "years": years}, money)
        plt.plot(time, decay)
        plt.show()

    elif(command == "continuous"):
        rate = float(input("\nWhat is your annual continuous interest rate?\n"))
        years = int(input("\nFor how many years?\n"))
        time = np.arange(0, years + 0.1, 0.1)
        growth = money * np.exp(rate * time)
        money = round(money * np.exp(rate * time[-1]), 2)
        print(f"${money}")
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
        addHist("new money value", initial_money, {"changed to": money}, money)

    elif(command == "showhist"):
        showHist()

    elif(command == "export"):
        filename = input("\nEnter filename (or press Enter for 'calc_history.csv'): ").strip()
        if not filename:
            filename = "calc_history.csv"
        exportHistToCSV(filename)

    elif(command == "import"):
        filename = input("\nEnter filename to import (or press Enter for 'calc_history.csv'): ").strip()
        if not filename:
            filename = "calc_history.csv"
        importHistFromCSV(filename)
    
    elif(command == "exit"):
        addHist("exit", money, {}, "Session ended")
        break

    else:
        print('err: invalid')

    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    
