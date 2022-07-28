import bpy, csv
import numpy as np
import math
import pdb
from mathutils import Vector

#fp = "D:\Alexander\HolisticBodyTracking/left_hand_positions.csv"
import json
import numpy as np

# open output file for reading
with open('D:\Alexander\HolisticBodyTracking/pose_positions.txt', 'r') as posityions:
    allframes = json.load(posityions)

# read frames used data
with open('D:\Alexander\HolisticBodyTracking/pose_frames.txt', 'r') as frames_pose:
    frame_count = json.load(frames_pose)


'''
For my setup by default: correct the coordinal axies
input => blender axies
z => y
x => x
y = > z
'''

# Below enter the numerical value of the joints to track. Eg: left and right shoulder are 11 and 12, so 10 and 11
Tracked_Limbs = [10, 11]

# List of joints names corresponding to the mediapipe names. Just keep here as a backup of the old names :)
#list_of_Joints = ['nose', 'left_eye_inner', 'left_eye', 'left_eye_outer', 'right_eye_inner', 'right_eye', 'right_eye_outer', 'left_ear', 'right_ear', 'mouth_left', 'mouth_right', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_pinky', 'right_pinky', 'left_index', 'right_index', 'left_thumb', 'right_thumb', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'leftankle', 'right_ankle', 'left_heel', 'right_heel', 'left_foot_index', 'right_foot_index']

# List of all joint names for ease of automation. Make sure names correspond to armeture bone names in blender made by MBLab Plugin
list_of_Joints = ['nose', 'left_eye_inner', 'left_eye', 'left_eye_outer', 'right_eye_inner', 'right_eye', 'right_eye_outer', 'left_ear', 'right_ear', 'mouth_left', 'mouth_right', 'clavicle_L', 'clavicle_R', 'left_elbow', 'upperarm_R', 'left_wrist', 'right_wrist', 'left_pinky', 'right_pinky', 'left_index', 'right_index', 'left_thumb', 'right_thumb', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'leftankle', 'right_ankle', 'left_heel', 'right_heel', 'left_foot_index', 'right_foot_index']

#In each frame
for alljoints in allframes:
    #For each joint being tracked
    for joint in Tracked_Limbs:
        x = format(alljoints[joint][0], '.8f')
        y = format(alljoints[joint][1], '.8f')
        z = format(alljoints[joint][2], '.8f')

        # Optionally amplify their coords for bigger models
        #clampedx = float(x) * 10
        #clampedy = float(y) * 10
        #clampedz = float(z) * 10

        # Get the current frame => set correct keyframe position on timeline
        current_frame = allframes.index(alljoints)
        current_frame = frame_count[current_frame]

        # Old code to get the object by bone name in skeleton
        #ob = bpy.context.scene.objects["f_ca01_skeleton"] 
        #ob = ob.pose.bones["clavicle_R"]

        # Get bone by name in list_of_joints and set its coords
        ob = bpy.context.scene.objects["f_ca01_skeleton"] 
        ob = ob.pose.bones[list_of_Joints[joint]]

        # Set the keyframe with that location, and which frame.
        #ob.keyframe_insert(data_path="location", frame=1) # Old method to declare coords on first frame
        ob.location = float(x), float(y), float(z)
        ob.keyframe_insert(data_path="location", frame=current_frame)
    
