
<h1>First Time Setup</h1>

- Create a python virtual environment: python3 -m venv venv
- To activate the virtual env run: source venv/bin/activate
- Install the requirements: pip install requirements.txt


<h1>General</h1>
To run the web server, from inside the objectdector folder run: uvicorn api:app --reload 

<h2>Project Description</h2>

This project detects the objects in a user uploaded image. It uses the facebook/resnet-50 model from the huggingface model hub for detection.

Database
A MongoDB Atlas Cluster is used for this project. The Connection string is stored as an environment variable. 
The mongoDB has a "ProcessedImages" Collection which stores the image Id, image name, annotated image location and list of detected objects. 

API
Detect Objects endpoint (/detectobjects)
Upload a image (jpeg) file, run object detection model on it and returns the annotated image as the response with the object_id in the header.
This Image Id can then be used to query for the labels in the Mongo DB

Object Labels endpoint (/objectlabels/{image_id})
The Image Id is used to query for the labels in the Mongo DB, and these labels are returned as the response.


