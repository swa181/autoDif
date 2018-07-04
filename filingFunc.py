import os
import shutil
from tkinter import filedialog
from tkinter import *
import tkinter.messagebox

#account specifics
investmentOpts = ["OPEN", "RRSP", "TFSA", "RESP", "LRSP", "LIRA", "RRIF", "SRSP"]
meetingOpts = ["Meeting Notes", "meeting notes", "Meeting notes"]
profileOpts = ["Investor Profile", "Investor profile", "investor profile"]
insuranceOpts = ["Equitable", "BMO"]
otherStuff = ["Processed Items"]
allOptions = investmentOpts + meetingOpts + profileOpts + insuranceOpts
allplusOther = otherStuff + allOptions


# Assumes that dest exists
# Responsible for creating new directories
def findType(fileName, dest):
    ''' Returns destination to the Client's appropriate folder '''

    original = dest
    
    # dest has the client's name
    fileType = ""
    for option in allOptions: # finds the file type
        index = fileName.find(option)
        if index != -1:
            fileType = option
            break
    if index == -1:
        # The file is neither investment/investor profile/meeting notes
        return "N/A"

    # find client's name from dest
    clientName = dest[dest.rfind('/')+1:]
    # find the indivs name
    name = findNamefromFileName(fileName)

    categories = [line.rstrip() for line in open('folderCat.txt')]
    #format: [0]investments, [1]meeting notes, [2]investor profile, [3]insurance, [4]processed

    # Builds appropriate path for the file depending on its name
    if fileType in investmentOpts:
        found = 0
        indivName = clientName
        if "and" in clientName and "and" in name:
            dest += categories[0] + fileType
            if not os.path.isdir(dest):
                os.makedirs(dest)
        elif "and" in clientName:
            indivName = findIndivName(fileName, dest, clientName, investmentOpts)
            if indivName == "N/A":
                return "N/A"
            # finds name via files
            files = os.listdir(dest+categories[0])
            for f in files:
                if indivName in f:
                    if os.path.isdir(f):
                        dest += categories[0] + '/' + f
                        found =1
                        break
            # finds name via directories
            if found ==0:
                for root, dirs, files in os.walk(dest+categories[0]):
                    for each in files:
                        if (fileType in each) and (indivName in each):
                            dest = root.replace("\\","/")
                            break
                    if (fileType in root[len(dest):]) and (indivName in root[len(dest):]):
                        dest = root.replace("\\","/")
                        break
            # creates a folder if none found
            if dest == original:
                dest += categories[0] + indivName + '/' + fileType
                if not os.path.isdir(dest):
                    os.makedirs(dest)
        else:
            dest += categories[0] + fileType
            # Creates a new folder if there is no OPEN/RRSP/.. folder
            if not os.path.isdir(dest):
                os.makedirs(dest)
    elif fileType in meetingOpts:
        dest += categories[1]
    elif fileType in profileOpts:
        if "and" in clientName:
            indivName = findIndivName(fileName, dest, clientName, investmentOpts)
            if indivName == "N/A":
                return "N/A"
            dest += categories[2] + '/' + indivName
        else:
            dest += categories[2]
    elif fileType in insuranceOpts:
        # find the appropriate folder
        # go through the files and sees where the owner's insurance thing is at

        if "and" in clientName and "and" in name:
            indivName = clientName
        elif "and" in clientName:
            indivName = findIndivName(fileName, dest, clientName, insuranceOpts)
        else:
            indivName = clientName
        for root, dirs, files in os.walk(dest+categories[3]):
            # finds a file with a similar name
            for each in files:
                if (fileType in each) and (indivName in each):
                    dest = root.replace("\\","/")
                    break
            # finds a path with similar name
            if (fileType in root[len(dest):]) and (indivName in root[len(dest):]):
                dest = root.replace("\\","/")
                break
        # if it cant find a directory, makes one
        if dest == original:
            if "and" in clientName:
                dest += categories[3]+'/'+indivName+'/'+fileType
            else:
                dest += categories[3]+'/'+fileType
            os.makedirs(dest)
    else:
        return "N/A"
    
    if dest == original:
        return "N/A"
    return dest

def findPerson(fileName, dest):
    ''' Returns the path leading to the person's folder'''
    # dest - folder of client names
    
    name = findNamefromFileName(fileName)
    path = dest+"/"+name
    if os.path.isdir(path):
        return path
    else:
        path = findAlternateName(name, dest)
        if path != "N/A":
            return path

    return "N/A"

def findNamefromFileName(fileName):
    index = -1
    for option in allOptions:
        index = fileName.find(option)
        if index != -1:
            break
    if index == -1:
        return "N/A"
    return fileName[9:index-1]

# directed towards couples; not for finding large client folder
# only for investment and insurance
# can find complex paths to children
# finds names based on directories and files
# returns "N/A" if theres no folder of their name in Investments/Insurance
def findIndivName(fileName, path, clientName, investORinsure):
    # path includes clientName
    name = findNamefromFileName(fileName)
    categories = [line.rstrip() for line in open('folderCat.txt')]
    destinations =[line.rstrip() for line in open('dest.txt')]

    if investORinsure == investmentOpts:
        fileType = categories[0]
    else:
        fileType = categories[3]
    fileType = fileType.replace("/","\\")
    altname = ""
    # finds a file with a similar name:
    for root, dirs, files in os.walk(path+'\\'+fileType):
        for each in files:
            if (name in each):
                altname = root
                break
        # finds a directory with similar name
        if (name in root[len(path):]):
            altname = root
            break
    if altname == "":
        return "N/A"
    altname = altname.replace("\\", '/')
    if investORinsure == investmentOpts:
        altname = altname[len(path+fileType+'/'):]
    else:
        altname = altname[len(path+'/'+fileType+'/'):]
    fileType = ""
    for each in investORinsure:
        if each in altname:
            fileType = each
    altname = altname.replace('\\','/')
    if fileType != "":
        index = altname.find("/")
        if index != -1:
            altname = altname[:index]
    if altname == "":
        return "N/A"
    return altname

def findAlternateName(name, path):
    altname = ""
    # finds a file with a similar name:
    for root, dirs, files in os.walk(path):
        for each in files:
            if name in each:
                altname = root
                break
    # finds where the file is stored:
    if altname == "":
        return "N/A"

    for each in allplusOther:
        nameend = altname.find(each,len(path)+1)
        if nameend != -1:
            break;
    if nameend == -1:
        return "N/A"
    name = altname[len(path)+1:nameend-1]
    namelist = list(name)
    for each in range(len(namelist)):
        if namelist[each] == '\\':
            namelist[each] = '/'
    name = "".join(namelist)
    if os.path.isdir(path):
        return path+'/'+name
    return "N/A"
