# podcast-quiz-ai By Liam Green-Hughes
This is an experimental AI powered quiz podcast generator that uses OpenAI's ChatGPT and Text-To-Speech APIs to generate a ten-ish minute long quiz podcast. The program is quite rough and ready as it was meant for experimentation. The music clip used in the podcasts was generated by Facebook's MusicGen AI music generator. 

## Dependencies

### FFMPEG
Install from here: https://ffmpeg.org/
On Windows you can copy ffmpeg.exe to the same folder as these scripts if you want.

### Python
pip install openai pydub

### OpenAI
You will need an OpenAI API account to use this program. See [OpenAI Platform QuickStart Tutorial](https://platform.openai.com/docs/quickstart?context=python). The environment variable OPENAI_API_KEY must have the value of your API key.

** Usage of this project will incur charges with the OpenAI platform. ** I would recommend setting a spending limit.

## Usage
Creating a podcast quiz with this program is a two part process. You will need a command line to run these scripts and to be in the same directory as the files below.

### genquiz.py
This program generate a script for the quiz. Alter the *topic* to the subject you would like the whole quiz to be about, e.g. "General Knowledge", "Kent and Medway history". Alter the *language* as desired. When you run this script it should eventually output a "script.txt" file in the output folder. You can edit this if you wish to check for anything the AI has got wrong.

### performquiz.py
This script uses OpenAI's Text-To-Speech services to turn the script.txt file into an audio MP3 file. Output is generated in chunks the combined into a single MP3. The script also does things like voice switching for the different contestants and inserting sound effects. Run this after generating a quiz and a file named *00aiquiz.mp3*.

## Known issues
Sometimes ChatGPT doesn't get all of its facts right! If you are going to rely on this podcast for revision or other uses then I would recommend that you edit the script before generating the podcast.

Copyright Liam Green-Hughes 2023, licences under GPL3.

