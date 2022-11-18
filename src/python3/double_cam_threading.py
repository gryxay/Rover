import cv2
import threading
import matplotlib.pyplot as plt

# 640x480 - max resolution of usb cams
# 160x120 - max resolution with 2 usb cams on same usb controler

class camThread(threading.Thread):
    def __init__(self, previewName, camID, width=0, height=0):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.cam = cv2.VideoCapture(self.camID, cv2.CAP_DSHOW)
        if width and height:
            self.cam.set(3, width)
            self.cam.set(4, height)
    def run(self):
        print("Starting " + self.previewName)
        #self.camPreview()

    def camPreview(self):
        cv2.namedWindow(self.previewName)
        if self.cam.isOpened():
            rval, frame = self.cam.read()
        else:
            rval = False

        while rval:
            cv2.imshow(self.previewName, frame)
            rval, frame = self.cam.read()
            key = cv2.waitKey(20)
            if key == 27:
                break
        print(self.previewName + " - failed, or turned off")
        cv2.destroyWindow(self.previewName)
    
    def getFrame(self):
        if self.cam.isOpened():
            rval, frame = self.cam.read()
        else:
            rval = False
        return rval, frame


thread1 = camThread("Camera 1", 0)
thread2 = camThread("Camera 2", 1)

thread1.start()
thread2.start()
print()
print("Active threads", threading.activeCount())

class deapthMapWiever:
    def __init__(self, th1=None, th2=None):
        self.th1 = th1
        self.th2 = th2
        self.stereo = cv2.StereoBM_create(numDisparities=16, blockSize=51)
    
    def _getPictures(self):
        rval1, frame1 = self.th1.getFrame()
        rval2, frame2 = self.th2.getFrame()
        if rval1 and rval2:
            return frame1, frame2
        print("Error: can't get pictures from cameras")
        Exception("Error: can't get pictures from cameras")
    
    def pre_procesing(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.GaussianBlur(image, (51, 51), 2)
        return image
    
    def getDisparityMap(self):
        try:
            frame1, frame2 = self._getPictures()

            frame1 = self.pre_procesing(frame1)
            frame2 = self.pre_procesing(frame2)
            disparity = self.stereo.compute(frame2, frame1)  # left, right [:, :, 0]
            return disparity
        except Exception as e:
            print(e)
            return None
    
    def displayDepthMap(self):
        disparity = self.getDisparityMap()
        disp = cv2.normalize(disparity, None, alpha=0, beta=255,
                             norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        cv2.namedWindow("Depth Map")
        print("Displaying depth map")
        while disparity is not None:
            disparity = self.getDisparityMap()
            disp = cv2.normalize(disparity, None, alpha=0, beta=255,
                             norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            cv2.imshow("Depth Map", disp)
            key = cv2.waitKey(100)
            if key == 27:
                break
        cv2.destroyWindow("Depth Map")

deapthMap = deapthMapWiever(thread1, thread2)
deapthMap.displayDepthMap()
#cv2.destroyAllWindows()
