import tkinter as tk
import language_tool_python
from tkinter import ttk
from tkinter import font,colorchooser,filedialog,messagebox
from spellchecker import SpellChecker
from PIL import Image,ImageEnhance
import os,sys,io,execjs,subprocess,time

main_application=tk.Tk()
main_application.geometry('1200x800')
main_application.title('Vpad text editor')

# ****************************************Main Menu**************************************************************

main_menu=tk.Menu(main_application)
file_menu=tk.Menu(main_menu,tearoff=False)
#file icons
new_icon=tk.PhotoImage(file='Sem3_Python_Project/new1.png')
open_icon=tk.PhotoImage(file='Sem3_Python_Project/open1.png')
save_icon=tk.PhotoImage(file='Sem3_Python_Project/save1.png')
Saveas_icon=tk.PhotoImage(file='Sem3_Python_Project/Save_as1.png')
Exit_icon=tk.PhotoImage(file='Sem3_Python_Project/Exit1.png')
# file menus

# main menu functioanlity

url=''
def new_file():
    global url
    url=''
    text_editor.delete(1.0,'end')

file_menu.add_command(label='New',image=new_icon,compound=tk.LEFT,accelerator='Ctrl+N',command=new_file)

def open_file():
    global url
    url=filedialog.askopenfilename(initialdir="D:/",title='Select File',filetypes=(('Text File','*.txt'),('All files','*.*')))
    print(url)
    try:
        with open(url,'r') as fr:
            text_editor.delete(1.0,'end')
            text_editor.insert(1.0,fr.read())
    except FileNotFoundError:
        return
    except:
        return
    main_application.title(os.path.basename(url))

file_menu.add_command(label='Open',image=open_icon,compound=tk.LEFT,accelerator='Ctrl+O',command=open_file)


# Save functionality

def save_file():
    global url
    try:
        if url:
            with open(url,'w',encoding='utf-8') as fw:
                content=text_editor.get(1.0,'end')
                fw.write(content)
        else:
            url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text file','*.txt'),('All files','*.*')))
            content2=text_editor.get(1.0,'end')
            url.write(content2)
            url.close()
    except:
        return

file_menu.add_command(label='Save',image=save_icon,compound=tk.LEFT,accelerator='Ctrl+S',command=save_file)

def save_file_as():
    global url
    try:
            url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text file','*.txt'),('All files','*.*')))
            content2=text_editor.get(1.0,'end')
            url.write(content2)
            url.close()
    except:
        return


file_menu.add_command(label='Save As..',image=Saveas_icon,compound=tk.LEFT,accelerator='Ctrl+Alt+S',command=save_file_as)


def exit():
    global url,text_changed
    try:
        if text_changed:
            mbox=messagebox.askyesnocancel('Warning','Do you want to save this file')
            if mbox is True:
                if url:
                    try:
                        with open(url,'w') as fw:
                            fw.write(text_editor.get(1.0,'end'))
                            main_application.destroy()
                    except:
                        return
                else:
                    url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text file','*.txt'),('All files','*.*')))
                    url.write(text_editor.get(1.0,'end'))
                    url.close()
                    main_application.destroy()
            elif mbox is False:
                    main_application.destroy()
        else:
            main_application.destroy()
    except:
        return

        

file_menu.add_command(label='Exit',image=Exit_icon,compound=tk.LEFT,accelerator='Ctrl+Q',command=exit)

# edit icons
edit_menu=tk.Menu(main_menu,tearoff=False)

copy_icon=tk.PhotoImage(file='Sem3_Python_Project/Copy1.png')
paste_icon=tk.PhotoImage(file='Sem3_Python_Project/Paste1.png')
cut_icon=tk.PhotoImage(file='Sem3_Python_Project/Cut1.png')
clear_icon=tk.PhotoImage(file='Sem3_Python_Project/Clear1.png')
find_icon=tk.PhotoImage(file='Sem3_Python_Project/Find1.png')

# Find Functionality

