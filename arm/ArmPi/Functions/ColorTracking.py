#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/luke/ArmPi/')
import cv2
import time
import Camera
import threading
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *

from typing import Tuple, List, Dict, Any




class ColorTracking():
    def __init__(self) -> None:
        self.AK = ArmIK()

        self.__target_color: Tuple[str, Any] = ('red', )
        

        self.range_rgb: Dict[str, Tuple[int, int, int]] = {
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
        }

        # Angle at which the gripper closes when gripping
        self.servo1_grip_angle: int = 500

        self.count: int = 0
        self.track: bool = False
        self._stop: bool = False
        self.get_roi: bool = False
        self.center_list: list = []
        self.first_move: bool = True
        self.__isRunning: bool = False
        self.detect_color: str = 'None'
        self.action_finish: bool = True
        self.start_pick_up: bool = False
        self.start_count_t1: bool = True

        self.t1: int = 0
        self.roi: tuple = ()
        self.last_x: int = 0
        self.last_y: int = 0

    
        self.count: int = 0

        self.unreachable: bool = False

        # color block home coordinates (x, y, z)
        self.coordinate: Dict[str, Tuple[float, float, float]] = {
            'red':   (-15 + 0.5, 12 - 0.5, 1.5),
            'green': (-15 + 0.5, 6 - 0.5,  1.5),
            'blue':  (-15 + 0.5, 0 - 0.5,  1.5),
        }

        # World definitions
        self.rect = None
        self.size: Tuple[int, int] = (640, 480)
        self.rotation_angle: int = 0
        self.unreachable: bool = False
        self.world_X: int = 0
        self.world_Y: int = 0
        self.world_x: int = 0
        self.world_y: int = 0

        return

    
    def setTargetColor(self, target_color: str) -> None:
        """ Set the detection color
        Parameters
        ----------
            target_color (str): target color in self.range_rgb?
        Returns
        -------
            None
        """
        self.__target_color = (target_color, )
        return
    
    
    def initMove(self) -> None:
        """Go to initial position
        Parameters
        ----------
            None
        Returns
        -------
            None
        """
        Board.setBusServoPulse(1, self.servo1_grip_angle - 50, 300)
        Board.setBusServoPulse(2, 500, 500)
        self.AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)
        return


    def getAreaMaxContour(self, contours: list):
        """ Find the contour with the largest area
        Parameters
        ----------
            contours (list): a list of countours to compare
        Returns
        -------
            area_max_contour
            contour_area_max
        """
        contour_area_temp = 0
        contour_area_max = 0
        area_max_contour = None

        for c in contours:
            contour_area_temp = math.fabs(cv2.contourArea(c))  # calculate contour area
            if contour_area_temp > contour_area_max:
                contour_area_max = contour_area_temp
                
                # If the contour area is greater than 300, the contour of the largest area is valid to filter interference
                if contour_area_temp > 300:
                    area_max_contour = c

        return area_max_contour, contour_area_max  # returns the largest contour





    def setBuzzer(self, timer: float) -> None:
        """Turn on the buzzer
        Parameters
        ----------
            timer (float): time to turn on the buzzer
        Returns
        -------
            None
        """
        Board.setBuzzer(0)
        Board.setBuzzer(1)
        time.sleep(timer)
        Board.setBuzzer(0)
        return

