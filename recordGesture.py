import sys, os, errno, Leap
import numpy as np

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
        self.tally = 0

    def on_init(self, controller):
        self.newListen = PinchListener(RecorderListener(GestureRecord()))


    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty:
            for hand in frame.hands:
                hpp = hand.palm_position
                hpv = hand.palm_velocity #hehe, hpv
                #self.grecord.append(frame, hpp, hpv)
                
                print "  frame %s, hpp %s, hpv: %s, strg: %s" % (
                frame.id, hand.palm_position, hand.palm_velocity, hand.pinch_strength)
                if hand.pinch_strength < 0.5:
                    self.tally += 1
                else:
                    self.grecord.append(hpp, hpv)

                if self.tally > 10:
                    controller.remove_listener(self)
                    controller.add_listener(self.newListen)
                    self.grecord.toFile("testing/%s/%s" % (gestureName, str(frame.id)))


class GestureRecord():
    def __init__(self):
        self.poss = np.zeros((1, 2))
        self.vels = np.zeros((1, 2))
        self.uninitialized  = True

    def append(self, pos, vel):
        if self.uninitialized:
            self.poss = np.array([pos.to_float_array()])
            self.vels = np.array([vel.to_float_array()])
            self.uninitialized = False
        else:
            self.poss = np.append(self.poss, [pos.to_float_array()],axis=0)
            self.vels = np.append(self.vels, [vel.to_float_array()],axis=0)

    def toFile(self, fName):
        output1 = self.poss[:,[0,1]]
        print output1
        np.save("%sposs" % fName, output1)

        output2 = self.vels[:,[0,1]]
        print output2
        np.save("%svels" % fName, output2)

# From StackOverflow: http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
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
    if gestureName:
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
    print "Enter pressed; ending recording session!"


if __name__ == "__main__":
    main()
