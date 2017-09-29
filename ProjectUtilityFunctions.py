
###################################
# Script:  ProjectUtilityFunctions.py
# Author:  Conrad Schaefer
# Date Created:  09/25/2017
# Purpose:  Build utility functions and store in a class for use elsewhere
# Inputs:
# Outputs:
# Modifications:
###################################
import sys
class ProjectUtilityFunctions(object):
    def __init__(self):
        return
    def openFile(self, strFilePath, strOpenMode):
        try:
            fhand = open(strFilePath, strOpenMode)
        except:
            print "ProjectUtilityFunctions Class: Unable to open file."
            sys.exit()
        return fhand

    def buildLineList(self, line):
        return line.split(",")
    def removeEmptyCoordinate(self,lsCoords):
        try:
            lsCoords.remove('')
        except:
            pass