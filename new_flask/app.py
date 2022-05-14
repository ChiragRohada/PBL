from __future__ import print_function
from distutils.log import error
import errno
from tkinter import E
from flask import*
import os
from matplotlib.pyplot import text
import pymongo
from flask_mail import Mail, Message
import random
import time
from threading import Timer




 
app = Flask(__name__)
 
import pyttsx3

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["chirag"]



mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kjseit.q@gmail.com'
app.config['MAIL_PASSWORD'] = 'ramramsa123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

n = random.randint(1000,9999)


def display():
  global n
  n = random.randint(1000,9999)
  
thisdict = {
  "name":"User",
  "email":"user@gmail.com",
  "password":"hello"
}
text=""


#----------------------------------------------------HOME PAGE-------------------------------------------------


@app.route("/")
def hello_world():
  global text
  text=""
  z=[]
  y="questions"

   
  mycol = mydb[y]
  for x in mycol.find().sort("_id",-1):
      z.append(x)

  print(z)  

  if(thisdict["email"]=="user@gmail.com"):
    fu="login"
  else:
    fu="logout"

   
   
   
  return render_template('index.html',name=z,detail=thisdict,fu=fu) 


#-------------------------------------------your questions--------------------------------------------


@app.route("/Questions")
def your_q():
  
  z=[]
  y="questions"

   
  mycol = mydb[y]
  for x in mycol.find({"email":thisdict["email"]}):
      z.append(x)

  print(z)  

  if(thisdict["email"]=="user@gmail.com"):
    fu="login"
  else:
    fu="logout"

   
   
   
  return render_template('yourQ.html',name=z,detail=thisdict,fu=fu) 





#------------------------------------------------LOG_OUT------------------------------------------------------



@app.route("/logout")
def logout():
        thisdict["email"] = "user@gmail.com"
        thisdict["password"] = "user"
        thisdict["name"] = "user"
        return redirect(url_for('hello_world'))

@app.route("/search",methods = ['POST', 'GET'])
def search():
      if request.method == 'POST':
        search=request.form['search']
      z=[]
      y="questions"

     
      mycol = mydb[y]
      for x in mycol.find({"$text":{ "$search": search }},{ "score": { "$meta": "textScore" } }).sort([('score', {'$meta': 'textScore'})]):
          z.append(x)

          print(z) 
      return render_template('index.html',name=z,detail=thisdict)  


@app.route("/logou")
def logou():
        thisdict["email"] = "user@gmail.com"
        thisdict["password"] = "user"
        thisdict["name"] = "user"
        return redirect(url_for('login'))


#---------------------------------------------------- LOGIN --------------------------------------------

@app.route("/login/",methods = ['POST', 'GET'])
def login():
    global thisdict

    error=""

    if request.method == 'POST':
      email1=request.form['email']
      password1=request.form['password']
      y="email"


      try:
          mycol = mydb[y]
          x=mycol.find_one({"email":email1,"password":password1})
          if(x):
            thisdict["email"] = email1
            thisdict["password"] = email1
            thisdict["name"] = x["name"]
            return redirect(url_for('hello_world'))
      except:
          print("ahkj")
      else:
        error="invalid email !"
        
      
      
    return render_template('login.html',error=error)

        
        
        
      

      
      

    
    
  
    
#----------------------------------------------------SIGN_up---------------------------------------------------------------

name_reg="user"
email_reg="user@gmail.com"
password_reg="hello"

@app.route("/sign_up",methods = ['POST', 'GET'])
def sign_up():
    global name_reg,email_reg,password_reg,n
    
    
    

    if request.method == 'POST':
        name_reg=request.form['name']
        password_reg=request.form['password']
        email_reg=request.form['email']
      

        y="email"
   
        mycol = mydb[y]
        x=mycol.find_one({"email":email_reg})
        if x:
          return render_template('sign-up.html',text="email aleardy register")
        else:
          mylist = [name_reg, email_reg, password_reg]
          
          n = random.randint(1000,9999)
    
      

    

      
           

      
      

      
      
           
        
      
          msg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [email_reg]
               )
          msg.html ="""
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:0px auto;width:70%;padding:20px 0">
      <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"><img src="https://cdn-icons.flaticon.com/png/512/807/premium/807281.png?token=exp=1651862406~hmac=78bd78f7ee897e93794795877841398c" alt="img1" style="height: 100px ;width: 110px;"><h3>Ecom.kjseit</h3></a>
      </div>
      <p style="font-size:1.1em">Hi,</p>
      <p>Thank you for choosing ecom. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
      <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">"""+str(n)+"""</h2>
      <p style="font-size:0.9em;">Regards,<br />Ecom.kjseit</p>
      <hr style="border:none;border-top:1px solid #eee" />
      <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
        <p>Ecom.kjseit</p>
        <p>Flat 302</p>
        <p>Mumbai , MH.</p>
      </div>
    </div>
  </div>
        """
      
        mail.send(msg)
   
   
        return redirect(url_for('check'))
    return render_template("sign-up.html",text=text)
    
  
    


