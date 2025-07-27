from ModelCaching import *
from PreProcess import * 


stock_symbols = {
#LargeCap
'HCL TECH': "HCLTECH.NS" ,
'INFOSYS': "INFY.NS",
'TCS': "TCS.NS",
'WIPRO': "WIPRO.NS",
'Tech Mahindra': "TECHM.NS",
'LTIMindtree': "LTIM.NS",
#MidCap
"Persistent Systems":"PERSISTENT.NS",
"Oracle Financial Services":"OFSS.NS",
"Policy Bazar":"POLICYBZR.NS",
#Small Cap
"Sasken Tech":"SASKEN.NS",
"Quick Heal":"QUICKHEAL.NS",
"Birlasoft":"BSOFT.NS"
}

def StockSelection():
    for key in stock_symbols:
        print(f"{key}","\n")
    print('\n')

def Menu():
    print("\n"*5)
    print("*********")
    print("1. Select Stock")
    print("2. Predict the stock's Closing Price...")
    print("3. Exit")
def NormalMode():
    choice=0
    symbol=''
    while choice!=3:
        Menu()
        choice=int(input("Enter your Choice: "))
        if choice==1:
            StockSelection()
            s=input("Enter Stock Name: ")
            symbol=stock_symbols[s]
        elif choice==2 and symbol!='':
            print("predicted close price: $",Predict_StockPrice(symbol))
        elif choice==3:
            print("Thankyou for using our product!")
        else:
            print("Invalid choice")
def ObservationMode():
    k=1
    for key in stock_symbols:
        print("\n\n\n\n\n\n\n\n",f"{k}.  Prediction for {key}")
        Predict_StockPrice(stock_symbols[key])
        k+=1
    print("********************************")
    print("Done")
    print("********************************")
ObservationMode()
# NormalMode()



