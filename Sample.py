################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
import sys

#sys.path.append("/LeapSDK/lib")
#sys.path.append("/LeapSDK/lib/x64")
#sys.path.append("/LeapSDK/lib/x86")

import Leap
import thread, time
import numpy as np

lFrame = np.zeros((1, 1))
lPosData = np.zeros((1,3))
lVelData = np.zeros((1,3))

rFrame = np.zeros((1, 1))
rPosData = np.zeros((1,3))
rVelData = np.zeros((1,3))

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        # Get hands
        for hand in frame.hands:
            global lFrame, lPosData, lVelData, rFrame, rPosData, rVelData
            handType = "Left hand" if hand.is_left else "Right hand"

            
            if handType == "Left hand":
                lFrame   = np.append(lFrame, [frame.id])
                lPosData = np.append(lPosData,[hand.palm_position.to_float_array()], axis=0)
                lVelData = np.append(lVelData,[hand.palm_velocity.to_float_array()], axis=0)
            if handType == "Right hand":
                rFrame   = np.append(rFrame, [frame.id])
                rPosData = np.append(rPosData,[hand.palm_position.to_float_array()], axis=0)
                rVelData = np.append(rVelData,[hand.palm_velocity.to_float_array()], axis=0)

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction


        if not frame.hands.is_empty:
            print ""

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

        global lFrame, lPosData, lVelData, rFrame, rPosData, rVelData
        # Do data stuff
        np.size(lFrame, 0)
        lData = np.hstack((lPosData, lVelData))
        rData = np.hstack((rPosData, rVelData))
        #np.set_printoptions(precision=3)
        print "\nLeft Hand Array"
        print lData
        print "\nRight Hand Array"
        print rData
        
        


if __name__ == "__main__":
    main()
