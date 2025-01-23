'''
To Run:
``python test.py``
'''

from openai import OpenAI

client = OpenAI(api_key="--- insert API key here ----")
import pandas as pd
import numpy as np

#Read in your CSV file
data = pd.read_csv("test_data-full-cropped-input.csv") # <------ Change input file name here

# Create a new column for the GPT output
data['gpt_output'] = None

# Define the function to get ChatGPT response
def ask_chatgpt(party, message):
    # Prepare the prompt
    prompt = (
        f"""Given a tweet and the author's party affiliation (Democrat or Republican), assign one of these labels:
            0: The message reflects typical positions or rhetoric associated with the author's party affiliation 1: The message contradicts or challenges typical positions associated with the author's party affiliation 2: The message is politically neutral or focused on general updates, celebrations, or acknowledgments
            Consider both the explicit content and underlying tone/implications when assessing party alignment. Focus on whether the message would be generally expected from someone of that party affiliation in contemporary American politics.

            please return in the form of a csv without altering the tweets itself. please label all the tweets
            party: {party}
            text: {message} 
        """
    )

    # Call the OpenAI API to create the chat completion
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0)

    # Return the content of the response
    return response.choices[0].message.content.strip()

# Iterate over each row in the DataFrame and call the GPT function
for index, row in data.iterrows():
    party = row['party']
    message = row['text_for_analysis']
    gpt_response = ask_chatgpt(party, message)
    data.at[index, 'gpt_output'] = gpt_response # GPT response itr saved into data['gpt_output'] column created above
    print(f"Row {index + 1} - GPT Output: {gpt_response}")

data.to_csv("test_data-full-output-35.csv", index=False) # <------ Change desired output file name here

# Print the modified DataFrame to the terminal
print(data)
