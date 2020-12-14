from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import time as tm
import os
import random
import datetime

listFileTemplate = "Item1,C,5\nItem2,C,5\nItem3,C,5\nItem4,C,5\nItem5,C,5\nItem6,C,5"

global runTimer
global cachedTime
global goalListItems
global goalListRarities
global goalListWeights
global todoListIndices

doneButtons = []
removeButtons = []
todoListItems = []
goalListItems = []
goalListRarities = []
goalListWeights = []
todoListIndices = [-1,-1,-1,-1,-1]
runTimer = False

commonMultiplier = 3
uncommonMultiplier = 2
rareMultiplier = 1

def setErrorMessage(errorMessage):
	messagebox.showerror("Error", errorMessage)

def clickThing():
	#print(addInputField.get())
	#addInputField.delete(0, END)
	print("Placeholder clicked")
	messagebox.showinfo("Information","Informative message")

def printString(toPrint):
	print(toPrint)

def setTimer():
	global startTime
	minutes = timerInput.get()

	try:
		minuteInt = int(minutes)
	except:
		if minutes == "":
			setErrorMessage("No time is entered")
		else:
			setErrorMessage(minutes + " is not an integer")
		return
	
	if minuteInt < 10:
		timerText.set("0" + minutes + ":00")
	else:
		timerText.set(minutes + ":00")
	
	timerSeconds.set(minuteInt * 60)
	stopTimer()

	print(minutes + " set")
	timerInput.delete(0, END)
	#startTime = tm.time()
	#root.after(500, timerTest)

def timerTest():
	end_time = tm.time()
	print(str(end_time))
	#print(str(end_time - startTime))

def startTimer():
	global runTimer
	global cachedTime

	runTimer = True
	cachedTime = tm.time()
	timerUpdate()

def stopTimer():
	global runTimer
	runTimer = False
	print("Stopped Timer")

def timerUpdate():
	global runTimer
	global cachedTime

	if runTimer:
		currentTime = tm.time()
		deltaTime = currentTime - cachedTime
		cachedTime = currentTime

		print("New Delta Time: " + str(deltaTime))
		timerSeconds.set(timerSeconds.get() - deltaTime)
		
		if timerSeconds.get() <= 0:
			timerSeconds.set(-1)
			timerText.set("00:00")
			stopTimer()
			messagebox.showinfo("Timer","Countdown has finished")
			print("Played alert")
		else:
			timerText.set(getTimeString(int(round(timerSeconds.get()))))
			root.after(500, timerUpdate)

def getTimeString(seconds):
	minutes = 0

	while seconds >= 60:
		minutes += 1
		seconds -= 60
	
	if minutes < 10:
		minuteString = "0" + str(minutes)
	else:
		minuteString = str(minutes)
	
	if seconds < 10:
		secondString = "0" + str(seconds)
	else:
		secondString = str(seconds)
	
	return minuteString + ":" + secondString

def EnsureListDirectory():
	if not os.path.exists(os.getcwd() + "/GoalLists"):
		os.makedirs(os.getcwd() + "/GoalLists")

def getFileName(filePath):
	splitOnSlashes = filePath.split('/')
	splitOnPeriods = splitOnSlashes[len(splitOnSlashes)-1].split('.')
	return splitOnPeriods[0]

def correctFileExtension(filePath):
	newFilePath = ""
	splitOnSlashes = filePath.split('/')
	splitOnPeriods = splitOnSlashes[len(splitOnSlashes)-1].split('.')
	
	for i in range(0, len(splitOnSlashes) - 1):
		newFilePath = newFilePath + splitOnSlashes[i] + "/"
	
	newFilePath = newFilePath + splitOnPeriods[0] + ".csv"
	return newFilePath

