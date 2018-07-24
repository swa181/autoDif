import shutil
import os
from filingFunc import *
from tkinter import *
import tkinter.messagebox

# -- START --
# -- END --

# the source/dest docs
sourcedoc= [line.rstrip() for line in open('source.txt')]
destinations = [line.rstrip() for line in open('dest.txt')]
if len(sourcedoc):
    source = sourcedoc[0]
else:
    source = ""
sourceOpts = []
destinationOpts = []

def defineFolderCat():
    # Opens new window to choose folder paths
    def doesNotWork():
        '''returns 1 if it does not work; 0 otherwise'''
        if investment.get() == "" or meetingNotes.get() == "" or investorProfile.get() == "" or insurance.get() == "" or processed.get() == "":
            return 1
        return 0
    def closeCat():
        if doesNotWork() == 0:
            catDoc = open('folderCat.txt','w')
            catDoc.write("/"+ investment.get()+"/\n")
            catDoc.write("/"+ meetingNotes.get()+"\n")
            catDoc.write("/"+ investorProfile.get()+"\n")
            catDoc.write("/"+ insurance.get()+"\n")
            catDoc.write("/"+ processed.get())
            catDoc.close()
            win.destroy()
        else:
            tkinter.messagebox.showinfo("Error", "The form is incomplete.")
        
    # create array of items in doc
    caty = [line.rstrip() for line in open('folderCat.txt')]
    categories = []
    for each in caty:
        if each[0] == "/":
            each = each[1:]
        if each[len(each)-1] == "/":
            each = each[:len(each)-1]
        categories.append(each)
    #format: [0]investments, [1]meeting notes, [2]investor profile, [3]insurance, [4]processed
        
    win = Toplevel()
    win.grab_set()
    win.title('Edit Folder Locations')
    Label(win, text="\nDefine Folder Locations", font="Helvetica 15").pack(padx=200)
    Label(win, text="Fill in the blanks :).").pack()

    Label(win, text="\nInvestments").pack()
    investmentBox = Frame(win)
    investmentBox.pack()
    Label(investmentBox, text=destinations[0]+"/CLIENT_NAME/").pack(side=LEFT)
    investment = Entry(investmentBox, width=30)
    investment.pack(side=LEFT)
    investment.insert(0, categories[0])
    Label(investmentBox, text="/RRSP").pack(side=LEFT)
    
    Label(win, text="\nMeeting Notes").pack()
    meetingBox = Frame(win)
    meetingBox.pack()
    Label(meetingBox, text=destinations[0]+"/CLIENT_NAME/").pack(side=LEFT)
    meetingNotes = Entry(meetingBox, width=40)
    meetingNotes.pack(side=LEFT)
    meetingNotes.insert(0,categories[1])

    Label(win, text="\nInvestor Profile").pack()
    investorPBox = Frame(win)
    investorPBox.pack()
    Label(investorPBox, text=destinations[0]+"/CLIENT_NAME/").pack(side=LEFT)
    investorProfile = Entry(investorPBox, width=40)
    investorProfile.pack(side=LEFT)
    investorProfile.insert(0,categories[2])

    Label(win, text="\nInsurance").pack()
    insuranceBox = Frame(win)
    insuranceBox.pack()
    Label(insuranceBox, text=destinations[0]+"/CLIENT_NAME/").pack(side=LEFT)
    insurance = Entry(insuranceBox, width=40)
    insurance.pack(side=LEFT)
    insurance.insert(0,categories[3])

    Label(win, text="\nProcessed Items").pack()
    processedBox = Frame(win)
    processedBox.pack()
    Label(processedBox, text=destinations[0]+"/CLIENT_NAME/").pack(side=LEFT)
    processed = Entry(processedBox, width=40)
    processed.pack(side=LEFT)
    processed.insert(0,categories[4])

    confirmButt = Button(win, text="Update All", command=closeCat)
    confirmButt.pack(pady=30)

def helpTab():
    output.delete(0.0, END)
    output.insert(END,"\nThe Automated Digital Filing System (autoDiF) is a program catered to the filing system of Financial Advisor Winnie Wu.")
    output.insert(END,"\n\nTo get started:")
    output.insert(END,"\n\t> Please provide the document locations as outlined in the welcome pop-up window.")
    output.insert(END,"\n\t")
    output.insert(END,"\nFeatures in autoDiF v1.0 (released Jul 1, 2018):")
    output.insert(END,"\n\t> The source locations are not hard-coded and can be edited to accomodate the changing environment.")
    output.insert(END,"\n\t> An intuitive approach to the GUI environment (with a resizeable window!!!!) where filing is as simple as the press of a button.")
    output.insert(END,"\n\t> A counter for the number of documents filed.")
    output.insert(END,"\n\t> The program searches for similar names of the files - removes need for keeping track of preferred or legal names.")
    output.insert(END,"\n\t> Determines the appropriate folder for couple accounts too.")
    output.insert(END,"\n\nFor any inquiries, email to: sandywu1@outlook.com")

