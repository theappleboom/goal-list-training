![Goal List](CheckBox.png)

# Goal List Training
 An executive function hijacker

# Releases
 [Releases are found here.](https://github.com/theappleboom/goal-list-training/releases) The first kind is the main release, the second is for debugging purposes, and the third is the main release with some example files.

# CODE BASE CHANGE
 This branch is this source code for the original python release.

# How To Use
## General
 Goal List is a training program that procedurally creates a basic training regimen. You don't need to plan how to train at all. You only need to tell the program what you want to do.
### Journaling
 Whenever you complete an item, it generates a journal entry in the same folder as the Goal List executable. Check out the GoalListJournal and it will tell you what you did and when.

## List File Section
 This looks first in your GoalLists folder, and creates one if it's not there already. Goal List files are CSVs that save your tasks and weights.

## Timer Section
 A basic alarm clock to help with timed tasks. It currently can only take minutes as input.

## Goal List Section
### Task Input Section
 Text box takes in the name of your task. Drop down box controls how often you want to see your task (common, uncommon, or rare). Add puts your task into your current open Goal List. Print List prints out your Goal List to the console when running the 'with console' version.
### Things To Do Section
 This is your procedurally generated training regimen. Whenever you complete a task item, another one from your regimen takes its place. Clicking done both marks the item done on your list and writes the completion time down in your journal. Remove removes the task item from your Goal List permanently.