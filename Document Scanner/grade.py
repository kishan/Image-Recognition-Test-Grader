#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html
import cv2
import numpy as np
from scan_new import reposition_object

################################################################################
## source1: http://blog.ayoungprogrammer.com/2013/03/tutorial-creating-
##          multiple-choice.html
## 
## 
## 
## organizing circles into rows - derived from source 1
## sort circles in each group by x values - myself
## function to find density of white pixels - myself
## 
##
################################################################################


# paramters are image, center of circle, and radius
# function returns the density of white pixels in the square region with side 
# length 2*r centered around the center of the circle 
def whitePixelDensity(img, center, r):
    radius = r
    (height, width) = img.shape[:2]
    (cx,cy) = center
    #upper and lower bounds of x and y coordinates
    left_cx, right_cx = int(cx-radius), int(cx+radius)
    top_cy, bottom_cy = int(cy-radius), int(cy+radius)
    #if square region is off image, adjust region
    if left_cx<= 0: left_cx = 1
    if right_cx >= width: right_cx= width-1
    if top_cy <=0: top_cy = 1
    if bottom_cy >= height: bottom_cy = height -1
    count = 0
    #count number of white pizels in square region
    for x in xrange(left_cx,right_cx+1):
        for y in xrange(top_cy, bottom_cy+1):
            r,g,b = img[y,x]
            if (r,g,b) == (255,255,255): count+=1
    #area of region which pizels are being counted from
    area = (right_cx - left_cx)*(bottom_cy - top_cy)
    return float(count)/area


# filename = "!snapshot.png"

def grade_paper(filename):

    reposition_object(filename) #repositions file and saves as "!.jpg"
    new_filename = "!"+str(filename)
    # img = cv2.imread("!!!.jpg",0)  
    img = cv2.imread(new_filename,0)  

    cimg = cv2.adaptiveThreshold(img,255,\
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,75,10)

    cimg = cv2.cvtColor(cimg,cv2.COLOR_GRAY2RGB)

    #20 questions
    circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,minDist = 25 ,
                                param1=100,param2=10,minRadius=7,maxRadius=13)

    ti = cv2.adaptiveThreshold(img,255,\
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,75,10)
    ti = cv2.cvtColor(ti,cv2.COLOR_GRAY2RGB)


    ############################################################################
    #-organize all circles in rows
    #-rows list will contain tuples representing each row where 1st element in
    #   tuple is y-coord of row and 2nd element is index of row in bubble list
    #-bubble list contains lists of circles grouped by row
    ############################################################################

    bubble = []
    row = []

    if circles is not None: 
        for i in circles[0,:]: #loop through all circles
            found = False
            x = i[0]
            y = i[1]
            r = i[2]
            # loop through all different rows
            for j in xrange(len(row)):
                y2 = row[j][0]
                if y-r<y2 and y+r>y2: #check if two circles are in the same row
                #add circle to corresponding list inside bubble list
                    bubble[j].append(i) 
                    found = True
                    break
            # if circle is in new row, create new row in row and bubble list
            if found == False:
                index = len(row)
                row.append((y,index)) 
                bubble.append([i])
            found = False

    # print "###############################################"

    removeCounter = 0
    for i in xrange(len(bubble)):
        # print len(bubble[i-removeCounter])
        if len(bubble[i-removeCounter])<= 2:
            # print "!!!!",i
            bubble = bubble[:i - removeCounter] + bubble[i+1 - removeCounter:]
            row = row[:i - removeCounter] + row[i+1 - removeCounter:]
            removeCounter +=1


    # sort group of circles based on row (y-coordinate)
    # sort by comparing y-coordinate of first cricle of each group
    bubble.sort(key = lambda x: x[0][1])


    # sort circles in each group by x values
    # sort by comparing x-coordinate of each circle in each group
    for groupIndex in xrange(len(bubble)):
        bubble[groupIndex].sort(key = lambda x: x[0])




    student = {}
    """
    total = 0
    for i in xrange(len(bubble)):
        if len(bubble[i])>=3:
            total+= len(bubble[i])
    numOfRows = len(bubble)
    bubblePerRow = total/numOfRows
    """
    bubblePerRow = 5


    # loop through each row of circles in order from top to bottom
    # determine the circle which has the greatest density in each row
    for i in xrange(len(bubble)):
        maxDensity = 0
        filledCir = 0
        index = -1
        for j in xrange(len(bubble[i])):
            cir = bubble[i][j]
            x,y,r = cir[0], cir[1], cir[2]
            # cv2.rectangle(cimg,(x-r,y-r),(x+r,y+r),(255,0,0),2)
            density = whitePixelDensity(cimg, (x,y), r)
            print i+1, density
            if density>= 0.5 and density> maxDensity:
                maxDensity = density
                index = j

                # zzz = (x,y,r)
        # print i+1,maxDensity
        # (x,y,r) = zzz
        # cv2.circle(cimg,(x,y),r,(150,100,255),3, 8, 0)
        if index <= -1:
            print "%d:*" % (i+1)
            student[i+1] = "*"
        else:
            if len(bubble[i])>bubblePerRow: index-=len(bubble[i])-bubblePerRow
            print "%d:%s" %(i+1, chr(ord("A")+index))
            student[i+1] = chr(ord("A")+index)


    """
    #display sorted bubble 1 by 1
    if bubble is not None: 
        for group in bubble:
            for cir in group:
                # draw the outer circle
                cv2.circle(ti,(cir[0],cir[1]),cir[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(ti,(cir[0],cir[1]),2,(0,0,255),3)

    cv2.imshow('test',ti)
    """
    return student

# cv2.circle(cimg,(215,160),8,(150,100,255),3)
# cv2.circle(cimg,(65,150),25,(0,255,255),2)
# cv2.imshow('detected circles',cimg)
# cv2.imshow('test',ti)


# print grade_paper("!snapshot.png")

def get_answers():
    return student

# cv2.waitKey(0)
# cv2.destroyAllWindows()