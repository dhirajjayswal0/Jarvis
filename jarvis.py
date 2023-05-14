import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys

# Choosing voice type
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


# Text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# Audio input
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=8)

    try:
        print("Recognizing")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

    except Exception as e:
        speak("Say that again please...")
        return "none"
    return query


# Greet function
def greet():
    hour = int(datetime.datetime.now().hour)

    if 0 < hour < 12:
        speak("good morning sir, I am jarvis. Please tell me how can i help you")
    elif 12 <= hour < 18:
        speak("good afternoon sir, I am jarvis. Please tell me how can i help you")
    else:
        speak("good evening sir, I am jarvis. Please tell me how can i help you")


# To send email
# Need to allow less secure apps in google account to enable login

# def sendemail(to, content):
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.login('dhirajjayswal012@gmail.com', 'Manorma01@')
#     server.sendmail('dhirajjayswal012@gmail.com', to, content)
#     server.close()


if __name__ == "__main__":
    greet()
    while True:
        query = takecommand().lower()

        # Logic building for task
        if "open notepad" in query:
            notepadPath = "C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(notepadPath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in query:
            music_dir = "C:\\Users\\495949\\Music"
            songs = os.listdir(music_dir)
            for song in songs:
                if song.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir, song))

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"your IP address is {ip}")

        elif "wikipedia" in query:
            speak("searching wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(results)

        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")

        elif "open stackoverflow" in query:
            webbrowser.open("www.stackoverflow.com")

        elif "open google" in query:
            speak("sir, what should i search on google")
            search = takecommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={search}")

        elif "send message" in query:
            hour = int(datetime.datetime.now().hour)
            minute = int(datetime.datetime.now().minute)
            kit.sendwhatmsg("+917000552971", "this is a test message from jarvis", hour, minute + 2)

        elif "open youtube" in query:
            speak("sir, what should i play on youtube")
            search = takecommand().lower()
            kit.playonyt(f"{search}")

        elif "tell me about Ayush" in query:
            speak("sir, Ayush is a bhosdiwala")

        # Need to allow less secure apps in google account to enable login
        # elif "send email" in query:
        #     try:
        #         speak("what should i say?")
        #         content = takecommand().capitalize()
        #         # Here we can create a database of name and email
        #         # and email will be sent to the name spoken
        #         to = "dhirajjayswal0@gmail.com"
        #         sendemail(to, content)
        #         # again using name we can say to whom it was sent
        #         speak("Email has been sent")
        #
        #     except Exception as e:
        #         print(e)
        #         speak("Sorry sir, i was unable to send the message")

        elif "shutdown" in query:
            speak("Thanks for using me sir, have a good day.")
            sys.exit()

        speak("")

