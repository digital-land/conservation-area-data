import shapely
import pandas as pd
import geopandas
 
import datetime
from shapely.ops import cascaded_union, unary_union
from shapely.geometry import Polygon, LineString, Point, MultiPoint, MultiPolygon

print('=============================================================')
x = datetime.datetime.now()
y = x.strftime("%y%m%d_%H%M")

inputFile  = r'C:\Users\DavidBrown\Documents\GIS\beer\beer2\Vectorised_240726.csv'
outputFile = r'C:\Users\DavidBrown\Documents\GIS\beer\beer2\thePolygon_' + y + '.csv'


#inputFile  = r'C:\Users\DavidBrown\Documents\GIS\vector_sidbury.csv'
#outputFile = r'C:\Users\DavidBrown\Documents\GIS\_vector_sidbury_' + y + '.csv'    
    
    
pDefs = []

df = pd.read_csv(inputFile)

i = 0
MP = []
for idx, row in df.iterrows():
    i = i + 1
    #if (i > 66): 
    #    break
    
    polyDef = []
    pDef    = []
    
    POLYGON = row['WKT'].replace('POLYGON ','')
    POLYGON = POLYGON.replace('))','')
    POLYGON = POLYGON.replace('((','')
    
    PS= POLYGON.split(',')
 
    for c0 in PS:
        (c1, c2) = c0.split(' ')
        thistuple0 = (c1, c2)
        thistuple1 = tuple(float(el) for el in c0.split(' '))
        polyDef.append(thistuple1)  
        
    PE = Polygon(polyDef)
    pDefs.append(PE)

#print("46")
#print(pDefs)

# Create a GeoDataFrame from polygons
gdf = geopandas.GeoDataFrame({'geometry': pDefs})

# Ensure they are all individual polygons, not multipolygons
individual_polygons = [poly for poly in gdf.geometry]

#print("79")
#print(individual_polygons)


# [<POLYGON ((-344600.216 6568623.267, -344600.216 6568621.853,

bDefs = []

for p in individual_polygons:
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    polygon_type = ""
    width = 0
    height = 0
    xx, yy = p.exterior.coords.xy
    
    for x in range(0, 4):
        #print(xx[x], yy[x])

        i = float(xx[x]) - float(xx[x+1]) # horizontal width
        j = float(yy[x]) - float(yy[x+1]) # vertical height
    
        # TODO not refined enough, ambiguous
        if i > 2 or i < -2:
            #print(p)
            polygon_type = "horizontal"
            width = i
            height = float(yy[x]) - float(yy[x-1]) # vertical height
        elif j > 2 or j < -2:
            polygon_type = "vertical" 
            height = j
        else:
            polygon_type = "singleCube"
            height = i
            width = i


    
    # want to triple height
    if polygon_type == "horizontal":
        newPolyCoords = []
        for x in range(0, 5):

            x0 = xx[x]
            y0 = yy[x]
            #print(x0, y0)
                
            # if top left or right  
            if x == 0 or x ==3 or x ==4:
                xCoord = x0
                yCoord = y0 + height
                    
            # if bottom left or right  
            elif x == 1 or x == 2:
                xCoord = x0
                yCoord = y0 - height
                                
        
            t = tuple((xCoord, yCoord))
        
            newPolyCoords.append(t)

        
        d = Polygon(newPolyCoords)
        bDefs.append(d)

    elif polygon_type == "singleCube":
        #print("165:singleCube")
        newPolyCoords = []
        for x in range(0, 5):
        
            x0 = xx[x]
            y0 = yy[x]

            # if top left
            if x == 0 or x == 4:
                xCoord = x0 - height
                yCoord = y0 + height
            # if bottom right
            elif x == 1:
                xCoord = x0 - height
                yCoord = y0 - height
            # if bottom left
            elif x == 2:
                xCoord = x0 + height
                yCoord = y0 - height
            # if top left
            elif x == 3:
                xCoord = x0 + height
                yCoord = y0 + height
                                
      
            t = tuple((xCoord, yCoord))
            
            newPolyCoords.append(t)

        d = Polygon(newPolyCoords)
        bDefs.append(d)
        
    elif polygon_type == "vertical":
        #print("202:vertical")        
        pass
        
        
#print("195:bDefs")
#print(bDefs)
    
k = geopandas.GeoDataFrame({'geometry': bDefs})

#k.geometry = k.buffer(-20)
#k = k.buffer(1, cap_style=1, join_style=2)

#k.scale(0.5, 0.5)

#k.simplify(1)

# Use cascaded_union to merge all polygons into one
merged_polygon = unary_union(k)

#print("204")
#print(merged_polygon)


ordered_points = list(merged_polygon.exterior.coords)

final_polygon = Polygon(ordered_points)

final_polygon.buffer(-20, join_style=1)

#final_polygon = final_polygon.simplify(15, preserve_topology=False)

#final_polygon.scale(0.9, 0.9)

if (1==1):
    f = open(outputFile, "w")
    f.write('WKT\n')
    f.write('"')
    f.write(str(final_polygon))
    f.write('"')
    f.close()

print("DONE")

