# StorAIteller
This is the repository of the code I have developed for the ARI-3333 Generative AI assignment

## Description of the project
The aim of this project is to make use of LLM technology to create a product that generates fictional stories based on a set of parameters, such as genre, register, keywords, main characters, etc. defined by users through a Web User Interface. 

The objectives of this project are the following: 

- implementation of a textual story generation module based on a Large Language Model (like GPT-3 or Llama 3.2) to generate a fictional story based on user input (e.g., theme, characters' names and other settings). The generated story has to be coherent and follow a structured narrative with a beginning, a development of the story and a conclusion.
- implementation of a Web User Interface through which users can:
  - define the parameters to be considered for the story generation
  - refine the generated story and regenerate part of it
  - provide a positive feedback to the generated story in order to include the story in an external fine-tuning process
 
## Installation 

The project is made of 3 main modules:
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



