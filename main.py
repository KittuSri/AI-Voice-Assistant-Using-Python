import speech_recognition as sr  #convert voice to text
import webbrowser                #open website in your defult browser
import pyttsx3                   #convert text to voice
import time
import musicLibraray
from ollama import chat
import sys

recognizer = sr.Recognizer()    #recognizer used to recognize the voice
engine = pyttsx3.init()               #initialize the text to speech engine

def ask_ai(prompt):
    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "Answer in 2 or 3 short sentences."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]



def speak(text):
    engine.say(text)
    engine.runAndWait()                  #ensures your program doesn't continue until the speech has completed

def processCommand(c):
    print("Inside processCommand:", c)

    if "stop" in c.lower():
        engine.stop()
        return
    elif "google" in c.lower():
        print("Opening Google...")
        webbrowser.open("https://www.google.com")

    elif "youtube" in c.lower():
        print("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")

    elif "facebook" in c.lower():
        print("Opening Facebook...")
        webbrowser.open("https://www.facebook.com")
    
    elif c.lower().startswith("play"):

         song = c.lower().replace("play", "").strip()

         if song in musicLibraray.music:
                webbrowser.open(musicLibraray.music[song])
                speak(f"Playing {song}")

         else:
             speak("Sorry. I couldn't find that song.")
    
    elif "exit" in c.lower() or "goodbye" in c.lower() or "quit" in c.lower():
          speak("Goodbye Shweta. Have a nice day.")
          sys.exit()
    
    else:
        #let open ai handle the request
          try:
            answer = ask_ai(c)
            speak(answer)

          except Exception as e:
               print(e)
               speak("Sorry, I couldn't understand your request.")



if __name__ == "__main__":
    speak("Hello, I am your voice assistant. How can I help you today?")
    while True:
        #listen for the wake word jarvis 
        #obtain audio from the microphone
        r=sr.Recognizer()
        

        #recognize speech using sphinx 
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                   print("Listening...")
                   audio = r.listen(source)
            word = r.recognize_google(audio)  #sphinx take alot of time to listen so we use google
            print("Wake word:", word)
            if(word.lower() == "jarvis"):
                speak("Yes, how can I help you?")
                time.sleep(1)
                #listen for command
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print("Command:", command)

                    processCommand(command)
        except Exception as e:
            print("error; {0}".format(e))