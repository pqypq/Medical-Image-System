from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QMatrix, QNativeGestureEvent, QTransform, QPixmap, QImage, QColor, qRed, qGreen, qBlue, QFont, QBrush
from PySide2.QtCore import QObject, QEvent
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsPixmapItem, QGestureEvent, QPinchGesture, QGraphicsSimpleTextItem, QGraphicsTextItem
import cv2
import numpy as np


class Viewer(QGraphicsView):
    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        QGraphicsView.__init__(self, parent, flags)
        self.scene = QGraphicsScene(self)
        # self.item = QGraphicsTextItem()
        # self.item.setPlainText("hello")
        # self.item.setFont(QFont("Consolas",30))                #改变字体和大小
        # self.item.setDefaultTextColor(QColor(255,0,0))         #改变字体的颜色 
        # self.item.setFlag(QGraphicsItem.ItemIgnoresTransformations)  

        # self.iitem = QGraphicsTextItem()
        # self.iitem.setPlainText("ok")
        # self.iitem.setFont(QFont("Consolas",30))                #改变字体和大小
        # self.iitem.setDefaultTextColor(QColor(255,0,0))         #改变字体的颜色
        # self.iitem.setFlag(QGraphicsItem.ItemIgnoresTransformations)

        # self.iitem.setPos(500,500)
        # self.scene.addItem(self.iitem)
        # self.item.setPos(0,0)
        # self.scene.addItem(self.item) 

        #self.item.setPos(100,100)
        self.setScene(self.scene)
        #self.setBackgroundBrush(QPixmap("/User
        # s/wonder/projects/Archive/timg.jpg"))
        self.setBackgroundBrush(QBrush(Qt.black))
        self.zoom = 250
        self.rotate = 0
        self.image = QPixmap()

    def PrintOneLine(self, text, x, y):
        item = QGraphicsTextItem()
        item.setPlainText(text)
        item.setFont(QFont("Consolas",10))                #改变字体和大小
        item.setDefaultTextColor(QColor(255,255,51))         #改变字体的颜色 
        item.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        item.setPos(x,y)
        self.scene.addItem(item)
        

#---------------------------------------------------------------
    # def convertQImageToMat(self, incomingImage):
    #     #'''  Converts a QImage into an opencv MAT format  '''
    #     #incomingImage = incomingImage.convertToFormat(QImage.Format_Indexed8)
    #     width = incomingImage.width()
    #     height = incomingImage.height()
    #     ptr = incomingImage.bits()
    #     ptr.setsize(incomingImage.byteCount())
    #     arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    #     return arr

    def QImage2CV(self, qimg):                                          #将QImage对象转换为cv2可以直接处理的图象
        tmp = qimg
        #使用numpy创建空的图象
        cv_image = np.zeros((tmp.height(), tmp.width(), 3), dtype=np.uint8)
        for row in range(0, tmp.height()):
            for col in range(0,tmp.width()):
                r = qRed(tmp.pixel(col, row))
                g = qGreen(tmp.pixel(col, row))
                b = qBlue(tmp.pixel(col, row))
                cv_image[row,col,0] = r
                cv_image[row,col,1] = g
                cv_image[row,col,2] = b
        return cv_image

    def CV2QImage(self, data):                                      #将image转换为QImage
        # width = cv_image.shape[1]               #获取图片宽度
        # height = cv_image.shape[0]              #获取图片高度
        # pixmap = QPixmap(width, height)         #根据已知的高度和宽度新建一个空的QPixmap,
        # qimg = pixmap.toImage()                 #将pximap转换为QImage类型的qimg
        # #循环读取cv_image的每个像素的r,g,b值，构成qRgb对象，再设置为qimg内指定位置的像素
        # for row in range(0, height):
        #     for col in range(0,width):
        #         r = cv_image[row,col,0]
        #         g = cv_image[row,col,1]
        #         b = cv_image[row,col,2]   
        #         pix = qRgb(r, g, b)
        #         qimg.setPixel(col, row, pix)
        # return qimg                             #转换完成，返回
        # data[data < 0] = 0
        # data[data > 255] = 255
        # data = data.astype("int8")
        return QImage(data, data.shape[1], data.shape[0], QImage.Format_Indexed8)
#----------------------------------------------------------------

    def grey_scale_increase(self,image):                 #调节灰度(increase)
        img_gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        print(img_gray.shape)
        img2 = np.power(img_gray / 255.0, 0.9)
        rows,cols = img2.shape
        flat_gray = img2.reshape((cols * rows,)).tolist()
        A = min(flat_gray )
        B = max(flat_gray )
        print('A = %d,B = %d' %(A,B))
        img2 = np.uint8(255 / (B - A) * (img2 - A) + 0.5)
        return img2

    def increase_option(self):
        adjust_image = self.image.toImage()
        src = self.QImage2CV(adjust_image)                  #src = self.convertQImageToMat(adjust_image)
        result = self.grey_scale_increase(src)
        final_result = self.CV2QImage(result)
        pixmap = QPixmap.fromImage(final_result)
        self.setPixmap(pixmap)

    def grey_scale_decrease(self,image):                 #调节灰度(decrease)
        img_gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        print(img_gray.shape)
        img2 = np.power(img_gray / 255.0, 1.1)
        rows,cols = img2.shape
        flat_gray = img2.reshape((cols * rows,)).tolist()
        A = min(flat_gray )
        B = max(flat_gray )
        print('A = %d,B = %d' %(A,B))
        img2 = np.uint8(255 / (B - A) * (img2 - A) + 0.5)
        return img2

    def decrease_option(self):
        adjust_image = self.image.toImage()
        src = self.QImage2CV(adjust_image)                  #src = self.convertQImageToMat(adjust_image)
        result = self.grey_scale_decrease(src)
        final_result = self.CV2QImage(result)
        pixmap = QPixmap.fromImage(final_result)
        self.setPixmap(pixmap)


        # rows,cols = img_gray.shape
        # flat_gray = img_gray.reshape((cols * rows,)).tolist()
        # A = min(flat_gray)
        # B = max(flat_gray)
        # print('A = %d,B = %d' %(A,B))
        # output = np.uint8(255 / (B - A) * (img_gray - A) + 0.5)
        # print(output.shape)
        # return output
        # image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        # enh_bri = ImageEnhance.Brightness(image)
        # brightness = 1.5
        # image_brightened = enh_bri.enhance(brightness)
        # image_brightened.show()
        
