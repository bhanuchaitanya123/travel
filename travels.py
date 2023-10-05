from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import session
from selenium import webdriver
from selenium.webdriver.common.by import By
import mysql.connector
import pyttsx3 as p
import datetime
import time
import math
import random
import pyautogui as p
import pywhatkit as py
app=Flask(__name__)

@app.route("/home",methods=["POST","GET"])
def home():
    if request.method=="POST":
       user=request.form['usr']
       phone=request.form['ph']
       fromaddr=request.form['f']
       toaddr=request.form['t']
       if user !='' and phone != '' and fromaddr != '' and toaddr != '':
           digits='0123456789'
           otp=''
           for i in range(4):
            otp+=digits[math.floor(random.random()*10)]
           global a
           a=otp
           global b
           b=user
           global c
           c=phone
           global d
           d=fromaddr
           global e
           e=toaddr
           if(b != '' and c != ''and d != ''and e != ''):
             mydb=mysql.connector.connect(host="localhost",password="mysql123456",database="car_rent",port="3306",user="root",auth_plugin='mysql_native_password')
             c=mydb.cursor()
             kpo="insert into travels(eid,name,pho,f_addr,t_addr) values(1,%s,%s,%s,%s)"
             klp=(user,phone,fromaddr,toaddr)
             c.execute(kpo,klp)
             mydb.commit()
           hr=datetime.datetime.now().strftime('%H')
           mi=datetime.datetime.now().strftime('%M')
           if(int(mi)==58 or int(mi)==59):
             #print("plz,wait for 2 mins")
             time.sleep(120)
           k=datetime.datetime.now().strftime('%H,%M')
           h=datetime.datetime.now().strftime('%H')
           m=datetime.datetime.now().strftime('%M')
           if(int(m)!=59):
             import os
             file_name = r'C:\\Users\munab\\OneDrive\\python\\PyWhatKit_DB.txt'
             with open(file_name, 'w', encoding='utf-8') as f:
                f.write('first line' + '\n')
             py.sendwhatmsg('+91'+ phone,otp,int(h),int(m)+2)
             time.sleep(10)
             #p.press("enter")
           if(int(m)== 59):
             import os
             file_name = r'C:\\Users\munab\\OneDrive\\python\\PyWhatKit_DB.txt'
             with open(file_name, 'w', encoding='utf-8') as f:
                f.write('first line' + '\n')
             py.sendwhatmsg('+91'+ phone,otp,int(h),int(m))
             time.sleep(10)
             #p.press("enter")
           return redirect(url_for("login"))
    else:
        return render_template("car_home.html")
@app.route("/home/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        ot=request.form["otpnm"]
        if ot == a:
            import mysql.connector
            mydb=mysql.connector.connect(host="localhost",password="mysql123456",port="3306",user="root",auth_plugin='mysql_native_password',database="car_rent")
            c=mydb.cursor()
            #sql='insert into travels(user,phone,from_addr,to_addr)values(%s,%s,%s,%s)'
            #st=(sel1,sel2,sel3,sel4)
            c.execute("select name,pho,f_addr,t_addr from travels where eid=1")
            myres=c.fetchall()
            i=[]
            for res in myres:
                i.append(res)
            sql='insert into travels(user,phone,from_addr,to_addr)values(%s,%s,%s,%s)'
            st=(i[0][0],i[0][1],i[0][2],i[0][3])
            c.execute(sql,st)
            mydb.commit()
            if(b != '' and c != ''and d != ''and e != ''):
                state=True
                if(state==True):
                   path="C:\\Users\\munab\\Downloads\\chromedriver_win32.zip\\chromedriver.exe"
                   driver=webdriver.Chrome(path)
                   driver.get("https://www.google.com/maps/@15.8954619,80.7610164,7z")
                   time.sleep(5)
                   driver.find_element(By.ID,"searchbox-searchbutton").click()
                   time.sleep(7)
                   driver.find_element(By.XPATH,"/html/body/div[3]/div[8]/div[3]/div[1]/div[1]/div/div[2]/form/input").click()
                   p.typewrite(d)
                   p.press("enter")
                   time.sleep(5)
                   driver.find_element(By.XPATH,"/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button/span/span").click()
                   time.sleep(5)
                   driver.find_element(By.XPATH,"/html/body/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input").click()
                   p.typewrite(e)
                   p.press("enter")
                   time.sleep(10)
                   driver.find_element(By.XPATH,"/html/body/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/button/img").click()
                   time.sleep(10)
                   distance=driver.find_element(By.XPATH,"/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div/div[1]/div/div[1]/div[2]/div")
                   time_taken=driver.find_element(By.XPATH,"/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div/div[1]/div/div[1]/div[1]")
                   c.execute("update travels set eid =0 where eid = 1")
                   mydb.commit()
                   x=distance.text.split()
                   if '.' in x:
                      o=x.split('.',1)
                      if(int(o[1])>=5):
                          k=math.ceil(float(x[0]))
                          
                      else:
                          k=math.floor(float(x[0]))
                   else:
                      k=x[0]
                   money=int(float(k))*12
                   global fee
                   fee=money
            return redirect(url_for("page"))
    else:
        return render_template("user_otp.html")
@app.route("/home/login/page")
def page():
    return f'<h1>{fee}</h1>'
if __name__=="__main__":
    app.run(debug=True,port=5000, host='0.0.0.0') 
