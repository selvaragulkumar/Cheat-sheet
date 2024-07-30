import csv
import requests
import json
import openai
from bs4 import BeautifulSoup
import pandas as pd

#input config

url = "<website-url>"
key="<openai-api-key>"


prompt='''
Categorize the entire page to work as a cheat sheet, only extract the major content from it.
Do not just give the entire webpage content as a cheat sheet, extract major contents and tabluate it into repective coloumns to make sense, tabulate kiterally everything in multiple coloumns if necessary
Identifiy the main subjects in the webpage, create coloumns based on what fits best, according to the content in the webpage, it should come about a cheat sheet table
This should serve as a sumarized short cheat sheet to understand the intention of the webpage in a tabular format, only extract the major things to tabulate.
return it as a json. remember double qoutes
Do not include feedback

example:
    This is a sample cheat sheet for a webpage that has a How to do manual
    the coloumns are main sibjects dicussed in the specific webpage, hence just consider it as an example
    
    Add a monitor:
        
            step: Add config
            detail: do that and do this
            option: do this
            
            step: <>
            detail: <>
            option: <>
            
    Configure options:
        
            Option: Add one more
            Detail: <>

The json you return will be parsed hence dont give any comments or quotes, just return the dictionary!!
Text: {document_text}
'''

def extract_main_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Target the div with class 'content'
            main_content = soup.find('div', {'class': 'content'})

            if main_content:
                # Extract and clean the text
                text = main_content.get_text(separator=' ', strip=True)
                return text
            else:
                print("Main content not found on the webpage.")
                return None
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

webpage_text = extract_main_content(url)

if webpage_text:
    document = webpage_text
else:
    document = "Failed to extract text from the main content of the webpage."

def create_prompt_1():
    return prompt.format(document_text=document)

def call_openai_api_1(prompt=create_prompt_1()):
    openai.api_key = key
    response = openai.chat.completions.create(
      model="gpt-4o",
      temperature=0,
      messages=[
            {"role": "system", "content": "You are a helpful agent that generates cheat sheet from webpages"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

json_file= call_openai_api_1()

print(json_file)

json_file=json.loads(json_file)

with open('cheat_sheet_json.json', 'w') as json1:
    json.dump(json_file, json1, indent=4)




