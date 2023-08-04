import arcpy

mxd = arcpy.mapping.MapDocument(r"D:\ArcGIS projects\MXD\Chainager.mxd")
dataframe_Layers = arcpy.mapping.ListDataFrames(mxd, 'Layers')[0]
lines = arcpy.mapping.ListLayers(mxd, "Pipeline", dataframe_Layers)[0]
points = arcpy.mapping.ListLayers(mxd, "Points_from_building_footprint", dataframe_Layers)[0]

# Run the Copy Features tool, setting the output to the geometry object.
# geometries is returned as a list of geometry objects.

geometries = arcpy.CopyFeatures_management(lines,arcpy.Geometry())
length = 0
with arcpy.da.SearchCursor(points, ['Pipe_id','SHAPE@XY']) as cursor:
   for row in cursor:
       coordX = row[1][0]
       coordY = row[1][1]
       for geometry in geometries:
           length = geometry.measureOnLine(arcpy.Point(coordX, coordY))
           lengthRoundsplit = str(round(length)).split(".")[0]
           points.definitionQuery = "Pipe_id=" +"'"+row[0]+"'"
           with arcpy.da.UpdateCursor(points,'Chainage') as cursor:
               for row in cursor:
                   if len(lengthRoundsplit) == 1:
                       chainage = "0"+"+"+"0"+"0" + lengthRoundsplit
                       print chainage
                       row[0] = chainage
                   if len(lengthRoundsplit) == 2:
                       chainage = "0"+"+"+"0"+lengthRoundsplit
                       print chainage
                       row[0] = chainage
                   if len(lengthRoundsplit) == 3:
                       chainage = "0"+"+"+lengthRoundsplit
                       print chainage
                       row[0] = chainage
                   if len(lengthRoundsplit) >= 4:
                       constantVar = len(lengthRoundsplit) - 3
                       chainage = lengthRoundsplit[:constantVar] + "+" + lengthRoundsplit[constantVar:]
                       print chainage
                       row[0] = chainage
                   cursor.updateRow(row)
           points.definitionQuery = None
del cursor
del mxd
