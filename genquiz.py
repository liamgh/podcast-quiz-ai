from openai import OpenAI
import io

# Change these settings to your preferences
model_name="gpt-4-1106-preview"
topic="1980s British computer products and companies"
language="British English"
# End

client = OpenAI()
message_stack =  [{"role": "system", "content": "You are a helpful assistant."}]

initial_prompt = """
Create a %s themed radio quiz show in %s script with a host and three contestants. 
Begin with introductions. Use the structure below, inserting sound effect placeholders and ensuring contestants occasionally answer incorrectly, allowing others to earn bonus points. Only use real questions and answers. Only use specified options for SFX. Do not add descriptions of what is happening.
There are no commercial breaks. Write out numbers or years in dialogue as text. Do not end the quiz or say goodbye until told to.
Use this structure and respect newlines:
[SFX:music|buzzer|correct|wrong]
[HOST (male|female)|CONTESTANT (male|female) 1|2|3]
text
"""

def call_completions(message_content):
    message_stack.append({"role": "user", "content": message_content})
    response = client.chat.completions.create(
        model=model_name,
        messages=message_stack
    )
    gentext = response.choices[0].message.content
    print(gentext)
    message_stack.append({"role": "assistant", "content": gentext})
    return gentext

with io.open("output/script.txt", "w", encoding='utf8') as f:
    f.write(call_completions(initial_prompt % (topic, language)))
    f.write(call_completions("Generate the next round"))
    f.write(call_completions("Generate the last round"))
    f.write(call_completions("End quiz with score, the winner and thank yous. Say goodbye until next time."))
    f.close()

# Copyright Liam Green-Hughes 2023
#
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 