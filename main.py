import turtle
import matplotlib.pyplot as plt
import numpy as np

print("""
                                                                                  $$\           
                                                                                  $$ |          
 $$$$$$\   $$$$$$$\  $$$$$$\  $$$$$$$\   $$$$$$\  $$$$$$\$$$$\   $$$$$$$\$$$$$$\  $$ | $$$$$$$\ 
$$  __$$\ $$  _____|$$  __$$\ $$  __$$\ $$  __$$\ $$  _$$  _$$\ $$  _____\____$$\ $$ |$$  _____|
$$$$$$$$ |$$ /      $$ /  $$ |$$ |  $$ |$$ /  $$ |$$ / $$ / $$ |$$ /     $$$$$$$ |$$ |$$ /      
$$   ____|$$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ | $$ | $$ |$$ |    $$  __$$ |$$ |$$ |      
\$$$$$$$\ \$$$$$$$\ \$$$$$$  |$$ |  $$ |\$$$$$$  |$$ | $$ | $$ |\$$$$$$$\$$$$$$$ |$$ |\$$$$$$$\ 
 \_______| \_______| \______/ \__|  \__| \______/ \__| \__| \__| \_______\_______|\__| \_______|
\n
""")

while True:
    money = float(input("\nHow much money do you have?\n"))
    command = input("\nWhat do you want to do?\n")
    time = np.arange(0, 10.1, 0.1)
    
    if(command == "help"):
        print("commands includes add,subtract,divide,multiply,invest,exit,decay,compound,continuous")
    
    elif(command == "add"):
        value = float(input("\nHow much?\n"))
        money += value

        print(f"${round(money, 2)}")

    elif(command == "subtract"):
        value = float(input("\nHow much?\n"))
        
        money -= value
        print(f"${round(money, 2)}")

    elif(command == "multiply"):
        value = float(input("\nHow much?\n"))
        
        money *= value  
        print(f"${round(money, 2)}")
        
    elif(command == "divide"):
        value = float(input("\nHow much?\n"))
        if value == 0:
            print("err: cannot divide by 0\n")
        else:
            money /= value
            print(f"${round(money, 2)}")
    
    elif(command == "compound"):
        rate = float(input("\nWhat is your annual compounded interest rate?\n"))
        periods = int(input("\nHow many times is your interest compounded in a year?\n"))
        years = int(input("\nFor how many years?\n"))
        time = np.arange(0, years + 1/periods, 1/periods)
        growth = money * np.pow((1 + rate / periods), (time * periods))
        plt.plot(time, growth)
        plt.show()

    elif(command == "invest"):
        rate = float(input("\nWhat is the annual investment rate?\n"))
        growth = money * np.power(1 + rate, time)
        plt.plot(time, growth)
        plt.show()

    elif(command == "decay"):
        rate = float(input("\nWhat is the annual decay rate?\n"))
        growth = money * np.power(1 + rate, -time)
        plt.plot(time, growth)
        plt.show()
    
    #work on continuous interest
    elif(command == "continuous"):
        rate = float(input("\nWhat is your compound interest rate?\n"))
        year = int(input("\nFor how much time? (y)\n"))
        growth = money * pow(numpy.e, (rate * year))
        plt.plot(time, growth)
        plt.show()

    elif(command == "exit"):
        break
    
    else:
        print('err: invalid')
    print('----------------------------------------------------------------------')
