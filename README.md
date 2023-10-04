# python-trading-bot
a simple python bot that pixel checks for a buy/sell signal then opens a trade with a broker

img <folder>  saves your screenshots taken by pyautogui
grids<folder>  houses your grids you make with makeGrid.py

breakout.py - main program, runs a loop to check for open positions and calls the 'nasdaq_logic.py' functions to place a trade if a signal is found

nasdaq_logic.py
  getredgreen() - scans an area on the tradingview app to look for the latest buy or sell indicator as it pops up
  submitBuyOrder() - submits a buy/long order if the 'buy' indicator appears
  submitSellOrder() -  submits a sell/short order if the 'sell' indicator appears
  NASDAQ() - main function in the file to start checking for the indicator and place an order if it finds it

mouse.py -  got this from somewhere, just a program that shows you the current x,y pixel of your mouse. i use it to determine how im going to make my grid and where the x,y coord of the Watchlist is
makeGrid.py -  makes an x,y grind starting at (0,0) that ends at what your tell it. i.e you want to scan from pixel (0,0) to (3,3) it makes
(0,0)
(0,1)
(0,2)
(1,0)
(1,1)
(1,2)
...
to (2,2)
you then reverse the line order in a text editor so (0,0) is at the bottom, this way you will scan right to left

basic steps (Windows machine, will work on linux but you'll need Wine for the tradingview app)
- you'll need a demo broker account via your favorite broker. im using hanktotrade for testing
- install the tradingview app and get it setp up (https://www.tradingview.com/desktop/)
- install MT5, add your broker account (your broker will usually have an MT5 to download
  
Tradingview app
-  add indicator'SWING TRADE SIGNALS' by nicks1008, under 'Style, uncheck 'Long SMA, change the opactity for 'BuyShape' and 'SellShape' to 100%, change the colors to something different then the buy/sell green/red candles so they can be found easier
-  add NASDAQ to your watchlist if you are trading NASDAQ
-  use the mouse.py file to find the start area of the grid you will be making. i added a screenshot to help
-  use the mouse.py to find the x,y coords of the NASDAQ button, or whatever you are trading, in the watchlist
-  create a grid using makeGrid.py and save it to a text file. clean up the file so it only has the grid coords (0,0) to (x,x) in one column (example included), and reverse the line order so (0,0) is at the bottom
-  modify your x,y start coords on line 57 of nasdaq_logic.py to match your grid start area and size
-  modify lines 21 and 22 to match the RGB code of your buy and sell indicator (use paint or similar to find it)
- add your broker account info on line 19 of breakout.py, lines 68 and 136 of nasdaq_logic.py
- add the x,y coords of your trading pair (NASDAQ in my case) to line 204 of nasdaq_logic.py
- run 'breakout.py' and start troubleshooting as you go. you should have a screenshot of the grid area as 'redgreen.png' to show you what the screenshot is capturing
 

## python modules ##
pyautogui
time
sys
os
datetime
re
ast
requests
PIL
functools
MetaTrader5



