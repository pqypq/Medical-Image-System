import pydicom


def load_file_information(filename):
    information = {}
    ds = pydicom.read_file(filename)
    information['BodyPartExamined'] = ds.BodyPartExamined
    information['PatientID'] = ds.PatientID
    information['PatientName'] = ds.PatientName
    information['PatientBirthDate'] = ds.PatientBirthDate
    information['PatientAge'] = ds.PatientAge
    information['PatientSex'] = ds.PatientSex
    information['Position'] = ds.PatientPosition
    information['PatientAddress']=ds.PatientAddress
    information['StudyID'] = ds.StudyID
    information['StudyDate'] = ds.StudyDate
    information['StudyTime'] = ds.StudyTime
    information['InstitutionName'] = ds.InstitutionName
    information['Manufacturer'] = ds.Manufacturer
    information['PixelRepresentation'] = ds.PixelRepresentation
    information['AcquisitionDate'] = ds.AcquisitionDate
    information['AcquisitionTime'] = ds.AcquisitionTime
    information['AcquisitionNumber'] = ds.AcquisitionNumber
    information['AccessionNumber'] = ds.AccessionNumber

    # print(dir(ds))
    return information


a = load_file_information("/Users/wonder/Desktop/马文秀动脉/IM81")
for key in a.keys():
    print(key + ":" + str(a[key]))