varfind=tk.StringVar()
varreplace=tk.StringVar()
def find1():
    text_editor.tag_remove("highlight",'1.0','end')
    search_text = varfind.get().strip() 
    pos='1.0'
    while True:
        pos=text_editor.search(varfind.get(),pos,stopindex=tk.END)
        if not pos:
            break
        end_pos=f'{pos}+{len(search_text)}c'
        text_editor.tag_add('highlight',pos,end_pos)
        pos=end_pos
    text_editor.tag_config('highlight',foreground='red',background="yellow")


def find(event):
    global varfind,varreplace
    new_win=tk.Toplevel()
    new_win.title("Find")
    new_win.geometry("300x200")
    find_label=tk.Label(new_win,text='Enter Text to find')
    find_label.grid(row=0,column=0,padx=20,pady=20,sticky=tk.W)
    find_entry=tk.Entry(new_win,width=16,textvariable=varfind)
    find_entry.grid(row=0,column=1,pady=20)
    replace_label=tk.Label(new_win,text='Enter Text to replace')
    replace_label.grid(row=1,column=0,padx=20,pady=20,sticky=tk.W)
    replace_entry=tk.Entry(new_win,width=16,textvariable=varreplace)
    replace_entry.grid(row=1,column=1,pady=20)
    find_btn=tk.Button(new_win,text='Find',command=find1)
    find_btn.grid(row=2, column=0, columnspan=2)
    

edit_menu.add_command(label='Copy',image=copy_icon,compound=tk.LEFT,accelerator='Ctrl+C',command=lambda:text_editor.event_generate("<<Copy>>"))
edit_menu.add_command(label='Paste',image=paste_icon,compound=tk.LEFT,accelerator='Ctrl+V',command=lambda:text_editor.event_generate("<<Paste>>"))
edit_menu.add_command(label='Cut',image=cut_icon,compound=tk.LEFT,accelerator='Ctrl+X',command=lambda:text_editor.event_generate("<<Cut>>"))
edit_menu.add_command(label='Clear',image=clear_icon,compound=tk.LEFT,accelerator='Ctrl+Alt+X',command=lambda:text_editor.delete(1.0,'end'))
edit_menu.add_command(label='Find',image=find_icon,compound=tk.LEFT,accelerator='Ctrl+F',command=lambda:find(None))


# view icons
tool_var=tk.IntVar(value=0)
status_var=tk.IntVar(value=0)

def hide_tool():
    if(tool_var.get()==1):
        tool_bar.pack_forget()
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=tk.TOP,fill='x')
        text_editor.pack(expand=True,fill='both')
        status_bar.pack(side=tk.BOTTOM)
def hide_status():
    if(status_var.get()==1):
        status_bar.pack_forget()
    else:
        tool_bar.pack_forget()
        text_editor.pack_forget()
        tool_bar.pack(side=tk.TOP,fill='x')
        text_editor.pack(expand=True,fill='both')
        status_bar.pack(side=tk.BOTTOM)

view_menu=tk.Menu(main_menu,tearoff=False)

tick_icon=tk.PhotoImage(file='D:/Python/GUI/Tick1.png')
view_menu.add_checkbutton(label="Tool bar",variable=tool_var,command=hide_tool)
view_menu.add_checkbutton(label="Status bar",variable=status_var,command=hide_status)

# color theme

themeVar=tk.StringVar()

def change_color(a):
    text_editor.config(background=a)
color_menu=tk.Menu(main_menu,tearoff=False)
color1=tk.PhotoImage(file='Sem3_Python_Project/White1.png')
color2=tk.PhotoImage(file='Sem3_Python_Project/Red1.png')
color3=tk.PhotoImage(file='Sem3_Python_Project/Yellow1.png')
color4=tk.PhotoImage(file='Sem3_Python_Project/Black1.png')

