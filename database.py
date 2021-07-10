#run this file in the songs folder 
import librosa
from librosa.feature.spectral import melspectrogram, spectral_bandwidth, spectral_rolloff
from matplotlib.pyplot import specgram 
from pydub import AudioSegment
from tempfile import mktemp
import librosa.display
import numpy as np
import os
import pylab
from PIL import Image
import imagehash
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import csv
from imagededup.methods import PHash 
features=['melspectrogram','MFCC']
header = ['name', 'spectrogram_code','melspectrogram_code','MFCC_code']
with open('Hashes2.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for filename in os.listdir():   
        if filename.endswith(".mp3"):    
            mp3_audio,samplingFrequency =librosa.load(filename,duration=60)
            ##spectrogram
            Spectro_Path = 'spectrograms/'+os.path.splitext(os.path.basename(filename))[0]+'.png'
            pylab.axis('off')   
            pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) 
            spectrogram= librosa.power_to_db((np.abs(librosa.stft(mp3_audio)))**2, ref=np.max)
            librosa.display.specshow(spectrogram, y_axis='linear')
            pylab.savefig(Spectro_Path, bbox_inches=None, pad_inches=0)
            pylab.close()
            Image_array=Image.fromarray(spectrogram)
            spectrogram_code = imagehash.phash(Image_array,hash_size=16)
            ##extract features
            for feature in features:
                if feature=='melspectrogram':
                    melspectrogram= librosa.feature.melspectrogram(y=mp3_audio ,S=spectrogram, sr=samplingFrequency)
                    Image_array=Image.fromarray(melspectrogram)
                    melspectrogram_code = imagehash.phash(Image_array,hash_size=16)
                elif feature=='MFCC':
                    MFCC = librosa.feature.mfcc(y=mp3_audio,sr=samplingFrequency)
                    Image_array=Image.fromarray( MFCC)
                    MFCC_code = imagehash.phash(Image_array,hash_size=16)
                    
            data=[str(filename),str(spectrogram_code),str(melspectrogram_code),str(MFCC_code)]
            writer.writerow(data)






