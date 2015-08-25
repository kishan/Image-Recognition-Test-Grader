################################################################################
## -setting up webcam derived from 112 webcam demo
## -taking snapshot of video feed when spacebar is pressed and saving image 
##      as png file implemented by me
## -taking snapshot of video feed when spacebar is pressed and saving image 
##      as png file implemented by me
## -option to keep picture or retake picture implemented by me
##
##
##
################################################################################
################################################################################
## CODE DESCRIPTION
## 
## Program grades tests via Webcam
## -enables webcam and displays feed in window.
## -First Step is to take capture picture of answer sheet
## -Then user can begin grading all of his/her tests
## -After all tests are graded, complete score reports are shown for each test
## 
################################################################################

import cv2
import time
from grade import grade_paper
from display import draw_complete_score_report
import Tkinter
import tkMessageBox

#hard coded answers for testing
a_dict = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'A', 7: 'B', 8: 'C', 9: 'D', 10: 'E', 11: 'A', 12: 'B', 13: 'C', 14: 'D', 15: 'E', 16: 'A', 17: 'B', 18: 'C', 19: 'D', 20: 'E'}
s_dict = {1: '*', 2: 'B', 3: 'C', 4: 'A', 5: 'C', 6: 'A', 7: 'E', 8: 'C', 9: '*', 10: 'A', 11: 'A', 12: '*', 13: 'C', 14: 'C', 15: 'B', 16: 'A', 17: 'B', 18: 'C', 19: 'C', 20: 'D'}
s_dict1 = {1: 'D', 2: 'A', 3: 'B', 4: 'D', 5: 'A', 6: 'B', 7: 'E', 8: 'D', 9: '*', 10: 'A', 11: 'A', 12: '*', 13: 'B', 14: 'D', 15: 'E', 16: 'A', 17: 'B', 18: 'C', 19: 'C', 20: 'E'}

testDict = {1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'B', 6: 'B', 7: 'B', 8: 'B', 9: 'C', 10: 'C', 11: 'C', 12: 'C', 13: 'C', 14: 'D', 15: 'D', 16: 'D', 17: 'D', 18: 'D', 19: 'E', 20: 'E'}


#request user to capture snapshot of test
def get_picture_from_user(pic_option):
    def take_picture():
        ret, frame = camera.read()
        return frame
    window_name = "Webcam!"
    print cv2.CV_WINDOW_AUTOSIZE
    cam_index = 0 # Default camera is at index 0.
    cv2.namedWindow(window_name, cv2.CV_WINDOW_AUTOSIZE)
    camera = cv2.VideoCapture(cam_index) # Video capture object
    camera.open(cam_index) # Enable the camera
    if pic_option == "answer":
        pic_option_text = "Take picture of answer sheet"
        position = (60,25)
    else:
        pic_option_text = "Take picture of test"
        position = (130,25)
    # pictureChosen = False
    while True:
        ret, frame = camera.read()
        if frame is not None:
            cv2.putText(frame,pic_option_text,position, cv2.FONT_HERSHEY_PLAIN,
             2,(0,0,255),3)
            cv2.putText(frame,'Press Spacebar to take photo',(65,470), 
                cv2.FONT_HERSHEY_PLAIN, 2,(0,255,0),3)
            cv2.imshow(window_name, frame)
        k = cv2.waitKey(10) & 0xFF
        #take snapshot of video when spacebar is pressed
        if k == ord(" "): # Spacebar
            snapshot = take_picture()
            #flip image
            # snapshot = cv2.flip(snapshot, 1)
            #save image locally with filename !snapshot.png
            snapshotName = "!snapshot.png"
            cv2.imwrite(snapshotName, snapshot) #create png file with snapshot
            cv2.destroyAllWindows()
            camera.release() 
            break
            print "AMAZING"
         #close video window when user pressed Esc key
        if k == 27: # Escape key
            cv2.destroyAllWindows()
            camera.release()
            break

