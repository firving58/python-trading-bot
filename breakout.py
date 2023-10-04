# this is the 'main' program
import time
import pyautogui as pag
#from PIL import ImageGrab  # needed if using multi monitor
#from functools import partial  # needed for multi monitor
import MetaTrader5 as mt5


from nasdaq_logic import NASUSD
# add them as you use them
#from xauusd_logic import XAUUSD


# checks to see if there is an order against trading pair 'NASUSD.HKT'
# and if there is, returns how many orders are open
# this is using Hankotrade for testing, which is why the pair ends in .HKT
def checkNASDAQ():
    # establish MetaTrader 5 connection to a specified trading account
    if not mt5.initialize(login='your account  ID here', server="Hankotrade-Demo",password="enter your password here"):
        print("initialize() failed, error code =",mt5.last_error())
        #quit()
        return
    account_info=mt5.account_info()
    if account_info!=None:
        # get open positions on NASDAQ
        positions=mt5.positions_get(symbol="NASUSD.HKT")
        if positions==None:
            return "No positions on nasusd, error code={}".format(mt5.last_error())
        elif len(positions)>0:
            NASDAQPre = len(positions)
            NASDAQ = int(NASDAQPre)
            return NASDAQ          

xm = 1
while xm > 0:
    # check to see if there is an open position, if there is; skip
    # if no open positions go to the logic file
    getNASDAQpos = checkNASDAQ()
    if getNASDAQpos != 1:   # max of 1 order open at a time, if you want more then 1 change it to 2,3,4 etc
        NASUSD()
    else:
        print(getNASDAQpos, ' open order found')
    time.sleep(65) # this is your pause cycle. on a 1 minute chart, checking just 1 pair, i check it about every minute. the width of your scanning area # 
    # in the 'grid' of the nasdaq_logic.py file determines how far back you are checking. 
    # if you have a wide x coord check (like 30px), check about every 1.5 minutes
    # if you are checking 3 different pairs, divide this number by 3
    #
    #
    # just add in more as you use them
    #getXAUUSDpos = checkXAUUSD()
    #if getXAUUSDpos != 1:
        #XAUUSD()
    #else:
        #print(getXAUUSDpos, ' open order found')
    #time.sleep(35)
    
   
    

    
    
