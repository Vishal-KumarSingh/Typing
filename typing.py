from tkinter import Tk,Text,Label,Scrollbar
import tkinter
from _thread import start_new_thread
import time
from pygame import mixer
def playmusic():
    mixer.music.load("sms.mp3")
    mixer.music.set_volume(1.0)
    mixer.music.play()

def startthread(event):
    global thread_status
    if thread_status==1:
        start_new_thread(countdown, (15*60,))
        thread_status=0
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        timer_clock.configure(text=timer)
        time.sleep(1)
        t -= 1
    playmusic()
    typing_space.configure(state="disabled")
def next_line(event):
    global current_line,current_word_in_line
    current_line+=1
    current_word_in_line=1
    color_word(current_line,current_word_in_line)


def submit_word(event):
    global current_line,current_word_in_line,score,wrong,score,input_text
    current_word_in_line+=1
    typed_text = typing_space.get("1.0", tkinter.END).split(" ")
    if len(typed_text)>1:
        input_text = typed_text[-2]

        if input_text == current_word:
            score += 1
            correct_word.configure(text=score)
        else:
            wrong+=1
            wrong_word.configure(text=wrong)
            playmusic()

    color_word(current_line,current_word_in_line)


def color_word(current_line , current_word_in_line):
    global current_word
    for tag in msg_field.tag_names():
        msg_field.tag_delete(tag)
    current_line_str = list_of_line[current_line-1]
    current_words_in_line = current_line_str.split(" ")
    current_word = current_words_in_line[current_word_in_line-1]
    startingindex = current_line_str.find(current_word)
    start=str(current_line)+"."+str(startingindex)
    endindex=current_line_str.find(" ",startingindex)
    if(endindex==-1):
        endindex=200
    end=str(current_line)+"."+str(endindex)
    msg_field.tag_add("start", start, end)
    msg_field.tag_config("start", background="black", foreground="yellow")



def typingspace():
    global display,file,list_of_line

    scrollview.place(x=1000, y=20, width="10", height="300")
    msg_field.place(x=400, y=20, height='300', width="600")

    msg_field.insert(tkinter.INSERT, string)

    msg_field.configure(state="disabled")
    typing_space.place(x=400, y=350, height='300',width="600")
    typing_space.bind("<FocusIn>", startthread)
    scrollview.config(command=msg_field.yview)
    timer_clock.place(x=1100,y=20, height="100", width="100")
    wrong_word.place(x=50,y=20, height="50", width="300")
    correct_word.place(x=50,y=120, height="50", width="300")

    display.bind('<space>', submit_word)
    display.bind('<Return>', next_line)
    list_of_line = msg_field.get("1.0", tkinter.END).split("\n")
    submit_word(0)



mixer.init()
current_word=""
input_text=""
score=0
wrong=0
thread_status=1
list_of_line=[]
current_line=1
current_word_in_line=0
display = Tk()
display.geometry("1400x800")
display.title("Typing Expert")
display.iconbitmap('typing.ico')
file = open("exercise.txt", "rt")
string = file.read()
scrollview = Scrollbar(display)
msg_field = Text(display, bg="#03fce3", fg="black", yscrollcommand=scrollview.set, font=("Helvetica", 15))
typing_space = Text(display, bg="#dffc03", fg="black", font=("Helvetica", 20))
timer_clock = Label(display, text="15:00" , bg="black", fg="white", font=("Helvetica", 20))
correct_word = Label(display, text="Correct Words" , bg="white", fg="green", font=("Helvetica", 20))
wrong_word = Label(display, text="Wrong Words" , bg="white", fg="red", font=("Helvetica", 20))
typingspace()
display.mainloop()
file.close()