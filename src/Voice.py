import random
import subprocess
from bottle_websocket import websocket
import cv2
import pytesseract
import googlesearch
from werkzeug import Client
import wolframalpha
import wikiquote
import pyttsx3
import json
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import pycaw
import time
import requests
from pynput.keyboard import Key, Controller
import fileinput
import getpass
import wmi
import os
from os import listdir
from pathlib import Path
from os.path import isfile, join
from clint.textui import progress
from selenium import webdriver
# from Gesture_Controller import gc1
import openai

from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
from threading import Thread


# ---------------Object Initialization-----------------
keyboard = Controller()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

DIRECTORIES = {
    "HTML": [".html5", ".html", ".htm", ".xhtml"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif", ".psd"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  "pptx"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAINTEXT": [".txt", ".in", ".out"],
    "PDF": [".pdf"],
    "PYTHON": [".py",".pyi"],
    "XML": [".xml"],
    "EXE": [".exe"],
    "SHELL": [".sh"]
}
FILE_FORMATS = {file_format: directory
                for directory, file_formats in DIRECTORIES.items()
                for file_format in file_formats}

# -----------Variables-----------
file_exp_status = False
files =[]
path = ''
is_awake = True

openai_api_key = "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"
openai.api_key = openai_api_key

def bol_be(audio):
    engine.say(audio)
    engine.runAndWait()

def countdown(n) :
    while n > 0:
        print (n)
        n = n - 1
    if n ==0:
        print('BLAST OFF!')

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        bol_be("Good Morning Sir!")

    elif hour>=12 and hour<18:
        bol_be("Good Afternoon Sir!")   

    else:
        bol_be("Good Evening Sir!")  

    assname=("B5 Assist")
    bol_be("I am your Assistant")
    bol_be(assname)

def usrname():
    bol_be("What should I call you sir")
    uname=takeCommandname()
    bol_be("Welcome Mister")
    bol_be(uname)
    print("#####################")
    print("Welcome Mr.",uname)
    print("#####################")

def quotaton():
    bol_be(wikiquote.quote_of_the_day())
    print(wikiquote.quote_of_the_day())

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)    
        print("Unable to Recognizing your voice.")  
        return "None"
    return query

def takeCommandname():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Username...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Trying to Recognizing Name...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)    
        print("Unable to Recognizing your name.")
        takeCommandname()  
        return "None"
    return query

def takeCommandmessage():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Enter Your Message")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print(f'Message to be sent is : {query}\n')

    except Exception as e:
        print (e)
        print("Unable to recognize your message")
        print("Check your Internet Connectivity")
    return query

def takeCommanduser():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Name of User or Group")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print(f'Client to whome message is to be sent is : {query}\n')

    except Exception as e:
        print (e)
        print("Unable to recognize Client name")
        bol_be("Unable to recognize Client Name")
        print("Check your Internet Connectivity")
    return query

def takeCommandcontent():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("What Should I say, Sir")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print(f'Message to be sent is: {query}\n')

    except Exception as e:
        print (e)
        print("Unable to recognize")
    return query

def open_application(path):
    if os.path.isfile(path):
        os.startfile(path)
    elif os.path.isdir(path):
        os.startfile(os.path.join(path,""))
    else: 
        subprocess.Popen(path)

def execute_command(command):
    try:
        os.system(command)
        print("Command executed successfully")
    except Exception as e:
        print("Error executing command: " + str(e))

# def adjust_volume(level):
#     try:
#         session = pycaw.audio.DeviceFromName("Speakers")
#         devices = pycaw.audio.GetAudioDevices(devices=[session])
#         device = devices[0]
#         device.set_volume(level)
#         print("Volume adjusted to: " + str(level))
#     except Exception as e:
#         print("Error adjusting volume: " + str(e))
        
def adjust_volume(level):
    """Adjusts the volume of the audio output."""
    devices = pycaw.get_audio_devices()
    session = pycaw.audio.DeviceFromName("Speakers")
    for device in devices:
        if device['name'] == session.name:
            device.set_volume(level, 0)
            print("Volume adjusted to: " + str(level))

