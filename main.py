import fastapi from FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}