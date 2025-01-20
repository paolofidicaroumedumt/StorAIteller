FROM D:\ollama\Ollamamodels\blobs\sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff
# add the adpater
ADAPTER D:\python\venvforfinetuning\llama.cpp\storaiteller.gguf

# sets the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 0.8
# sets the lenght of the context window so that long stories can be generated without losing cohesion
PARAMETER num_ctx 120000
