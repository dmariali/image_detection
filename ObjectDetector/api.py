from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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