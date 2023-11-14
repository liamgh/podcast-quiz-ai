from pathlib import Path
from openai import OpenAI
client = OpenAI()

speech_file_path = "speech-gv.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="nova",
  #input=""""[ENGLISH WOMAN] This is the  latest shipping forecast for Kent, UK.
  #
  #  During the afternoon, East and Southeast England, including Kent, will experience dry and sunny weather. Winds will be light and variable, with some patches of fog possibly persisting. Temperatures are expected to range between 5-7°Celcius.
  #  Into the evening, the area will continue to see clear skies and dry conditions, with temperatures falling quickly after sunset due to light to calm winds.
  #  Overnight, the forecast predicts a dry and clear night with variable cloud amounts. Rain will move eastwards along the south coast, becoming patchy from Dorset to Kent during the afternoon. Temperatures will be around 6-8°Celcius, but it may feel cooler due to a fresh south/southwest wind along the coast
  #"""
  input="""
Ta Ruth Keggin ginsh dooin mychione yn Chooish 2023.
Shoh coloayrtys rish yn Ghreinneyder, Oaseir ny Gaelgey da Culture Vannin, Ruth Keggin Gell, mychione yn Chooish 2023. S'treih lhiam nagh row eh ry chlashtyn ayns 'Traa dy Liooar' Jelune 30oo Jerrey Fouyir, agh shoh eh nish.
"""
)

response.stream_to_file(speech_file_path)