# Automatic motion generator
Author:
Qingyun Wang
Prerequisite: 
Software: amc2bvh, motionbuilder
Library: pyfbsdk (included in motionbuilder)
Functionality:
Amc2bvh can batch convert asf and amc files into bvh files
Retargeter.py can retarget bvh files into existing character model to render video
Steps:
Create list_asf.txt, list_amc.txt,list_bvh.txt, List the source files in amc, asf list and destination into bvh list
Run AMC2BVH file
Open motionbuilder
Run the retargeter.py
Choose the folder which characters prototype exists and then choose the source of bvh file 
