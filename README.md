# StorAIteller
This is the repository of the code I have developed for the ARI-3333 Generative AI assignment

## Description of the project
The aim of this project is to make use of LLM technology to create a product that generates fictional stories based on a set of parameters, such as genre, register, keywords, main characters, etc. defined by users through a Web User Interface. 

The objectives of this project are the following: 

- implementation of a textual story generation module based on a Large Language Model (Llama 3.2) to generate a fictional story based on user input (e.g., theme, characters' names and other settings). The generated story has to be coherent and follow a structured narrative with a beginning, a development of the story and a conclusion.
- implementation of a Web User Interface through which users can:
  - define the parameters to be considered for the story generation
  - refine the generated story and regenerate part of it
  - provide a positive feedback to the generated story in order to include the story in an external fine-tuning process
- implementation of the fine-tuning process that applies adapters to the LLM in order to consider the positive feedback provided by the users and enhance the quality of future story generations.
 
## Installation 

The project is made of 4 main modules:
- Ollama platform:
  - Install locally the Ollama platform, see [here](https://github.com/ollama/ollama) 
  - Install the [Ollama library](https://github.com/ollama/ollama-python) for Python
  - Install Llama 3.2 3B parameters 2.0 GB model locally by running the command (Windows cmd): ollama pull llama3.2  
  - Run the LLama 3.2 model by executing this command (Windows cmd): ollama run llama3.2
- Back-end, that is implemented by the StorAIteller.py Python script file that acts as API gateway and bridge between the Ollama platform and the Front-end
  - Install [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) locally
  - Install the [FastAPI](https://github.com/fastapi/fastapi) Python library and [Uvicorn](https://github.com/encode/uvicorn) ASGI Web server for Python
  - Run the StorAIteller.py script available in this repository; this will create a web server listening to host="127.0.0.1" and port=8000 (local machine)
- Front-end that is implemented by the StorAIteller.html and stylesheet.css files, both available in this repository, that need to be installed in the same directory.
- Fine-tuning process, that is implemented by the finetuner.py Python script that has dependencies with the [Unsloth Python library](https://github.com/unslothai/unsloth) and that require also the installation of the [llama.cpp library](https://github.com/ggerganov/llama.cpp). This process must be run in a Linux-Unix environment. If the installation is done on a Windows machine, the [WSL environment](https://github.com/microsoft/WSL) must be installed and the processes must be run inside WSL.
  
## Features

The product has been named **StorAITeller** and this is a detailed description of its features:

1. *Story generation settings* : This section of the product allows the users to define the parameters to be considered for the story generation, such as:
    - Main characters' names, a free text field where the users can input the characters' names separated by a comma;
    - Story keywords, a free text field where the users can input the main keywords of the story separated by a comma;
    - Genre, a drop-down field where the user can select one of the following genre of the story:
      - Adventure
      - Biography
      - Comedy
      - Drama
      - Fantasy
      - Gothic
      - Historical
      - Horror
      - Mistery
      - Quirky
      - Romance
      - Scy-fy
      - Thriller
      - Tragedy
      - War
   - Register, a drop-down field where the user can select one of the following registers to be used as style to write the story:
      - Casual
      - Cerebral
      - Conversational
      - Descriptive
      - Direct
      - Elegant
      - Formal
      - Irreverent
      - Playful
      - Vivid
    - Child-friendly content, a checkbox field that, if selected, instructs the generative model to write a content that is suitable for children
    - Max number of words, a text field that accepts only integers that define the maximum length of the story
    - Final twist, a checkbox that, if selected, instructs the generative model that the story must have a twist in its finale.
            
    The users can submit the settings, by clicking on the * *Submit* * button; by submitting the story settings the prompt for the generation of the story is assembled. The users can also reset the form, by clicking on the * *Reset* * button.  

2. *Write a new story*: When the story generation settings have been submitted and the prompt for the generation of the story has been assembled, the users can trigger the generation of the story by clicking on the * *Write a new story* * button. The story is generated by the LLM and it is sent via a Websocket to the Web UI of the tool. The story is prompted to the users in streaming-mode.

3. *Regenerate the story*: Once the entire story has been written, the users can regenerate the whole story from scratch making use of the same story parameters settings.

4. *Edit the story*: Once the entire story has been written, the users can amend part of the story manually.

5. *Select part to be rewritten*: Once the entire story has been written, the users can select part of the generate text using the mouse, and commit to change the selected part by clicking on the *Select part to be rewritten* button.

6. *Regenerate selected part only*: Once the users have selected the part of the text to be regenerated, they can trigger the partial regeneration of the story, that targets only the selected part to be rewritten. The sections of text that precede and that follow the selected part to be rewritten, will remain the same. The model will regenerate the selected part using the same story generation settings  and taking in consideration the context provided by the unchanged sections. 

7. *Positive feedback*: the users can provide their feedback to the generated story by clicking on the *Good story* button. Through such feedback, the story will be included in the next cycle of fine-tuning of the LLM performed through an external process. 

![image](https://github.com/user-attachments/assets/386c8313-93e7-43ed-9072-c8902201fe06)


## System architecture

The architecture of the system, depicted in below figure, includes the following modules:

![StorAITeller architecture csv](https://github.com/user-attachments/assets/5fc1ee47-ab7d-4e65-bcf4-cdbaeb94d00a)

A. *Web UI*, built in HTML and Javascript, using an external CSS file (stylesheet.css). The Web UI is contained in the storaitellerui.html file.

B. *API gateway*, built in Python using the FastAPI library running on Uvicorn (a Web Server implementation for Python) that runs locally (host="127.0.0.1", port=8000). The API gateway has been developed in the storaiteller.py file and it takes care of the communication with the WebUI through REST APIs and orchestrates actions with Ollama and the Llama 3.2 model. These are the REST APIs defined in the API gateway:

- *setstory*, POST method that assembles the prompt to be fed to the LLM according to the parameters defined in the story generation settings of the Web UI.
The prompt is assembled inserting the story parameters in the placeholders of the following template: main prompt = "You are a writer. Write a story, without extra comments or questions, of maximum {maxnowords} words, where the main characters names are {maincharacter}. The story genre is {genre} and you have to use a {register} register. The keywords of the story are {keywords}. The story must have an introduction, a development".
<br/>If the {Final twist} parameter of the story generator settings is set as True, then this string is appended to the main prompt: "The finale of the story must have a twist."
<br/>If the {Child-friendly} parameter of the story generator settings is set as True, then this string is also appended to the main prompt: "The content must be child-friendly. The story might not involve children."

- *ws*, this method opens the web-socket between Ollama and the Web UI, triggers the generation of the story by the Llama 3.2 and the streaming of the generated content towards the Web GUI.

- *redopartofstory*, POST method that assembles a new prompt when only a part of the story must be regenerated. The story that needs to be partially redone is split in {initialpart, selectedpart} and {finalpart}, where the {selectedpart} is the section of the story that needs to be regenerated. This is the template of the {new prompt} }and how it is assembled: {new prompt = main prompt}} + 'It is important that the story starts with this part unchanged:{initialpart} and finishes with this part unchanged {finalpart}'.

 - *savestory*, POST method that saves a story and its prompt in the datastories CSV file when the users provides a positive feedback. The CSV file has the following comma separated fields:
   - Prompt, that contains the prompt that has generated the story;
   - Story, that contains the generated story.

C. *Ollama* platform that gives access to the Llama 3.2 model and its fine-tuned version (storaitellermodel).

D. The *fine tuning process* that fine-tunes the LLM model based on Llama 3.2 with the stories stored in the CSV file. This process (see Figure 3) is run by:
  1) executing the finetuner.py script that generates as output the LoRA adapter for the fine-tuning;
  2) executing a python script provided by the Llama.cpp library that transforms the LoRA adapter in a gguf file, a format of adapter supported by the Ollama platform;
  3) creating a new fine-tuned model through the Ollama platform, combining the current model and the adapter in gguf format.

![fine tuning process architecture](https://github.com/user-attachments/assets/3b28c9cc-74f1-4a33-8bdf-0f8fbfc1fc1b)


The finetuner.py script makes use of the Unsloth python library, an open source LLM fine tuning library that allows to generate LoRA (Low Rank Adaptation) adapters using efficiently the available hardware. This library runs on Linux or Unix operating systems, therefore the WSL (Windows Subsytem for Linux) framework has to be installed in Windows machines. A virtual environment specific for the fine-tuning process need also to be created in order to install all the libraries necessary for the task. The finetuner.py script creates the adapter starting from the current model (based on the Llama 3.2 3B pretrained model) and using the PEFT
(Parameter-Efficient Fine-Tuning) library to fine-tune only a part of the parameters of the model. These are the steps executed by the finetuner.py script:
  1) The data in the datastories.csv is loaded and the template expected by Ollama for the Llama 3.2 model is applied to the input dataset;
  2) The trainer is built defining its parameters (for example the number of training epochs, the learning rate, etc.) and the current model is trained accordingly;
  3) The finetuner.py script generates the LoRA adapter.
     
Considering that Ollama handles only adapters in the gguf format, the LoRA adapter must be converted to gguf file. This is done by executing from the CLI a script made available by the Llama.cpp library:
 
    python3 convert_lor_to_gguf.py ../lora_model/ --outype f16 --outfile storaiteller.gguf

 The f16 quantization has been applied in order to have a fast conversion and retain the accuracy of the original model. A modelfile.md file must be defined to instruct Ollama on how to integrate the current model with the above generated gguf adapter. The modelfile.md also defines the temperature of the model (when the temperature is closer to 1, the generated content is more creative, meaning that the next token selected in the sequence might not be the one with the highest probability) and the maximum length of the context window. The modelfile.md is defined as:

    FROM \modelfolder\storaitellermodel
  
    ADAPTER \adapterfolder\storaiteller.gguf
  
    PARAMETER temperature 0.8
  
    PARAMETER num_ctx 120000

 Running the following CLI command, Ollama generates the new fine-tuned storaitelledmodel model that now can be used to generate new stories:
     
     ollama create storaitellermodel-f ./modelfile.md

     
