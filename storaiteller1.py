import ollama
import re
import json


model='llama3.2'
#model='storaitellermodel'
currentprompt='Write a story of 100 words.'
initialprompt = currentprompt
jsonfilename = "training_stories.json"
csvfilename = "data_stories.csv"

#model='mywriter1'
#prompt='You are a writer. write a story of maximum 100 words'
#response = ollama.generate(model, prompt)
#print(response['response'])


import asyncio
from ollama import AsyncClient
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

def save_story_in_jsonfile(filename, line):

    try:
        with open(filename, 'a', encoding='utf-8') as file:  # 'a' for append mode, encoding for UTF-8
            #file.write(line + "\n")
            json.dump (line, file, indent = 6)
    except Exception as e:
        print(f"An error occurred: {e}")

# save the story in the csv file data_stories.csv
def save_story_in_csvfile(filename, line):

    try:
        with open(filename, 'a', encoding='utf-8') as file:  # 'a' for append mode, encoding for UTF-8
            file.write(line + "\n")
            
    except Exception as e:
        print(f"An error occurred: {e}")


app = FastAPI()

# necessary to allow post api calls from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# payload sent by the frontend to configure the prompt
class Payload(BaseModel):
    maincharacter: str 
    keywords: str
    genre: str
    registro: str
    childsafe: bool
    maxnowords: int
    twist: bool


# payload sent by the frontend to redo one part of the story
class Storyparts(BaseModel):
    textbefore: str
    textselected: str
    textafter: str

# update the prompt global variable
def update_prompt (prompt):
    global currentprompt
    currentprompt = prompt

# payload sent by the frontend to configure the prompt
class Payloadsavestory(BaseModel):
    maincharacter: str 
    keywords: str
    genre: str
    registro: str
    childsafe: bool
    maxnowords: int
    twist: bool
    story: str

# API call from the frontend to get the parameters and define the prompt accordingly
@app.post("/setstory/")
async def writestory(params: Payload):
    print ("Write story" + params.json())
    try:
        
        if (params.twist):
            prompt="You are a writer. write a story, without extra comments or questions, of maximum " + str(params.maxnowords) + " words, where the main characters names are " + params.maincharacter + ". the story genre is " + params.genre + " and you have to use a " + params.registro + " register. The keywords of the story are " + params.keywords + ". the story has to have an introduction, a development and a finale with a twist." 
        else: prompt="You are a writer. write a story, without extra comments or questions, of maximum " + str(params.maxnowords) + " words, where the main characters names are " + params.maincharacter + ". the story genre is " + params.genre + " and you have to use a " + params.registro + " register. The keywords of the story are " + params.keywords + ". the story has to have an introduction, a development and a finale."
        if(params.childsafe):    
                prompt= prompt + "The content must be child-friendly. The story might not involve children."
        print (prompt)
        update_prompt (prompt)
        global initialprompt
        initialprompt = prompt
        return {prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing job: {str(e)}")

# websocket to send the generate text from the backend tot he frontent in stream mode
async def writeinstreaming(websocket: WebSocket):

    global currentprompt
    message = {'role': 'user', 'content': currentprompt}
    print ("Current promtp is: " + currentprompt)
    try:
        # Notify client connection
        await websocket.accept()
        # Generate and send text in streaming mode
        async for part in await AsyncClient().chat(model, messages=[message], stream=True):
            content = part['message']['content']
            await websocket.send_text(content)
    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        await websocket.close()

# open web socket when receives the request
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await writeinstreaming(websocket)

# API call from the frontend to request a partial regeneration of the story
@app.post("/redopartstory/")
async def redopartstory(parts: Storyparts):
    try:
        print (parts.json())
        global currentprompt
        global initialprompt
        print ("redo")
        newprompt = initialprompt + "It is important that the story includes exactly this part at the beginning: '" + parts.textbefore + "' and exactly this part at the end: '" + parts.textafter + "'"
        print (newprompt)
        update_prompt (newprompt)
        return {newprompt}
        #return currentprompt
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing job: {str(e)}")


# API call from the frontend to request to store the story for the fine tuning process
@app.post("/savestory/")
async def savestory(storytobesaved: Payloadsavestory):
    try:
        print (storytobesaved.json())
        if (storytobesaved.twist):
            prompt="You are a writer. write a story, without extra comments or questions, of maximum " + str(storytobesaved.maxnowords) + " words, where the main characters names are " + storytobesaved.maincharacter + ". the story genre is " + storytobesaved.genre + " and you have to use a " + storytobesaved.registro + " register. The keywords of the story are " + storytobesaved.keywords + ". the story has to have an introduction, a development and a finale with a twist." 
        else: prompt="You are a writer. write a story, without extra comments or questions, of maximum " + str(storytobesaved.maxnowords) + " words, where the main characters names are " + storytobesaved.maincharacter + ". the story genre is " + storytobesaved.genre + " and you have to use a " + storytobesaved.registro + " register. The keywords of the story are " + storytobesaved.keywords + ". the story has to have an introduction, a development and a finale."
        if(storytobesaved.childsafe):    
                prompt= prompt + "The content must be child-friendly."
        
        #stringtosave="{'text': '<s>[INST] " + prompt + " [/INST]  " + storytobesaved.story + "</s>'}"
        #global jsonfilename
        #save_story_in_jsonfile(jsonfilename, stringtosave)

        stringtosave = prompt + "," + storytobesaved.story
        global csvfilename
        save_story_in_csvfile(csvfilename, stringtosave)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing job: {str(e)}")


#create the uvicorn process that works as webserver
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



