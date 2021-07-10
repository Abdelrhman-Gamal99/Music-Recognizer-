from PIL import Image
import PIL
import librosa
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from tempfile import mktemp
import librosa.display
import imagehash
import pylab
import os

class sound:
    def __init__(self,path):

        self.mp3_audio,self.samplingFrequency =librosa.load(path,duration=60)
           
    def spectrogram (song):
        Spectro_Path = 'Spectrogram.png'
        spectrogram= librosa.amplitude_to_db(np.abs(librosa.stft(song)), ref=np.max)
        pylab.axis('off')  
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  
        librosa.display.specshow(spectrogram, y_axis='linear')
        pylab.savefig(Spectro_Path, bbox_inches=None, pad_inches=0)
        pylab.close()
        spectrogram_code = str(imagehash.phash(Image.open(Spectro_Path),hash_size=16))
        return spectrogram_code 
        
    def spectrogram_features (song): 
        features_code=[]
        for spectrogram_feature in ['melspectrogram','mfcc']:
            feature=librosa.feature.__getattribute__(spectrogram_feature)(y=song,sr=22050)
            Image_array=Image.fromarray( feature)
            feature_code= str(imagehash.phash(Image_array,hash_size=16))
            features_code.append(feature_code)
        return features_code

    
    
    
        
        
            
           