color_menu.add_radiobutton(label="Black",image=color4,compound=tk.LEFT,variable=themeVar,command=lambda:change_color('black'))
color_menu.add_radiobutton(label="White",image=color1,compound=tk.LEFT,variable=themeVar,command=lambda:change_color('white'))
color_menu.add_radiobutton(label="Red",image=color2,compound=tk.LEFT,variable=themeVar,command=lambda:change_color('red'))
color_menu.add_radiobutton(label="Yellow",image=color3,compound=tk.LEFT,variable=themeVar,command=lambda:change_color('yellow'))
print(themeVar)

# cascade

main_menu.add_cascade(label='File',menu=file_menu)
main_menu.add_cascade(label='Edit',menu=edit_menu)
main_menu.add_cascade(label='View',menu=view_menu)
main_menu.add_cascade(label='Color Theme',menu=color_menu)

#****************************************************toolbar**********************************************************************************
tool_bar=ttk.Label(main_application)
tool_bar.pack(side=tk.TOP,fill=tk.X)
font_tuple=tk.font.families()
font_family=tk.StringVar()
font_box=ttk.Combobox(tool_bar,textvariable=font_family,state='readonly',width=30)
font_box['values']=font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0,column=0,padx=5)


# Side box
sizevar=tk.IntVar()
font_size=ttk.Combobox(tool_bar,textvariable=sizevar,state='readonly',width=14)
font_size['values']=tuple(range(8,81,2))
font_size.grid(row=0,column=1,padx=5)
font_size.current(4)

#Bold,Italic,Underline icons
bold_icon=tk.PhotoImage(file='Sem3_Python_Project/Bold1.png')
italic_icon=tk.PhotoImage(file='Sem3_Python_Project/Italic1.png')
underline_icon=tk.PhotoImage(file='Sem3_Python_Project/Underline1.png')


bold_btn=ttk.Button(tool_bar,image=bold_icon)
bold_btn.grid(row=0,column=2,padx=5)

italic_btn=ttk.Button(tool_bar,image=italic_icon)
italic_btn.grid(row=0,column=3,padx=5)

underline_btn=ttk.Button(tool_bar,image=underline_icon)
underline_btn.grid(row=0,column=4,padx=5)

# font_color button
fontcolor_icon=tk.PhotoImage(file='Sem3_Python_Project/Color1.png')
fontcolcor_btn=ttk.Button(tool_bar,image=fontcolor_icon)
fontcolcor_btn.grid(row=0,column=5,padx=5)

# align icons
align1=tk.PhotoImage(file='Sem3_Python_Project/alignleft1.png')
align1_btn=ttk.Button(tool_bar,image=align1)
align1_btn.grid(row=0,column=6,padx=5)

align2=tk.PhotoImage(file='Sem3_Python_Project/aligncenter1.png')
align2_btn=ttk.Button(tool_bar,image=align2)
align2_btn.grid(row=0,column=7,padx=5)


align3=tk.PhotoImage(file='Sem3_Python_Project/alignright1.png')
align3_btn=ttk.Button(tool_bar,image=align3)
align3_btn.grid(row=0,column=8,padx=5)
# align2=tk.PhotoImage(file='D:/Python/GUI/aligncenter1.png')
# align3=tk.PhotoImage(file='D:/Python/GUI/alignright1.png')

# align1_btn=ttk.Button(tool_bar,image=align1)
# align2_btn=ttk.Button(tool_bar,image=align2)
# align3_btn=ttk.Button(tool_bar,image=align3)

# align1_btn.grid(row=0,column=6,padx=5)
# align2_btn.grid(row=0,column=7,padx=5)
# align3_btn.grid(row=0,column=8,padx=5)


#----------------------------------------------------------------text editor------------------------------------------------------------------------------

text_editor=tk.Text(main_application)
text_editor.config(wrap='word',relief=tk.FLAT)

