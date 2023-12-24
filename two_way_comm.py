import speech_recognition as sr
import os
import gtts
from playsound import playsound
import RPi.GPIO as GPIO
from time import sleep
#back
in4 = 17
enb1 = 27
in3 = 22
in1 = 24
in2 = 23
ena1 = 25
#front
in2_4 = 9
enb2 = 10
in2_3 = 11
in2_1 = 7
in2_2 = 8
ena2 = 26
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(ena1,GPIO.OUT)
GPIO.setup(enb1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

GPIO.setup(in2_1,GPIO.OUT)
GPIO.setup(in2_2,GPIO.OUT)
GPIO.setup(in2_3,GPIO.OUT)
GPIO.setup(in2_4,GPIO.OUT)
GPIO.setup(ena2,GPIO.OUT)
GPIO.setup(enb2,GPIO.OUT)
GPIO.output(in2_1,GPIO.LOW)
GPIO.output(in2_2,GPIO.LOW)
GPIO.output(in2_3,GPIO.LOW)
GPIO.output(in2_4,GPIO.LOW)
p=GPIO.PWM(ena1,1000)
q=GPIO.PWM(enb1,1000)
t=GPIO.PWM(ena2,1000)
u=GPIO.PWM(enb2,1000)

q.start(25)
p.start(25)
t.start(25)
u.start(25)

recognizer = sr.Recognizer()

try:
    # List available microphones
    print("Available microphones:")
    print(sr.Microphone.list_microphone_names())

    # Select a specific microphone (optional)
    # with sr.Microphone(device_index = 1) as source:

    with sr.Microphone() as source:
        print("Adjusting noise...")
        recognizer.adjust_for_ambient_noise(source, duration = 1)
        tts = gtts.gTTS("Hi. I am Assist Bot. How can I help you?")
        tts.save("hello.mp3")
        playsound("hello.mp3")
        print("Recording audio for 15 seconds...")
        recorded_audio = recognizer.listen(source, timeout = 15)
        print("Done recording.")

except sr.UnknownValueError:
    print("Google Speech Recognition couldn't understand the audio.")
except sr.RequestError:
    print("Couldn't request results from Google Speech Recognition service.")
except Exception as ex:
    print("Error during recognition: ", ex)
    
try:
    print("Recognizing the text..")
    text = recognizer.recognize_google(recorded_audio, language = "en-US")
    print("Decoded Text: {}".format(text))
    if 'forward' in text:
        print("User said forward.")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        GPIO.output(in2_1,GPIO.HIGH)
        GPIO.output(in2_2,GPIO.LOW)
        GPIO.output(in2_3,GPIO.HIGH)
        GPIO.output(in2_4,GPIO.LOW)
        sleep(5)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        GPIO.output(in2_1,GPIO.LOW)
        GPIO.output(in2_2,GPIO.LOW)
        GPIO.output(in2_3,GPIO.LOW)
        GPIO.output(in2_4,GPIO.LOW)

except sr.UnknownValueError:
    print("Google Speech Recognition couldn't understand the audio.")
except sr.RequestError:
    print("Couldn't request results from Google Speech Recognition service.")
except Exception as ex:
    print("Error during recognition: ", ex)
