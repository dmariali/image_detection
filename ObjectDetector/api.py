from fastapi import FastAPI
from pydantic import BaseModel

import model

app = FastAPI()


class Image(BaseModel):
    name: str
    url: str
   


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/objectdetection/")
async def detect_objects(img: Image):
    print(img)
    response = model.detect_objects(img.name,img.url)
    return response