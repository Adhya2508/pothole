import os
import json
import shutil
import random
import xml.etree.ElementTree as ET

# -----------------------------
# Paths
# -----------------------------
SOURCE_FOLDER = "archive/annotated-images"
SPLITS_FILE = "splits.json"
DATASET_FOLDER = "dataset"

# -----------------------------
# Create YOLO folder structure
# -----------------------------
folders = [
    "train/images",
    "train/labels",
    "valid/images",
    "valid/labels",
    "test/images",
    "test/labels"
]

for folder in folders:
    os.makedirs(os.path.join(DATASET_FOLDER, folder), exist_ok=True)

# -----------------------------
# Read splits.json
# -----------------------------
with open(SPLITS_FILE, "r") as file:
    splits = json.load(file)

train_files = splits["train"]
test_files = splits["test"]

# -----------------------------
# Create validation set
# -----------------------------
random.seed(42)
random.shuffle(train_files)

split_index = int(len(train_files) * 0.8)

valid_files = train_files[split_index:]
train_files = train_files[:split_index]

# -----------------------------
# Convert XML to YOLO
# -----------------------------
def convert_xml_to_yolo(xml_path, txt_path):

    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    img_width = int(size.find("width").text)
    img_height = int(size.find("height").text)

    with open(txt_path, "w") as file:

        for obj in root.findall("object"):

            bbox = obj.find("bndbox")

            xmin = float(bbox.find("xmin").text)
            ymin = float(bbox.find("ymin").text)
            xmax = float(bbox.find("xmax").text)
            ymax = float(bbox.find("ymax").text)

            x_center = (xmin + xmax) / 2
            y_center = (ymin + ymax) / 2

            box_width = xmax - xmin
            box_height = ymax - ymin

            x_center /= img_width
            y_center /= img_height
            box_width /= img_width
            box_height /= img_height

            file.write(
                f"0 {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n"
            )

# -----------------------------
# Process dataset
# -----------------------------
def process_dataset(file_list, split_name):

    for xml_name in file_list:

        image_name = xml_name.replace(".xml", ".jpg")

        xml_path = os.path.join(SOURCE_FOLDER, xml_name)
        image_path = os.path.join(SOURCE_FOLDER, image_name)

        label_path = os.path.join(
            DATASET_FOLDER,
            split_name,
            "labels",
            xml_name.replace(".xml", ".txt")
        )

        new_image_path = os.path.join(
            DATASET_FOLDER,
            split_name,
            "images",
            image_name
        )

        if not os.path.exists(xml_path):
            print(f"Missing XML: {xml_name}")
            continue

        if not os.path.exists(image_path):
            print(f"Missing Image: {image_name}")
            continue

        shutil.copy(image_path, new_image_path)
        convert_xml_to_yolo(xml_path, label_path)

# -----------------------------
# Convert all datasets
# -----------------------------
process_dataset(train_files, "train")
process_dataset(valid_files, "valid")
process_dataset(test_files, "test")

# -----------------------------
# Create data.yaml
# -----------------------------
yaml_content = """train: dataset/train/images
val: dataset/valid/images
test: dataset/test/images

nc: 1

names:
  0: pothole
"""

with open(os.path.join(DATASET_FOLDER, "data.yaml"), "w") as file:
    file.write(yaml_content)

print("--------------------------------------")
print("Dataset conversion completed!")
print(f"Training Images   : {len(train_files)}")
print(f"Validation Images : {len(valid_files)}")
print(f"Testing Images    : {len(test_files)}")
print("--------------------------------------")