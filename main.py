from fastapi import FastAPI

app = FastAPI()

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Chatbot App!"}

# Example API endpoint
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}
