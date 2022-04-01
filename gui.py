from tkinter import *
import threading
import newtradingbot
from newtradingbot import *
#GUI For The Trading BOT

window  = Tk()
window.title('Long Entry Bot')
#window.geometry('600x400')
#Declaring Functions





def update_label():
    while True:
        price_updation_label.config(text = newtradingbot.live_price)
        
    

price_updater = threading.Thread(target = getLivePrice)
price_label_updater = threading.Thread(target = update_label)





    

started = False
def start_bot():
    global started
    global price_updater
    
    
    print(ticker_entry.get().upper())
    if started == False:
        start_button.config(text = 'Stop')
        print('The Bot Has Been Started')
        newtradingbot.ticker = ticker_entry.get().upper()

        


        
        price_updater.start()
        price_label_updater.start()
        




        
        started = True
    else:
        start_button.config(text = 'Start')
        print('The Bot Has Been Stopped')
        started = False
        
    

    


#Declaring Componenents And Positioning Them
ticker_label = Label(window,text = 'Enter The Ticker', font = ('Arial', 12, 'bold'))
ticker_label.grid(row = 0, column = 0)

ticker_entry = Entry(window, font = ('Arial',14))
ticker_entry.grid(row = 1, column = 0)


order_point_label = Label(window, text = 'Enter The Order Point', font = ('Arial', 12, 'bold'))
order_point_label.grid(row  = 0, column = 1)


order_point_entry = Entry(window, font = ('Arial',14))
order_point_entry.grid(row = 1,column = 1)


amount_label = Label(window,text = 'Amount', font = ('Arial', 12, 'bold'))
amount_label.grid(row = 0, column = 2)


amount_entry = Entry(window, font = ('Arial',14))
amount_entry.grid(row = 1, column = 2)

leverage_label = Label(window,text = 'Leverage', font = ('Arial', 12, 'bold'))
leverage_label.grid(row = 2, column = 1)

leverage_entry = Entry(window, font = ('Arial',14))
leverage_entry.grid(row = 3, column = 1)

start_button  = Button(window, text = "Start",width=20,command = start_bot)
start_button.grid(row = 2, column = 0)



status_label = Label(window, text = "Welcome", font = ('Arial',12 ,'bold'),bg = "#000", fg="green")
status_label.grid(row = 3, column = 0 )


price_label = Label(window,text = "Live Price" ,font = ('Arial',12,'bold'))
price_label.grid(row = 2,column = 2)

price_updation_label = Label(window, text = "Live Price:",font = ('Arial',12,'bold'))
price_updation_label.grid(row = 3,column = 2)


window.mainloop()




    
