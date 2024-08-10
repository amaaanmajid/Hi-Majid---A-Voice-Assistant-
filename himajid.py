from ollama import chat
import speech_recognition as sr
from datetime import date
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import threading
import queue
import time
import keyboard  # Import the keyboard library
from datetime import datetime
mixer.init()

today = str(date.today())

numtext = 0
numtts = 0
numaudio = 0

messages = []

def chatfun(request, text_queue, llm_finished, stop_event):
    global numtext, messages

    messages.append({'role': 'user', 'content': request})

    response = chat(
        model='llama3',
        messages=messages,
        stream=True,
    )

    shortstring = ''
    reply = ''
    append2log(f"AI: ")

    for chunk in response:
        if stop_event.is_set():  # Check if stop event is set
            break
        
        ctext = chunk['message']['content']
        shortstring = "".join([shortstring, ctext])

        if len(shortstring) > 40:
            print(shortstring, end='', flush=True)

            text_queue.put(shortstring.replace("*", ""))
            numtext += 1
            reply = "".join([reply, shortstring])
            shortstring = ''

        time.sleep(0.2)

    if len(shortstring) > 0:
        print(shortstring, end='', flush=True)
        shortstring = shortstring.replace("*", "")
        text_queue.put(shortstring)
        numtext += 1
        reply = "".join([reply, shortstring])

    messages.append({'role': 'assistant', 'content': reply})
    append2log(f"{reply}")

    llm_finished.set()  # Signal completion of the text generation by LLM

