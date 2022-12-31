from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

from pydantic import BaseModel, Field
import uuid
from typing import List

from pymongo import MongoClient
import os
from dotenv import load_dotenv, dotenv_values   
import model


load_dotenv()
config = dotenv_values(".env")

#FastAPI setup
app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['X-image-id'],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGO_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    app.collection = app.database["processedImages"]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


#Pydantic Typing Definitions
class Image(BaseModel):
    # id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    url: str
    object_labels: List[str]
   

#Load in Environment variables
INPUT_PICS_LOCATION = str(os.getenv('INPUT-PICS-LOCATION'))


#Endpoints

@app.get("/")
async def root():
    return {"Welcome Message": "Welcome To Object Detection"}



'''
Detect Objects endpoint (/detectobjects)
Upload a image (jpeg) file, run object detection model on it and returns the annotated image as the response with the object_id in the header.
this Object Id can then be used to query for the labels in the Mongo DB
'''
@app.post("/detectobjects")
async def create_upload_file(data: UploadFile = File(...)):
    file_location = f"{INPUT_PICS_LOCATION} + {data.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(data.file.read())
    # print("info": f"file '{data.filename}' saved at '{file_location}'")
    response = model.detect_objects(data.filename,file_location)
    _id = app.collection.insert_one(response) 

    headers= {"X-image-id": str(_id.inserted_id)}
    path = response['url']
    return FileResponse(path, headers=headers)  
    # return response

'''
Object Labels endpoint (/objectlabels/{image_id})
The Image Id is used to query for the labels in the Mongo DB, and these labels are returned as the response.
'''
@app.get("/objectlabels/{image_id}")
async def find_object_labels_by_image_name(image_id: str):
    query = {"_id": ObjectId(image_id)}
    response =  app.collection.find_one(query,{"_id":0})       
    return response

    