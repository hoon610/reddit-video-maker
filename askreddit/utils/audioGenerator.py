import os
import re
import json
import pyttsx3
import random
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from dotenv import load_dotenv

load_dotenv()

voices = [
    "Adam",
    "Antoni",
    "Arnold",
    "Domi",
    "Elli",
    "Josh",
    "Rachel",
    "Sam",
]

class elevenlabsRunner:
    def __init__(self):
        self.max_chars = 2500
        self.voices = voices

    def run(self, text, filepath, random_voice: bool = False):
        if random_voice:
            voice = self.randomvoice()
        else:
            voice = "Elli"

        text = self.processText(text)

        api_key=os.getenv("ELEVENLABS_API_KEY")

        client = ElevenLabs(
          api_key=api_key 
        )

        audio = client.generate(text=text, voice=voice, model="eleven_multilingual_v1")
        save(audio=audio, filename=filepath)

    def randomvoice(self):
        return random.choice(self.voices)
    
    def processText(self, text):

        with open('swears.json', 'r') as f:
            swears = json.load(f)

        words = text.split()
        for i in range(len(words)):
            if words[i] in swears:
                words[i] = swears[words[i]]
        text = ' '.join(words)
        text = re.sub(r'http\S+|www.\S+', '', text, flags=re.MULTILINE)
        text = text.replace('*', '')

        return text



def soundifyAuthor(title, asker):

    elevenlabs = elevenlabsRunner()
    elevenlabs.run(title, asker+"/temp"+"0"+".mp3", random_voice=True)


def soundifyComment(comment, index, sectionid, asker):
    sectionid = str(sectionid).zfill(2)

    elevenlabs = elevenlabsRunner()
    elevenlabs.run(comment, asker+"/temp"+index+"_"+sectionid+".mp3")

'''
for voice in voices:
    print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop()
'''