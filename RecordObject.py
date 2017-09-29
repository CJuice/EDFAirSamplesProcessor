
###################################
# Script:  ProjectUtilityFunctions.py
# Author:  CJuice on GitHub
# Date Created:  09/25/2017
# Purpose:  Take attribute data for each record and create an object for use
# Inputs:
# Outputs:
# Modifications:
###################################
class RecordObject(object):
    def __init__(self,lsLineContents):
        self.lsLineContents = lsLineContents
        self.strDate = lsLineContents[0]
        self.strTime = lsLineContents[1]
        self.strMeasurementType = lsLineContents[2]
        self.Benzene = lsLineContents[3]
        self.Toluene = lsLineContents[4]
        self.Ethylbenzene = lsLineContents[5]
        self.Xylenes = lsLineContents[6]
        self.strWindDirn = lsLineContents[7]
        self.strWindSpeed = lsLineContents[8]
        self.strStaticEventLatitude = lsLineContents[9]
        self.strStaticEventLongitude = lsLineContents[10]
        self.strMobileEventLatitudeTrack = lsLineContents[11]
        self.strMobileEventLongitudeTrack = lsLineContents[12]

    def checkForValidChemicalValues(self):
        try:
            value = float(self.Benzene)
            self.Benzene = value
        except:
            self.Benzene = -9999.0

        try:
            value = float(self.Toluene)
            self.Toluene = value
        except:
            self.Toluene = -9999.0

        try:
            value = float(self.Ethylbenzene)
            self.Ethylbenzene = value
        except:
            self.Ethylbenzene = -9999.0

        try:
            value = float(self.Xylenes)
            self.Xylenes = value
        except:
            self.Xylenes = -9999.0