#-----------------------------------------------------------------

    def event(self, e):
        if e.type() == QEvent.NativeGesture:
            e.__class__ = QNativeGestureEvent
            self.nativeGestureEvent(e)
        return super().event(e)

    def nativeGestureEvent(self, e):
        if e.gestureType() == Qt.ZoomNativeGesture:
            delta = e.value()
            if delta > 0:
                self.zoomIn()
            elif delta < 0:
                self.zoomOut()
        elif e.gestureType() == Qt.RotateNativeGesture:
            delta = e.value()
            if delta > 0:
                self.addRotate(3)
            elif delta < 0:
                self.addRotate(-3)

    def wheelEvent(self, e):
        if e.delta() > 0:
            self.zoomIn(5)
        else:
            self.zoomOut(5)
        e.accept()

    def resetView(self):
        self.zoom = 250
        self.rotate = 0
        self.setupMatrix()
        self.setPixmap(self.originalPixmap)

    def viewRotate(self):
        return self.rotate

    def setPixmap(self, pixmap):
        self.scene.clear()
        self.image = pixmap
        item = self.scene.addPixmap(pixmap)
        item.setFlag(QGraphicsItem.ItemIsMovable)

    def setInformationText(self, information):                #输出meta信息
        a =  600
        b = -100
        for key in information.keys():
            text = key + ":" + str(information[key])
            self.PrintOneLine(text,a,b)
            b += 15
        self.setScene(self.scene)
        

    def setupMatrix(self):
        # self.scene.clear()
        # scale = pow(2, (self.zoom - 250)/50)
        # height = self.image.height()
        # width = self.image.width()
        # self.image = self.image.scaled(width*scale,height*scale)
        # self.scene.addPixmap(self.image)
        # item.setFlag(QGraphicsItem.ItemIsMovable)

        scale = pow(2, (self.zoom - 250)/50)
        matrix = QMatrix()
        matrix.scale(scale, scale)
        matrix.rotate(self.rotate)
        self.setMatrix(matrix)


    def zoomIn(self, level = 1):
        self.zoom += level
        if self.zoom > 500:
            self.zoom = 500
        self.setupMatrix()

    def zoomOut(self, level = 1):
        self.zoom -= level
        if self.zoom < 1:
            self.zoom = 1
        self.setupMatrix()

    def addRotate(self, angle):
        self.rotate += angle
        self.setupMatrix()

    def setRotate(self, angle):
        self.rotate = angle
        self.setupMatrix()
        
    def flip(self):
        pixmap_reflect = self.image.transformed(QTransform().scale(-1,1))
        self.setPixmap(pixmap_reflect)

#--------------------------------------------------------------------------
    def adjustHueLight(self):
        # print("hello")
        # adjust_image = self.image.toImage()
        # for i in range(0,adjust_image.width()):
        #     for j in range(0,adjust_image.height()):
        #         color = adjust_image.pixelColor(i,j)
        #         hue = color.hue()
        #         print(hue)
        #         hue +=500
        #         color.setHsv(hue, color.saturation(), color.value(), color.alpha())
        #         adjust_image.setPixelColor(i,j,color)
        
        # self.image = QPixmap.fromImage(adjust_image)
        # self.setPixmap(self.image)
        # src = cv2.imread('mini.jpg')
        # result = self.grey_scale(src)
        # cv2.imshow('src',cv2.cvtColor(src,cv2.COLOR_BGR2GRAY))
        # cv2.imshow('result',result)

        # cv2.waitKey()
        # cv2.destroyAllWindows()

        adjust_image = self.image.toImage()
        src = self.QImage2CV(adjust_image)                  #src = self.convertQImageToMat(adjust_image)
        result = self.grey_scale_increase(src)
        final_result = self.CV2QImage(result)
        pixmap = QPixmap.fromImage(final_result)
        self.setPixmap(pixmap)
        # #cv2.imshow('src',cv2.cvtColor(src,cv2.COLOR_BGR2GRAY))
        # #cv2.imshow('result',result)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

    def adjustHueDark(self):
        adjust_image = self.image.toImage()
        src = self.QImage2CV(adjust_image)                  
        result = self.grey_scale_decrease(src)
        final_result = self.CV2QImage(result)
        pixmap = QPixmap.fromImage(final_result)
        self.setPixmap(pixmap)
#------------------------------------------------------------------------------
    def setOriginalPixmap(self, pixmap):
        self.originalPixmap = pixmap
