import pyttsx3
import time


def onStart(name):
    print('starting', name)


def onEnd(name, completed):
    print('finishing', name, completed)


def onWord(name, location, length):
    print('word', name[location:location + length], location, length)


engine = pyttsx3.init()
engine.connect('started-utterance', onStart)
engine.connect('finished-utterance', onEnd)
engine.connect('started-word', onWord)

# words per minute
engine.setProperty('rate', 180)

text = 'The quick brown fox jumped over the lazy dog.'
# engine.say(text, text)
engine.save_to_file(text, 'test.wav')
engine.runAndWait()
