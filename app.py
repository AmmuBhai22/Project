import mysql.connector as ms
import time
import datetime as dt
import datetime
from email.message import EmailMessage
import smtplib, ssl
import imaplib
from flask import Flask, make_response,request,render_template
import requests as rq
import random as rand

app=Flask("School CS WEEK PROJECT  By Aman Adlakha 6th E")
#server_url="http://localhost:5000/"
server_url="http://scpj.ammubhai.serv00.net/"
#con=ms.connect(host='sql12.freesqldatabase.com',database='sql12664020',user='sql12664020',password='l4b8Hrbztq')
#con=ms.connect(host='localhost',database='project',user='root',password='')
con=ms.connect(host="db4free.net",database="am_project",user="project_am",password="Abc@1234")
cur=con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS send_mail (email varchar(255), txt varchar(255), date DATE, id INT PRIMARY KEY);")
con.commit()
def check_key():
	ran=rand.randint(0,9999)
	cur.execute("SELECT id FROM send_mail")
	dt=cur.fetchall()
	ky=[]
	for j in dt:
		d=j[0]
		ky.append(d)
	if ran in ky:
		ran=rand.randint(0,9999)
	return ran
@app.route("/credits")
def credits():
	return "This application is created by Aman Adlakha of 6th E of BMVB ASMA SECOND SHIFT for CS WEEK project"

@app.route("/check_send")
def send():
	date=dt.date.today()
#	date="2023/11/21"
	cur.execute("SELECT date FROM send_mail")
	datea2=cur.fetchall()
#	print(datea2)
	date2=datea2
	for k,j in enumerate(date2):
		j=j[0]
		#print(j,date,j==date)
		if j==date:
			cur.execute("SELECT txt FROM send_mail")
			mot=cur.fetchall()[k][0]
			#print(mot)
			mos = EmailMessage()
			mos['Subject'] = "REMINDER MAIL"
			mos['From'] = "maheshstore@yahoo.com"
			mos.set_content(mot)
			cur.execute("SELECT email FROM send_mail")
			mol=cur.fetchall()[k][0]
			context = ssl.create_default_context()
			mos['To'] = mol
			#print(mol)
			#print(mos)
			#with imaplib.IMAP4_SSL(host='imap.gmail.com',port=993) as server:
			with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465,context=context) as server:
				server.login("maheshstore@yahoo.com","lrilkrddpzoovazl")
				#print("Logged In")
			#	server.login("ttr@ammubhai.serv00.net",'^BEBG8RcK0B@Wz3BRlQ4')
				server.send_message(mos)
			cur.execute("SELECT id FROM send_mail")
			koy=cur.fetchall()[k][0]
			cur.execute(f"DELETE FROM send_mail WHERE id={koy}")
			con.commit()
	return "Work Done!"

@app.route("/add",methods=["GET","POST"])
def add():
	if request.method=="GET":
		return render_template("add.html")
	if request.method=="POST":
		frm=request.form
		koy=check_key()
		dt4=frm["dt"].replace("-","/")
		cur.execute(f'''INSERT INTO send_mail VALUES("{frm["email"]}","{frm["sms"]}",'{dt4}',{koy})''')
		con.commit()
		check=rq.get(server_url+"check_send")
		return render_template("addLast.html")

@app.route("/")
def index():
	dota=""
	cur.execute("SELECT * FROM send_mail")
	lal=cur.fetchall()
	for j in lal:
		mail=j[0]
		text=j[1]
		date=j[2]
		dt2=f'<div class="template" ><h3><center>Email:- {mail}</h3><br><h3>Date To Send On:- {date}</h3><br><h3>Message:- {text}</h3></center></div><br><br>'
		dota+=dt2
	if len(lal)!=0:
		return render_template("index.html",dta=dota)
	else:
		return render_template("notify.html",line1="NO REMINDER",line2="FOUND")

@app.route("/clear",methods=["GET","POST"])
def clear():
	cur.execute("SELECT * FROM send_mail")
	lal=cur.fetchall()
	if request.method=="GET":
		if len(lal)!=0:
			return render_template("clear.html",history=lal)
		else:
			return render_template("notify.html",line1="NO REMINDER FOUND",line2="TO CLEAR")
	elif request.method=="POST":
		sta=request.form
		for j in sta.keys():
			lal=eval(sta[j])
			id=lal[3]
			cur.execute(f"DELETE FROM send_mail WHERE id={id}")
		con.commit()
		return render_template("notify.html",line1="SELECTED REMINDERS",line2="SUCCESSFULLY DELETED")

@app.route("/clearall")
def clrA():
	cur.execute("DROP TABLE send_mail")
	con.commit()
	cur.execute("CREATE TABLE IF NOT EXISTS send_mail (email varchar(255), txt varchar(255), date DATE, id INT PRIMARY KEY);")
	con.commit()
	return render_template("notify.html",line1="ALL REMINDERS",line2="HAVE BEEN DELETED")
#Index Sample Below
#<div class="template" >{{dta}}</center></div> 
