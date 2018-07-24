import os
import shutil
from tkinter import filedialog
from tkinter import *
import tkinter.messagebox

#account specifics
investmentOpts = ["OPEN", "RRSP", "TFSA", "RESP", "LRSP", "LIRA", "RRIF", "SRSP"]
meetingOpts = ["Meeting Notes", "meeting notes", "Meeting notes"]
profileOpts = ["Investor Profile", "Investor profile", "investor profile"]
insuranceOpts = ["Equitable", "BMO", "GWL"]
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
        if " and " in clientName and " and " in name:
            files = os.listdir(dest+categories[0])
            for each in files:
                if "and" in each or "joint" in each or "Joint" in each:
                    clientName = each
            dest += categories[0] + clientName + '/' + fileType
            if not os.path.isdir(dest):
                os.makedirs(dest)
                print("NEW FOLDER: "+dest)
        elif " and " in clientName:
            indivName = findIndivName(fileName, dest, clientName, investmentOpts)
            if indivName == "N/A":
                return "N/A"
            dest += categories[0] + indivName + '/' + fileType

            # creates a folder if none found
            if dest == original:
                dest += categories[0] + indivName + '/' + fileType
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                    print("NEW FOLDER: "+dest)
        else:
            dest += categories[0] + fileType
            # Creates a new folder if there is no OPEN/RRSP/.. folder
            if not os.path.isdir(dest):
                os.makedirs(dest)
                print("NEW FOLDER: "+dest)
    elif fileType in meetingOpts:
        if not os.path.isdir(dest + categories[1]):
            return "N/A"
        dest += categories[1]
    elif fileType in profileOpts:
        if " and " in clientName:
            indivName = findIndivName(fileName, dest, clientName, investmentOpts)
            if indivName == "N/A":
                return "N/A"
            dest += categories[2] + '/' + indivName
        else:
            dest += categories[2]
    elif fileType in insuranceOpts:
        # find the appropriate folder
        # go through the files and sees where the owner's insurance thing is at

        if " and " in clientName and " and " in name:
            indivName = clientName
        else:
            indivName = findIndivName(fileName, dest, clientName, insuranceOpts)
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
            if " and " in clientName:
                dest += categories[3]+'/'+indivName+'/'+fileType
            else:
                dest += categories[3]+'/'+fileType
            os.makedirs(dest)
            print("NEW FOLDER: "+dest)
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
    print(name)
    categories = [line.rstrip() for line in open('folderCat.txt')]
    destinations =[line.rstrip() for line in open('dest.txt')]

    if investORinsure == investmentOpts:
        fileType = categories[0]
    else:
        fileType = categories[3]
    altname = ""
    # finds a file with a similar name:
    for root, dirs, files in os.walk(path+fileType):
        if " and " not in name:
            for each in files:
                if (name in each) and " and " not in each:
                    altname = root
                    break
            # finds a directory with similar name
            print(root)
            if (name in root[len(path+fileType):]) and clientName not in root[len(path+fileType):]:
                altname = root
                break
        else:
            for each in files:
                if (name in each):
                    altname = root
                    break
            # finds a directory with similar name
            if (name in root[len(path+fileType):]) or "joint" in root[len(path+fileType):] or "Joint" in root[len(path+fileType):]:
                altname = root
                break
    
    if altname == "":
        if investORinsure == investmentOpts:
            os.makedirs(path+fileType+'/'+name)
            print("NEW FOLDER: "+path+fileType+'/'+name)
            return name
        else:
            os.makedirs(path+'/'+fileType+'/'+name)
            print("NEW FOLDER: "+path+'/'+fileType+'/'+name)
            return name
    altname = altname.replace("\\", '/')
    if investORinsure == investmentOpts:
        altname = altname[len(path+fileType):]
    else:
        altname = altname[len(path+'/'+fileType):]
    print(altname)
    index = altname.find("/")
    if index != -1:
        altname = altname[:index]
    if altname == "":
        return "N/A"
    return altname

def findViaNameFirst(name, path):
    files = os.listdir(path)
    nameList = name.split()
    newName = []
    for f in files:
        for each in nameList:
            if each in f:
                    newName.append(each)
        if set(newName) == set(nameList):
            return f
        newName.clear()
    return ""

def findAlternateName(name, path):
    altname = ""
    altname = findViaNameFirst(name, path)
    if altname != "":
        return path + '/' + altname
    # finds a file with a similar name:
    for root, dirs, files in os.walk(path):
        for each in files:
            if name in each and "Nancy Lee" not in root:
                altname = root
                break
    # finds where the file is stored:
    if altname == "":
        return "N/A"
    altname = altname.replace('\\', '/')
    nameend = altname.find('/',len(path)+1)
    if nameend == -1:
        return "N/A"
    name = altname[len(path)+1:nameend]
    if os.path.isdir(path):
        print(path+'/'+name)
        return path+'/'+name
    return "N/A"
