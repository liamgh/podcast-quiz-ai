import io
import re
import random
import shutil 
from pathlib import Path
from openai import OpenAI

client = OpenAI()

# TODO Change to a class

male_voices = ("alloy", "echo", "fable", "onyx")
female_voices = ("alloy", "fable", "nova", "shimmer")
allocated_voices = {}
current_voice = ""
used_voices = ["none"]
file_id = 0

def change_voice(line):
    global current_voice
    current_voice = line
    if current_voice not in allocated_voices:
        # allocate voice
        print("Need to allocate voice for ", line)
        allocated_voices[current_voice] = allocate_voice(line)
        print(allocated_voices)

def speak(line):
    global current_voice
    global file_id
    print(current_voice, "/", allocated_voices[current_voice], ": ", line)
    speech_file_path = "output/part%d.mp3" % (file_id)
    response = client.audio.speech.create(
        model="tts-1",
        voice=allocated_voices[current_voice],
        input=line
    )
    response.stream_to_file(speech_file_path)
    file_id= file_id +1

def parse_speaker_id(line):
    person = {"id": "", "gender": "", "number": 0}
    parts = re.search(r"\[(CONTESTANT|HOST) \((male|female)\)\s?(\d)?\]", line)
    if parts != None:
        person["id"] = parts.group(1)
        person["gender"] = parts.group(2)
        if len(parts.groups()) == 3:
            person["number"] = parts.group(3)
    return person

def allocate_voice(line):
    voice = "none"
    person = parse_speaker_id(line)
    while voice in used_voices:
        if person["gender"] == "female":
            voice = random.choice(female_voices)
        else:
            voice = random.choice(male_voices)
    used_voices.append(voice)
    return voice   

def process_line(line):
    line = line.strip()
    if line == "":
        return 
    
    if line.startswith("[SFX:music"):
        play_music()
    elif line.startswith("[SFX:buzzer]"):
        add_buzzer()
    elif line.startswith("[SFX:correct]"):
        add_correct_sound()
    elif line.startswith("[SFX:wrong]"):
        add_wrong_sound()
    elif line.startswith("[HOST "):
        change_voice(line)
    elif line.startswith("[CONTESTANT "):
        change_voice(line)
    else:
        speak(line)

def play_music():
    add_file("sfx-music-betweenrounds.mp3","mp3")

def add_buzzer():
    add_file("chime.wav","wav")

def add_correct_sound():
    add_file("correct.wav","wav")

def add_wrong_sound():
    add_file("wrong.wav","wav")

def add_file(source, ext):
    global file_id
    shutil.copyfile(source, "output/part%d.%s" % (file_id, ext))
    file_id = file_id + 1

with io.open("output/script.txt", "r", encoding='utf8') as f:
    for line in f.readlines():
        print(line)
        process_line(line)
    f.close()