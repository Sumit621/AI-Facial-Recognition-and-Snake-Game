import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from time import sleep
import csv
import pandas as pd
import Snake as sk
from csv import DictWriter
import shutil


def get_encoded_faces():
  
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./Recorded_Faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("Recorded_Faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    """
    encode a face given the file name
    """
    source="Entry_Queue/"+img
    dest="Recorded_Faces/"+img
    shutil.copyfile(source,dest)
    nameLs=img.split(".")
    name=nameLs[0]
    os.remove(source)
    print('****Hello '+name+'!****')
    snake_color=input('Enter preferred Snake Color: ')
    food_color=input('Enter preferred Food Color: ')
    food_shape=input('Enter preferred Food Shape: ')
    print('----------------------------------------')
    fields = ['Name','Snake_Color','Food_Shape','Food_Color','Highscore']
    data_dict={'Name':name.lower() ,'Snake_Color':snake_color ,'Food_Shape':food_shape ,'Food_Color':food_color ,'Highscore':0}				
    with open("Recognized_Faces.csv", 'a') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=fields)
        dictwriter_object.writerow(data_dict)
        f_object.close()

def delete_image_record(img):
    face = fr.load_image_file("Recorded_Faces/" + img)
    encoding = fr.face_encodings(face)[0]
    nameLs=img.split(".")
    name=nameLs[0]
    os.remove("Recorded_Faces/"+img)
    df=pd.read_csv("Recognized_Faces.csv")
    df=df[df.Name!=name.lower()]
    df.to_csv("Recognized_Faces.csv",index=False)	
    print('Record Deleted!')


def get_faces():
   
    faces = get_encoded_faces()
    data_list=[]
    for key,value in faces.items():
        face_name=key
        print('****Hello '+face_name+'!****')
        sn_color=input('Enter preferred Snake Color: ')
        fd_color=input('Enter preferred Food Color: ')
        fd_shape=input('Enter preferred Food Shape: ')
        print('----------------------------------------')
        data_dict={'Name':face_name.lower() ,'Snake_Color':sn_color.lower() ,'Food_Shape':fd_shape.lower() ,'Food_Color':fd_color.lower() ,'Highscore':0}
        data_list.append(data_dict)
    fields=['Name','Snake_Color','Food_Shape','Food_Color','Highscore']
    filename="Recognized_Faces.csv"
    with open(filename, 'w') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
        writer.writeheader() 
        writer.writerows(data_list)
    csvfile.close()


def classify_face(im):

    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread("Face_Scan/"+im)
    #img = cv2.resize(img, (800, 600))
 
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
           
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

            cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)

    while True:

        cv2.imshow('Scanned', img)
        return face_names
      

def play_game(im):
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    df=pd.read_csv("Recognized_Faces.csv")

    img = cv2.imread("Face_Scan/"+im, 1)
    #img = cv2.resize(img, (800, 600))
 
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            temp=df[df["Name"]==name.lower()]
            snk_cl=list(temp.Snake_Color)
            fd_cl=list(temp.Food_Color)
            fd_sp=list(temp.Food_Shape)
            hs=list(temp.Highscore)
            sk.RunSnake(name,snk_cl[-1],fd_cl[-1],fd_sp[-1],hs[0])
        else:
            print('Sorry Cannot Access, Face not recognized!')
        face_names.append(name)