def update():
    global sourcedoc, destinations, source, sourceOpts, destinationOpts
    sourcedoc= [line.rstrip('\n') for line in open('source.txt','r')]
    destinations = [line.rstrip('\n') for line in open('dest.txt','r')]
    sourceOpts = []
    destinationOpts = []
    if len(sourcedoc):
        source = sourcedoc[0]
    else:
        source = ""


def openfileDialog(root2, opts):
    global sourcedoc, destinations, sourceOpts, destinationOpts
    name = filedialog.askdirectory()
    if name != '':
        if opts == "s":
            sourceOpts.append(IntVar(value=1))
            sourcedoc.append(name)
            option = Checkbutton(root2, text=sourcedoc[len(sourcedoc)-1], variable=sourceOpts[len(sourceOpts)-1], fg="blue")
            option.pack()
        else:
            destinationOpts.append(IntVar(value=1))
            destinations.append(name)
            option = Checkbutton(root2, text=destinations[len(destinations)-1], variable=destinationOpts[len(destinationOpts)-1], fg="blue")
            option.pack()

def welcomeText():
    update()
    output.delete(0.0, END)
    output.insert(END,"\nYour documents to file are in: \n\t"+source)
    output.insert(END,"\nYour client folders are in: \n")
    for each in destinations:
        output.insert(END,"\t"+each+"\n")

def checkboxToFile(win):
    open('source.txt','w').close()
    sourcef = open('source.txt','w')
    for each in range(len(sourcedoc)):
        if sourceOpts[each].get():
            sourcef.write(sourcedoc[each])
            source = sourcedoc[each]
            break
    sourcef.close()
    open('dest.txt','w').close()
    destf = open('dest.txt','w')
    for each in range(len(destinations)):
        if destinationOpts[each].get():
            destf.write(destinations[each]+"\n")
    destf.close()
    welcomeText()
    messagebox.showinfo("Success", "Updated!")
    win.destroy()

def firstTimeStart():
    def destDialog():
        openfileDialog(destinationsFrame, "d")
    def sourceDialog():
        openfileDialog(sourceFrame, "s")
    def confirmClose():
        # SOMETHING IS WRONG ???????
        bad = 1
        for each in range(len(destinationOpts)):
            if destinationOpts[each].get():
                bad = 0
                break
        for each in range(len(sourceOpts)):
            if sourceOpts[each].get():
                bad = 0
                break
        if bad:
            tkinter.messagebox.showinfo("Error", "This form is incomplete.")
        else:
            checkboxToFile(win)
    win = Toplevel()
    win.grab_set()
    win.title('Source and Destination Editor')
    Label(win, text="\nWelcome to the Automated Digital Filing System!", font="Helvetica 15").pack(padx=60)

    update()

    # destination selection:
    destinationsFrame = Frame(win)
    destinationsFrame.pack()
    Label(destinationsFrame, text="\nYour client folders are directly in (Choose as many):").pack()
    for each in range(len(destinations)):
        destinationOpts.append(IntVar(value=1))
        option = Checkbutton(destinationsFrame, text=destinations[each], variable=destinationOpts[len(destinationOpts)-1], fg="blue")
        option.pack()
    Button(win, text="Add New Destination Path", command=destDialog).pack()
    # source selections:
    sourceFrame = Frame(win)
    sourceFrame.pack()
    Label(sourceFrame, text="\nYour scanned documents are in (Choose one): ").pack()
    for each in range(len(sourcedoc)):
        sourceOpts.append(IntVar(value=1))
        option = Checkbutton(sourceFrame, text=sourcedoc[each], variable=sourceOpts[len(sourceOpts)-1], fg="blue")
        option.pack()

    Button(win, text="Add Source Path", command=sourceDialog).pack()
    # update and confirm:
    confirmFrame = Frame(win)
    confirmFrame.pack(pady=30)
    Label(confirmFrame, text="**Must press \"Update all\" to save.**").pack()
    confirmButt = Button(confirmFrame, text="Update All", command=confirmClose)
    confirmButt.pack()

