import config
import telebot
import requests
from bs4 import BeautifulSoup as BS
from telebot import types
import psycopg2
import time
from datetime import datetime

bot  = telebot.TeleBot(config.token)

user_data = {}


class User:
    def __init__(self,name):
        self.name = name
        self.birth = ''
        
con = psycopg2.connect(
          host = "ec2-3-222-150-253.compute-1.amazonaws.com",
            database = "ddrsrbmbeplv8n",
            user = "qblnsbutvvoobf",
            port = "5432",
            password = "d562b8b974c3c7bdfbb5feedb8946096a2030a275a89be6af5d7fde2aeca0c15" )

cur = con.cursor()
        

# cur.execute("create table users (id serial ,name text,birth_date date)")
# con.commit()
# con.close()        
        
@bot.message_handler(commands=[ 'start'])
def main(message):
    while True:  
        con = psycopg2.connect(
            host = "ec2-3-222-150-253.compute-1.amazonaws.com",
            database = "ddrsrbmbeplv8n",
            user = "qblnsbutvvoobf",
            port = "5432",
            password = "d562b8b974c3c7bdfbb5feedb8946096a2030a275a89be6af5d7fde2aeca0c15"   )

        cur = con.cursor()
        
      
                

        cur.execute("SELECT  name ,birth_date, EXTRACT(MONTH FROM birth_date) , EXTRACT(DAY FROM birth_date) ,EXTRACT(MONTH from current_timestamp) , EXTRACT(DAY from current_timestamp)  from users;")

        rows = cur.fetchall()
        for r in rows:
            if r[2]==r[4] and r[3]==r[5]:
                bot.send_message(message.chat.id , ("Bugun "+r[0]+"ning tug'ilgan kuni tug'ilgan sanasi: "+str(r[1])))
            if r[2]==r[4] and r[3]-1==r[5]:
                bot.send_message(message.chat.id , ("Ertaga "+r[0]+"ning tug'ilgan kuni tug'ilgan sanasi: "+str(r[1])))
            cur.close()
        con.close()
        time.sleep(86400)





@bot.message_handler(commands=['add'])
def main(message):
        msg = bot.send_message(message.chat.id ,  "Ism yuboring")
        bot.register_next_step_handler(msg, process_name_step)
    
def process_name_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id ,  "Tug'ilgan sana yuboring format: MM.DD.YYYY")
        bot.register_next_step_handler(msg, process_birth_step)
    except Exception as e:
        bot.reply_to(message, "Noto'g'ri ma'lumot kiritildi /add orqali qaytadan urinib ko'ring")
        
def process_birth_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.birth = message.text
        con = psycopg2.connect(
             host = "ec2-3-222-150-253.compute-1.amazonaws.com",
            database = "ddrsrbmbeplv8n",
            user = "qblnsbutvvoobf",
            port = "5432",
            password = "d562b8b974c3c7bdfbb5feedb8946096a2030a275a89be6af5d7fde2aeca0c15"  )

        cur = con.cursor()
        print(message.text)
        cur.execute("insert into users (name,birth_date) values (%s,%s)" , (user.name , user.birth))
        con.commit()
        cur.close()        
        bot.send_message(message.chat.id,"Malumotlar bazasiga qo'shildi ")
        
    except Exception as e:
        bot.reply_to(message, "Noto'g'ri ma'lumot kiritildi qaytadan /add orqali qaytadan urinib ko'ring")
    

@bot.message_handler(commands=['remove'])
def main(message):
        msg = bot.send_message(message.chat.id ,  "Id yuboring")
        bot.register_next_step_handler(msg, process_remove_step)
        
def process_remove_step(message):
    try:
        tr = message.text
        con = psycopg2.connect(
           host = "ec2-3-222-150-253.compute-1.amazonaws.com",
            database = "ddrsrbmbeplv8n",
            user = "qblnsbutvvoobf",
            port = "5432",
            password = "d562b8b974c3c7bdfbb5feedb8946096a2030a275a89be6af5d7fde2aeca0c15"  )

        cur = con.cursor()
        cur.execute("delete from users where id = "+tr)
        
        con.commit()
        cur.close()        
        bot.send_message(message.chat.id,"Malumotlar bazasidan o'chirildi ")
        
    except Exception as e:
        bot.reply_to(message, "Noto'g'ri ma'lumot kiritildi /remove orqali qaytadan urinib ko'ring")
    
    
    
@bot.message_handler(commands=['get'])
def main(message):
    con = psycopg2.connect(
        host = "ec2-3-222-150-253.compute-1.amazonaws.com",
            database = "ddrsrbmbeplv8n",
            user = "qblnsbutvvoobf",
            port = "5432",
            password = "d562b8b974c3c7bdfbb5feedb8946096a2030a275a89be6af5d7fde2aeca0c15"  )

    cur = con.cursor()
    cur.execute("SELECT  name ,birth_date, id  from users;")

    rows = cur.fetchall()
    for r in rows:
        
            bot.send_message(message.chat.id , ("Id:"+str(r[2])+" Ism: "+r[0]+ " Tug'ilgan sanasi: "+str(r[1])))
            cur.close()
    con.close()



# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()


if __name__ == '__main__':
    bot.polling(none_stop=True)