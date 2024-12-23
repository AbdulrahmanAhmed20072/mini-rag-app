## mini-rag

This is a minimal implementation of the RAG (Retrieval-Augmented Generation) model for question answering.

## Requirements

- Python 3.8 or later

### Install Python using MiniConda

1. Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install).

2. Create a new environment using the following command:
   ```bash
    conda create -n mini-rag python=3.8
   ```
3. activate conda environment:
    ```bash
    conda activate mini-rag
    ```
## (optional) setup your comman line interface for better readability:
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## run the FastAPI server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN collection
download POSTMAN collection from [assets/mini-rag-app.postman_collection.json](/mnt/c/Users/Abdulrahman/anaconda3/envs/mini-rag-app/assets/mini-rag-app.postman_collection.json)

## Run Docker Compose Services
```bash
$ cd docker
$ cp .env.example .env
```
 
- update `.env` with your credentials


```bash
$ cd docker
$ sudo docker compose up -d
```