toFileDest = []
toFileButton = []

def openFolder():
    win = Toplevel()
    for each in range(len(toFile)):
        toFileButton

def main():
    if os.stat("source.txt").st_size == 0 or os.stat("dest.txt").st_size == 0:
        tkinter.messagebox.showinfo("Error", "Please indicate the file locations in settings.")
        return
    index=0
    scannedTotal = 0

    files = os.listdir(source)
    
    output.delete(0.0, END)
    totalFiled.delete(0.0, END)
    output.insert(END,"---\n")

    for f in files:
        if f == "desktop.ini":
            continue
        
        fpath = source + '/' + f
        if os.path.isdir(fpath):
            continue
        
        scannedTotal += 1
        # Sees if Person's folder exists
        for eachDestination in destinations:
            ultpath = findPerson(f, eachDestination)
            if ultpath == "N/A":
                continue
            else:
                break
        if ultpath == "N/A":
            output.insert(END,"#### FAIL ####\nPerson/Category does not exist yet: "+f+"\n---\n")
            continue

        # Sees if the file can be filed away using investment/investor profile/meeting notes system
        ultpath = findType(f, ultpath)
        if ultpath == "N/A":
            output.insert(END,"#### FAIL ####\nNot appropriate file: "+f+"\n---\n")
            continue

        if os.path.exists(ultpath + '/' + f):
            output.insert(END,"#### FAIL ####\nFile with same name exists: "+f)
            output.insert(END,"\nPlease check path: "+ultpath+'/'+f+"\n---\n")
            continue
        
        shutil.move(fpath, ultpath)
        output.insert(END,"\""+ f +"\":\nFiled away at: " + ultpath+"\n---\n")
        index += 1

    totalFiled.insert(END,"Filed total: "+str(index)+" of "+str(scannedTotal)+" items.")


#the tkinter window::
root = Tk()
root.title('autoDiF (v1.0)')
root.iconbitmap('newFav.ico')
root.geometry("900x500")

# menu
menu = Menu(root)
root.config(menu=menu) #configure a menu and its this one right here

subMenu = Menu(menu)
#menu.add_cascade(label="File",menu=subMenu) #add dropdown; file button and subMenu is dropdown
#subMenu.add_command(label="New Project...", command=welcomeText)
#subMenu.add_separator()
#subMenu.add_command(label="New...", command=welcomeText)

editMenu = Menu(menu)
menu.add_cascade(label="Edit",menu=editMenu)
editMenu.add_command(label="Folder Locations",command=defineFolderCat)

#viewMenu = Menu(menu)
#menu.add_cascade(label="View",menu=viewMenu)
#viewMenu.add_command(label="Nicknames...",command=welcomeText)

helpMenu = Menu(menu)
menu.add_cascade(label="Help",menu=helpMenu)
helpMenu.add_command(label="About autoDiF",command=helpTab)

# toolbar
toolbar = Frame(root, bg="#48494f")
# logo
logo = PhotoImage(file="15270551349196465.png")
label= Label(toolbar, image=logo, bg="#48494f")
label.pack(side=LEFT, padx=2, pady=2)
settingsIcon = PhotoImage(file="settings.png")
settingsL = Button(toolbar, bg="#48494f", command=firstTimeStart)
settingsL.pack(side=RIGHT, padx=5)
settingsL.config(image=settingsIcon)
submitB = Button(toolbar, text="SUMBIT", width=14, command=main)
submitB.pack(side=RIGHT, padx=10)
submitB = Button(toolbar, text="CLEAR", width=14, command=welcomeText)
submitB.pack(side=RIGHT, padx=10)
toolbar.pack(side=TOP, fill=X)

# bottom box
statusBox = Frame(root, bg="#48494f")
statusBox.pack(side=BOTTOM, fill=X)
totalFiled = Text(statusBox, font="Helvetica 10", fg="white", bg="#48494f", height=1, width=21)
totalFiled.pack(side=LEFT)

# output
scrollbar= Scrollbar(root)
scrollbar.pack(side=RIGHT,fill=Y)
output = Text(root, font="Helvetica 10", wrap=WORD, background="#313338", fg="white" , yscrollcommand=scrollbar.set)
output.pack(side=LEFT, fill=BOTH, expand=1)
helpTab()

if os.stat("source.txt").st_size == 0:
    firstTimeStart()

scrollbar.config(command=output.yview)
root.mainloop()