scroll_bar=tk.Scrollbar(main_application)
text_editor.focus_set()  #----------> TO focus on text editor
scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
text_editor.pack(fill=tk.BOTH,expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

# font family and font size functionality
current_font_family='Arial'
current_font_size=16

def change_font(main_application):
    global current_font_family
    current_font_family=font_family.get()
    text_editor.configure(font=(current_font_family,current_font_size))
def change_font_size(main_application):
    global current_font_size
    current_font_size=sizevar.get()
    text_editor.configure(font=(current_font_family,current_font_size))

font_box.bind('<<ComboboxSelected>>',change_font)
font_size.bind('<<ComboboxSelected>>',change_font_size)

# -------------------------------------button functionality---------------------------------
# bold
def change_bold():
    text_property=tk.font.Font(font=text_editor['font'])
    if text_property.actual()['weight']=='normal':
        if text_property.actual()['underline']==1:
            if text_property.actual()['slant']=='roman':
                text_editor.config(font=(current_font_family,current_font_size,'bold underline'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'bold italic underline'))
        else:
            if text_property.actual()['slant']=='roman':
                text_editor.config(font=(current_font_family,current_font_size,'bold'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'bold italic'))
    else:
        if text_property.actual()['underline']==1:
            if text_property.actual()['slant']=='roman':
                text_editor.config(font=(current_font_family,current_font_size,'underline'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'italic underline'))
        else:
            if text_property.actual()['slant']=='roman':
                text_editor.config(font=(current_font_family,current_font_size,'normal'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'italic'))


bold_btn.configure(command=change_bold)

# Italic function

def change_italic():
    text_property=tk.font.Font(font=text_editor['font'])
    if text_property.actual()['slant']=='roman':
        if text_property.actual()['underline']==1:
            if text_property.actual()['weight']=='normal':
                text_editor.config(font=(current_font_family,current_font_size,'italic underline'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'bold italic underline'))
        else:
            if text_property.actual()['weight']=='normal':
                text_editor.config(font=(current_font_family,current_font_size,'italic'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'bold italic'))
    else:
        if text_property.actual()['underline']==1:
            if text_property.actual()['weight']=='normal':
                text_editor.config(font=(current_font_family,current_font_size,'underline'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'bold underline'))
        else:
            if text_property.actual()['weight']=='normal':
                text_editor.config(font=(current_font_family,current_font_size,'normal'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'bold'))

italic_btn.configure(command=change_italic)


# Underline

def change_underline():
    text_property=tk.font.Font(font=text_editor['font'])
    if text_property.actual()['underline']==0:
        if text_property.actual()['slant']=='roman':
            if text_property.actual()['weight']=='normal':
                text_editor.config(font=(current_font_family,current_font_size,'underline'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'bold underline'))
        else:
            if text_property.actual()['weight']=='normal':
                text_editor.config(font=(current_font_family,current_font_size,'italic'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'bold italic'))
       
    else:
        if text_property.actual()['slant']=='roman':
            if text_property.actual()['weight']=='normal':
                text_editor.config(font=(current_font_family,current_font_size,'normal'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'bold'))
        else:
            if text_property.actual()['weight']=='normal':
                text_editor.config(font=(current_font_family,current_font_size,'italic'))
            else:
                text_editor.config(font=(current_font_family,current_font_size,'bold italic'))
underline_btn.configure(command=change_underline)

# font color
def change_font_color():
    color_var=colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])

fontcolcor_btn.configure(command=change_font_color)

# align functinaolity

def alignleft():
    text_content=text_editor.get(1.0,'end')
    text_editor.tag_config('left',justify=tk.LEFT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_content,'left')

align1_btn.configure(command=alignleft)


def aligncenter():
    text_content=text_editor.get(1.0,'end')
    text_editor.tag_config('center',justify='center')
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_content,'center')

align2_btn.configure(command=aligncenter)

def alignright():
    text_content=text_editor.get(1.0,'end')
    text_editor.tag_config('right',justify=tk.RIGHT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_content,'right')

align3_btn.configure(command=alignright)

text_editor.configure(font=('Arial',16))

# --------------------------------------------------------------End text editor---------------------------------------------------------
# -------------------------------------------------------------status bar--------------------------------------------------------

status_bar=ttk.Label(main_application,text='Status Bar')
status_bar.pack(side=tk.BOTTOM)