def newGoalListFile():
	EnsureListDirectory()
	root.filePath = filedialog.asksaveasfilename(initialdir=os.getcwd() + "/GoalLists", title="Create New Goal List", filetypes=(("CSV files", "*.csv"),))
	
	if getFileName(root.filePath) != "":
		root.filePath = correctFileExtension(root.filePath)

		fileString = "GoalListFile," + getFileName(root.filePath) + ","

		f = open(root.filePath,"w")
		f.write(fileString)
		f.close()
		
		if goalListStringToVars(fileString):
			PopulateTodoList()
			addButton["state"] = "normal"
			printOutButton["state"] = "normal"
			newListButton["state"] = "disabled"
			openListButton["state"] = "disabled"
			closeListButton["state"] = "normal"
			listName.set(getFileName(root.filePath))
	else:
		#Operation was canceled
		root.filePath = "No File Loaded"
		listName.set(getFileName(root.filePath))

def openGoalListFile():
	EnsureListDirectory()

	try:
		root.filePath = filedialog.askopenfilename(initialdir=os.getcwd() + "/GoalLists", title="Select a Goal List", filetypes=(("CSV files", "*.csv"),))

		f = open(root.filePath, "r")
		fileString = f.read()
		f.close()

		if goalListStringToVars(fileString):
			PopulateTodoList()
			addButton["state"] = "normal"
			printOutButton["state"] = "normal"
			newListButton["state"] = "disabled"
			openListButton["state"] = "disabled"
			closeListButton["state"] = "normal"
			listName.set(getFileName(root.filePath))
	except:
		#Operation was canceled
		root.filePath = "No File Loaded"
		listName.set(getFileName(root.filePath))

def closeGoalListFile():
	global goalListItems
	global goalListRarities
	global goalListWeights
	global todoListIndices

	root.filePath = "No File Loaded"

	goalListItems = []
	goalListRarities = []
	goalListWeights = []
	VoidTodoList()

def VoidTodoList():
	global todoListIndices

	todoListIndices = [-1,-1,-1,-1,-1]

	for i in range(0, 5):
		todoListItems[i].set("Empty Slot")
		doneButtons[i]["state"] = "disabled"
		removeButtons[i]["state"] = "disabled"
	
	addButton["state"] = "disabled"
	printOutButton["state"] = "disabled"
	newListButton["state"] = "normal"
	openListButton["state"] = "normal"
	closeListButton["state"] = "disabled"
	listName.set("No File Loaded")

def updateListFile():
	if root.filePath != "No File Loaded":
		f = open(root.filePath,"w")
		f.write("GoalListFile,")
		f.write(getFileName(root.filePath))
		f.write(",")
		if len(goalListItems) > 0:
			f.write("\n")
			f.write(goalListVarsToString())
		f.close()

def goalListStringToVars(goalListString):
	global goalListItems
	global goalListRarities
	global goalListWeights

	goalListItems = []
	goalListRarities = []
	goalListWeights = []
	VoidTodoList()

	lines = goalListString.split('\n')
	currentLine = 0

	if lines[0].split(',')[0] != "GoalListFile":
		setErrorMessage(getFileName(root.filePath) + " is not a Goal List file, or is corrupted.")
		closeGoalListFile()
		return False

	try:
		for i in range(1, len(lines)):
			currentLine = i
			itemList = lines[i].split(',')
			goalListItems.append(itemList[0])
			goalListRarities.append(itemList[1])
			goalListWeights.append(int(itemList[2]))
	except Exception as e:
		print(e)
		print("Current line: " + str(currentLine))
		setErrorMessage(getFileName(root.filePath) + " is corrupted.")
		closeGoalListFile()
		return False
	
	print("File successfully loaded")
	return True

def goalListVarsToString():
	global goalListItems
	global goalListRarities
	global goalListWeights

	goalListString = ""

	for i in range(0, len(goalListItems)):
		goalListString = goalListString + goalListItems[i] + "," + goalListRarities[i] + "," + str(goalListWeights[i])
		if i != len(goalListItems) - 1:
			goalListString = goalListString + "\n"
	
	print("Vars successfully converted")
	return goalListString
	
