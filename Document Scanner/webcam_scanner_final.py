from webcam_with_screenshot import run_webcam_with_screenshot
from webcam_scanner_scan_test import save_scanned_test
import eventBasedAnimation
from Tkinter import *


def mouseDemoInitFn(data):
    print data.width,data.height
    (data.x, data.y) = (data.width/2, data.height/2)
    data.cx = data.width/2
    data.cy = data.height/2
    data.grade_y = 350
    data.scan_y = 250
    data.rect_width = 100
    data.rect_height = 20
    data.aboutText = data.windowTitle = "Webcam Grader - Kishan Patel"
    #import webcam gif
    filename = "pics/webcam2.gif"
    data.image = PhotoImage(file=filename)


#run whichever program the user selects (Scan Test or Grade Test)
def mouseDemoMouseFn(event, data):
    (data.x, data.y) = (event.x, event.y)
    #Grade Test
    if data.cx-data.rect_width<= event.x <= data.cx+data.rect_width and data.grade_y-data.rect_height <= event.y <= data.grade_y+data.rect_height:
        run_webcam_with_screenshot()
    #Scan Test
    if data.cx-data.rect_width<= event.x <= data.cx+data.rect_width and data.scan_y-data.rect_height <= event.y <= data.scan_y+data.rect_height:
        save_scanned_test()

def mouseDemoDrawFn(canvas, data):
	#draw background
    canvas.create_rectangle(0,0,data.width, data.height, fill="cyan")
    #draw wecam gif
    canvas.create_image(data.width/2,110,image=data.image)
    #draw text
    canvas.create_text(data.cx, 20, text = "Webcam Grader", font= "Arial 25 bold", fill = "red")

    #draw program choices (Scan Test or Grade Test)
    canvas.create_rectangle(data.cx-data.rect_width, data.grade_y-data.rect_height,
     data.cx+data.rect_width, data.grade_y+data.rect_height, fill="red")
    canvas.create_text(data.cx,data.grade_y, text = "Grade Tests", font= "Arial 25 bold", fill = "white")
    canvas.create_rectangle(data.cx-data.rect_width, data.scan_y-data.rect_height,
     data.cx+data.rect_width, data.scan_y+data.rect_height, fill="red")
    canvas.create_text(data.cx,data.scan_y, text = "Scan Tests", font= "Arial 25 bold", fill = "white")
    canvas.create_rectangle(data.cx-data.rect_width-20, 200,
     data.cx+data.rect_width+20, 400, outline="black", width = 3)
    # canvas.create_rectangle(data.width/2 - 50,70,data.width/2+60, 170 , outline="black", width = 3)


eventBasedAnimation.run(
    initFn=mouseDemoInitFn,
    mouseFn=mouseDemoMouseFn,
    drawFn=mouseDemoDrawFn,
    width=600, height=600
    )