# def change_volume(command):
#     """Changes the volume of the audio output."""
#     devices = pycaw.get_audio_devices()
#     session = pycaw.audio.DeviceFromName("Speakers")
#     for device in devices:
#         if device['name'] == session.name:
#             if 'volume' in command:
#                 volume = int(command.split()[1])
#                 device.set_volume(volume, 0)
#                 print("Volume adjusted to: " + str(volume))
#             elif 'mute' in command:
#                 device.mute()
#                 print("Muted")
#             elif 'unmute' in command:
#                 device.unmute()
#                 print("Unmuted")

def search_question(query):
    if query:
        try:
            search_results = wikipedia.search(query)
            url = search_results[0]
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('p')
            answer = ''
            for article in articles:
                answer += article.get_text()
            print("Answer: " + answer)
        except Exception as e:
            print(e)
            print("Sorry, I couldn't find an answer to your question.")
    
def search_image(query):
    url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    for image in images:
        src = image.get('src')
        if src.startswith('https://'):
            print(f"Image URL: {src}")
            break

def scan_object():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(gray, config=config)
        search_object(text)
        cap.release()
        cv2.destroyAllWindows()
        print("Object scanned and searched")
    except Exception as e:
        print("Error scanning and searching object: " + str(e))

def search_object(query):
    try:
        search_results = googlesearch.search(query, num_results=1)
        url = search_results[0]
        print("Search result: " + url)
        bol_be("Here is the some result")
    except Exception as e:
        print("Error searching for object: " + str(e))

def ask_question(query):
    """Uses OpenAI's API to generate a response to the user's query."""
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=query,
        temperature=0.5,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0]['text']

def search_files(query):
    """Searches for files in the local directory."""
    directory = os.listdir('.')
    files = [f for f in directory if os.path.isfile(f)]
    matching_files = [f for f in files if query in f]
    print("Here are the matching files:")
    bol_be("Here are matching  file names.")
    for file in matching_files:
        print(file)

def organize():
    for entry in os.scandir():
        if entry.is_dir():
            continue
        file_path = Path(entry.name)
        file_format = file_path.suffix.lower()
        if file_format in FILE_FORMATS:
            directory_path = Path(FILE_FORMATS[file_format])
            directory_path.mkdir(exist_ok=True)
            file_path.rename(directory_path.joinpath(file_path))
    try:
        os.mkdir("OTHER")
    except:
        pass
    for dir in os.scandir():
        try:
            if dir.is_dir():
                os.rmdir(dir)
            else:
                os.rename(os.getcwd() + '/' + str(Path(dir)), os.getcwd() + '/OTHER/' + str(Path(dir)))
        except:
            pass

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@email.com', 'your-password')
    server.sendmail('youremail@email.com', to, content)
    server.close()

