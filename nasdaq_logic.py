import pyautogui as pag
import time
import sys
import os
from datetime import datetime
import re
from ast import literal_eval as make_tuple
import requests
from PIL import ImageGrab  # needed mostly for multiple monitors
from functools import partial
import MetaTrader5 as mt5

#ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)   # used for multi monitors

timenow = datetime.now()
timeString = str(timenow)

# colors
# this will be the dominant color of the buy or sell indicator in RGB color code
# in my case I named the sell indicator vmcRed, and the buy indicator vmcGreen
vmcRed = (255,152,0)
vmcGreen = (0,188,212)


# grids  
# the most convulted section. I needed a way to scan an area from top to bottom, column by column,
# to find a color based on the x or y coord. if your x row is small enough (5px-10px maybe) then
# it may be easier to just use a region
# example  https://pyautogui.readthedocs.io/en/latest/screenshot.html
# import pyautogui
# im = pyautogui.screenshot(region=(0,0, 300, 400))
# the below code makes a tuple out of your grid, its used to scan the grid area pixel by pixel
# so the getredgreen() function can find the buy or sell indicator based on color
tuple_list_breakout = []
a = open("grids/breakout_grid.txt", "r").readlines()
for sr in a:
    if sr != "":
        temp_breakout = make_tuple(sr)
        if len(temp_breakout) <= 4:
            tuple_list_breakout.append(temp_breakout)


# this function uses the grid file above to scan the area pixel by pixel for 
# the color of the buy or sell indicator
# in the example below, the start of the area is at pixel coords x-1473 and y-95 (top left)
# scan area is 15 pixels wide and 805 pixels deep. if your grid starts at 0,0 it scans left to right
# i start my grid at (14,804) (which is last, remember the numbers start at 0) which starts from the 
# bottom right and scans towards the top-left. this way i get the latest color available
# since the tradingview chart scrolls to the right. you'll see what I mean if you take a look

def getredgreen():
    filepath = ('img/redgreen.png') # i have a subdirectory called 'img' to store images
    if os.path.exists(filepath):
        os.remove(filepath)  # delete the file if its there so you have the latest screenshot
    else:
        print("redgreen.png doesnt exist; ignoring")
    im1 = pag.screenshot('img/redgreen.png', region=(1473, 95, 15, 805))
    for redgreenValue in tuple_list_breakout:
        colorPre = im1.getpixel(redgreenValue)
        if colorPre == vmcRed:
            return 'vmcRed'
        if colorPre == vmcGreen:
            return 'vmcGreen'

## Buy / Sell order area ##
# most of submitBuyOrder and submitSellOrder was copy/pasted from www.mql5.com/en/docs/python_metatrader5
def submitBuyOrder():
    if not mt5.initialize(login='your account id', server="Hankotrade-Demo",password="your password"):
        print("initialize() failed, error code =",mt5.last_error())
        #quit()
        return  # if it cant get your order info, like if your internet is down, just fail and return instead of killing the program
    account_info=mt5.account_info()
    symbol = "NASUSD.HKT"
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "NASUSD not found, can not call order_check()")
        mt5.shutdown()
        #quit()
        return
 
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "NASUSD is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            #quit()
            return
            
    if account_info!=None:
        lot = 0.01  
        point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).ask
        deviation = 20
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - 50 * point,  # .5 pips
            "tp": price + 200 * point,  # 20 pips
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
    }
    
    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. NASUSD order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        #mt5.shutdown()
        #quit()
        return
 
    print("2. NASUSD order_send done, ", result, timenow, timenow)

    return
    
def submitSellOrder():
    if not mt5.initialize(login='enter your account id', server="Hankotrade-Demo",password="enter your password"):
        print("initialize() failed, error code =",mt5.last_error())
        #quit()
        return
    account_info=mt5.account_info()
    symbol = "NASUSD.HKT"
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not NASUSD found, can not call order_check()")
        mt5.shutdown()
        quit()
 
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "NASUSD is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            #quit()
            return
            
    if account_info!=None:
        lot = 0.01
        point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).ask
        deviation = 20
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": price + 50 * point, 
            "tp": price - 200 * point,  
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
    }
    
    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        mt5.shutdown()
        #quit()
        return
 
    print("2. NASUSD order_send done, ", result, timenow, timenow)
    return


def NASUSD():
    pair = NASUSD
    time.sleep(0.5)
    pag.moveTo(1673,540) # coords for pair in watchlist on the tradingview app
    pag.click()
    time.sleep(0.5)
    #
    breakoutValidate = getredgreen()
    if breakoutValidate == 'vmcRed':
            submitSellOrder()
            return
    if breakoutValidate == 'vmcGreen':
            submitBuyOrder()
            return
 