# status bar functionality
text_changed=False
def changed(event):
    global text_changed
    if text_editor.edit_modified():
        text_changed=True
        words=len(text_editor.get(1.0,'end-1c').split())
        chracters=len(text_editor.get(1.0,'end-1c'))
        status_bar.configure(text=f'Chracters:{chracters}  Words:{words}')
    text_editor.edit_modified(False)
text_editor.bind('<<Modified>>',changed)


# ------------------------------------------------------------End of status bar------------------------------------------------


# ------------------------------------------------------------Extra Functionalites--------------------------------------------------

#-------------------------------------------------------SpellChecker-----------------------------------------------------
def highlights(l1,l2):
    # Adding highlight for misspelled words
    text_editor.tag_remove('highlight','1.0',tk.END)
    for i in l1:
        pos='1.0'
        while True:
            pos=text_editor.search(i,pos,stopindex=tk.END)
            if not pos:
                break
            endpos=f'{pos}+{len(i)}c'
            text_editor.tag_add('highlight',pos,endpos)
            pos=endpos
    text_editor.tag_config('highlight',background='yellow')
    # Adding highlight for new added words
    for i in l2:
        pos='1.0'
        while True:
            pos=text_editor.search(i,pos,stopindex=tk.END)
            if not pos:
                break
            endpos=f'{pos}+{len(i)}c'
            text_editor.tag_add('highlight1',pos,endpos)
            pos=endpos
    text_editor.tag_config('highlight1',background='blue')
def spellcheck():
    content=text_editor.get('1.0','end-1c')
    if(len(content)==0):
        messagebox.showinfo('SpellCheck','Enter Text')
    else:
        list=[]
        corrected_words=[]
        spell = SpellChecker()
        text=content
        words = text.split()
        print(words)

        # corrected_words = [spell.correction(word) for word in words]
        for word in words:
            d=spell.correction(word)
            if(d!=word):
                list.append(d)
            corrected_words.append(d)
        corrected_text = " ".join(corrected_words)

        print("Corrected:", corrected_text)
        print(list)


        tool = language_tool_python.LanguageTool('en-US')

        text = content

        # Get grammar corrections
        matches = tool.check(text)

        # Print corrected text
        corrected_text = language_tool_python.utils.correct(text, matches)
        print("Corrected:", corrected_text)

        ds=[]

        for i in corrected_text.split():
            if(i not in text):
                ds.append(i)
        print(ds)
        text_editor.delete('1.0','end')
        text_editor.insert('1.0',corrected_text)
        highlights(list,ds)


main_menu.add_command(label="SpellChecker",command=spellcheck)
#-------------------------------------------------------End spellchecker---------------------------------------------------

#------------------------------------------------------Image Functionality-------------------------------------------------
img_format=tk.StringVar()
img_sharpness=tk.StringVar()
img_brightness=tk.StringVar()
img_height=tk.StringVar()
img_width=tk.StringVar()
img_path=tk.StringVar()
img_savepath=tk.StringVar()


def sub():
    img1=Image.open(img_path.get())
    width,height=img1.size
    img_ss=img_savepath.get().split('.')[0]
    img_ss=img_ss+img_format.get()
    if len(img_width.get())>0 and len(img_height.get())>0:
        img1.thumbnail((int(img_width.get()),int(img_height.get())))
    if len(img_width.get())>0 and len(img_height.get())<=0:
        img1.thumbnail((int(img_width.get()),int(height)))
    if len(img_width.get())<=0 and len(img_height.get())>0:
        img1.thumbnail((int(width),int(img_height.get())))
    enhancer=ImageEnhance.Sharpness(img1)
    img_sharp=enhancer.enhance(int(img_sharpness.get()))
    enhancer=ImageEnhance.Brightness(img_sharp)
    enhancer.enhance(int(img_brightness.get())).save(img_ss)
    print('SIuu')
