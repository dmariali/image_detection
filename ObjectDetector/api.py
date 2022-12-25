from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import model

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

@app.post("/objectdetection")
async def detect_objects(img: Image):
    # print(img)
    response = model.detect_objects(img.name,img.url)
    return response


#Upload a file and return filename as response
@app.post("/uploadfile")
async def create_upload_file(data: UploadFile = File(...)):
#Prints result in cmd – verification purpose
    print(data.filename)
    file_location = f"pics/{data.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(data.file.read())
    # print("info": f"file '{data.filename}' saved at '{file_location}'")
    response = model.detect_objects(data.filename,file_location)
    return response

    