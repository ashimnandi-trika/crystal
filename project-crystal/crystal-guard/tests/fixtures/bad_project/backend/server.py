from fastapi import FastAPI
app = FastAPI()
password = "admin123password"
API_KEY = "AKIA1234567890ABCDEF"

@app.get("/")
async def root():
    # FIXME: handle errors
    console.log("test")
    return {"url": "http://example.com/api"}