if __name__ == '__main__':
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    # usrname()
    bol_be("Can I tell you a quote of day")
    useropt=takeCommand().lower()
    if 'yes' in useropt or 'sure' in useropt:
        quotaton()
    else:
        bol_be("Taking you to command function")

    bol_be("How can I Help you, Sir")
    while (True):
        query = takeCommand().lower()
        assname=("Baby")
        if "hey baby" in query or "baby" in query or "wake up baby" in query:
            is_awake = True

        if not is_awake:
            continue
    
        '''
        You need to write your code here.
        This is the place where you will add all the commands for Baby.
        Each condition should be separated by an elif statement.
        If there are multiple possible conditions for one command, use parentheses.
        For example:
            if (condition1) or (condition2) or ...:
                do this
            else:
                do that
        ''' 
        if 'wikipedia' in query:
            bol_be('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            bol_be("Answer From Wikipedia")
            print(results)
            bol_be(results)


        # ------------Conversational queries------------    
         
        elif any(word in query for word in ['hello', 'hi','hey']) and assname!='':
            greetings = ["Hello","Hey there", "Hi","Howdy","What's up?","Good Morning","Good Afternoon","Good Evening"]
            greetings = ["Hello","Hey there", "Hi","Howdy"]
            greeting = random.choice(greetings)
            bol_be(greeting+" "+assname+". How can I help you today?")

        elif "how are you" in query or "how r u" in query:
            feelings = ["Good","Great","Excellent","Fantastic","Wonderful","Awesome","Splendid","Superb","Perfectly fine","Just great"]
            feelings = ["Good","Great","Excellent","Fantastic","Wonderful","Awesome","Superb","Perfectly fine","Just great","Nice"]
            feelings = ["Good","Great","Excellent","Fantastic","Awesome","Wonderful","Nice","Splendid","Superb","Perfect"]
            feelings = ["Good","Great","Superb","Fantastic","Wonderful","Excellent","Perfect","Very good","Just great","Awesome"]
            feelings = ["Good","Great","Superb","Fantastic","Wonderful","Excellent","Perfect","Just great","Awesome","Nice"]
            feelings = ["Good","Great","Superb","Fantastic","Wonderful","Excellent","Perfect","Just great","Very good","Good job"]
            feelings = ["Good","Great","Excellent","Fantastic","Wonderful","Awesome","Superb","Perfectly fine","Just great","Feeling good"]
            feelings = ["Good","Great","Excellent","Fantastic","Wonderful","Awesome","Superb","Perfect","Just great","Nice"]
            feelings = ["Good","Great","Excellent","Fantastic","Awesome","Nice"]
            feeling = random.choice(feelings)
            bol_be(f"{feeling} as well. What can I do for you today?")

        elif "thank you" in query:
            thanks = ["You're welcome","My pleasure","Anytime","Welcome"]
            thankyou = random.choice(thanks)
            bol_be(thankyou + ". It was a pleasure helping you.")

        elif "goodbye" in query or "see you later" in query:
            byes = ["See you around","Talk to you soon","Have a great day","Bye for now"]
            bye = random.choice(byes)
            bol_be(bye+" "+assname)

        elif "Good Morning" in query:
            morning_greetings = ["Good Morning","It's a beautiful day outside"]
            morning_greeting = random.choice(morning_greetings)
            bol_be(morning_greeting+". Let's make the most of it.")

        elif 'exit' in query:
            bol_be("Thanks for giving me your time")
            exit()
            
        elif "What is your name" in query:
            bol_be("I am an AI Assistant developed using Python. My purpose is to assist users with their queries and tasks.")
            bol_be("I am an AI assistant.")
            bol_be(assname)

        elif "who made you" in query or "who created you" in query: 
            bol_be("I have been created by Group B5.")

        elif 'joke' in query:
            bol_be(pyjokes.get_joke())

        elif "who i am" in query:
            bol_be("If you talk then definately your human.")

        elif "why you came to world" in query:
            bol_be("Thanks to Group B5. further It's a secret")

        elif 'is love' in query:
            bol_be("It is 7th sense that destroy all other senses")

        elif "who are you" in query:
            bol_be("I am your virtual assistant created by Group B5")

        elif 'reason for you' in query:
            bol_be("I was created as a Minor project by Mister Group B5 ")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            bol_be(f"Sir, the time is {strTime}")

        elif "samay" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            bol_be(f"samaye hai {strTime}")

        elif "calculate" in query:
            app_id = "Wolframe Alpha API"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            bol_be("The answer is " + answer)


        # ---------Online/Search Commands---------

        elif 'open opera' in query:
            codePath = r"C:\Users\User\AppData\Local\Programs\Opera\launcher.exe"
            os.startfile(codePath)

        elif "wikipedia" in query and "hindi" in query:
            bol_be('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            query = query.replace("hindi", "")
            results = wikipedia.summary(query, sentences=3)
            bol_be("According to Wikipedia")
            r = sr.Recognizer()
            results = r.recognize_google(results, language='hi')
            print(results)
            bol_be(results)

        elif 'open youtube' in query:
            print("Opening YouTube...")
            os.system("start www.youtube.com") 
            print("Taking You To Youtube")
            bol_be("Taking You To Youtube")

        elif 'open google' in query:
            print("Opening Google Search Page...")
            bol_be("Taking you to Google")
            webbrowser.open("google.com")

        elif "open Gmail" in query:
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")

        elif 'search' in query:
            bol_be('Searching for ' + query.split('search')[1])
            url = 'https://google.com/search?q=' + query.split('search')[1]
            try:
                webbrowser.get().open(url)
                bol_be('This is what I found Sir')
            except:
                bol_be('Please check your Internet')

        elif "search image of" in query:
            image_query = query.replace( "search image of", "")
            search_image(image_query)
                
        elif "play song" in query or "play music" in query:
            bol_be('Playing  Music ' + query.split('play')[1])
            url = "http://music.youtube.com/search?q=" + query.split('play')[1].replace(' ', '%20').strip()+'&autoplay=1'
            try:
                webbrowser.get().open(url)
                bol_be("Here it is..")
            except:
                bol_be("Please check your connection")

        elif "where is" in query:
            query=query.replace("where is","")
            location = query
            bol_be("Locating ")
            bol_be(location)
            webbrowser.open("https://www.google.nl/maps/place/" + location + "")

        elif 'location' in query:
            bol_be('Which place are you looking for ?')
            temp_audio = takeCommand()
            # app.eel.addUserMsg(temp_audio)
            bol_be('Locating...')
            url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
            try:
                webbrowser.get().open(url)
                print('This is what I found Sir')
                bol_be('This is what I found Sir')
            except:
                bol_be('Please check your Internet')

        elif 'open stackoverflow' in query or "stackoverflow" in query:
            print("Opening Stackoverflow...")
            bol_be("Here you go to Stack Over flow.Happy coding")
            webbrowser.open("stackoverflow.com")

        elif 'google news' in query:
            try:
                jsonObj = urlopen('''https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey=Google news API key''')
                data = json.load(jsonObj)
                i = 1
                bol_be('')
                print('''===============Google News============'''+ '\n')
                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    bol_be(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                    print(str(e))

        elif "bbc news" in query:
            try:
                main_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=BBC News API key"
                open_bbc_page = requests.get(main_url).json() 
                article = open_bbc_page["articles"] 
                results = [] 
                for ar in article: 
                    results.append(ar["title"]) 
                for i in range(len(results)): 
                    print(i + 1, results[i])
            except Exception as e:
                print(str(e))

        elif 'news' in query:
            try:
                jsonObj = urlopen('''https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=Time of INDIA API key''')
                data = json.load(jsonObj)
                i = 1
                bol_be('here are some top news from the times of india')
                print('''===============TIMES OF INDIA============'''+ '\n')
                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    bol_be(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                print(str(e))

        elif "weather" in query or "temperature" in query:
            try:
                bol_be(" City name ")
                print("City name : ")
                cityName=takeCommand()
                api_key = "060679c8d7f2d5ff71b42bf42e0e6aa7" #Get your own API key from OpenWeathermap.org
                base_url = "http://api.openweathermap.org/data/2.5/weather?"
                complete_url = base_url + "appid=" + api_key + "&q=" + cityName
                response = requests.get(complete_url)
                data = response.json()
                if data['cod'] != '404':
                    main = data['main']
                    temperature = round((main["temp"] - 273.15), 2)
                    humidity = data['main']['humidity']
                    weather_report = data['weather']
                    wind_speed = data['wind']['speed']
                    s = f"The Temperature in {cityName} is {temperature} degree Celsius and Hummidy is {humidity}% and Wind Speed is {wind_speed}"
                    bol_be(s)
                    print(s)
                else:
                    bol_be("City Not Found!")
            except Exception as e:
                bol_be(e)

        # elif "weather" in query:
            # api_key = "Open weather map API key"

            # base_url = "http://api.openweathermap.org/data/2.5/weather?"
            # bol_be(" City name ")
            # print("City name : ")
            # city_name=takeCommand()
            # complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            # response = requests.get(complete_url) 
            # x = response.json() 
            # if x["cod"] != "404": 
            #     y = x["main"] 
            #     current_temperature = y["temp"] 
            #     current_pressure = y["pressure"] 
            #     current_humidiy = y["humidity"] 
            #     z = x["weather"] 
            #     weather_description = z[0]["description"] 
            #     print(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description)) 
            # else: 
            #     bol_be(" City Not Found ")

        # elif "open whatsapp" in query:
        #     bol_be("Opening Whatsapp")
        #     os.startfile("C:/Program Files/WhatsApp/Phone/WhatsApp.exe")

        elif "send a whatsaap message" in query or "send a WhatsApp message" in query:
            driver = webdriver.Chrome('Web Driver Location')
            driver.get('https://web.whatsapp.com/')
            bol_be("Scan QR code before proceding")
            tim=10
            time.sleep(tim)
            bol_be("Enter Name of Group or User")
            name = takeCommanduser()
            bol_be("Enter Your Message")
            msg = takeCommandmessage()
            count = 1
            user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
            user.click()
            msg_box = driver.find_element_by_class_name('_3u328')
            for i in range(count):
                msg_box.send_keys(msg)
                button = driver.find_element_by_class_name('_3M-N-')
                button.click()

        # elif "what is" in query:
        #     sub_query = query.replace("what is", "")
        #     language = 'en-US'
        #     client = Client()
        #     try:
        #         res = client.answer(sub_query, language=language, platform='web')
        #         print(res)
        #         bol_be(str(res))
        #     except:
        #         pass
        #     qry = takeCommand().lower()
        #     bol_be('Searching...')
        #     res = getattr(search, '     search_wiki')(qry)
        #     print(res)
        #     indx = random.randint(0, len(res)-1)
        #     url = res[indx]['url']
        #     webbrowser.open(url)
        #     bol_be(f"Here is what I found for {qry} on the web.")
        #     time.sleep(3)
        #     result = res[indx]['content'][:197]+'. . .'
        #     bol_be(result)
        # except Exception as e:
        #     print(e)

        # elif "what is" in query or "who is" in query:
        #     # res = websocket.search(query,1)
        #     # url = res['results'][0]['url']
        #     # title = res['results'][0]['title']
        #     # print(f"{title} \n {url}")
        #     # Pypdf.speak(title)
        #     # webbrowser.open(url)
        #     search_question(query)
            
        # elif "what is" in query or "who is" in query:
        #     # client= wolframalpha.Client("HLGG97-V25A3GP7G3")
        #     # res = client.query(query)
        #     # try:
        #     #     print(next(res.results).text)
        #     #     bol_be(next(res.results).text)
        #     # except StopIteration:
        #     #     print ("No results")
        #     res = ask_question(query)
        #     try:
        #         print(res)        
        #         bol_be(res)
        #     except:
        #         print('No result found')

        elif "write a note" in query:
            bol_be("What should i write , sir")
            note= takeCommand()
            file = open('Baby.txt','w')
            bol_be("Sir, Should i include date and time")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
        
        elif "show note" in query:
            bol_be("Showing Notes")
            file = open("Baby.txt", "r") 
            print(file.read())
            bol_be(file.read(6))

        elif "Organize Files" in query:
            organize()

        elif "camera" in query or "take a photo" in query:
            ec.capture(0,"Baby Camera ","img.jpg")

        elif "don't listen" in query or "stop listening" in query:
            bol_be("You can awake me by saying wake up Baby")
            is_awake = False

        elif is_awake and "wake up baby" in query:
            response = random.choice([
                "Hey there, it's {}. Time to get this party started!", 
                "Good morning, sleepyhead! It's time for you to be productive.",  
                "Rise and shine, coffee lover! The sun is out today."
            ])
            wishMe()

        elif "Show project Report" in query:
            bol_be("Opening Mega Project Report")
            projectre= r"D:\Colleage\Mini Project\Project Report.pdf"
            os.startfile(projectre)

        elif "countdown of" in query:
            query = int(query.replace("countdown of ",""))
            countdown(query)

        # ---------------OS commands---------------
        elif "open microsoft word" in query:
            bol_be("Opening MS Word")
            execute_command("start winword.exe")

        elif "open command prompt" in query:
            bol_be("Opening Command Prompt")
            execute_command("start cmd.exe")

        elif "open terminal" in query:
            bol_be("Opening Command Prompt")
            execute_command("start cmd.exe")

        elif "open task manager" in query:
            execute_command("start taskmgr.exe")

        elif "open control panel" in query:
            bol_be("Opening Control Pannel")
            execute_command("start control.exe")

        elif "open file explorer" in query:
            bol_be("Opening File Explorer")
            execute_command("start explorer.exe")

        elif "open settings" in query:
            bol_be("Opening Settings App")
            execute_command("start ms-settings:")

        elif "open calculator" in query:
            bol_be("Opening Calculator")
            execute_command("start calc.exe")

        elif "open notepad" in query:
            bol_be("Opening Notepad")
            execute_command("start notepad.exe")
        # # ----------------------Music controls------------------------
        # elif "play music" in query or "resume music" in query:
        #     playmusic()

        # elif "pause music" in  query:
        #     pausemusic()

        # elif "stop music" in query:
        #     stopmusic()
            
        # elif "next track" in query:
        #     nexttrack()

        # elif "previous track" in query:
        #     previoustrack()

        elif "open whatsapp" in query:
            bol_be("Openning Whatsapp")
            execute_command("start whatsapp.exe")

        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            bol_be("Recycle Bin Recycled")

        elif "shutdown" in query:
            bol_be("Shutting down the system")
            execute_command("shutdown /s /t 1")

        elif "restart" in query:
            bol_be("Restarting the system")
            execute_command("shutdown /r /t 1")

        elif "log off" in query:
            bol_be("Logging off")
            execute_command("shutdown /l")

        elif "lock" in query:
            bol_be("Shutting down the system")
            execute_command("rundll32.exe user32.dll,LockWorkStation")

        elif "sleep" in query:
            execute_command("rundll32.exe powrprof.dll,SetSuspendState 0,1")

        elif "increase volume" in query:
            execute_command("nircmd.exe setsysvolume 65535")

        elif "decrease volume" in query:
            execute_command("nircmd.exe setsysvolume 0")

        elif "mute volume" in query:
            execute_command("nircmd.exe mutesysvolume 1")

        elif "unmute volume" in query:
            execute_command("nircmd.exe mutesysvolume 0")

        # elif "set volume level to" in query:
        #     level = int(query.replace("set volume level to", "").strip())
        #     # execute_command(f"nircmd.exe setsysvolume {level * 655}")
        #     adjust_volume(level)

        elif "change brightness to " in query:
            query=query.replace("change brightness to","")
            brightness = query 
            c = wmi.WMI(namespace='wmi')
            methods = c.WmiMonitorBrightnessMethods()[0]
            methods.WmiSetBrightness(brightness, 0)

        elif "set volume to "in query:
            level = int(query.split(" ",0)[1])
            adjust_volume(level)
        
        # elif "volume" in query:
        #     change_volume(query)

        elif "close" in query and "terminate" in query:
            command = query.split(" ",2)[3]
            try:
                os._execute(f"/kill {command[1]}")
                bol_be(f"Closed program '{command[1]}'")
            except Exception as e:
                bol_be(e)

        # elif 'change background' in query:
        #     path = gen.get_background()
        #     bgset.start(path)
        #     bol_be('Background changed!')

        # elif "Baby" in query:
        #     wishMe()
        #     bol_be(assname, "in your service Mister")


        # --------------Live object detection--------------
        elif "scan object" in query or "what is in my hand" in query:
            scan_object()
            bol_be("Searching boss")
        
        
        # ---------------Gesture Controller---------------
        # elif 'launch gesture recognition' in query:
        #     if Gesture_Controller.GestureController.gc_mode:
        #         bol_be('Gesture recognition is already active')
        #     else:
        #         gc = Gesture_Controller.GestureController()
        #         t = Thread(target = gc.start)
        #         t.start()
        #         bol_be('Launched Successfully')

        # elif ('stop gesture recognition' in query) or ('top gesture recognition' in query):
        #     if Gesture_Controller.GestureController.gc_mode:
        #         Gesture_Controller.GestureController.gc_mode = 0
        #         bol_be('Gesture recognition stopped')
        #     else:
        #         bol_be('Gesture recognition is already inactive')


        #  --------------File Navigation----------------- 

        elif 'list' in query:
            counter = 0
            path = 'C://'
            files = listdir(path)
            filestr = ""
            for f in files:
                counter+=1
                print(str(counter) + ':  ' + f)
                filestr += str(counter) + ':  ' + f + '<br>'
            file_exp_status = True
            bol_be('These are the files in your root directory')
            
        elif file_exp_status == True:
            counter = 0   
            if 'open' in query:
                if isfile(join(path,files[int(query.split(' ')[-1])-1])):
                    os.startfile(path + files[int(query.split(' ')[-1])-1])
                    file_exp_status = False
                else:
                    try:
                        path = path + files[int(query.split(' ')[-1])-1] + '//'
                        files = listdir(path)
                        filestr = ""
                        for f in files:
                            counter+=1
                            filestr += str(counter) + ':  ' + f + '<br>'
                            print(str(counter) + ':  ' + f)
                        bol_be('Opened Successfully')
                        
                    except:
                        bol_be('You do not have permission to access this folder')
                                        
            if 'back' in query:
                filestr = ""
                if path == 'C://':
                    bol_be('Sorry, this is the root directory')
                else:
                    a = path.split('//')[:-2]
                    path = '//'.join(a)
                    path += '//'
                    files = listdir(path)
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    bol_be('ok')

        # else:
        #     print("I am not functioned to do this !")