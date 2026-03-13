import speech_recognition as sr

def get_voice_query():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak your query...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except:
        return "Could not understand voice"