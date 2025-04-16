import pyttsx3
import google.generativeai as genai
from langdetect import detect
import speech_recognition as sr

engine = pyttsx3.init()



API_KEY = "key"  
genai.configure(api_key=API_KEY)


model = genai.GenerativeModel("gemini-pro")


def set_voice(language):
    voices = engine.getProperty('voices')
    for voice in voices:
        if language in voice.name.lower():
            engine.setProperty('voice', voice.id)
            return True
    return False



def Takecomand():
    command = sr.Recognizer()
    with sr.Microphone() as mc:
        print("say command sir................... ")
        command.phrase_threshold =1
        audio =command.listen(mc)
        try:
            print('recording...')
            quer =command.recognize_google(audio,language='ar')
            print(f'you said :  {quer}')
        except Exception as Error:
            return None
        return  quer.lower()







def chat():
    print("مرحبًا بك في شات بوت Gemini! اكتب 'خروج' لإنهاء الدردشة.")
    while True:
       
        user_input = Takecomand()
        if user_input.lower() == "خروج":
            print("تم إنهاء الدردشة. إلى اللقاء!")
            break
        
        # Get the response from Gemini
        response = model.generate_content(user_input)
        
        # Extract the text from the response
        response_text = response.text
        
        # Print the response
        print("Gemini:", response_text)
        
        # Detect the language of the response
        try:
            lang = detect(response_text)
            print(f"Detected language: {lang}")
            
            # Set the voice based on the detected language
            if lang == 'ar':  # Arabic
                if not set_voice('arabic'):
                    print("Arabic voice not found! Using default voice.")
            elif lang == 'en':  # English
                if not set_voice('english'):
                    print("English voice not found! Using default voice.")
            else:
                print(f"Unsupported language: {lang}. Using default voice.")
        except Exception as e:
            print(f"Error detecting language: {e}")
        
        # Speak the response
        engine.say(response_text)
        engine.runAndWait()

# Start the chat
chat()