# 
    def set_rgb(self, color: str) -> None:
        """Set the RGB light color of the expansion board to match the color to be tracked
        Parameters
        ----------
            color (str): light color
        Returns
        -------
            None
        """
        if color == "red":
            Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))
            Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
            Board.RGB.show()
        elif color == "green":
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0))
            Board.RGB.setPixelColor(1, Board.PixelColor(0, 255, 0))
            Board.RGB.show()
        elif color == "blue":
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 255))
            Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 255))
            Board.RGB.show()
        else:
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
            Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
            Board.RGB.show()
        return


    def reset(self) -> None:
        """ Variable reset
        Parameters
        ----------
            None
        Returns
        -------
            None
        """
        self.count = 0
        self._stop = False
        self.track = False
        self.get_roi = False
        self.center_list = []
        self.first_move = True
        self.__target_color = ()
        self.detect_color = 'None'
        self.action_finish = True
        self.start_pick_up = False
        self.start_count_t1 = True
        return

    def init(self) -> None:
        """ App initialization call
        Parameters
        ----------
            None
        Returns
        -------
            None
        """
        print("ColorTracking Init")
        self.initMove()
        return

    def start(self) -> None:
        """ Start the colortracking
        Parameters
        ----------
            None
        Returns
        -------
            None
        """
        self.reset()
        self.__isRunning = True
        print("ColorTracking Start")
        return


    def stop(self) -> None:
        """ Stop the colortracking
        Parameters
        ----------
            None
        Returns
        -------
            None
        """
        self._stop = True
        self.__isRunning = False
        print("ColorTracking Stop")
        return


    def exit(self) -> None:
        """ Exit the program.
        Parameters
        ----------
            None
        Returns
        -------
            None
        """
        self._stop = True
        self.__isRunning = False
        print("ColorTracking Exit")
        None


    # Move robotic arm function
    def move(self) -> None:
        """ Move the arm
        Parameters
        ----------
            None
        Returns
        -------
            None
        """
        while True:
            if self.__isRunning:
                if self.first_move and self.start_pick_up: # when an object is first detected               
                    action_finish = False
                    self.set_rgb(self.detect_color)
                    self.setBuzzer(0.1)               
                    result = self.AK.setPitchRangeMoving((self.world_X, self.world_Y - 2, 5), -90, -90, 0) # do not fill in the running time parameter, adaptive running time
                    if result == False:
                        self.unreachable = True
                    else:
                        self.unreachable = False
                    time.sleep(result[2]/1000) # third item of the return parameter is time
                    start_pick_up = False
                    self.first_move = False
                    self.action_finish = True
                elif not self.first_move and not self.unreachable: # object not detected for the first time
                    self.set_rgb(self.detect_color)

                    # If in the tracking phaase
                    if self.track: 
                        if not self.__isRunning: # Stop and exit flag detection
                            continue
                        self.AK.setPitchRangeMoving((self.world_x, self.world_y - 2, 5), -90, -90, 0, 20)
                        time.sleep(0.02)                    
                        self.track = False

                    # If the object has not moved for a while, start gripping
                    if self.start_pick_up: 
                        self.action_finish = False
                        if not self.__isRunning:
                            continue
                        Board.setBusServoPulse(1, self.servo1_grip_angle - 280, 500)  # Gripper open
                        # Calculate the angle the gripper needs to rotate
                        self.servo2_angle = getAngle(self.world_X, self.world_Y, self.rotation_angle)
                        Board.setBusServoPulse(2, self.servo2_angle, 500)
                        time.sleep(0.8)
                        
                        if not self.__isRunning:
                            continue
                        self.AK.setPitchRangeMoving((self.world_X, self.world_Y, 2), -90, -90, 0, 1000)  # lower the altitude
                        time.sleep(2)
                        
                        if not self.__isRunning:
                            continue
                        Board.setBusServoPulse(1, self.servo1_grip_angle, 500)  # gripper closed
                        time.sleep(1)
                        
                        if not self.__isRunning:
                            continue
                        Board.setBusServoPulse(2, 500, 500)
                        self.AK.setPitchRangeMoving((self.world_X, self.world_Y, 12), -90, -90, 0, 1000)  # Arm raised
                        time.sleep(1)
                        
                        if not self.__isRunning:
                            continue
                        # Classify and place blocks of different colors
                        result = self.AK.setPitchRangeMoving((self.coordinate[self.detect_color][0], self.coordinate[self.detect_color][1], 12), -90, -90, 0)   
                        time.sleep(result[2]/1000)
                        
                        if not self.__isRunning:
                            continue
                        self.servo2_angle = getAngle(self.coordinate[self.detect_color][0], self.coordinate[self.detect_color][1], -90)
                        Board.setBusServoPulse(2, self.servo2_angle, 500)
                        time.sleep(0.5)

                        if not self.__isRunning:
                            continue
                        self.AK.setPitchRangeMoving((self.coordinate[self.detect_color][0], self.coordinate[self.detect_color][1], self.coordinate[self.detect_color][2] + 3), -90, -90, 0, 500)
                        time.sleep(0.5)
                        
                        if not self.__isRunning:
                            continue
                        self.AK.setPitchRangeMoving((self.coordinate[self.detect_color]), -90, -90, 0, 1000)
                        time.sleep(0.8)
                        
                        if not self.__isRunning:
                            continue
                        Board.setBusServoPulse(1, self.servo1_grip_angle - 200, 500)  # Open gripper and drop object
                        time.sleep(0.8)
                        
                        if not self.__isRunning:
                            continue                    
                        self.AK.setPitchRangeMoving((self.coordinate[self.detect_color][0], self.coordinate[self.detect_color][1], 12), -90, -90, 0, 800)
                        time.sleep(0.8)

                        self.initMove()  # Go back to initial position
                        time.sleep(1.5)

                        self.detect_color = 'None'
                        self.first_move = True
                        self.get_roi = False
                        self.action_finish = True
                        self.start_pick_up = False
                        self.set_rgb(self.detect_color)
                    else:
                        time.sleep(0.01)
            else:
                if self._stop:
                    self._stop = False
                    Board.setBusServoPulse(1, self.servo1_grip_angle - 70, 300)
                    time.sleep(0.5)
                    Board.setBusServoPulse(2, 500, 500)
                    self.AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)
                    time.sleep(1.5)
                time.sleep(0.01)



    def run(self, img) -> Any:

        
        img_copy = img.copy()
        img_h, img_w = img.shape[:2]
        cv2.line(img, (0, int(img_h / 2)), (img_w, int(img_h / 2)), (0, 0, 200), 1)
        cv2.line(img, (int(img_w / 2), 0), (int(img_w / 2), img_h), (0, 0, 200), 1)
        
        if not self.__isRunning:
            return img
        
        frame_resize = cv2.resize(img_copy, self.size, interpolation=cv2.INTER_NEAREST)
        frame_gb = cv2.GaussianBlur(frame_resize, (11, 11), 11)
        # If a recognized object is detected in a certain area, the area will be detected until no(object is left?)
        if self.get_roi and self.start_pick_up:
            self.get_roi = False
            frame_gb = getMaskROI(frame_gb, self.roi, self.size)    
        
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # Convert image to LAB space
        
        area_max = 0
        areaMaxContour = 0
        if not self.start_pick_up:
            for i in color_range:
                if i in self.__target_color:
                    self.detect_color = i
                    # Perform bitwise operations on origional image and mask
                    frame_mask = cv2.inRange(frame_lab, color_range[self.detect_color][0], color_range[self.detect_color][1])
                    # Open operation
                    opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6, 6), np.uint8)) 
                    # Close operation
                    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((6, 6), np.uint8))
                    # Find the outline
                    contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
                    # Find the largest contour
                    areaMaxContour, area_max = self.getAreaMaxContour(contours)  

            # If you have found a large area
            if area_max > 2500:  
                rect = cv2.minAreaRect(areaMaxContour)
                box = np.int0(cv2.boxPoints(rect))

                roi = getROI(box) # Get roi area
                get_roi = True

                # get coordinates of the center of the block
                img_centerx, img_centery = getCenter(self.rect, self.roi, self.size, self.square_length)  
                # Convert to real world coordinates.
                world_x, world_y = convertCoordinate(img_centerx, img_centery, self.size)
                
                
                cv2.drawContours(img, [box], -1, self.range_rgb[self.detect_color], 2)
                # Draw center point
                cv2.putText(img, '(' + str(self.world_x) + ',' + str(self.world_y) + ')', (min(box[0, 0], box[2, 0]), box[2, 1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.range_rgb[self.detect_color], 1)
                
                # get las coordinates to determine whether to move
                distance = math.sqrt(pow(self.world_x - self.last_x, 2) + pow(self.world_y - self.last_y, 2))
                self.last_x, self.last_y = world_x, world_y
                self.track = True


                # "Cumulative judgement" lmao ok thanks Google
                if self.action_finish:
                    if distance < 0.3:
                        self.center_list.extend((world_x, world_y))
                        self.count += 1
                        if self.start_count_t1:
                            self.start_count_t1 = False
                            self.t1 = time.time()
                        if time.time() - self.t1 > 1.5:
                            self.rotation_angle = rect[2]
                            self.start_count_t1 = True
                            self.world_X, self.world_Y = np.mean(np.array(self.center_list).reshape(self.count, 2), axis=0)
                            self.count = 0
                            self.center_list = []
                            self.start_pick_up = True
                    else:
                        self.t1 = time.time()
                        self.start_count_t1 = True
                        self.count = 0
                        self.center_list = []
        return img
    




if __name__ == '__main__':

    if sys.version_info.major == 2:
        print('Please run this program with python3!')
        sys.exit(0)

    ct = ColorTracking()
    ct.init()
    ct.start()


    # run the child thread (parent??)
    th = threading.Thread(target=ct.move)
    th.setDaemon(True)
    th.start()



    __target_color = ('red', )
    my_camera = Camera.Camera()
    my_camera.camera_open()
    while True:
        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            Frame = ct.run(frame)           
            cv2.imshow('Frame', Frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
    my_camera.camera_close()
    cv2.destroyAllWindows()
