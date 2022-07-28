import cv2
import mediapipe as mp
import csv

import json

# Set to true if original video was portrait and was taken on mobile 
# False by default
mobile_video = False;

from PIL import Image

# Testing CSV files to save coord data
csv_file = open('left_hand_positions.csv', mode='w')
fieldnames = ['frame', 'x', 'y', 'z', 'visibility']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

pose_file = open('pose_positions.csv', mode='w')
fieldnames = ['frame', 'coords']
wroter = csv.DictWriter(pose_file, fieldnames=fieldnames)
wroter.writeheader()


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


# Smooth landmarks are set to false by default 
holistic = mp_holistic.Holistic(
    min_detection_confidence=0.5, min_tracking_confidence=0.5, smooth_landmarks=False
)

# Create an object to read 
# from camera 
video = cv2.VideoCapture('test_face.mp4')


# We need to check if camera 
# is opened previously or not 
if (video.isOpened() == False): 
	print("Error reading video file") 

# We need to set resolutions. 
# so, convert them from float to integer. 
frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 


size = (frame_width, frame_height) 

# Below VideoWriter object will create 
# a frame of above defined The output 
# is stored in 'filename.avi' file. 

# depth array for yeah
z_forlefthand = []

# count fps in video => set fps of output video to original input
fps = video.get(cv2.CAP_PROP_FPS)
# count number of frames so we can show percentage complete
total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

result = cv2.VideoWriter('PoseTrackedVideo.avi', 
						cv2.VideoWriter_fourcc(*'MJPG'), 
						fps, size) 


test = 0

entire_list_of_positions = []
frame_numbers_posedetected = []

while(True): 
    ret, frame = video.read()
    if ret == True:
        
        # Write the frame into the 
        # file 'filename.avi'
        
        frame_number = video.get(cv2.CAP_PROP_POS_FRAMES)
        image = frame
        # code goes here XD
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = holistic.process(image)

        # Draw landmark annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw face landmarks on video
        #mp_drawing.draw_landmarks(
        #    image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS
        #)
        mp_drawing.draw_landmarks(
            image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS
        )
        mp_drawing.draw_landmarks(
            image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS
        )
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS
        )
        # write the holistics over the images and save as video file
        #result.write(image) ## USED TO BE HERE BUT CHECK END OF FILE FIRST
        
        # To fix rotation issue caused by mobile phone import, if mobile flag is true, fix rotation using small calculation
        # newY = oldX
        # newx = newheight - oldY


        # Attempt for each point in the body pose landmarks, try add text over the video specifying their id/number/name
        if(results.pose_landmarks):
            # Set start point as -1 so that it normalises to 0 on first, which matches up with the pose numbers guide :)
            join_point = -1
            list_of_joints = []
            for datapoint in results.pose_landmarks.landmark:
                # Print out the x y and z values of the body position on the image
                print(datapoint)

                if(mobile_video):
                    newy = datapoint.x
                    newx = 1 - datapoint.y
                    temp_position = [newx, newy, datapoint.z]
                else:
                   temp_position = [datapoint.x, datapoint.y, datapoint.z] 
                # Get x y and z values and append to a temporary array, then append array to a list
                #temp_position = [datapoint.x, datapoint.y, datapoint.z]
                list_of_joints.append(temp_position)
                # TEXT ONTOP OF VIDEO
                # Get the x and y so i can put text there, but multiply by width and height so that they match up with the scaling of the image frame
                position = (int(datapoint.x * frame_width), int(datapoint.y * frame_height))
                join_point = join_point + 1
                image = cv2.putText(image,"point " + str(join_point),position,cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3)


            # all points have been delt with, now processs
            frame_numbers_posedetected.append(frame_number)
            entire_list_of_positions.append(list_of_joints)

            #After the for in element means that here is after all pose joints in this frame
            #filehandle =  open('pose_positions.txt', 'w')
            #json.dump(list_of_joints, filehandle)

        else:
            position = (10,50)
            image = cv2.putText(image,"Python Examples",position,cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3)

        

        # print full landmark dict for left hand
        #print(results.left_hand_landmarks)
        # check if the hand is in frame, if so then proceed with getting its depth and positiobnal values
        # Actually used for fingers, for wrist position rather use the pose group and the number 14 and 15
        if(results.left_hand_landmarks):
            # get the depth values for the left hand
            for datapoint in results.left_hand_landmarks.landmark:
                #print(datapoint.z)
                clampedz = format(datapoint.z, '.8f')
                clampedz = float(clampedz) * 10
                clampedx = format(datapoint.x, '.8f')
                clampedx = float(clampedx) * 10
                clampedy = format(datapoint.y, '.8f')
                clampedy = float(clampedy) * 10
                writer.writerow({'frame': frame_number, 'x': clampedx, 'y': clampedy, 'z':clampedz})
                #z_forlefthand.append(datapoint.z)

        # write the holistics over the images and save as video file
        result.write(image) 
        # Print progress so far
        print(str(int(frame_number / total * 100)) + " % Complete")
            
        
    else: 
        break


# When everything done, release 
# the video capture and video 
# write objects
print(type(frame_numbers_posedetected))


# now that all frames are processed, write all pos data for each landmark on each frame to text file :0
filehandle =  open('pose_positions.txt', 'w')
json.dump(entire_list_of_positions, filehandle)
# write a list of the frames that were detected to get timing correct
framess =  open('pose_frames.txt', 'w')
json.dump(frame_numbers_posedetected, framess)

#print(z_forlefthand)
video.release() 
result.release() 

# Closes all the frames 
cv2.destroyAllWindows() 

print("The video was successfully saved") 
