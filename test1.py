# %%
import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import warnings
import matplotlib.patches as patches
import sqlite3
import datetime
import csv
# Root directory of the project
ROOT_DIR = os.path.abspath("../")
#print(ROOT_DIR)


warnings.filterwarnings("ignore")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "Mask_RCNN/samples/coco/")) # To find local version
import coco

#%matplotlib inline

# %%
# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join('', "C:\\Users\\vivek\\.conda\\envs\\MaskRCNN\\Mask_RCNN\\samples\\coco\\mask_rcnn_garbage_0030.h5")

# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "Mask_RCNN/Dataset/val")

# %%
class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()

def garbage_predict(loc):
    # %%
    model = modellib.MaskRCNN(mode="inference", model_dir='mask_rcnn_coco.hy', config=config)

    # Load weights trained on MS-COCO
    model.load_weights('C:\\Users\\vivek\\.conda\\envs\\MaskRCNN\\Mask_RCNN\\samples\\coco\\mask_rcnn_garbage_0008.h5', by_name=True)

    # %%
    class_names = ['BG', 'Plastic', 'Non-Plastic']

    # %%
    image = skimage.io.imread('Dataset/test/test.jpg')

    # original image
    plt.figure(figsize=(12,10))
    skimage.io.imshow(image)

    # %%
    results = model.detect([image], verbose=1)

    # Visualize results
    r = results[0]
    visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])

    # %%
    list1=[]
    classes=r['class_ids']
    print("Total objects found",len(classes))
    for i in range(len(classes)):
        print(class_names[classes[i]])
        list1.append(class_names[classes[i]])

    count_p=list1.count('Plastic')
    count_n=list1.count('Non-Plastic')
    print("Platic:",count_p)
    print("Non-Platic:",count_n)

    # connecting to the database  
    connection = sqlite3.connect("info.db") 
      
    # cursor  
    crsr = connection.cursor() 
    print("connection setup successfully!!")
    # SQL command to create a table in the database 
    # SQL command to create a table in the database 
    sql_command = """CREATE TABLE project_info(  
        id INTEGER PRIMARY KEY ,  
        plastic VARCHAR(20),    
        non_plastic VARCHAR(50),
        location VARCHAR(50),  
        date_created TEXT DEFAULT CURRENT_TIMESTAMP);"""    
        # execute the statement 
        #crsr.execute(sql_command)    

    crsr.execute("""INSERT INTO project_info (plastic, non_plastic, location, date_created) VALUES (?, ?, ?, datetime('now','localtime'))""",(count_p,count_n,loc)
    )
    print("inserted successfully!!")
    os.remove('output.csv')
    csvWriter = csv.writer(open("output.csv", "w"))
    headers = ['plastic','non_plastic','location','date_created']
    csvWriter.writerow(headers)
    rows=crsr.execute("select plastic,non_plastic,location,date() from project_info;")
    for row in rows:
	    csvWriter.writerow(row)
    connection.commit()
    crsr.close()
    connection.close()   
    # %%

    labels = ['Plastic', 'Non-Plastic']
    sizes = [count_p, count_n]
    colors = ['yellowgreen', 'lightskyblue']
    activities = ['Plastic', 'Non-Plastic']
    plt.pie(sizes, labels=activities, colors=colors, startangle=90, autopct='%.1f%%')
    plt.show()

    
    # %%


    # %%
