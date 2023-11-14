from openai import OpenAI
import io

client = OpenAI()
message_stack =  [{"role": "system", "content": "You are a helpful assistant."}]

model_name="gpt-4-1106-preview"
topic="Gravesend, UK"
language="English (UK)"

initial_prompt = """
Create a %s-themed radio quiz show in %s script with a host and three contestants. 
Begin with introductions. Use the structure below, inserting sound effect placeholders and ensuring contestants occasionally answer incorrectly, allowing others to earn bonus points. Use real answers for questions. Only use specified options for SFX. Do not add descriptions of what is happening.
There are no commercial breaks. Write out numbers or years in dialogue as text.
Structure:
[SFX:music|buzzer|correct|wrong]
[HOST (male_female)|CONTESTANT (male|female) number]
text
"""

def call_completions(message_content):
    message_stack.append({"role": "user", "content": message_content})
    response = client.chat.completions.create(
        model=model_name,
        messages=message_stack
    )
    gentext = response.choices[0].message.content
    message_stack.append({"role": "assistant", "content": gentext})
    return gentext

with io.open("output/script.txt", "w", encoding='utf8') as f:
    f.write(call_completions(initial_prompt % (topic, language)))
    f.write(call_completions("Generate the next round"))
    f.write(call_completions("Generate the last round"))
    f.close()