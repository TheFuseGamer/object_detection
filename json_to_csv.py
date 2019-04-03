import os
import glob
import pandas as pd
import json
import pickle
from math import floor
from shutil import copyfile

TEST_DATA_PERCENTAGE = 3

def json_to_csv():
    path_to_json = 'data/images'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    path_to_jpeg = 'data/images'
    jpeg_files = [pos_jpeg for pos_jpeg in os.listdir(path_to_jpeg) if pos_jpeg.endswith('.jpeg') or pos_jpeg.endswith('.jpg')]
    fjpeg=(list(reversed(jpeg_files)))
    test_data_count = floor(len(jpeg_files) / 100 * 3)
    csv_list_train = []
    csv_list_test = []
    labels=[]
    os.mkdir(os.path.join("data","annotations"))
    os.mkdir(os.path.join("data","images", "train"))
    os.mkdir(os.path.join("data","images", "test"))
    for j in json_files:
        data_file=open(path_to_json + '/{}'.format(j))   
        data = json.load(data_file)
        for item in data["assets"]:     
            is_test = False                  
            asset = data["assets"][item]["asset"]
            filename = asset["name"]
            if test_data_count > 0:
                test_data_count -= 1
                is_test = True
                copyfile(os.path.join(path_to_jpeg, filename), os.path.join("data","images", "test", filename))
            else:
                copyfile(os.path.join(path_to_jpeg, filename), os.path.join("data","images", "train", filename))
            width, height = asset["size"]["width"], asset["size"]["height"]
            regions = data["assets"][item]["regions"]
            for box in regions:
                tag = box["tags"][0]
                xmin = box["points"][0]["x"]
                ymin = box["points"][0]["y"]
                xmax = box["points"][2]["x"]
                ymax = box["points"][2]["y"]
                values = (filename, width, height, tag, xmin, ymin, xmax, ymax)
                if is_test:
                    csv_list_test.append(values)
                else:
                    csv_list_train.append(values)
    
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    csv_df_test = pd.DataFrame(csv_list_test, columns=column_name)
    csv_df_train = pd.DataFrame(csv_list_train, columns=column_name)
    labels_train=list(set(labels))
    with open("train_labels.txt", "wb") as fp:   #Pickling
        pickle.dump(labels_train, fp)
    return csv_df_train, csv_df_test

def main():
    csv_df_train, csv_df_test = json_to_csv()
    csv_df_train.to_csv('data/annotations/train_labels.csv', index=None)
    csv_df_test.to_csv('data/annotations/test_labels.csv', index=None)
    print('Successfully converted json to csv.')

main()