def Image1():
    def check_click(event):
        try:
            url=filedialog.askopenfile(title="Choose Image",filetypes=[("JPG FILES","*.jpg"),("PNG FILES","*.png"),("ALL FILES","*.*")])
            if url:
                entry1.insert(0,url.name)
                entry1.config(state='readonly')
                entry4.insert(0,url.name)
                # Checking if image url is correct or not
                try:
                    img1=Image.open(url.name)
                    # Creating a combobox for user to select img format
                    #-------------------------------------------------
                except Exception as e:
                    messagebox.showerror("Incoorect","Enter correct format")
                    new_win.destroy()
                #---------------------------------------
        except Exception as e:
            print(e)
        
    new_win=tk.Toplevel()
    new_win.title("Image COnverter")
    new_win.geometry("1000x500")
    lf=ttk.LabelFrame(new_win,text="Image",width=600, height=200)
    lf.pack()
    label1=ttk.Label(lf,text="Choose Image:")
    label1.grid(row=0,column=0,padx=10)
    entry1=ttk.Entry(lf,width=16,textvariable=img_path)
    entry1.grid(row=0,column=1,padx=10)
    entry1.bind('<Button-1>',check_click)

    label2=ttk.Label(lf,text="Choose Format:")
    label2.grid(row=1,column=0,padx=10)
    combobox1=ttk.Combobox(lf,width=16,textvariable=img_format,state='readonly')
    combobox1['values']=('.jpg','.png','.pdf')
    combobox1.current(0)
    combobox1.grid(row=1,column=1,pady=10)
    label3=ttk.Label(lf,text="Choose Sharpness:")
    label3.grid(row=2,column=0,padx=10)
    combobox2=ttk.Combobox(lf,width=16,state='readonly',textvariable=img_sharpness)
    combobox2['values']=tuple([i for i in range(11)])
    combobox2.current(1)
    combobox2.grid(row=2,column=1,pady=10)
    label4=ttk.Label(lf,text="Choose Brightness:")
    label4.grid(row=3,column=0,padx=10)
    combobox3=ttk.Combobox(lf,width=16,state='readonly',textvariable=img_brightness)
    combobox3['values']=tuple([i for i in range(11)])
    combobox3.current(1)
    combobox3.grid(row=3,column=1,pady=10)
    label5=ttk.Label(lf,text="Resize your image:")
    label5.grid(row=4,column=0)
    label6=ttk.Label(lf,text="Enter height:")
    label6.grid(row=5,column=0)
    entry2=ttk.Entry(lf,width=10,textvariable=img_height)
    entry2.grid(row=5,column=1,sticky='W')
    label7=ttk.Label(lf,text="Enter width:")
    label7.grid(row=6,column=0,pady=10)
    entry3=ttk.Entry(lf,width=10,textvariable=img_width)
    entry3.grid(row=6,column=1,sticky='W',pady=10)
    label8=ttk.Label(lf,text="Enter Path of Image to saved")
    label8.grid(row=7,column=0,pady=10)
    entry4=ttk.Entry(lf,width=16,textvariable=img_savepath)
    entry4.grid(row=7,column=1,sticky='W',pady=10)
    submit_btn=ttk.Button(new_win,text='Submit',command=sub)
    submit_btn.pack()
    lf.after(1, lambda: combobox1.current(combobox1['values'].index('.jpg')))
    lf.after(1, lambda: combobox2.current(combobox2['values'].index('1')))
    lf.after(1, lambda: combobox3.current(combobox3['values'].index('2')))

main_menu.add_command(label="Image",command=Image1)

# --------------------------------------------------End of image functionality-----------------------------------------------
#-------------------------------------------------------------Canva--------------------------------------------------------
canvas1=''
def freehand(event):
    global startx,starty
    startx,starty=event.x,event.y
def freehandmotion(event):
    global startx,starty
    canvas1.create_line(startx,starty,event.x,event.y,fill='black',width=5)
    startx,starty=event.x,event.y
