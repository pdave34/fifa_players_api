# fifa_players_api

## Introduction

[FastAPI](https://fastapi.tiangolo.com/) implementation for managing mock list of players. This mock list of players has been adjusted with randomized skill attributes and originate from [data.world](https://data.world/raghav333/fifa-players).

## Instructions

### Install Python 3.12.1

### Install required packages:

```python
pip install -r requirements.txt
```

### Run [uvicorn](https://www.uvicorn.org/):

```console
uvicorn main:app --reload
```

This will load an [ASGI](https://asgi.readthedocs.io/en/latest/) server at:

> http://127.0.0.1:8000

### Visit documentation:

> http://127.0.0.1:8000/docs

### Run tests:

```console
python test_api.py
```

### Test output:

Output of `test_api.py` is available in `test_api_out.txt` for reference.
