import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests
import wikipedia
from config import OPENWEATHER_API_KEY, NEWS_API_KEY

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How can I assist you today?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
    except Exception:
        speak("Sorry, I didn’t catch that. Please repeat.")
        return "None"
    return query.lower()

# ---------------- API Features ----------------

def get_weather(city="London"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        speak(f"The weather in {city} is {desc} with a temperature of {temp} degree Celsius.")
    else:
        speak("Sorry, I couldn't fetch the weather right now.")

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    if response.get("articles"):
        speak("Here are the top 3 headlines.")
        for i, article in enumerate(response["articles"][:3], 1):
            speak(f"Headline {i}: {article['title']}")
    else:
        speak("Sorry, I couldn't fetch the news.")

def get_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    speak(response.get("joke", "Couldn't find a joke right now."))

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(f"According to Wikipedia: {result}")
    except:
        speak("Sorry, I could not find information on that.")

# ---------------- Main ----------------
def main():
    wish_user()
    while True:
        query = take_command()

        if "time" in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif "play music" in query:
            music_dir = "C:\\Users\\Public\\Music"  # change this
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Playing music")
            else:
                speak("No music found")

        elif "weather" in query:
            speak("Please tell me the city name")
            city = take_command()
            if city != "None":
                get_weather(city)

        elif "news" in query:
            get_news()

        elif "joke" in query:
            get_joke()

        elif "wikipedia" in query:
            topic = query.replace("wikipedia", "").strip()
            search_wikipedia(topic)

        elif "exit" in query or "quit" in query:
            speak("Goodbye! Have a great day.")
            break

if __name__ == "__main__":
    main()
