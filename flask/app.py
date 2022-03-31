from flask import*

@app.route("/")
import pyttsx3
text_speech = pyttsx3.int()
result = input("text:")
text_speech.say(result)
text_speech.runAndWait()


def hello_world():
   return render_template('index.html') 


if __name__ == '__main__':  
   app.run(debug = True)  
