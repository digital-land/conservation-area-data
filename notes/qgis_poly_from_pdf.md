How to use QGIS to generate a map polygon from PDF map.

Using OSM Standard (Open Street Map) as layer to identify coordinates

Using Honiton as an example
<https://eastdevon.gov.uk/media/560777/honitoncaa.pdf>

1.  Identify ‘best’ map from available maps. I used the criteria of
    clearest outline, a legend which doesn’t cover the outline or
    significant portions of the map, and less artifacts in the map.
2.  Copy and paste into a .jpeg file (using snipping tool) and if
    necessary, rotate so north is upwards.

1.  Import into QGIS using the Georeferencer tool (Layer,
    Georeferencer).

1.  Map at least 6 points from the picture onto the world map to ensure
    it maps correctly. I find using road junctions, bridges, and corners
    of fields work well. With OS maps as the source and OSM as the
    target, the transformation type should be Projective.

1.  Confirm the maps are lined up using transparency, matching roads and
    other landmarks.
2.  Create a new vector layer and using the edit, add polygon feature,
    trace the
    outline.<img src="media/image4.png" style="width:6.26806in;height:4.03056in" />
3.  Export the polygon as a csv using the geometry
    AS\_WKT.<img src="media/image5.png" style="width:6.08418in;height:6.10502in" />
4.  This gives you a text file where you can get the MULTIPOLYGON
    definition of the polygon.

Consideration needs to be given to where on the line the actual border
is. Some areas use a thick line which can be outside, inside or across
the border. Usually it is obvious which but care must be taken as it can
vary depending on the policies of the LPA who look after the data.
