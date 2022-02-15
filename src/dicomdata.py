import pydicom
import numpy as np
import os

# Anatomical planes
TRANSVERSE = AXIAL = 0
FRONTAL = CORONAL = 1
MEDIAN = SAGITTAL = 2
ALLOWED_PLANES = (AXIAL, CORONAL, SAGITTAL)

class DicomData(object):
    ALLOWED_MODALITIES = ('CT', 'MR', 'CR', 'RT')

    def __init__(self, data, **kwargs):
        self._array = data
        self.modality = kwargs.get("modality")

    # @property
    # def array(self):
    #     """The underlying numpy array.

    #     :rtype: np.ndarray
    #     """
    #     return self._array

    @staticmethod
    def isDicomFile(path):
        if not os.path.isfile(path):
            return False
        try:
            with open(path, "rb") as f:
                return f.read(132).decode("ASCII")[-4:] == "DICM"
        except:
            return False

    @classmethod
    def fromFiles(cls, files):
        data = []
        modality = None

        for filePath in files:
            f = pydicom.dcmread(filePath)
            if modality:
                if modality != f.Modality:
                    raise RuntimeError("Cannot mix images from different modalities")
            elif f.Modality not in cls.ALLOWED_MODALITIES:
                raise RuntimeError("%s modality not supported" % f.Modality)
            else:
                modality = f.Modality

            data.append(cls.readPixData(f))

        # print(np.array(data))

        return cls(np.array(data), modality=modality)

    @classmethod
    def readPixData(cls,f):
        if f.Modality == "CT":
            data = f.RescaleSlope * f.pixel_array + f.RescaleIntercept
            return np.array(data)
        else:
            return np.array(f.pixel_array)

    def getSlice(self, plane, n):
        if plane not in ALLOWED_PLANES:
            raise ValueError("Invalid plane identificator (allowed are 0,1,2)")
        index = [slice(None, None, None) for i in range(3)]
        index[plane] = n
        print(index)
        return self._array[4]

    def getPixmap(self, index):
        if( index < len(self._array) ):
            return self._array[index]
        return None

    def getImageCount(self):
        return len(self._array)
        

            
