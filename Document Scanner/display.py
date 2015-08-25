import cv2
import numpy as np

(width,height) = (400,600)


#test dictionaries
y = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'A', 7: 'B', 8: 'C', 9: 'D', 10: 'E', 11: 'A', 12: 'B', 13: 'C', 14: 'D', 15: 'E', 16: 'A', 17: 'B', 18: 'C', 19: 'D', 20: 'E'}
z = {1: 'A', 2: 'B', 3: 'C', 4: 'A', 5: 'C', 6: 'A', 7: 'B', 8: 'C', 9: '*', 10: 'E', 11: 'A', 12: '*', 13: 'C', 14: 'D', 15: 'B', 16: 'A', 17: 'B', 18: 'C', 19: 'C', 20: 'E'}
# d = {1: '*', 2: '*', 3: '*', 4: '*', 5: '*', 6: '*', 7: '*', 8: '*', 9: '*', 10: '*', 11: '*', 12: '*', 13: '*', 14: '*', 15: '*', 16: '*', 17: '*', 18: '*', 19: '*', 20: '*'}

a = {1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'A', 6: 'A', 7: 'A', 8: 'A', 9: 'A', 10: 'A', 11: 'A', 12: 'A', 13: 'A', 14: 'A', 15: 'A', 16: 'A', 17: 'A', 18: 'A', 19: 'A', 20: 'A'}
b = {1: 'B', 2: 'B', 3: 'A', 4: 'B', 5: 'B', 6: 'B', 7: 'B', 8: 'B', 9: 'B', 10: 'B', 11: 'B', 12: 'B', 13: 'B', 14: 'B', 15: 'B', 16: 'B', 17: 'B', 18: 'B', 19: 'B', 20: 'B'}
c = {1: 'C', 2: 'C', 3: 'C', 4: 'B', 5: 'B', 6: 'C', 7: 'C', 8: 'C', 9: 'C', 10: 'C', 11: 'C', 12: 'C', 13: 'C', 14: 'C', 15: 'C', 16: 'C', 17: 'C', 18: 'C', 19: 'C', 20: 'C'}
d = {1: 'D', 2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'C', 7: 'C', 8: 'C', 9: 'D', 10: 'D', 11: 'D', 12: 'D', 13: 'D', 14: 'D', 15: 'D', 16: 'D', 17: 'D', 18: 'D', 19: 'D', 20: 'D'}
e = {1: 'E', 2: 'E', 3: 'E', 4: 'E', 5: 'E', 6: 'E', 7: 'E', 8: 'E', 9: 'D', 10: 'D', 11: 'D', 12: 'D', 13: 'E', 14: 'E', 15: 'E', 16: 'E', 17: 'E', 18: 'E', 19: 'E', 20: 'E'}

tests = [a,b,c]

#create new dictionary to compare student's responses to answers
# set value of eahc correct question key to "correct"
# put student' response as value if question is inccorect
def compare_answers(total_questions, a_dict, s_dict):
    compare_dict = {}
    correct = 0
    incorrect = 0
    for i in xrange(total_questions):
        question = i+1
        if a_dict[question] == s_dict[question]:
            compare_dict[question] = "correct"
            correct += 1
        else:
            compare_dict[question] = s_dict[question]
            incorrect += 1
    return (compare_dict, correct, incorrect)


#use percentage of correctly answered questions to determine letter grade
def determine_final_grade(percent_score):
    final_grade = ":)"
    if percent_score >= 97:
        final_grade = "A+"
    elif percent_score >= 93:
        final_grade = "A"
    elif percent_score >= 90:
        final_grade = "A-"
    elif percent_score >= 87:
        final_grade = "B+"
    elif percent_score >= 83:
        final_grade = "B"
    elif percent_score >= 80:
        final_grade = "B-"
    elif percent_score >= 77:
        final_grade = "C+"
    elif percent_score >= 73:
        final_grade = "C"
    elif percent_score >= 70:
        final_grade = "C-"
    elif percent_score >= 67:
        final_grade = "D+"
    elif percent_score >= 63:
        final_grade = "D"
    elif percent_score >= 60:
        final_grade = "D-"
    else:
        final_grade = "F"
    return final_grade


top_margin = height/6 #top section for displaying score
# bottom section for displaying questions with choices
answer_space_height = height - top_margin 
max_number_of_questions = 20
# height of each column
column_height = answer_space_height/max_number_of_questions 


def draw_background_and_score(fraction_score, percent_score_str, correct, incorrect, test_name):
    canvas.create_rectangle(0, 0, width, height, fill="sky blue", width=0)
    canvas.create_rectangle(0, 0, width, top_margin, fill="gold", width=0)

    # draw fraction and perceft score on top of canvas
    # display number of correct and incorrect questios
    text_margin = 15
    canvas.create_text(text_margin+20, top_margin/3, text =fraction_score, anchor="nw", 
            fill = "black", font = "Arial 30 bold")
    canvas.create_text(width-text_margin, top_margin/3, text=percent_score_str, 
            anchor = "ne", fill = "black", font = "Arial 30 bold")
    canvas.create_text((width)/2, top_margin - 15, text = "Correct: "+
        str(correct), anchor = "s", fill = "black", font = "Arial 10 bold")
    canvas.create_text((width)/2, top_margin/3, text = test_name, anchor= "center", fill = "blue", font = "Arial 30 bold")
    canvas.create_text((width)/2, top_margin, text = "Incorrect: "+
        str(incorrect), anchor = "s", fill = "black", font = "Arial 10 bold")


