from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
import torchvision
from torchvision.io import read_image
from torchvision.utils import draw_bounding_boxes
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

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
        print(
                f"Detected {model.config.id2label[label.item()]} with confidence "
                f"{round(score.item(), 3)} at location {box}"
        )

    output_img_path = draw_bounding_box(img_url,img_name,results["boxes"],labels)
    response = {
        'name':img_name,
        'url': output_img_path,
        'object_labels': labels,
    }
    return response

def draw_bounding_box(img_url,img_name,boxes,labels):
    image = read_image(img_url)
  
    box = torch.tensor(boxes)
    box = torch.tensor(boxes, dtype=torch.int)
    
    # draw bounding box and fill color
    img = draw_bounding_boxes(image, box, width=5,
                            colors="green", 
                            fill=False,
                            labels=labels
                            )
    
    # transform this image to PIL image
    img = torchvision.transforms.ToPILImage()(img)
    output_img_path = str(os.getenv('OUTPUT-PICS-LOCATION','output-pics/')) + img_name +'-labeled-image.jpeg'
    img.save(output_img_path)
    
    return output_img_path


