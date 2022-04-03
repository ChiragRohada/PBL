from flask import*
import os

 
app = Flask(__name__)
 
import pyttsx3

@app.route("/")
def hello_world():
   return render_template('index.html') 



@app.route("/tts",methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
      text=request.form['text']
      gender=request.form['custId']
      action=request.form['custId2']
    
    folder = "C:/Users/webho/Desktop/flask/static/text.mp3"
    os.remove(folder)
    
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    
    engine.save_to_file(text,'static/text.mp3')
    engine.runAndWait()
    engine.stop()
    return render_template('index.html',text=text)
    
 
    
       
    
 
    
     


    

if __name__ == '__main__':  
   app.run(debug = True)  
