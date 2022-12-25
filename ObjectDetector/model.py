from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
import torchvision
from torchvision.io import read_image
from torchvision.utils import draw_bounding_boxes
from PIL import Image
import requests
import json

def detect_objects(img_name,img_url):
#image = Image.open(requests.get(url, stream=True).raw)
# img_url='pics/dani-nala.jpeg'
    image = Image.open(img_url)

    
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    # let's only keep detections with score > 0.9
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
    # print(results)

    labels = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        labels.append(model.config.id2label[label.item()])
        print(labels)
        print(
                f"Detected {model.config.id2label[label.item()]} with confidence "
                f"{round(score.item(), 3)} at location {box}"
        )

    response = draw_bounding_box(img_url,img_name,results["boxes"],labels)
    return response

def draw_bounding_box(img_url,img_name,boxes,labels):
    image = read_image(img_url)
  
    box = torch.tensor(boxes)
    box = torch.tensor(boxes, dtype=torch.int)
    
    # draw bounding box and fill color
    # labels = ["person","dog","other1","other2"]
    img = draw_bounding_boxes(image, box, width=5,
                            colors="green", 
                            fill=False,
                            labels=labels
                            )
    
    # transform this image to PIL image
    img = torchvision.transforms.ToPILImage()(img)
    
    # display output
    #img.show()
    img_path = 'output-pics/' + img_name +'-labeled-image.jpeg'
    img.save(img_path)
    response = {
        'image-path-labled': img_path,
        'objects': labels,
    }
    return response