def WeightedRandomPick():
	global goalListItems
	global goalListRarities
	global goalListWeights

	returnIndex = -1

	#Return if list is empty
	if len(goalListItems) == 0:
		return returnIndex

	weightTotal = 0
	for i in range(0, len(goalListWeights)):
		weightTotal += goalListWeights[i]

	#Return if total weight is zero
	if weightTotal == 0:
		return returnIndex
	
	weightCountDown = random.randint(1, weightTotal)

	for i in range(0, len(goalListItems)):
		weightCountDown -= goalListWeights[i]
		if weightCountDown <= 0:
			goalListWeights[i] = 0
			returnIndex = i
			weightCountDown = weightTotal
		else:
			#print("Raising weight for " + str(i) + " from " + str(goalListWeights[i]))
			goalListWeights[i] += FindRarityMultiplier(goalListRarities[i]) * 1
			#print("To " + str(goalListWeights[i]))
	
	return returnIndex

def PopulateTodoList():
	global goalListItems
	global todoListIndices

	takenSlots = SetUpOldTodoList()

	if takenSlots < 5:
		for i in range(0, 5):
			if todoListIndices[i] == -1:
				todoListIndices[i] = WeightedRandomPick()
				CorrectTodoListWeights()
				if todoListIndices[i] != -1:
					todoListItems[i].set(goalListItems[todoListIndices[i]])
					doneButtons[i]["state"] = "normal"
					removeButtons[i]["state"] = "normal"
				else:
					todoListItems[i].set("Empty Slot")
	print(goalListWeights)

def SetUpOldTodoList():
	global goalListItems
	global goalListWeights
	takenSlots = 0

	for i in range(0, len(goalListWeights)):
		if goalListWeights[i] == 0:
			if takenSlots < 5:
				todoListIndices[takenSlots] = i
				todoListItems[takenSlots].set(goalListItems[todoListIndices[takenSlots]])
				doneButtons[takenSlots]["state"] = "normal"
				removeButtons[takenSlots]["state"] = "normal"
				takenSlots += 1
			else:
				print("Too many items with a weight of 0.")
	
	print(takenSlots)
	return takenSlots

def CorrectTodoListWeights():
	global goalListWeights
	global todoListIndices

	for i in range(0, 5):
		if todoListIndices[i] != -1:
			goalListWeights[todoListIndices[i]] = 0
			#print("Updating weight for index " + str(todoListIndices[i]))

def FindRarityMultiplier(rarityChar):
	if rarityChar == "C":
		return commonMultiplier
	if rarityChar == "U":
		return uncommonMultiplier
	if rarityChar == "R":
		return rareMultiplier

def FinishItem(todoIndex):
	global goalListItems
	global goalListWeights
	global todoListIndices
	currentIndex = todoListIndices[todoIndex]
	finishedItem = todoListItems[todoIndex].get()

	if currentIndex == -1:
		#ignore this button
		return

	#Clear out label
	todoListItems[todoIndex].set("Empty Slot")

	#Find new item
	todoListIndices[todoIndex] = WeightedRandomPick()
	if todoListIndices[todoIndex] != -1:
		todoListItems[todoIndex].set(goalListItems[todoListIndices[todoIndex]])
		CorrectTodoListWeights()
	else:
		todoListItems[todoIndex].set("Empty Slot")

	#Check for special case with 5 or less items
	if todoListIndices[todoIndex] == -1 and len(goalListItems) <= 5:
		messagebox.showinfo("Small List","Your task has been completed, but there are not enough items in your list to replace it.")
		todoListIndices[todoIndex] = currentIndex
		todoListItems[todoIndex].set(goalListItems[todoListIndices[todoIndex]])
		CorrectTodoListWeights()
	
	#Update Journal Here
	UpdateJournal(finishedItem)
	#Update ListFile
	updateListFile()

def RemoveItem(todoIndex):
	global goalListItems
	global goalListRarities
	global goalListWeights
	global todoListIndices

	indexToRemove = todoListIndices[todoIndex]
	todoListIndices[todoIndex] = -1

	#remove item from all 3 collections
	goalListItems.pop(indexToRemove)
	goalListRarities.pop(indexToRemove)
	goalListWeights.pop(indexToRemove)

	#update todoListIndices of value greater than removed index
	for i in range(0, 5):
		if todoListIndices[i] > indexToRemove:
			todoListIndices[i] -= 1
	
	#replace item
	#Clear out label
	todoListItems[todoIndex].set("Empty Slot")

	#Find new item
	todoListIndices[todoIndex] = WeightedRandomPick()
	if todoListIndices[todoIndex] != -1:
		todoListItems[todoIndex].set(goalListItems[todoListIndices[todoIndex]])
		CorrectTodoListWeights()
	else:
		todoListItems[todoIndex].set("Empty Slot")
	
	if todoListIndices[todoIndex] == -1:
		#Deactivate done and remove buttons
		removeButtons[todoIndex]["state"] = "disabled"
		doneButtons[todoIndex]["state"] = "disabled"

	#Update ListFile
	updateListFile()

