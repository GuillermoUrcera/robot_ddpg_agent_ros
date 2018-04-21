#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
import robot_ddpg_agent.src.gazebo_parameters as gazebo_parameters
from robot_ddpg_gazebo.srv import *
import csv

xx=[]
yy=[]
tt=[]
x=[]
y=[]
t=[]

f=open("/tmp/kautham_path_to_gazebo.csv","r")
cr=csv.reader(f,delimiter=';')
for row in cr:
		if row[0]=="--":
			xx.append(x)
			yy.append(y)
			tt.append(t)
			x=[]
			y=[]
			t=[]
		else:
			x.append(float(row[0]))
			y.append(float(row[1]))
			t.append(float(row[2]))
f.close()

target_file=open("/tmp/kautham_path_in_gazebo.csv","w")
writer=csv.writer(target_file,delimiter=';') #print: Distance;Obstacle displacement;reward

rospy.wait_for_service('kautham_loop_service')

for e in range(len(xx)):
	try:			
		client=rospy.ServiceProxy('kautham_loop_service',KauthamLoopSrv)
		#float32[] x;float32[] y;float32[] t;int16 num_points;string[] obstacles;int16 num_obstacles;float32[] obstacle_positions;
		response=client(xx[e],yy[e],tt[e],len(xx[0]),gazebo_parameters.OBSTACLE_NAMES,gazebo_parameters.NUM_OBSTACLES,gazebo_parameters.OBSTACLE_POSITIONS)
		writer.writerow([response.distance_covered,response.obstacle_displacement,response.reward])
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
target_file.close()

