from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog
from PySide2.QtCore import Qt, QDir, QFileInfo, QObject, QTimer,QSize
from PySide2.QtGui import QIcon, QPixmap, QImage, QTransform, QPixmap, QImage
from PySide2 import QtCore

from .viewer import Viewer
from .dicomdata import DicomData

import pydicom

class MainWindow(QMainWindow):
    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        QMainWindow.__init__(self, parent, flags)
        self.index = 0
        self.createViewer()                       #central widget
        self.createAction()                       #abstract
        self.createMenu()                         #menu bar
        self.createToolBar()                      #toolbar
        #====================================
        self.timer = QTimer(self)                 #初始化一个定时器
        self.timer.timeout.connect(self.PlayNext)  #计时结束调用operate()方法
        #====================================
        self.showFullScreen()                     #初始化为全屏

    def load_file_information(self,filename):
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
        return information

    def createViewer(self):
        self.viewer = Viewer(self)
        self.setCentralWidget(self.viewer)

    def createAction(self):
        self.openAct = QAction(QIcon(":/res/baseline-folder_open-24px.svg"), "&Open", self)
        self.saveAct = QAction(QIcon(":/res/baseline-save_alt-24px.svg"), "&Save", self)
        
        self.zoomInAct = QAction(QIcon(":/res/baseline-zoom_in-24px.svg"), "zoomIn", self)
        self.zoomOutAct = QAction(QIcon(":/res/baseline-zoom_out-24px.svg"), "zoomOut", self)         #&是快捷键

        self.rotateLeftAct = QAction(QIcon(":/res/baseline-rotate_left-24px.svg"), "rotateLeft", self)
        self.rotateRightAct = QAction(QIcon(":/res/baseline-rotate_right-24px.svg"), "rotateRight", self)
        self.rotate90Act = QAction(QIcon(":/res/baseline-rotate_90_degrees_ccw-24px.svg"), "&rotate90", self)
        
        self.flipAct = QAction(QIcon(":/res/baseline-flip-24px.svg"), "&flip", self)             #镜像图标
        self.restoreAct = QAction(QIcon(":/res/baseline-restore-24px.svg"), "&restore", self)

        self.adjustAct_light = QAction(QIcon(":/res/baseline-brightness_5-24px.svg"), "&light", self)       #调节灰度变亮
        self.adjustAct_dark = QAction(QIcon(":/res/baseline-brightness_3-24px.svg"), "&dark", self)         #调节灰度变暗
        
        self.playAct = QAction(QIcon(":/res/baseline-play_arrow-24px.svg"), "&play", self)         #播放
        self.pauseAct = QAction(QIcon(":/res/baseline-pause-24px.svg"), "&pause", self)       #暂停

        self.openAct.triggered.connect(self.onOpenActTriggered)
        self.saveAct.triggered.connect(self.onSaveActTriggered)

        self.zoomInAct.triggered.connect(self.onZoomInActTriggered)
        self.zoomOutAct.triggered.connect(self.onZoomOutActTriggered)

        self.rotateLeftAct.triggered.connect(self.onRotateLeftActTriggered)
        self.rotateRightAct.triggered.connect(self.onRotateRightActTriggered)
        self.rotate90Act.triggered.connect(self.onRotate90ActTriggered)

        self.flipAct.triggered.connect(self.onFlipActTriggered)
        self.restoreAct.triggered.connect(self.viewer.resetView)

        self.adjustAct_light.triggered.connect(self.onAdjustActLightTriggered)
        self.adjustAct_dark.triggered.connect(self.onAdjustActDarkTriggered)

        self.playAct.triggered.connect(self.onPlayActTriggered)
        self.pauseAct.triggered.connect(self.onPauseActTriggered)

    def createMenu(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.zoomInAct)
        self.editMenu.addAction(self.zoomOutAct)
        
        self.editMenu.addSeparator()                           #加分隔符

        self.editMenu.addAction(self.rotateLeftAct)
        self.editMenu.addAction(self.rotateRightAct)
        self.editMenu.addAction(self.rotate90Act)

        self.editMenu.addSeparator()

        self.editMenu.addAction(self.flipAct)                  #镜像键功能

        self.editMenu.addSeparator()

        self.editMenu.addAction(self.restoreAct)               #重置键功能

        self.editMenu.addSeparator()

        self.editMenu.addAction(self.adjustAct_light)                #调节灰度增加
        self.editMenu.addAction(self.adjustAct_dark)                 #调节灰度增加

        self.editMenu.addSeparator()

        self.editMenu.addAction(self.playAct)                  #播放键功能
        self.editMenu.addAction(self.pauseAct)                 #暂停键功能

    def createToolBar(self):                                   #创建toolbar
        self.mainToolBar = self.addToolBar("mainToolBar")
        self.mainToolBar.addAction(self.openAct)
        self.mainToolBar.addAction(self.saveAct)

        self.mainToolBar.addSeparator()

        self.mainToolBar.addAction(self.zoomInAct)
        self.mainToolBar.addAction(self.zoomOutAct)
        
        self.mainToolBar.addSeparator()

        self.mainToolBar.addAction(self.rotateLeftAct)
        self.mainToolBar.addAction(self.rotateRightAct)
        self.mainToolBar.addAction(self.rotate90Act)

        self.mainToolBar.addSeparator()

        self.mainToolBar.addAction(self.flipAct)

        self.mainToolBar.addSeparator()

        self.mainToolBar.addAction(self.restoreAct)

        self.mainToolBar.addSeparator()

        self.mainToolBar.addAction(self.adjustAct_light)
        self.mainToolBar.addAction(self.adjustAct_dark)

        self.mainToolBar.addSeparator()

        self.mainToolBar.addAction(self.playAct)
        self.mainToolBar.addAction(self.pauseAct)

    #-----------------------------------------------------
    def onPlayActTriggered(self):
        #self.index = 0
        self.timer.start(100)                                              #设置计时间隔并启动
        if(self.index == self.dicomData.getImageCount()):
            self.index = 0

    def PlayNext(self):
        self.index += 1
        if( self.index >= self.dicomData.getImageCount()):
            self.timer.stop()
        data = self.dicomData.getPixmap(self.index)
        data[data < 0] = 0
        data[data > 255] = 255
        data = data.astype("int8")
        image = QImage(data, data.shape[1], data.shape[0], QImage.Format_Indexed8)
        self.pixmap = QPixmap.fromImage(image)
        self.viewer.setPixmap(self.pixmap)

    def onPauseActTriggered(self):
        self.timer.stop()
    #-----------------------------------------------------
    def onAdjustActLightTriggered(self):
        self.viewer.adjustHueLight()

    def onAdjustActDarkTriggered(self):
        self.viewer.adjustHueDark()

    #-----------------------------------------------------
    def onOpenActTriggered(self):
        path = QFileDialog.getExistingDirectory(self, "Open Directory")
        dir = QDir(path)
        # filters = ["*.jpg"]
        # dir.setNameFilters(filters)

        meta_information = {}
        # for info in dir.entryInfoList():
        #     print(info.absoluteFilePath())
        #     #meta_information = self.load_file_information("/Users/wonder/Desktop/马文秀动脉/IM81")
        #     break
        # for key in meta_information.keys():
        #     print(key + ":" + str(meta_information[key]))
        
        files = []
        for info in dir.entryInfoList():
            if DicomData.isDicomFile(info.absoluteFilePath()) :
                print(info.absoluteFilePath())
                files.append(info.absoluteFilePath())
            # self.viewer.setPixmap(QPixmap(info.absoluteFilePath()))
            # break;
        if(len(files)):    
            meta_information = self.load_file_information(files[0])
            for key in meta_information.keys():
                print(key + ":" + str(meta_information[key]))
        self.dicomData = DicomData.fromFiles(files)

        # data = dicomData.getSlice(dicomdata.AXIAL, 0)  
        data = self.dicomData.getPixmap(1)
        data[data < 0] = 0
        data[data > 255] = 255
        data = data.astype("int8")   
        image = QImage(data, data.shape[1], data.shape[0], QImage.Format_Indexed8)
        self.pixmap = QPixmap.fromImage(image)
        self.viewer.setPixmap(self.pixmap)
        self.viewer.setInformationText(meta_information)
        self.viewer.setOriginalPixmap(self.pixmap)
        print(data.shape)
        # Dicom.fromFiles(files)

    def keyPressEvent(self, event):
        print(event.key())
        if( event.key() == Qt.Key_D ):                                       #如果按D键那就跳转下一张
            self.index += 1
            if(self.index >= self.dicomData.getImageCount()):
                self.index = self.dicomData.getImageCount()
            data = self.dicomData.getPixmap(self.index)
            data[data < 0] = 0
            data[data > 255] = 255
            data = data.astype("int8")
            image = QImage(data, data.shape[1], data.shape[0], QImage.Format_Indexed8)
            self.pixmap = QPixmap.fromImage(image)
            self.viewer.setPixmap(self.pixmap)
            self.viewer.setOriginalPixmap(self.pixmap)
            print("key pressed")
        elif( event.key() == Qt.Key_A ):                                     #如果按A键那就跳转前一张
            self.index -= 1
            if(self.index <= 0):
                self.index = 0
            data = self.dicomData.getPixmap(self.index)
            data[data < 0] = 0
            data[data > 255] = 255
            data = data.astype("int8")
            image = QImage(data, data.shape[1], data.shape[0], QImage.Format_Indexed8)
            self.pixmap = QPixmap.fromImage(image)
            self.viewer.setPixmap(self.pixmap)
            self.viewer.setOriginalPixmap(self.pixmap)
            print("key pressed")
        elif( event.key() == Qt.Key_W ):
            self.viewer.increase_option()
        elif( event.key() == Qt.Key_S ):
            self.viewer.decrease_option()
        else:                                                                #否则没有反应
            pass

    def onZoomInActTriggered(self):
        self.viewer.zoomIn()

    def onZoomOutActTriggered(self):
        self.viewer.zoomOut()

    def onRotateLeftActTriggered(self):
        self.viewer.addRotate(6)
    
    def onRotateRightActTriggered(self):
        self.viewer.addRotate(-6) 

    def onRotate90ActTriggered(self):
        rotate = self.viewer.viewRotate() + 90
        if rotate%90 is 0:
            self.viewer.setRotate(rotate)
        else:
            self.viewer.setRotate(90)

    def onFlipActTriggered(self):
        self.viewer.flip()

    def onSaveActTriggered(self, n):
        tup = QFileDialog.getSaveFileName(self, "Save Image", "","Images (*.png *.jpg)")    #创建一个保存文件的dialog框
        print(tup[0])
        self.pixmap.save(tup[0])         #保存图片