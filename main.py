from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hola Segurarse, soy Renzo"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))  
    uvicorn.run(app, host="0.0.0.0", port=port)