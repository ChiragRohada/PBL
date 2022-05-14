from flask import*
import os
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()


  


 
app = Flask(__name__)
 
@app.route("/speech1")
def hello_world1():
 with sr.Microphone() as source2:
   r.adjust_for_ambient_noise(source2,duration=0.2)

   audio2 = r.listen(source2)

   MyText=r.recognize_google(audio2)
   MyText =MyText.lower()

   print("did you say"+MyText)
   return render_template('speech.html',text=MyText) 
 

   

@app.route("/")
def hello_world():
   return render_template('index.html') 

@app.route("/speech2")
def hello_world2():
   return render_template('speech.html') 



@app.route("/tts",methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
      text=request.form['text']
      gender=request.form['custId']
      action=request.form['custId2']
    
    folder = "C:/Users/webho/Desktop/python_sem4_project/static/text.mp3"
    os.remove(folder)

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if(gender=="Female"):
      engine.setProperty('voice', voices[1].id)
      print(gender)
    
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