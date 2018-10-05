#!/usr/bin/env python2.7
import gym
import reacher.Reacher
import numpy as np
import cv2
import math
import scipy as sp
import collections
import time
class MainReacher():
    def __init__(self):
        self.env = gym.make('ReacherMy-v0')
        self.env.reset()

    def detect_l1(self,image,quadrant):
        #The quadrant parameter should be set to the location of the end of the link whether it is in the upper-right (UR), upper-left (UL), lower-right (LR), lower-left (LL) quarter with respect to the previous joint. This will tell you the angle sign and values
        #In this method you can focus on detecting the rotation of link 1, colour:(102,102,102)
        
        if quadrant == "UR":
            #should be between 0 and math.pi/2
            
            return 
        elif quadrant == "UL":
            #should be between math.pi/2 and math.pi
            
            return 
        elif quadrant == "LR":
            #should be between -0 and -math.pi/2
            
            return
        elif quadrant == "LL":
            #should be between -math.pi/2 and -math.pi
            
            return

    def detect_l2(self,image,quadrant):
        #The quadrant parameter should be set to the location of the end of the link whether it is in the upper-right (UR), upper-left (UL), lower-right (LR), lower-left (LL) quarter with respect to the previous joint. This will tell you the angle sign and values
        #In this method you can focus on detecting the rotation of link 2, colour:(51,51,51)
        
        if quadrant == "UR":
            #should be between 0 and math.pi/2
            
            return 
        elif quadrant == "UL":
            #should be between math.pi/2 and math.pi
            
            return 
        elif quadrant == "LR":
            #should be between -0 and -math.pi/2
            
            return
        elif quadrant == "LL":
            #should be between -math.pi/2 and -math.pi
            
            return

    def detect_l3(self,image,quadrant):
        #The quadrant parameter should be set to the location of the end of the link whether it is in the upper-right (UR), upper-left (UL), lower-right (LR), lower-left (LL) quarter with respect to the previous joint. This will tell you the angle sign and values
        #In this method you can focus on detecting the rotation of link 3, colour:(0,0,0)
        
        if quadrant == "UR":
            #should be between 0 and math.pi/2
            
            return 
        elif quadrant == "UL":
            #should be between math.pi/2 and math.pi
            
            return 
        elif quadrant == "LR":
            #should be between -0 and -math.pi/2
            
            return
        elif quadrant == "LL":
            #should be between -math.pi/2 and -math.pi
            
            return


    def detect_blue(self,image):
        #In this method you can focus on detecting the center of the blue circle
        
        return

    def detect_green(self,image):
        #In this method you should focus on detecting the center of the green circle
        
        return

    def detect_red(self,image):
        #In this method you should focus on detecting the center of the red circle
        return

    def detect_target(self,image):
        #Detect the center of the target circle (Colour: [200,200,200])
        return

    def detect_joint_angles(self,image):
        #Calculate the relevant joint angles from the image
        return

    def detect_joint_angles_chamfer(self,image):
        #Calculate the relevant joint angles from the image
        return 

    def detect_ee(self,image):
        #Detect the end effector location
        return

    def FK(self,joint_angles):
        #Forward Kinematics using homogeneous matrices to calculate end effector location
        #Each link is 1m long
        return

    def FK_analytic(self,joint_angles):
        #Forward Kinematics using the analytic equation
        #Each link is 1m long
        return

    def Jacobian(self,joint_angles):
        #Geometric Jacobian
        return

    def Jacobian_analytic(self,joint_angles):
        #Analytic Jacobian
        return

    def IK(self, current_joint_angles, desired_position):
        #Inverse Kinematics calculations
        return

    def coordinate_convert(self,pixels):
        #Converts pixels into metres
        return np.array([(pixels[0]-self.env.viewerSize/2)/self.env.resolution,-(pixels[1]-self.env.viewerSize/2)/self.env.resolution])

    def go(self):
        #The robot has several simulated modes:
        #These modes are listed in the following format:
        #Identifier (control mode) : Description : Input structure into step function

        #POS : A joint space position control mode that allows you to set the desired joint angles and will position the robot to these angles : env.step((np.zeros(3),np.zeros(3), desired joint angles, np.zeros(3)))
        #POS-IMG : Same control as POS, however you must provide the current joint angles and velocities : env.step((estimated joint angles, estimated joint velocities, desired joint angles, np.zeros(3)))
        #VEL : A joint space velocity control, the inputs require the joint angle error and joint velocities : env.step((joint angle error (velocity), estimated joint velocities, np.zeros(3), np.zeros(3)))
        #TORQUE : Provides direct access to the torque control on the robot : env.step((np.zeros(3),np.zeros(3),np.zeros(3),desired joint torques))
        self.env.controlMode="POS"
        #Run 100000 iterations
        prev_JAs = np.zeros(3)
        prev_jvs = collections.deque(np.zeros(3),1)
        self.env.D_gains[0] = 80
        for _ in range(100000):
            #The change in time between iterations can be found in the self.env.dt variable
            dt = self.env.dt
            #self.env.render returns and rgb_array containing the image of the robot
            rgb_array = self.env.render('rgb-array')

            jointAngles = np.array([3.14,-2,-1.14])
            #jointAngles = np.array([0,3.14,3.14])
            self.env.step((np.zeros(3),np.zeros(3),jointAngles, np.zeros(3)))
            #The step method will send the control input to the robot, the parameters are as follows: (Current Joint Angles/Error, Current Joint Velocities, Desired Joint Angles, Torque input) 

#main method
def main():
    reach = MainReacher()
    reach.go()

if __name__ == "__main__":
    main()
