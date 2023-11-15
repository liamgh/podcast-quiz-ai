import io
import re
import random
import shutil 
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment
import time

client = OpenAI()

class PerformQuiz:
    voices = {'male': ("alloy", "echo", "fable", "onyx"), 'female': ("alloy", "fable", "nova", "shimmer")}
    allocated_voices = {}
    current_voice = ""
    used_voices = ["none"]
    file_id = 0
    scriptfile = ""
    line = ""
    files = []

    def __init__(self, scriptfile) -> None:
        self.scriptfile = scriptfile

    def change_voice(self):
        person = self.parse_speaker_id()
        if person["hash"] not in self.allocated_voices:
            # allocate voice
            self.allocated_voices[person["hash"]] = self.allocate_voice()
        self.current_voice = person["hash"]

    def get_output_part_path(self, ext):
        self.file_id = self.file_id +1
        filename =  "output/part%02d.%s" % (self.file_id, ext)
        self.files.append(filename)
        return filename

    def speak(self):
        print(self.current_voice, "/", self.allocated_voices[self.current_voice], ": ", self.line)
        response = client.audio.speech.create(
            model="tts-1",
            voice= self.allocated_voices[self.current_voice],
            input=self.line
        )
        response.stream_to_file(self.get_output_part_path("mp3"))       
        # wait a little whicle to space out requests to the API
        print("API rest")
        time.sleep(2)

    def parse_speaker_id(self):
        person = {"id": "", "gender": "", "number": 0}
        parts = re.search(r"\[(CONTESTANT|HOST) \((male|female)\)\s?(\d)?", self.line)
        if parts != None:
            person["id"] = parts.group(1)
            person["gender"] = parts.group(2)
            if len(parts.groups()) == 3 and parts.group(3) is not None and parts.group(3).isnumeric():
                person["number"] = parts.group(3)
        person["hash"] = "%s-%s-%s" % (person["id"], person["gender"], person["number"])
        return person
    
    def allocate_voice(self):
        voice = "none"
        person = self.parse_speaker_id()
        for cvoice in self.voices[person["gender"]]:
            if cvoice not in self.used_voices and voice == "none":
                voice = cvoice
        self.used_voices.append(voice)
        return voice 
    
    def play_music(self):
        self.add_file("sfx-music-betweenrounds.wav")

    def add_buzzer(self):
        self.add_file("chime.wav")

    def add_correct_sound(self):
        self.add_file("correct.wav")

    def add_wrong_sound(self):
        self.add_file("wrong.wav")

    def add_file(self, source):
        ext = source[source.rfind(".")+1:]
        shutil.copyfile(source, self.get_output_part_path(ext))
    
    def process_line(self):
        line = self.line.strip().replace(" ", "")
        if line == "":
            return 
        
        if line.startswith("[SFX:music"):
            self.play_music()
        elif line.startswith("[SFX:buzzer]"):
            self.add_buzzer()
        elif line.startswith("[SFX:correct]"):
            self.add_correct_sound()
        elif line.startswith("[SFX:wrong]"):
            self.add_wrong_sound()
        elif line.startswith("[HOST"):
            self.change_voice()
        elif line.startswith("[CONTESTANT"):
            self.change_voice()
        elif not line.startswith("["):
            self.speak()
        else:
            print("Unrecognised command: ", line)

    def combine_files(self):
        combined_sound = AudioSegment.silent(duration=1)
        for partfile in self.files:
            print("Combining:", partfile)
            combined_sound = combined_sound + AudioSegment.from_file(partfile)
        combined_sound.export("output/00aiquiz.mp3", format="mp3")

    def start(self):
        with io.open(self.scriptfile, "r", encoding='utf8') as f:
            for line in f.readlines():
                self.line = line.strip()
                self.process_line()
            f.close()
        self.combine_files()

perform = PerformQuiz("output/script.txt")
perform.start()


# Copyright Liam Green-Hughes 2023
#
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.                 