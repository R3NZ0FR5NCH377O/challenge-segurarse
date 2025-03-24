import os
from fastapi import FastAPI

app = FastAPI()

user_name = os.getenv("USER_NAME", "Renzo Franchetto")

@app.get("/")
def read_root():
    return {"message": f"Hola Segurarse, soy {user_name}"}