def AddItem():
	global goalListItems
	global goalListRarities
	global goalListWeights
	global todoListIndices

	if IsInputFieldValid(addInputField.get()):
		goalListItems.append(addInputField.get())
		goalListRarities.append(rarityString.get())
		goalListWeights.append(5)

		messagebox.showinfo("Adding Item","Added " + addInputField.get() + " to your goal list.")

		#Search for empty slot to fill in
		for i in range(0, 5):
			if todoListIndices[i] == -1:
				todoListItems[i].set(addInputField.get())
				todoListIndices[i] = len(goalListItems) - 1
				doneButtons[i]["state"] = "normal"
				removeButtons[i]["state"] = "normal"
				CorrectTodoListWeights()
				break
		
		#Update ListFile
		updateListFile()
	else:
		setErrorMessage("List item cannot be empty.")
	
	addInputField.delete(0, END)

def IsInputFieldValid(inputString):
	trimmedInput = inputString.replace(" ", "")

	if trimmedInput == "":
		return False
	else:
		return True

def PrintOut():
	global goalListItems
	global goalListRarities
	global goalListWeights

	for i in range(0, len(goalListItems)):
		print(goalListItems[i] + ", " + goalListRarities[i] + ", " + str(goalListWeights[i]))
	
def UpdateJournal(itemFinished):
	journalFilePath = initialdir=os.getcwd() + "\GoalListJournal.txt"
	fileString = ""

	try:
		f = open(journalFilePath, "r")
		fileString = f.read()
		f.close()
	except:
		print("No previous journal file exists")
	
	f = open(journalFilePath, "w+")
	if fileString != "":
		f.write(fileString + "\n")
	else:
		f.write(fileString)
	f.write(tm.strftime("%d %b %Y, %I:%M %p ", tm.localtime()) + itemFinished)
	f.close()

	print("Wrote to journal")
	print(journalFilePath)

root = Tk()
root.title("Goal List v0.1")
root.iconbitmap('resources/CheckBox.ico')

#Create Frames
goalListFrame = LabelFrame(root, text="Goal List", padx=40, pady=40)
goalListFrame.grid(row=0, column=0, padx=10, pady=10, sticky="n", rowspan=2)

timerFrame = LabelFrame(root, text="Timer", padx=40, pady=40)
timerFrame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

listFileFrame = LabelFrame(root, text="List File", padx=40, pady=40)
listFileFrame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

#Create Goal List Widgets
rarityString = StringVar()
rarityString.set("C")
addInputField = Entry(goalListFrame, width=50)
rarityBox = OptionMenu(goalListFrame, rarityString, "C", "U", "R")
addButton = Button(goalListFrame, text="Add", command=AddItem, state="disabled")
printOutButton = Button(goalListFrame, text="Print List", command=PrintOut, state="disabled")
listTitleLabel = Label(goalListFrame, text="Things To Do")

item1Text = StringVar()
item1Label = Label(goalListFrame, textvariable=item1Text)
item1DoneButton = Button(goalListFrame, text="Done", command= lambda: FinishItem(0), state="disabled")
item1RemoveButton = Button(goalListFrame, text="Remove", command= lambda: RemoveItem(0), state="disabled")
item1Text.set("Empty Slot")

item2Text = StringVar()
item2Label = Label(goalListFrame, textvariable=item2Text)
item2DoneButton = Button(goalListFrame, text="Done", command= lambda: FinishItem(1), state="disabled")
item2RemoveButton = Button(goalListFrame, text="Remove", command= lambda: RemoveItem(1), state="disabled")
item2Text.set("Empty Slot")

