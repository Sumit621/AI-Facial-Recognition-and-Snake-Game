import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5.uic import loadUi
import face_rec as fcr
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

class HomeScreen(QDialog):
    def __init__(self):
        super(HomeScreen,self).__init__()
        loadUi("HomeScreen.ui",self)
        self.scanButton.clicked.connect(self.scanfunction)
        self.addButton.clicked.connect(self.addfunction)
        self.delButton.clicked.connect(self.delfunction)
        self.gameButton.clicked.connect(self.gamefunction)


    def scanfunction(self):
        sc=ScanRecord()
        widget.addWidget(sc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addfunction(self):
        add=AddRecord()
        widget.addWidget(add)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def delfunction(self):
        dl=DelRecord()
        widget.addWidget(dl)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gamefunction(self):
        gm=GameLoad()
        widget.addWidget(gm)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

class AddRecord(QDialog):
    def __init__(self):
        super(AddRecord,self).__init__()
        loadUi("AddRecord.ui",self)
        self.addRecButton.clicked.connect(self.single_face)
        self.backButton.clicked.connect(self.backfunc)

    def backfunc(self):
        hs=HomeScreen()
        widget.addWidget(hs)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def single_face(self):
        #print('****Hello '+face_name+'!****')
        img=self.Ntxt.text()
        source="Entry_Queue/"+img
        dest="Recorded_Faces/"+img
        shutil.copyfile(source,dest)
        nameLs=img.split(".")
        face_name=nameLs[0]
        os.remove(source)
        sn_color = self.SCtxt.text()
        fd_color= self.FCtxt.text()
        fd_shape= self.FStxt.text()
            #print('----------------------------------------')
        faces = fcr.get_encoded_faces()
        fl=False
        for key,value in faces.items():
            if key==face_name:
                fl=True
                break
        if fl==True:
            fields = ['Name','Snake_Color','Food_Shape','Food_Color','Highscore']
            data_dict={'Name':face_name.lower() ,'Snake_Color':sn_color.lower() ,'Food_Shape':fd_shape.lower() ,'Food_Color':fd_color.lower() ,'Highscore':0}				
            with open("Recognized_Faces.csv", 'a') as f_object:
                dictwriter_object = DictWriter(f_object, fieldnames=fields)
                dictwriter_object.writerow(data_dict)
                f_object.close()
            print('Record Added!')
        hs=HomeScreen()
        widget.addWidget(hs)
        widget.setCurrentIndex(widget.currentIndex()+1)

class ScanRecord(QDialog):
    def __init__(self):
        super(ScanRecord,self).__init__()
        loadUi("ScanFace.ui",self)
        self.scanButton.clicked.connect(self.face_scan)
        self.backButton.clicked.connect(self.backfunc)

    def backfunc(self):
        hs=HomeScreen()
        widget.addWidget(hs)
        widget.setCurrentIndex(widget.currentIndex()+1) 

    def face_scan(self):
        face_name=self.SNmtxt.text()
        fcr.classify_face(face_name)
        hs=HomeScreen()
        widget.addWidget(hs)
        widget.setCurrentIndex(widget.currentIndex()+1)

class DelRecord(QDialog):
    def __init__(self):
        super(DelRecord,self).__init__()
        loadUi("DelFace.ui",self)
        self.delRButton.clicked.connect(self.face_del)
        self.backButton.clicked.connect(self.backfunc)

    def backfunc(self):
        hs=HomeScreen()
        widget.addWidget(hs)
        widget.setCurrentIndex(widget.currentIndex()+1) 

    def face_del(self):
        face_name=self.DNmtxt.text()
        fcr.delete_image_record(face_name)
        hs=HomeScreen()
        widget.addWidget(hs)
        widget.setCurrentIndex(widget.currentIndex()+1)

class GameLoad(QDialog):
    def __init__(self):
        super(GameLoad,self).__init__()
        loadUi("GameLoad.ui",self)
        self.gpButton.clicked.connect(self.load_game)
        self.backButton.clicked.connect(self.backfunc)

    def backfunc(self):
        hs=HomeScreen()
        widget.addWidget(hs)
        widget.setCurrentIndex(widget.currentIndex()+1) 

    def load_game(self):
        face_name=self.GNmtxt.text()
        fcr.play_game(face_name)
        hs=HomeScreen()
        widget.addWidget(hs)
        widget.setCurrentIndex(widget.currentIndex()+1)


app=QApplication(sys.argv)
mainwindow=HomeScreen()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(654)
widget.setFixedHeight(631)
widget.show()
app.exec_()
