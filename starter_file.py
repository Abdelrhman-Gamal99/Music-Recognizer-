from PyQt5 import QtWidgets ,QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction,QTableWidget
from GUI import Ui_MainWindow
from sound_class import sound
import os
import sys
import matplotlib.pyplot as plot
import librosa 
from pydub import AudioSegment
from tempfile import mktemp
import librosa.display
import numpy as np
from PIL import Image
import imagehash
import pylab
import textdistance
import pandas as pd
from math import floor, ceil
import operator
import sounddevice as sd 
from difflib import SequenceMatcher
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 
        self.two_song=False
        self.outputSong=None
        self.Hashes = pd.read_csv('Hashes.csv')
        self.ui.open_song1.clicked.connect(lambda:self.getfile(1))
        self.ui.open_song2.clicked.connect(lambda:self.getfile(2))
        self.ui.open_song2.setDisabled(True) 
        self.ui.Mixing_Slider.sliderReleased.connect(lambda:self.mixer())
        
    def getfile(self,songNumber):
        fname= QFileDialog.getOpenFileName( self, 'choose the signal', os.getenv('HOME') ,"mp3(*.mp3)" ) 
        self.path = fname[0] 
        Audio=sound(self.path)
        if self.path =="" :
            return
        else:
            if songNumber==1 :
                self.ui.song1_label.setText(os.path.splitext(os.path.basename(self.path))[0])
                self.ui.open_song2.setDisabled(False) 
                self.mp3_audio1=Audio.mp3_audio
                self.samplingFrequency1 =Audio.samplingFrequency
                
            elif songNumber==2 :
                self.ui.song2_label.setText(os.path.splitext(os.path.basename(self.path))[0])
                self.mp3_audio2=Audio.mp3_audio
                self.samplingFrequency2 =Audio.samplingFrequency
                self.two_song=True

    def mixer(self) :

        if self.two_song:
            sliderRatio = self.ui.Mixing_Slider.value()/100
            self.outputSong = self.mp3_audio1 * sliderRatio + self.mp3_audio2 * (1-sliderRatio)           
        else:
            self.outputSong=self.mp3_audio1
 
        self.spectrogram_code=sound.spectrogram(self.outputSong)
        self.features_code=sound.spectrogram_features(self.outputSong)
        self.compare()

   
    
    def jaro_distance(self,s1, s2):
    
        # If the s are equal
        if (s1 == s2):
            return 1.0
        # Length of two s
        len1 = len(s1)
        len2 = len(s2)
        max_dist = floor(max(len1, len2) / 2) - 1
        # Count of matches
        match = 0
        # Hash for matches
        hash_s1 = [0] * len(s1)
        hash_s2 = [0] * len(s2)
    
        # Traverse through the first
        for i in range(len1):
            # Check if there is any matches
            for j in range(max(0, i - max_dist), 
                        min(len2, i + max_dist + 1)):
                # If there is a match
                if (s1[i] == s2[j] and hash_s2[j] == 0):
                    hash_s1[i] = 1
                    hash_s2[j] = 1
                    match += 1
                    break
    
        # If there is no match
        if (match == 0):
            return 0.0
        # Number of transpositions
        t = 0
        point = 0
        for i in range(len1):
            if (hash_s1[i]):
    
                # Find the next matched character
                # in second
                while (hash_s2[point] == 0):
                    point += 1
    
                if (s1[i] != s2[point]):
                    point += 1
                    t += 1
        t = t//2
    
        # Return the Jaro Similarity
        return (match/ len1 + match / len2 + 
                (match - t + 1) / match)/ 3.0

    def compare(self ) :
        self.ui.tableWidget.clearContents()
        songs_similarity = dict()
        for i in range(0,len(self.Hashes)):
            Name=self.Hashes.iloc[i,0]
            feature1_similarity=self.jaro_distance(self.spectrogram_code,self.Hashes.iloc[i,1])
            feature2_similarity=self.jaro_distance(self.features_code[0],self.Hashes.iloc[i,2])
            feature3_similarity=self.jaro_distance(self.features_code[1],self.Hashes.iloc[i,3]) 
            similarityindex=((feature1_similarity+feature2_similarity+feature3_similarity)/3)*100
            songs_similarity.update({Name:similarityindex})
        sorted_dict= sorted(songs_similarity.items(),key=operator.itemgetter(1),reverse=True)  
        top_ten=sorted_dict[0:11]
        for row in range(1,11) :
            name = QtWidgets.QTableWidgetItem(str(top_ten[row-1][0]))
            similarity_index=QtWidgets.QTableWidgetItem(str(top_ten[row-1][1])+'%')
            self.ui.tableWidget.setItem(row,0,name)
            self.ui.tableWidget.setItem(row,1,similarity_index)
               
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()
if __name__ == "__main__":
    main()