def speak_text(text):
    mp3file = BytesIO()
    tts = gTTS(text, lang="en", tld='us')
    tts.write_to_fp(mp3file)

    mp3file.seek(0)

    try:
        mixer.music.load(mp3file, "mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)

    except KeyboardInterrupt:
        mixer.music.stop()
        mp3file.close()

    mp3file.close()

def text2speech(text_queue, textdone, llm_finished, audio_queue, stop_event):
    global numtext, numtts

    while not stop_event.is_set():  # Keep running until stop_event is set
        if not text_queue.empty():
            text = text_queue.get(timeout=0.5)  # Wait for 0.5 seconds for an item

            numtts += 1

            mp3file = BytesIO()
            tts = gTTS(text, lang="en", tld='us')
            tts.write_to_fp(mp3file)

            audio_queue.put(mp3file)

            text_queue.task_done()

        if llm_finished.is_set() and numtts == numtext:
            time.sleep(0.2)
            textdone.set()
            break

def play_audio(audio_queue, textdone, stop_event):
    global numtts, numaudio

    while not stop_event.is_set():  # Keep running until stop_event is set
        if audio_queue.empty() and textdone.is_set():
            break

        if not audio_queue.empty():
            mp3audio = audio_queue.get()

            numaudio += 1

            mp3audio.seek(0)

            mixer.music.load(mp3audio, "mp3")
            mixer.music.play()

            while mixer.music.get_busy():
                time.sleep(0.1)

            audio_queue.task_done()

def append2log(text):
    global today
    fname = 'chatlog-' + today + '.txt'
    with open(fname, "a", encoding='utf-8') as f:
        f.write(text + "\n")

def main():
    global today, numtext, numtts, numaudio, messages

    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold = False
    rec.energy_threshold = 400
    sleeping = True

    # Define the stop event
    stop_event = threading.Event()
    
    def stop_listening():
        stop_event.set()
    import requests
    def extract_city(request):
    # Simple implementation to extract city from request. Modify as needed.
    # This could be a more sophisticated NLP process.
        city = request.split("in")[-1].strip()
        return city
    def greeting():
        from datetime import datetime
        import pytz

        # Define the timezone
        timezone = pytz.timezone("Asia/Kolkata")  # Replace with your timezone

        # Get current time in that timezone
        now = datetime.now(timezone)

        # Extract current time
        current_time = now.time()

        # Define time ranges including early morning hours
        morning_start = datetime.strptime("00:00:00", "%H:%M:%S").time()
        morning_end = datetime.strptime("12:00:00", "%H:%M:%S").time()
        afternoon_start = datetime.strptime("12:00:00", "%H:%M:%S").time()
        afternoon_end = datetime.strptime("16:00:00", "%H:%M:%S").time()
        evening_start = datetime.strptime("16:00:00", "%H:%M:%S").time()
        evening_end = datetime.strptime("23:59:59", "%H:%M:%S").time()

        # Print greeting based on the time of day
        if morning_start <= current_time < morning_end:
            return "Good Morning"
        elif afternoon_start <= current_time < afternoon_end:
            return "Good Afternoon"
        elif evening_start <= current_time <= evening_end:
            return "Good Evening"






    def get_weather(city):
        api_key = 'cbdb278933f319813c5a544f13259f77'  # Your API key
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'  # Use 'imperial' for Fahrenheit
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        if data.get('cod') != 200:
            return "I couldn't fetch the weather information. Please try again."

        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        return f"The current temperature in {city} is {temperature}°C with {weather_description}."

        
        # Set up the listener for the 'q' key
    keyboard.add_hotkey('q', stop_listening)

    while True:
        with mic as source:
            rec.adjust_for_ambient_noise(source, duration=1)

            print("Listening ...")

            try:
                audio = rec.listen(source, timeout=20, phrase_time_limit=30)
                text = rec.recognize_google(audio, language="en-EN")

                if sleeping:
                    if "majid" in text.lower():
                        request = text.lower().split("majid")[1]
                        sleeping = False
                        append2log(f"_" * 40)
                        today = str(date.today())
                        messages = []

                        if len(request) < 2:
                            greetingtext= greeting()
                            speak_text(f"Hi, there, {greetingtext} my name is majid. how can I help?")
                            append2log(f"AI: Hi, there,{greetingtext} my name is majid. how can I help? \n")
                            continue

                    else:
                        continue

                else:
                    request = text.lower()

                    if "that's all" in request:
                        append2log(f"You: {request}\n")
                        speak_text("Bye now")
                        append2log(f"AI: Bye now. \n")
                        print('Bye now')
                        sleeping = True
                        continue

                    if "your name" in request:
                        append2log(f"You: {request}\n")
                        speak_text("my name is majid")
                        append2log(f"AI: my name is majid \n")
                        print('my name is majid')
                        sleeping = True
                        continue
                    if "weather" in request:
                        city = extract_city(request)  # Implement this function to extract city from request
                        weather_info = get_weather(city)
                        append2log(f"You: {request}\n")
                        speak_text(weather_info)
                        append2log(f"AI: {weather_info}\n")
                        print(weather_info)
                        sleeping = True
                        continue
                    if "temperature" in request:
                        city = extract_city(request)  # Implement this function to extract city from request
                        weather_info = get_weather(city)
                        append2log(f"You: {request}\n")
                        speak_text(weather_info)
                        append2log(f"AI: {weather_info}\n")
                        print(weather_info)
                        sleeping = True
                        continue
                    
                    if "majid" in request:
                        request = request.split("majid")[1]

                    append2log(f"You: {request}\n ")

                    print(f"You: {request}\n AI: ", end='')

                    text_queue = queue.Queue()
                    audio_queue = queue.Queue()

                    llm_finished = threading.Event()
                    textdone = threading.Event()

                    stop_event.clear()

                    llm_thread = threading.Thread(target=chatfun, args=(request, text_queue, llm_finished, stop_event))
                    tts_thread = threading.Thread(target=text2speech, args=(text_queue, textdone, llm_finished, audio_queue, stop_event))
                    play_thread = threading.Thread(target=play_audio, args=(audio_queue, textdone, stop_event))

                    llm_thread.start()
                    tts_thread.start()
                    play_thread.start()

                    llm_thread.join()
                    time.sleep(0.5)
                    audio_queue.join()

                    stop_event.set()
                    tts_thread.join()
                    play_thread.join()

                    numtext = 0
                    numtts = 0
                    numaudio = 0

                    print('\n')

            except Exception as e:
                continue
    

if __name__ == "__main__":
    main()
