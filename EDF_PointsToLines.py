
###################################
# Script:  EDF_PointsToLines.py
# Author:  CJuice on GitHub
# Date Created:  09/25/2017
# Purpose:  Convert multi-value comma separated latitude and longitude fields to points that are vertices in a line. The lines are mobile monitoring events. The true points (one lat, one lon) are static monitoring events. Store the lines in a feature class and the static points in a feature class.
# Inputs:  CSV file containing event data for 4 chemicals. This includes chemical readings and geographic data.
# Outputs:  feature classes (point, line)
# Modifications:
###################################
#ADDITIONAL IMPORTS
import arcpy
import ProjectUtilityFunctions as PUF
import RecordObject as RO

#VARIABLES
strCSVFilePath = r""
strOpenInReadMode = "r"
strGISWorkspaceEnv = r""
strLineFeatureClassName = "lnMobileEvents"
strPointFeatureClassName = "ptStaticEvents"
strNullData = "Null"
strPipeSeparator = "|"
tupFieldsInStaticEventFeatureClassRow = ("OBJECTID","SHAPE@XY","Date","Time","MeasurementType","BenzenePPB","ToluenePPB","EthylbenzenePPB","XylenesPPB","WindDirection","WindSpeed")
tupFieldsInMobileEventFeatureClassRow = ("OBJECTID","SHAPE@","Date","Time","MeasurementType","BenzenePPB","ToluenePPB","EthylbenzenePPB","XylenesPPB","WindDirection","WindSpeed","SHAPE_Length")
intLineCount = 0
intStaticEventCount = 0
intMobileEventCount = 0
instancePUF = PUF.ProjectUtilityFunctions()
arcpy.env.workspace = strGISWorkspaceEnv
arcpyEditSession = arcpy.da.Editor(arcpy.env.workspace)
arcpyEditSession.startEditing(False,False)

#FUNCTIONALITY
    #open and read csv
fHandCSVFile = instancePUF.openFile(strCSVFilePath, strOpenInReadMode)
for line in fHandCSVFile:
    line = line.strip()
    if intLineCount == 0:
        # store header indices
        intLineCount += 1
    else:
        objRecord = RO.RecordObject(instancePUF.buildLineList(line))
        objRecord.checkForValidChemicalValues()
        lsTrackLatitudeCoords = objRecord.strMobileEventLatitudeTrack.split("|")
        lsTrackLongitudeCoords = objRecord.strMobileEventLongitudeTrack.split("|")
        #there was one empty coord on the end of every coordinate track list, remove it.
        instancePUF.removeEmptyCoordinate(lsTrackLatitudeCoords)
        instancePUF.removeEmptyCoordinate(lsTrackLongitudeCoords)

        if (objRecord.strMeasurementType).lower() == "static":
            #create a point and add it to point feature class
            floatLatitude = float(objRecord.strStaticEventLatitude)
            floatLongitude = float(objRecord.strStaticEventLongitude)
            tupRowContents =(intStaticEventCount,[floatLongitude,floatLatitude],objRecord.strDate,objRecord.strTime,
                             objRecord.strMeasurementType,objRecord.Benzene,
                             objRecord.Toluene,objRecord.Ethylbenzene,
                             objRecord.Xylenes,int(objRecord.strWindDirn),int(objRecord.strWindSpeed))
            arcpyEditSession.startOperation()
            with arcpy.da.InsertCursor(strPointFeatureClassName, tupFieldsInStaticEventFeatureClassRow) as cursorPointFeatureClass:
                cursorPointFeatureClass.insertRow(tupRowContents)
            arcpyEditSession.stopOperation()
            intStaticEventCount += 1
        else:
            #create points, store them in an Array, then make a line and store in the line feature class
            lsArcpyPointsForLine = []
            for i in range(len(lsTrackLatitudeCoords)):
                floatLatitude = float(lsTrackLatitudeCoords[i])
                floatLongitude = float(lsTrackLongitudeCoords[i])
                point = arcpy.Point(floatLongitude,floatLatitude)
                lsArcpyPointsForLine.append(point)
            array = arcpy.Array(lsArcpyPointsForLine)
            polyline = arcpy.Polyline(array)
            tupRowContents = (intMobileEventCount,
                              polyline,
                              objRecord.strDate,objRecord.strTime,objRecord.strMeasurementType,
                              objRecord.Benzene,objRecord.Toluene,objRecord.Ethylbenzene,objRecord.Xylenes,
                              int(objRecord.strWindDirn),int(objRecord.strWindSpeed),0.0)
            arcpyEditSession.startOperation()
            with arcpy.da.InsertCursor(strLineFeatureClassName, tupFieldsInMobileEventFeatureClassRow) as cursorLineFeatureClass:
                cursorLineFeatureClass.insertRow(tupRowContents)
            arcpyEditSession.stopOperation()
            intMobileEventCount += 1
        del objRecord

#DELETE STATEMENTS
fHandCSVFile.close()
arcpyEditSession.stopEditing(True)
if cursorLineFeatureClass:
    del cursorLineFeatureClass
if cursorPointFeatureClass:
    del cursorPointFeatureClass
del fHandCSVFile
print "Script completed."