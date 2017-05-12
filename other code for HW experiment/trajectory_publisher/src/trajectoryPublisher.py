#!/usr/bin/env python

import roslib
roslib.load_manifest('trajectory_publisher')

import numpy as np
import rospy
import os
import rospkg
import time
# from geometry_msgs.msg import PoseArray
# from geometry_msgs.msg import Pose
from imp_messages_package.msg import ImpedanceControlArray
from imp_messages_package.msg import ImpedanceControl
#import ImpedanceControlArray
#import ImpedanceControl

# get path to trajectory_publisher ros package
p = rospkg.RosPack().get_path('trajectory_publisher')
# get filelist in the trajectories dir
fs  = os.listdir(p+'/trajectories/new')
# initialize publisher
rospy.init_node('trajectoryPublisher')
pub = rospy.Publisher('/trajectories',ImpedanceControlArray)

p_new = p+'/trajectories/new/'
p_sent = p+'/trajectories/sent/'

# monitor folder for new files
while True:
    print 'checking for new files'
    fs  = os.listdir(p_new)
    for f in fs:
        thisFile = open(p_new+f,'r')
        msg = ImpedanceControlArray()
        for line in thisFile:
            line_s = line.split()
            thisImpCtrl = ImpedanceControl()
            thisImpCtrl.pose.position.x = float(line_s[0])
            thisImpCtrl.pose.position.y = float(line_s[1])
            thisImpCtrl.pose.position.z = float(line_s[2])
            thisImpCtrl.pose.orientation.x = float(line_s[3])
            thisImpCtrl.pose.orientation.y = float(line_s[4])
            thisImpCtrl.pose.orientation.z = float(line_s[5])
            thisImpCtrl.pose.orientation.w = float(line_s[6])
            thisImpCtrl.stiff = float(line_s[7])
            msg.poses.append(thisImpCtrl.pose)
	    msg.stiffs.append(thisImpCtrl.stiff)
        pub.publish(msg)
	print 'message published'
        thisFile.close()
 #       move to sent trajectories folder
        os.rename(p_new+f,p_sent+f)
    time.sleep(5)




