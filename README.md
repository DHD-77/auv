# auv



TASK 1:

Creating a package:
  A package is like a folder, inside which we keep all our codes and files. To create a package, type:
  ros2 pkg create --build-type ament_python --node-name comm_node comm_link --dependencies rclpy std_msgs

  After creating check if the build is successfull by the following cmd:
  colcon build --packages-select comm_link

  i'm going to use python to write the code, thats why we build using ament_python, the node name is comm_node and    the package name is comm_link
  Dependencies are the libraries that we are going to use, it makes our code a lot simpler.


Writing Code:
  First line is the default line called the Shebang which is #!/bin/usr/env python3

  Then we import all the classes and libraries:
  import rclpy
  from rclpy.node import Node
  from std_msgs.msg import String
  import sys

  Creating a class:
    First i give the node a name as chat_node.
    Then to know who the speaker is, i get the name from the user and store it in self.username. It helps in           reducing noise as i dont wanna print the data to the person who spoke.

  Then i publish a message(String) in the topic chat.
  self.publisher_ = self.create_publisher(String, 'chat', 10)

  Then i create a subscriber.
  self.subscription = self.create_subscription(String, 'chat',self.listener_callback, 10)
  Here listener_callback is a function which is run every time this subscription happens

Threading:
  This is a very important part. By default a python script has only one thread. In this task we have two subtasks that wait forever. rclpy.spin(), and input(). Whichever comes first, the code is stuck in that.
  So we create two threads, such that they can be independent of each other, but still in the same node

  self.input_thread = threading.Thread(target=self.input_loop)
  this creates a worker, it tells the worker that its only job is to run this function

  self.input_thread.daemon = True
  this is a safety setting, a daemon is a helper thread. It means if the main program closes, its job is to kill this thread also.

  self.input_thread.start()
  this is the 'go' signal, the worker leaves the main group and starts running the input_loop on its own.

input_loop:
  it waits for the input from the user, it checks if its an empty string or not, if not then it publishes it.




TASK 2:

I have to create 3 nodes inside a package and connect them in a pipe sort of manner.
Created the package in the same manner as before.
The first node is pretty simple, its just publishing multiples of 2 to raw_signal topic.
The difference is now we have to import Int32 as we are dealing with integers.

Challenge: Dont know how to create a second node.
Sol: Go to the package and inside it go to the executable python file. type touch node2.py and continue.

Second node, i had to subscribe to raw_signal and publish to processed_signal

Third node, i had to simply subscribe to processed_signal and print data + 10


TASK 3:

First i have to create a interface.
As I have to create a datatype on my own. This will be down by creating a new package, which uses C language.
Python acts like a worker, while C is used for defining Dictionaries and all.
in custom_interfaces i create a msg file in which all the data is there. In that i create BotPose, in which i have x,y and direction.
Now to convert this english into something that the computer can understand i have to add some line of code to the 
package_xml and Cmakelists.txt

build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
add this to package.xml
the first line converts english to a language which computer understands
second line adds some runtime libraries
third tells that this is  a specialized interface

Writing Code:
  The code is pretty simple for this task, nothing different from previous tasks

The differnce in this task is how do i create my own datatype and use it.


TASK 4:

In this i have to use the opencv library and do this task.
Lets do this step by step.

Step 1: Making the camera work
Code: I created a vision_node.py in which imported cv2 
self.cap = cv2.VideoCapture(0)
0 means the default camera in the laptop, this step connects to the webcam.

For 30 frames per second, I tell it to capture a photo every 1/30 sec
self.timer = self.create_timer(1.0/30.0, self.timer_callback)

timer_callback: 
ret, frame = self.cap.read()
ret will be true if it worked.
if its true then we create a window and show the frame inside it by cv2.imshow("Feed", frame)
cv2.waitKey(1) -> waitinig 1ms to allow the window to process the image

Now we move on to creating a new window which shows us the mask.
We will be using HSV so that the colour does not change if its in shadow or not.
first convert the frame from bgr to hsv -> hsv_frame = (cv2.cvtColor(frame, cvw.COLOR_BGRHSV))
Then we define the lower and upper bounds of color red and store it in an array
low_red = np.array([0,120,70])

Then create the mask: this turns everything red into white and rest to black
mask = cv2.inRange(hsv_frame, lower_blue , upper_blue)
Then show the window: cv2.imshow("Mask Filter", mask)

Now we find the centre of the white mask, to do that we use moments
Moments are basically weighted averages that describe the shape of the obju=ect
M = cv2.moments(mask)
m["m00"] -> area
m["m10"] -> sum of x coordinates
m["m01"] -> sum of y coordinates

cX is x coordinates by area, similar for y also
Then to know that its working we create a circle on the object
cv2.circle(frame, (cx,cy),20,(0,255,0),-1)

Then based on the values of x and y, I put the corresponding filter.

# I know that you told to commit every day, I did, I added everything daily to my README
# (Whatever I learnt each day), but while pushing the files I accidently deleted my
# README. 

