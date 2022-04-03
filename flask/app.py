from flask import*

@app.route("/")
def hello_world():
   return render_template('index.html') 

@app.route("/tts",methods = ['POST', 'GET'])
def hello_world():
if request.method == 'POST':
        text=request.form['text']
        gender=request.form['custId']
   
import pyttsx3
text_speech = pyttsx3.int()
result = input("text:")
text_speech.say(result)
text_speech.runAndWait()

   return render_template('index.html') 



if __name__ == '__main__':  
   app.run(debug = True)  
