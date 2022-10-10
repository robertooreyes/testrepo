import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', rate-50)

action = input(">> Enter text:  ")

def speak(audio):
	engine.say(audio)
	engine.runAndWait()

while action != 'quit':
	speak(action)
	action = input("\n>> Enter text:  ")