# find the upper y-value of given row
def col_y(row_index):
    return top_margin + row_index*column_height

# find the center y value of given row
def col_cy(row_index):
    return col_y(row_index) + column_height/2

# draw answer choices next for each question number
def draw_answer_choices(start_x, height, margin):
    canvas.create_text(start_x+margin*0, height, text = "A", anchor = "center", 
        fill = "black", font = "Arial 10 bold")
    canvas.create_text(start_x+margin*1, height, text = "B", anchor = "center", 
        fill = "black", font = "Arial 10 bold")
    canvas.create_text(start_x+margin*2, height, text = "C", anchor = "center", 
        fill = "black", font = "Arial 10 bold")
    canvas.create_text(start_x+margin*3, height, text = "D", anchor = "center", 
        fill = "black", font = "Arial 10 bold")
    canvas.create_text(start_x+margin*4, height, text = "E", anchor = "center", 
        fill = "black", font = "Arial 10 bold")


# circle and highlight the correct answer in green
def circle_correct_choice(start_x, height, margin, correctIndex):
    index = correctIndex
    # center and redius of green circle to draw
    cx = start_x+margin*index
    cy = height
    r = 10
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline="black", fill = "green", width=2)

# if student answer is incorrect, higlight incorrect answer in red
def circle_wrong_choice(start_x, height, margin, wrongIndex, omitted):
        if wrongIndex != None:
            index = wrongIndex
            # center and redius of red circle to draw
            cx = start_x+margin*index
            cy = height
            r = 10
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline="black", fill = "red", width=2)
            if omitted == False:
                canvas.create_text(start_x+margin*5, height, text = "Incorrect", anchor = "w", fill = "black", font = "Arial 10 bold")

def draw_omitted(start_x, height, margin, omitted, wrongIndex):
    if omitted == True:
        index = wrongIndex
        # left coordinates of text
        lx = start_x+margin*index
        ly = height
        canvas.create_text(start_x+margin*5, height, text = "Omitted", anchor = "w", fill = "black", font = "Arial 10 bold")

def draw_final_letter_grade(percent_score):
    final_grade = determine_final_grade(percent_score)
    cx = width-width/4
    cy = height/2
    r = 40
    text_size = 50
    if len(final_grade) == 2:
        text_size = 40
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline="red", width=2)
    canvas.create_text(cx,cy, text = final_grade, anchor = "center", fill="red", 
        font = "Arial "+str(text_size)+" bold")


# turn multiple choice letter option into index where "A" has index of 0
def choice_to_index(letter):
    return ord(letter) - ord("A") 


def draw_results(percent_score, total_questions, compare_dict, a_dict, s_dict):
    # for every question draw question number, choices, and highlighting of 
    # corret and incorrect answers
    for i in xrange(total_questions):
        question = i + 1
        omitted = False
        if s_dict[question] == "*":
            omitted = True
        correctIndex = choice_to_index(a_dict[question])
        if compare_dict[question] != "correct":
            wrongIndex = choice_to_index(s_dict[question])
        else: wrongIndex = None
        l_margin = 45 #where to start letter choices
        space_between_choices = 30
        canvas.create_text(2, col_cy(i), text = str(i+1) + ".)", anchor = "w", 
            fill = "black", font = "Arial 10 bold")
        circle_correct_choice(l_margin,col_cy(i),space_between_choices,correctIndex)
        circle_wrong_choice(l_margin, col_cy(i), space_between_choices, wrongIndex, omitted)
        draw_answer_choices(l_margin, col_cy(i), space_between_choices)
        draw_omitted(l_margin, col_cy(i), space_between_choices,omitted, wrongIndex)
        draw_final_letter_grade(percent_score)

from Tkinter import *



def draw_complete_score_report(a_dict, s_dict, test_name):#, s1_dict, s2_dict):
    root = Tk()
    global canvas
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()




    total_questions = 20
    (compare_dict, correct, incorrect) = compare_answers(total_questions, a_dict, s_dict)
    #calculate score in fraction form and percent form
    fraction_score = str(correct) + "/" + str(total_questions)
    percent_score = float(correct)/total_questions*100
    percent_score_str = str(float(correct)/total_questions*100) + "%"

    
    draw_background_and_score(fraction_score, percent_score_str, correct, incorrect, test_name)
    draw_results(percent_score, total_questions, compare_dict, a_dict, s_dict)
    # t = {1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'B', 6: 'B', 7: 'B', 8: 'B', 9: 'C', 10: 'C', 11: 'C', 12: 'C', 13: 'C', 14: 'D', 15: 'D', 16: 'D', 17: 'D', 18: 'D', 19: 'E', 20: 'E'}

    # debugging
    # draw_complete_score_report(y,z)

