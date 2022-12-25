from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import model

#FastAPI setup
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Pydantic Typing Definitions
class Image(BaseModel):
    name: str
    url: str
   

#Load in Environment variables
INPUT_PICS_LOCATION = str(os.environ.get('INPUT-PICS-LOCATION','pics/'))


#Endpoints

@app.get("/")
async def root():
    return {"message": "Hello World"}



'''
Detect Objects endpoint (/detectobjects)
Upload a image (jpeg) file, run object detection model on it and return response as given below
Example Response: 
{
  "outputImageUrl": "output-pics/6D3AEA56-E7A5-4819-909D-7D703B0A9C23.jpeg-labeled-image.jpeg",
  "objects": [
    "oven",
    "sink",
    "oven"
  ]
}
'''
@app.post("/detectobjects")
async def create_upload_file(data: UploadFile = File(...)):
    file_location = f"{INPUT_PICS_LOCATION} + {data.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(data.file.read())
    # print("info": f"file '{data.filename}' saved at '{file_location}'")
    response = model.detect_objects(data.filename,file_location)
    path = response['outputImageUrl']
    return FileResponse(path)
    # return response

    