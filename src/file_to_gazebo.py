#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
import gazebo_parameters
from robot_ddpg_gazebo.srv import *
import csv

x=[]
y=[]
t=[]
f = open("/tmp/kautham_path_to_gazebo.csv","r")
cr = csv.reader(f,delimiter=';')
for row in cr:
	x.append(row[0])
	y.append(row[1])
	t.append(row[2])

rospy.wait_for_service('kautham_loop_service')
try:			
	client=rospy.ServiceProxy('kautham_loop_service',KauthamLoopSrv)
	#float32[] x;float32[] y;float32[] t;int16 num_points;string[] obstacles;int16 num_obstacles;float32[] obstacle_positions;
	response=client(x,y,t,len(x),gazebo_parameters.OBSTACLE_NAMES,gazebo_parameters.NUM_OBSTACLES,gazebo_parameters.OBSTACLE_POSITIONS)
	return response.reward
except rospy.ServiceException, e:
	print "Service call failed: %s"%e