def Shapes():
    global canvas1
    fillcolor=tk.StringVar()
    outlinecolor=tk.StringVar()
    shapewidth=tk.StringVar()
    sw=tk.StringVar()
    new_win=tk.Toplevel()
    new_win.geometry('1200x800')
    new_win.title("Draw Shapes")
    notebook=ttk.Notebook(new_win)
    notebook.pack(expand=True,fill='both')
    tab1=ttk.Frame(notebook)
    tab2=ttk.Frame(notebook)

    notebook.add(tab1,text="Tab 1")
    notebook.add(tab2,text="Tab 2")

    labelframe=ttk.LabelFrame(tab1,text="Shapes",height=300,width=300)
    labelframe.pack()

    label1=ttk.Label(labelframe,text='Select Shape')
    label1.grid(row=0,column=0)
    combobox=ttk.Combobox(labelframe,width=16,state='readonly',textvariable=sw)
    combobox['values']=('Rectangle','Oval','Circle',"Line",'Polygon')
    combobox.grid(row=0,column=1)


    canvas=tk.Canvas(tab1,width=400,height=300,bg='lightgray')
    canvas.pack()

    la=ttk.Label(tab2,text="Draw freehand drawing:")
    la.pack()

    canvas1=tk.Canvas(tab2,height=600,width=600,bg='lightgray')
    canvas1.pack()
    canvas1.bind('<Button-1>',freehand)
    canvas1.bind('<B1-Motion>',freehandmotion)

    def select(event):
        current_shape=sw.get()
        val1=tk.StringVar()
        val2=tk.StringVar()
        val3=tk.StringVar()
        val4=tk.StringVar()
        l=[val1,val2,val3,val4]

        def draw():
            def on_press(event):
                global selected_item, start_x, start_y
                selected_item = canvas.find_closest(event.x, event.y)[0]  
                start_x, start_y = event.x, event.y
            def on_drag(event):
                global start_x, start_y
                dx, dy = event.x - start_x, event.y - start_y  # Calculate movement
                canvas.move(selected_item, dx, dy)  # Move shape
                start_x, start_y = event.x, event.y  # Update position

            try:
                a1=int(val1.get())
                a2=int(val2.get())
                a3=int(val3.get())
                a4=int(val4.get())
                try:
                    if current_shape=='Oval':
                        oval=canvas.create_oval(a1,a2,a3,a4,fill=fillcolor.get(),outline=outlinecolor.get(),width=int(shapewidth.get()))
                        canvas.tag_bind(oval, "<Button-1>", on_press)
                    if current_shape=='Rectangle':
                        rect=canvas.create_rectangle(a1,a2,a3,a4,fill=fillcolor.get(),outline=outlinecolor.get(),width=int(shapewidth.get()))
                        canvas.tag_bind(rect, "<Button-1>", on_press)
                    if current_shape=='Line':
                        line=canvas.create_line(a1,a2,a3,a4,fill=fillcolor.get(),width=int(shapewidth.get()))
                        canvas.tag_bind(line, "<Button-1>", on_press)
                    canvas.bind("<B1-Motion>", on_drag)
                except Exception as e:
                    messagebox.showerror("Error","Incorrect width or color")
                    new_win.destroy()
            except Exception as e:
                messagebox.showerror("Error","Enter Correct Points")
                new_win.destroy()
        label1=ttk.Label(labelframe,text='Enter four points')
        label1.grid(row=1,column=0,columnspan=2,sticky='W')
        for i in range(2,6):
            label=ttk.Label(labelframe,text=f'Enter point:{i-1}')
            entry=ttk.Entry(labelframe,width=5,textvariable=l[i-2])
            label.grid(row=i,column=0)
            entry.grid(row=i,column=1)
            #-------------fill color------------------------
            label2=ttk.Label(labelframe,text='Choose color:')
            label2.grid(row=6,column=0)
            fill_entry=ttk.Entry(labelframe,width=10,textvariable=fillcolor)
            fill_entry.grid(row=6,column=1)
            label3=ttk.Label(labelframe,text='Choose outline color:')
            label3.grid(row=7,column=0)
            outline_entry=ttk.Entry(labelframe,width=10,textvariable=outlinecolor)
            outline_entry.grid(row=7,column=1)
            label4=ttk.Label(labelframe,text='Choose width:')
            label4.grid(row=8,column=0)
            width_entry=ttk.Entry(labelframe,width=10,textvariable=shapewidth)
            width_entry.grid(row=8,column=1)
    
            
            #----------------------------------------------------
        stb_btn=ttk.Button(labelframe,text='Submit',command=draw)
        stb_btn.grid(row=9,column=0,columnspan=2)

    combobox.bind('<<ComboboxSelected>>',select)