item3Text = StringVar()
item3Label = Label(goalListFrame, textvariable=item3Text)
item3DoneButton = Button(goalListFrame, text="Done", command= lambda: FinishItem(2), state="disabled")
item3RemoveButton = Button(goalListFrame, text="Remove", command= lambda: RemoveItem(2), state="disabled")
item3Text.set("Empty Slot")

item4Text = StringVar()
item4Label = Label(goalListFrame, textvariable=item4Text)
item4DoneButton = Button(goalListFrame, text="Done", command= lambda: FinishItem(3), state="disabled")
item4RemoveButton = Button(goalListFrame, text="Remove", command= lambda: RemoveItem(3), state="disabled")
item4Text.set("Empty Slot")

item5Text = StringVar()
item5Label = Label(goalListFrame, textvariable=item5Text)
item5DoneButton = Button(goalListFrame, text="Done", command= lambda: FinishItem(4), state="disabled")
item5RemoveButton = Button(goalListFrame, text="Remove", command= lambda: RemoveItem(4), state="disabled")
item5Text.set("Empty Slot")

#Create Timer Widgets
timerText = StringVar()
timerDisplay = Label(timerFrame, textvariable=timerText)
timerPlayButton = Button(timerFrame, text="Play", command= startTimer)
timerStopButton = Button(timerFrame, text="Stop", command= stopTimer)
timerInput = Entry(timerFrame, width=10)
timerSetButton = Button(timerFrame, text="Set", command= setTimer)

#Create File Widgets
listName = StringVar()
listName.set("No File Loaded")
listNameLabel = Label(listFileFrame, textvariable=listName)
newListButton = Button(listFileFrame, text="New", command=newGoalListFile)
openListButton = Button(listFileFrame, text="Open", command=openGoalListFile)
closeListButton = Button(listFileFrame, text="Close", command=closeGoalListFile, state="disabled")

#Place widgets
#Goal List Frame
addInputField.grid(row=0, column=0, columnspan=2)
rarityBox.grid(row=0, column=2)
addButton.grid(row=0, column=3)
printOutButton.grid(row=0, column=4)
listTitleLabel.grid(row=1, column=0)

item1Label.grid(row=2, column=0)
item1DoneButton.grid(row=2, column=2)
item1RemoveButton.grid(row=2, column=3)

item2Label.grid(row=3, column=0)
item2DoneButton.grid(row=3, column=2)
item2RemoveButton.grid(row=3, column=3)

item3Label.grid(row=4, column=0)
item3DoneButton.grid(row=4, column=2)
item3RemoveButton.grid(row=4, column=3)

item4Label.grid(row=5, column=0)
item4DoneButton.grid(row=5, column=2)
item4RemoveButton.grid(row=5, column=3)

item5Label.grid(row=6, column=0)
item5DoneButton.grid(row=6, column=2)
item5RemoveButton.grid(row=6, column=3)

#Timer Frame
timerDisplay.grid(row=0, column=0)
timerPlayButton.grid(row=1, column=0)
timerStopButton.grid(row=1, column=1)
timerInput.grid(row=2, column=0, columnspan=2)
timerSetButton.grid(row=2, column=2)

#File Frame
listNameLabel.grid(row=0, column=0, columnspan=3)
newListButton.grid(row=1, column=0)
openListButton.grid(row=1, column=1)
closeListButton.grid(row=1, column=2)

#Set up references
removeButtons.append(item1RemoveButton)
removeButtons.append(item2RemoveButton)
removeButtons.append(item3RemoveButton)
removeButtons.append(item4RemoveButton)
removeButtons.append(item5RemoveButton)

doneButtons.append(item1DoneButton)
doneButtons.append(item2DoneButton)
doneButtons.append(item3DoneButton)
doneButtons.append(item4DoneButton)
doneButtons.append(item5DoneButton)

todoListItems.append(item1Text)
todoListItems.append(item2Text)
todoListItems.append(item3Text)
todoListItems.append(item4Text)
todoListItems.append(item5Text)

timerText.set("00:00")
timerSeconds = DoubleVar()
timerSeconds.set(-1)

root.mainloop()