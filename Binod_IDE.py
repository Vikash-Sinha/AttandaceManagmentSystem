#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 11:25:47 2020
@author: vikash
"""
from tkinter import *
from tkinter import filedialog
from tkinter import font
import subprocess
import os


#color formating for text area
 # Python keywords
keywords = [
            ' and ', ' assert ', ' break', 'class ', 'continue', 'def ',
            'del ', 'elif', 'else', 'except ', 'exec ', 'finally ',
            'for ', 'from ', 'global ', 'if', 'import ', ' in ',
            'is ', 'lambda', 'not ', 'or ', 'pass', 'print',
            'raise ', 'return ', 'try', 'while', 'yield',
            'None', 'True', 'False',
        ]
# Python operators
operators = [
            '=',
            # Comparison
            '==', '!=', '<', '<=', '>', '>=',
            # Arithmetic
            '\+', '-', '\*', '/', '//', '\%', '\*\*',
            # In-place
            '\+=', '-=', '\*=', '/=', '\%=',
            # Bitwise
            '\^', '\|', '\&', '\~', '>>', '<<',
        ]

# Python braces
braces = [
            '{', '}', '(', ')', '[', ']',
        ]
#from pynput import keyboard
root=Tk()
root.geometry('1850x850')
root.title('Binod IDE For Python')
path=""

#gloabal variable
global selected
global line_no
line_no=1
selected= False
global lngu
lngu="py"
val=StringVar(root)
val.set("language")

#function of line no
def lineDel(n=False):
    global line_no
    lists.delete(0,END)
    if line_no>0:
     for i in range(1,line_no+1):
         lists.insert(END, i)
    if(n):
        for i in range(line_no+1,n):
            lists.insert(END,i)
              
#functions of menu
def newFile(n=False):
    global path
    global text_area
    global line_no
    text_area.delete(1.0,END)
    line_no=1
    lineDel()
    path=""

    
def openFile(n=False):
    global path
    global line_no
    path=  filedialog.askopenfilename(initialdir = "/home/vikash/Windows_files_and_folder/Vikash_Sinha/d_drive/",title = "Select file",filetypes = (("java files","*.java"),("Python files","*.py")))
   # path="/home/vikash/Windows_files_and_folder/Vikash_Sinha/d_drive/java/chess/chess.java"
    try:
        if path!="":
            st=open(path,'r')
            opendata=st.read()
           
            global text_area
            text_area.delete(1.0,END)
            text_area.insert(END, opendata)
            # for line no
            count=opendata.split("\n")
            line_no=len(count)
            print(line_no)
            lineDel()
            formateColor()
            st.close()
    except:
        pass


def saveFile(n=False):
    global path
    if(path==""):
        file_name= filedialog.asksaveasfile(defaultextension=".py",initialdir="/home/vikash/Windows_files_and_folder/Vikash_Sinha/d_drive/python")
        path=file_name.name
        
    
       

    st=open(path,'w')
    st.write(text_area.get(1.0,END))
    st.close()
    
def saveAs(n=False):
    global path
    file_name= filedialog.asksaveasfile(defaultextension=".py",initialdir="/home/vikash/Windows_files_and_folder/Vikash_Sinha/d_drive/python")
    path=file_name.name

    st=open(path,'w')
    st.write(text_area.get(1.0,END))
    st.close()

def exits():
    root.destroy()

def cuttext():
    global selected
    selected=text_area.selection_get()
    text_area.delete("sel.first","sel.last")
    x=str(text_area.get(1.0,END))
    count=x.split("\n")
    no=len(count)
    lineDel(no)

def copytext():
    global selected
    selected=text_area.selection_get()
    
def pastetext():
    global selected

    if selected:
        pos=text_area.index(INSERT)
        text_area.insert(pos, selected)
        x=str(text_area.get(1.0,END))
        count=x.split("\n")
        no=len(count)
        lineDel(no)
        formateColor()

def formateColor():
    clr_font=font.Font(text_area,text_area.cget("font"))
    text_area.tag_configure("keywd", font=clr_font,foreground="red")
    for i in keywords:
        offset = '+%dc' % len(i) # +5c (5 chars)

        # search word from first char (1.0) to the end of text (END)
        pos_start = text_area.search(i, '1.0', END)
        
        # check if found the word
        while pos_start:
            # create end position by adding (as string "+5c") number of chars in searched word 
            pos_end = pos_start + offset
            
            text_area.tag_add('keywd', pos_start, pos_end)
            pos_start = text_area.search(i, pos_end, END)
    text_area.tag_configure("oprts", font=clr_font,foreground="#D68DD9")
    for i in operators:
        offset = '+%dc' % len(i) # +5c (5 chars)

        # search word from first char (1.0) to the end of text (END)
        pos_start = text_area.search(i, '1.0', END)
        
        # check if found the word
        while pos_start:
            # create end position by adding (as string "+5c") number of chars in searched word 
            pos_end = pos_start + offset
            text_area.tag_add('oprts', pos_start, pos_end)
            pos_start = text_area.search(i, pos_end, END)
    text_area.tag_configure("brces", font=clr_font,foreground="#797979")
    for i in braces:
        offset = '+%dc' % len(i) # +5c (5 chars)

        # search word from first char (1.0) to the end of text (END)
        pos_start = text_area.search(i, '1.0', END)
        
        # check if found the word
        while pos_start:
            # create end position by adding (as string "+5c") number of chars in searched word 
            pos_end = pos_start + offset
            text_area.tag_add('brces', pos_start, pos_end)
            pos_start = text_area.search(i, pos_end, END)
                
def checkNewLine(event):
    x=str(text_area.get(1.0,END))
    count=x.split("\n")
    no=len(count)
    lineDel(no)
    formateColor()
    
def runP(n=False):
  global lngu 
  global output
  saveFile()
  if path!="":
    exp=0
    if lngu=="py":
        a="python"+" "+path
        try:
            a = subprocess.check_output(a, shell=True)
            output.delete(1.0,END)
            print("jai mata di")
            output.insert(1.0,"Binod Bhaya>> \n")
            output.insert(END, a)
        except:
            '''exp_path=" &> /home/vikash/anaconda3/exception.txt"
            a="python "+path+exp_path
            print("a= ",a)
            os.system(a)
            s=open('/home/vikash/anaconda3/exception.txt','r')
            st=s.read()
            s.close()
            '''
            output.delete(1.0,END)
            output.insert(1.0,"Binod Bhaya>> \n Check your syntax")
    else:
        print("jai")
        global t
       
        t="ab"
        try:
            a=os.path.dirname(path)
            k=os.path.basename(path)
            os.chdir(a)
            a="javac "+k
            t = subprocess.check_output(a,shell=True)
            a=k[0:-5]
           
            a="java "+a
            t=subprocess.check_output(a, shell=True)
            output.delete(1.0,END)
            output.insert(1.0,"Binod Bhaya>> \n")
            output.insert(END, str(t))
        except:
          output.delete(1.0,END)
          output.insert(1.0,"Binod Bhaya>> \n Check Syntax Correctly")
          
        
  else:
    saveAs()
def javaP():
    global lngu
    lngu="java"
def pythP():
    global lngu
    lngu="py"
def lng(event):
    global lngu   
    if event=='Python':
        lngu="py"
    else:
        lngu="java"


#text area creation
menu_frame=Frame(root,background ="#24200C")
menu_frame.pack(fill=X)
op=OptionMenu(menu_frame,val,'Python','Java',command=lng)
op.pack(side=LEFT)
op=Button(menu_frame,text="Run", command=lambda: runP())
op.pack(side=LEFT)

scroll_frame=Frame(root)

scroll_frame.pack(fill=Y,side=LEFT)


 

#text area scroll bar create
text_scroll=Scrollbar(scroll_frame)
text_scroll.pack(fill=Y,side=RIGHT)
hscroll=Scrollbar(scroll_frame,orient='horizontal')
hscroll.pack(fill=X,side=BOTTOM)


#list created
lists=Listbox(scroll_frame, height=48,width=3,font='TkTextFont 14 bold',bg="#24200C",fg="#82AD3A",justify=CENTER,yscrollcommand=text_scroll.set)
lists.pack(fill=Y,side=LEFT)

text_area=Text(scroll_frame ,width=120,height=48,bg="#333",fg="#CEDF9F",font='TkTextFont 14 bold', wrap='none' ,yscrollcommand=text_scroll.set,xscrollcommand=hscroll.set)
text_area.bind('<Key>',checkNewLine)
text_area.pack(fill=Y,side=LEFT)


text_scroll.config(command=text_area.yview)
hscroll.config(command=text_area.xview)


#create Menu bar
my_menu=Menu(root,bg='#343434',fg='white',font='TkMenuFont 12 bold')
root.config(menu=my_menu)


lists.insert(0, 1)
#add file menu
file_menu=Menu(my_menu,font='TkMenuFont 12 bold')
my_menu.add_cascade(label='File',menu=file_menu)
file_menu.add_command(label='New',command= lambda: newFile(False),accelerator="Ctrl+n")  
file_menu.add_command(label='Open',command=lambda: openFile(False),accelerator="Ctrl+o")
file_menu.add_command(label='Save',command=lambda: saveFile(False),accelerator="Ctrl+s")
file_menu.add_command(label='Save As',command=lambda: saveAs(False),accelerator="Ctrl+shift+Q")
file_menu.add_separator()
file_menu.add_command(label='Exit',command=exits)

#add edit medu
edit_menu=Menu(my_menu,font='TkMenuFont 12 bold')
my_menu.add_cascade(label="Edit",menu=edit_menu)
edit_menu.add_command(label='Cut',command=cuttext)
edit_menu.add_command(label='Copy',command=copytext)
edit_menu.add_command(label='Paste',command=pastetext)
edit_menu.add_separator()
edit_menu.add_command(label='Undo',command=text_area.edit_undo())
edit_menu.add_command(label='Redo',command=text_area.edit_redo())

#add Run medu
run_menu=Menu(my_menu,font='TkMenuFont 12 bold')
my_menu.add_cascade(label="Run",menu=run_menu,accelerator="Ctrl+r")
run_menu.add_command(label='Run',command=lambda: runP())
run_menu.add_command(label='Stop')
val=StringVar()
'''#add language medu
lng_menu=Menu(my_menu,font='TkMenuFont 12 bold')
my_menu.add_cascade(label="Language",menu=lng_menu)
lng_menu.add_command(label='Python',command=pythP)
lng_menu.add_command(label='Java',command=javaP)'''




#console area creation
console=LabelFrame(root,text="BINODE CONSOLE",font='Arial 19 bold' ,fg='#332611')
console.pack(side=RIGHT,fill=Y)
#text area scroll bar create
text_scroll=Scrollbar(console)
text_scroll.pack(side=RIGHT,fill=Y)
output=Text(console,width=34,height=53,bg="#0F292C",fg="#B6D9E7",font='TkTextFont 14 bold',yscrollcommand=text_scroll.set)
text_scroll.config(command=output.yview)
output.pack(expand=YES)
output.insert(END,"Binod Bhaya >> \n")

#binding shortcut key
root.bind('<Control-Key-n>', newFile)
root.bind('<Control-Key-o>', openFile)
root.bind('<Control-Key-r>', runP)
root.bind('<Control-Key-s>', saveFile)
#root.bind('<Control_Key+n>', newFile())

root.mainloop()
