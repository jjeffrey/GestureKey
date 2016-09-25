import sys, os, errno
import numpy as np
from sklearn.cluster import KMeans
import Leap
import socket
import time

gestureName = "g1"

class PinchListener(Leap.Listener):
    def __init__(self, recorderListener):
        super(PinchListener, self).__init__()
        self.recorder = recorderListener
    
    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty:
            for hand in frame.hands:
                if hand.pinch_strength > 0.7:
                    controller.remove_listener(self)
                    controller.add_listener(self.recorder)

class RecorderListener(Leap.Listener):
    def __init__(self, record):
        super(RecorderListener, self).__init__()
        self.grecord = record

    def on_init(self, controller):
        self.newListen = PinchListener(RecorderListener(GestureRecord()))


    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty:
            for hand in frame.hands:
                hpp = hand.palm_position
                hpv = hand.palm_velocity #hehe, hpv
                #self.grecord.append(frame, hpp, hpv)
                self.grecord.append(hpv)
                print "  frame %s, hpp %s, hpv: %s, strg: %s" % (
                frame.id, hand.palm_position, hand.palm_velocity, hand.pinch_strength)
                if hand.pinch_strength < 0.5:
                    controller.remove_listener(self)
                    controller.add_listener(self.newListen)
                    self.grecord.toFile(''.join(['testing/', gestureName, '/', str(frame.id)]))


class GestureRecord():
    def __init__(self):
        #self.frames = np.zeros((1, 1))
        #self.poss = np.zeros((1, 3))
        self.vels = np.zeros((1, 3))

    def append(self, vel):
       # if np.size(self.vels,axis=1) == 1:
            #self.frames = np.array([[frame.id]])
            #self.poss = np.array([pos.to_float_array()])
            self.vels = np.array([vel.to_float_array()])
       # else:
            #self.frames = np.append(self.frames, [frame.id])
            #self.positions = np.append(self.poss, [pos.to_float_array()])
            self.vels = np.append(self.vels, [vel.to_float_array()])

    def toFile(self, fName):
        file = open(fName, "w")
        self.vels.tofile(file)
        file.close()

# def get_point_centroids(data, K, D)

# mean = np(size(dat))

def recToPinch(frecord):
    return PinchListener(RecorderListener(frecord))

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def main():
    listener = PinchListener(RecorderListener(GestureRecord()))
    controller = Leap.Controller()

    global gestureName

    print "Type the name of the new gesture you want to add."
    gestureName = sys.stdin.readline()[:-1]
    controller.add_listener(listener)
    print "Press Enter when you are done adding versions of the gesture! (You can type in a new gesture name to change the gesture you are recording for.)"
    while(gestureName):
        make_sure_path_exists(''.join(["testing/", gestureName]))
        print "Recording for the gesture '%s':" % (gestureName)
        try:
            gestureName = sys.stdin.readline()[:-1]
        except KeyboardInterrupt:
            pass
        finally:
            pass

if __name__ == "__main__":
    main()