#------------------------------------------------------------OTP_CHECK--------------------------------------------------------



@app.route("/check",methods = ['POST', 'GET'])
def check():

  global n,text
  
  
  

  try:
      if request.method == 'POST':
        otpp=request.form['otp']
     
      
      if (str(n) == str(otpp)):
        y="email"
        msgg = Message(
                'Hello',
                sender ='kjseit.q@gmail.com',
                recipients = [email_reg]
               )
        msgg.html ="""
           
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document_for_email</title>
    <style>
        .center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
    </style>
</head>

<body >
    <div style="padding-left: 200px; padding-right: 200px; padding-top: 25px; ">
        <div style="border: 2px solid; border-color: grey; border-radius: 25px; height: auto;" >
            <div>
                <a href="" style="font-size:1.4em;color: #00466a;padding-left: 200px ;text-decoration:none;font-weight:600"><img src="https://cdn-icons.flaticon.com/png/512/807/premium/807281.png?token=exp=1651862406~hmac=78bd78f7ee897e93794795877841398c" class="center" alt="img1" style="height: 100px ;width: 110px;"><h3 style=";text-align: center;" ;>Ecom.kjsieit</h3></a>
            </div><br>

        <div style="font-size: 20px; padding-left: 100px;padding-right: 100px; text-align: justify;">
    
            The Internet is a huge resource of knowledge and information where you can find virtually anything.
But,very often there are situations where you aren’t able to find the answers to your questions.Your question
may require local knowledge or particular expertise. <br><br>
            Fortunately there are sites out there that can not only be used to find peoples thoughts and opinions
about a particular topic but will also will help in finding experts in various fields. Herein find some best sites
where you can ask questions and get answers from real people online. <br><br>
            You can find answers to various questions from different categories on Answerbag You may ask questions
on any topic but will need to register to do so. You can also browse through questions in selected categories of 
your choice and read all the questions and answers posted by other people. <br><br>
Probably the most popular community Q&A powered site with millions of users and thousands of questions asked and answered every day. All the questions are categorized in such a way that you can easily search for a related question in a category or place you question in a relevant category. Answers are rated by visitors and the best rated answer will be displayed as the best answer for a question.
<br><br>
You need to register with the site in order to ask or answer the questions. To make the users participate actively, it has a points system. When you ask a question you’ll spend points and when you answer the questions you’ll earn them. Based on the points earned, the user level will be defined.
<br><br>
This is another site where you can ask questions and answer them without  registration. You can also browse through questions in various categories and browse through the Q&A’s posted by other people.
<br><br><br>        
        </div>
        <hr style="border:none;border-top:1px solid #eee">
            <div style="float: right;padding-right: 75px;color:#aaa;font-size:1.0em;line-height:1;font-weight:300">
                <p>Ecom.kjsieit</p>
                <p>Flat 302</p>
                <p>Mumbai , MH.</p>
            </div>
    
        <footer style="padding-left: 100px; float: inline-end; text-align: center;color:#aaa;font-size:1.0em;line-height:1;font-weight:300">  
        <br><br><br><br><br><br>
        @Copyright Ecom.kjsieit 2022- All Right Reserved.   
        <br>
        </footer>
    </div>
</div>

</body>
</html>

"""
       
        
        mail.send(msgg)
   
        mycol = mydb[y]
        mycol.insert_one({"email":email_reg,"name":name_reg,"password":password_reg})

       
        text=""
        return redirect(url_for('login'))
      else:
        n = random.randint(1000,9999)
        
        
        text="invalid email"
        return redirect(url_for('sign_up'))

  except:
    print(error)





  return render_template('check.html')



    
    
  
    
      

   
      


 
    
       
    
 
    
     


    

if __name__ == '__main__':  
   app.run(debug = True)  