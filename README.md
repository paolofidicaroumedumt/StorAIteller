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
- Ollama platform
- Back-end that is implemented by the StorAIteller.py file
- Front-end that is implemented by the StorAIteller.html file
