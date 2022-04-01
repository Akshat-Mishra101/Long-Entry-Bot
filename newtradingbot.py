import time
from binance import Client
from decimal import Decimal
import threading


api_key = ''
api_secret = ''


lever = 20
quant = 15
order_point = 0


zone = [1.3300,1.3200]


ticker = 'WAVESUSDT'


print('Connecting To The Binance Servers')
client = Client(api_key,api_secret)
print('Connected To The Binance Server')

#Fixed Declarations
counter = 0
buffer = .2
live_price = 0
clock_speed = 1
initial_run = True
last_order_point = 0

#Fixed Declarations
order_has_been_taken = False
real_order_point = 0
#Fixed Declarations

#Tested
def CloseOrder(OrderType:str):
    global ticker
    global lever
    global quant
    orderBuy = client.futures_change_leverage(symbol=ticker, leverage=lever)
   
    #reversing the order type to close the position
   
    if OrderType == 'BUY':
       OrderType = 'SELL'
    else:
       OrderType = 'BUY'
    try:
       print(client.futures_create_order(
       symbol=ticker,
       type='MARKET',
       side=OrderType,
       quantity=quant,
       reduceOnly=True))
       print(OrderType+" Closed Successfuly")
    #Reduce Only Ensures This Does Not Open A New Order And Only Closes The Existing Order
    except:
       print("No "+OrderType+" Order To Close")
   



#Tested
def openOrder(OrderType:str):
    
    global ticker
    global lever
    global quant
    orderBuy = client.futures_change_leverage(symbol=ticker, leverage=lever)
    print(client.futures_create_order(
       symbol=ticker,
       type='MARKET',
       side=OrderType,
       quantity=quant))
    print(OrderType+" Placed Successfuly")

#Tested
def getLivePrice():
    
    global live_price
    global clock_speed
    global order_point
    
    while True:
       data = (client.futures_symbol_ticker(symbol=ticker))
       live_price = float(data['price'])
       print(f'\nThe Current Price is {live_price} and The Order Point is {order_point}\n')
       time.sleep(.5)
       
def is_greater_than_any(bottoms:list,number:float):
    the_truth = False
    for i in bottoms:
        if number >= i:
            the_truth = True
    return the_truth

def contains(bottoms:list,number:float):
    the_truth = False
    for i in bottoms:
        if number == i:
            the_truth = True
            break
    return the_truth

def order_execution():
    bottoms = []#Empty List
    print('run please')
    pair = [0,0]
    #record prices as they move down,taking snapshots of live_price and the order_point, when the price enters the order point which is .2% of the live_price, place a buy order
    #if the real price goes below .2% of the order_point, close the trade
    global last_order_point
    global clock_speed
    global live_price
    global order_point
    global buffer

    global order_has_been_taken
    global initial_run

    while True:
        

        

        if initial_run:
            
            
            order_point = live_price
            last_order_point = order_point
            initial_run = False
            order_has_been_taken = True
            openOrder('BUY')
            pair[0] = order_point
            pair[1] = round(order_point-((buffer/100)*order_point),4)
            print(f'Took An Initial Trade At {order_point}')
            print('The Prices Can Either Go Up Or Down From Here')
            print('The Bot Has Taken An Entry')
            print('The Bot Has A CoolDown For 2 Seconds')
            print(f'The Pair is {pair}')
            clock_speed = 1
            time.sleep(2)
            

            

        if live_price <= order_point:
            
            
           clock_speed = .2
                        
           #When the prices are going down
           
           print('Prices Have Gone Below The Order Point')
           
           if order_has_been_taken:

               
               

               print("We Have Closed The Trade")
               CloseOrder('BUY')
               print("We Reset The Values")
               order_has_been_taken = False

           if live_price < pair[1]:

               hypothesis = round(((buffer/100)*live_price)+live_price,4)

               if contains(bottoms,hypothesis) == False:
                   bottoms.append(hypothesis)
                   print(f'.2 percent shifted order point is {hypothesis}')

           if is_greater_than_any(bottoms,live_price):
               print(bottoms)
               print(f'Open A Trade at {live_price}')
               openOrder('BUY')
               clock_speed = 1
               bottoms.clear()
               order_has_been_taken = True
               order_point = live_price
               last_order_point = order_point
               pair[0] = order_point
               pair[1] = round(order_point-((buffer/100)*order_point),4)
               time.sleep(1)
               
               print('Price Hit One Of The Retraced Values')
               
                
               
        elif live_price > order_point:
            
            if order_has_been_taken == False:
                openOrder('BUY')
                print('We Perform A Buy Order')
                bottoms.clear()
                order_has_been_taken = True
                order_point = last_order_point
                pair[0] = order_point
                pair[1] = round(order_point-((buffer/100)*order_point),4)
                time.sleep(1)
                
            print(f"At A Profitable Position at order point {order_point} and live price {live_price}")
                
        
                
                

                
             
        
        else:
            print("Bot Hasn't Been Updates Or The Price is At Breakeven")
        time.sleep(clock_speed)
        
def trigger():
    global zone
    while True:
        if live_price <= zone[0] and live_price >= zone[1]:
            print('Price Has Entered The Zone')
            break
        else:
            print('Waiting For The Price To Enter The Zone')
        

if __name__ == '__main__':
    print('The Bot Has Been Started IN CLI MODE')
    
    price_updater = threading.Thread(target = getLivePrice)
    price_updater.start()
    time.sleep(1)
    order_execution_thread = threading.Thread(target = order_execution)
    order_execution_thread.start()

    
          






     
    

    