#give user option to either keep or retake snapshot
def keep_or_retake_picture(pic_option):
    while(True):
        snapshotImage = cv2.imread("!snapshot.png") 
        cv2.putText(snapshotImage,'Make sure image includes box',(60,25), 
            cv2.FONT_HERSHEY_PLAIN, 2,(255,0,0),3)
        cv2.putText(snapshotImage,'containing answers',(150,55), 
            cv2.FONT_HERSHEY_PLAIN, 2,(255,0,0),3)
        cv2.putText(snapshotImage,'Press Spacebar to grade next test',(20,447), 
            cv2.FONT_HERSHEY_PLAIN, 2,(0,0,255),3)
        if pic_option != "answer":
            cv2.putText(snapshotImage,'Press "x" if done grading',
            (90,422), cv2.FONT_HERSHEY_PLAIN, 2,(0,255,255),3)
        cv2.putText(snapshotImage,'Press "r" to retake photo',(87,475), 
            cv2.FONT_HERSHEY_PLAIN, 2,(0,255,0),3)
        cv2.imshow('img',snapshotImage)
        k = cv2.waitKey(33)
        if k==27:    # Esc key to stop
            cv2.destroyAllWindows()
            return "escape"
            break
        if k == ord(" "):
            cv2.destroyAllWindows()
            break
        if k == ord("s"):
            cv2.destroyAllWindows()
            return "place-holder"
            break
        #user presses x if finished grading
        if k == ord("x"):
            cv2.destroyAllWindows()
            return "finished"
        #user presses r to retake picture
        if k == ord("r"):
            cv2.destroyAllWindows()
            get_picture_from_user(pic_option)
            snapshotImage = cv2.imread("!snapshot.png") 
        elif k==-1:  # normally -1 returned,so don't print it
            continue
        else:
            print "Please press spacebar or 'r'" 


#########################################################################

def run_webcam_with_screenshot():
    taken = None
    count = 0
    #capture image of answer sheet and create dictionary of answers
    while taken == None:
        #get picture of answer sheet from user
        get_picture_from_user("answer")
        status = keep_or_retake_picture("answer")
        taken = "taken"
        #dictionary containing answers from answer sheet
        a_dict = grade_paper("!snapshot.png")
        #if user presses Esc key stop program
        if status == "escape":
            continue
        #if 20 bubbles are not recognized show error message to user
        if len(a_dict)!= 20:
            message1 = "Could not recognize answers. "
            message2 = "Please make sure box is completely inside frame and"
            message3 = "as close to screenas possible. Press OK to retake picture."
            title = "Error box"
            root = Tkinter.Tk()
            root.withdraw()
            tkMessageBox.showerror(title, message1 + message2 + message3)
            taken = None
            continue


    print "picture selected"

    #capture image of every test from user
    #create dictionary of answers for each test
    #create list containing dictionaries for all the tests
    tests = []
    complete = None
    count = 0
    while complete == None:
        #capture image of test from user
        get_picture_from_user("test")
        complete = keep_or_retake_picture("test")
        #add dictionary to tests list
        tests.append({})
        #add dictionary to list at count index
        tests[count] = grade_paper("!snapshot.png")
        #if user presses Esc key, exit program
        if complete == "escape":
            del tests[-1]
            continue
        # do ____ if s key is pressed"
        if complete == "place-holder":
            print "s pressed"
        #show error message if 20 answers are not detected
        if len(tests[count])!= 20:
            message1 = "Could not recognize answers. "
            message2 = "Please make sure box is completely inside frame and"
            message3 = "as close to screenas possible. Press OK to retake picture."
            title = "Error box"
            root = Tkinter.Tk()
            root.withdraw()
            tkMessageBox.showerror(title, message1 + message2 + message3)
            complete = None
            del tests[-1]
            continue
        count+=1


    print len(tests)
    for i in xrange(len(tests)):
        print tests[i]
        print
    

    # draw_complete_score_report(a_dict,s_dict)

    #draw score reports for each test
    def draw_multiple_score_reports(answers,testAnswers):
        for i in xrange(len(testAnswers)):
            testname = "Test " + str(i+1)
            draw_complete_score_report(answers,testAnswers[i], testname)
            time.sleep(0.1)


    #tests list fo dictionaries for testing
    # tests = [s_dict,s_dict1,testDict]
    draw_multiple_score_reports(a_dict,tests)