main_menu.add_command(label='Draw Shapes',command=Shapes)
#----------------------------------------------------------End of Canva----------------------------------------------------------

#---------------------------------------------------------Code Compile---------------------------------------------------------

url=''
entry=''
combobox=''
text_area=''
select_language=tk.StringVar()
def fetch_combo():
    language=select_language.get()
    content=''
    try: 
        if  url:
            with open(url.name,encoding='UTF-8') as f:
                content=f.read()
                text_area.insert('1.0',content)
        else:
            content=text_area.get('1.0','end-1c')
        
        if select_language.get()=="Python":
            old_stdout = sys.stdout  # Save original stdout
            redirected_output = io.StringIO()  # Create a buffer
            sys.stdout = redirected_output  # Redirect stdout

            exec(content)  # Execute the code

            sys.stdout = old_stdout  # Restore original stdout

            output_str = redirected_output.getvalue() 
            print(output_str)
            text_area.delete('1.0','end')
            text_area.insert('1.0',output_str)
        if select_language.get()=="Java":
            with open("HelloWorld.java", "w") as file:
                file.write(content)

    # Compile Java program
            compile_process = subprocess.run(["javac", "HelloWorld.java"], capture_output=True, text=True)

            if compile_process.returncode != 0:
                print("Compilation Error:\n", compile_process.stderr)
            else:  
                run_process = subprocess.run(["java", "HelloWorld"], capture_output=True, text=True)

                text_area.delete("1.0",'end')
                text_area.insert("1.0",run_process.stdout)

            
    except Exception as e:
        messagebox.showerror("Error",e)

def open_code_file(event):
    global url
    try:
        url=filedialog.askopenfile(title='Choose File:',filetypes=[("Python",".py")])
        if len(url.name)>0:
            entry.insert(0,url.name)
    except Exception as e:
        messagebox.showerror('Error',e)

def code_compiler():
    global entry,combobox,text_area
    new_win=tk.Toplevel()
    new_win.title("Code compiler")
    new_win.geometry('1000x1000')

    labelframe=ttk.LabelFrame(new_win)
    labelframe.pack()
    
    label=ttk.Label(labelframe,text="Choose language:")
    combobox=ttk.Combobox(labelframe,width=16,state='readonly',textvariable=select_language)
    combobox['values']=('Python',"Java")
    label.grid(row=0,column=0)
    combobox.grid(row=0,column=1)

    label1=ttk.Label(labelframe,text="Enter file or wite on textarea:")
    entry=ttk.Entry(labelframe,width=20)

    label1.grid(row=1,column=0,pady=10)
    entry.grid(row=1,column=1,columnspan=2,pady=10)

    text_area=tk.Text(new_win)
    text_area.config(wrap='word',relief=tk.FLAT)
    text_area.pack(side=tk.LEFT,expand=True,fill='both')

    scroll=tk.Scrollbar(new_win)
    scroll.pack(side=tk.RIGHT,fill=tk.Y)
    scroll.config(command=text_area.yview)
    text_area.config(yscrollcommand=scroll.set)


    sub_btn=ttk.Button(labelframe,text="Submit",command=fetch_combo)
    sub_btn.grid(row=2,column=0,columnspan=2)


    entry.bind('<Button-1>',open_code_file)
    combobox.bind('<<ComboboxSelected>>',)

    new_win.mainloop()

main_menu.add_command(label='Code Compiler',command=code_compiler)
#-----------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------

def sa(event):
    text_editor.delete(1.0,'end')


main_application.bind('<Control-Alt-x>',sa)
main_application.bind('<Control-f>',find)
main_application.config(menu=main_menu)
main_application.mainloop()