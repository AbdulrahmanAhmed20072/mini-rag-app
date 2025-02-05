## mini-rag

This is a minimal implementation of the RAG (Retrieval-Augmented Generation) model for question answering.

## Requirements

- Python 3.9 or later

### Install Python using MiniConda

1. Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install).
2. Create a new environment using the following command:
   ```bash
   $ conda create -n mini-rag python=3.9
   ```
3. activate conda environment:
    ```bash
    $ conda activate mini-rag
    ```

### (optional) setup your comman line interface for better readability:
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

### (optional) Run Ollama Local LLM Server using Colab + Ngrok
- check the [notebook](https://colab.research.google.com/drive/1kDoLkd72--wLWVP7KiHuNlA5mGTu3EXp?usp=sharing)

## Installation

### Install the required packages
```bash
$ pip install -r requirements.txt
```

### Setup the environment variables
Copy the example `.env` file and update it with your credentials:
```bash
$ cp .env.example .env
```
Modify the `.env` file to include necessary API keys, such as:
```
OPENAI_API_KEY=your-api-key-here
```

## Run Docker Compose Services

1. Navigate to the `docker` directory:
   ```bash
   $ cd docker
   ```
2. Copy the example `.env` file and update it:
   ```bash
   $ cp .env.example .env
   ```
3. Modify `.env` with your credentials.
4. Start the Docker services:
   ```bash
   $ sudo docker compose up -d
   ```

## Run the FastAPI Server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection
You can import the Postman collection from:
[src/assets/mini-rag-app.postman_collection.json](https://github.com/AbdulrahmanAhmed20072/mini-rag-app/blob/b99c12058703c1aebe54ae9dbd92497904079b2d/src/assets/mini-rag-app.postman_collection.json)
