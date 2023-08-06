##############################################################################
# MIT License
# 
# Copyright (c) 2020-2021 Her Majesty the Queen in Right of Canada, as 
# represented by the President of the Treasury Board
# 
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.
# 
##############################################################################

import os
import sys
from xml.etree import ElementTree
import json
import logging
try:
    import ogr
    import osr
    GDAL_INSTALLED = True
except ImportError:
    try:
        import osgeo.ogr as ogr
        import osgeo.osr as osr
        GDAL_INSTALLED = True
    except ImportError:
        GDAL_INSTALLED = False
    
# try:
    # import geojson
    # GEOJSON_INSTALLED = True
# except ImportError:
    # GEOJSON_INSTALLED = False

class EODMSGeo:
    """
    The Geo class contains all the methods and functions used to perform 
        geographic processes mainly using OGR.
    """
    
    def __init__(self, eodmsrapi):
        """
        Initializer for the Geo object.
        
        @type  aoi_fn: str
        @param aoi_fn: The AOI filename.
        """
        self.aoi = None
        
        self.logger = logging.getLogger('EODMSRAPI')
        
        self.wkt_types = ['Geometry', 'Point', 'LineString', 'Polygon', \
                        'MultiPoint', 'MultiLineString', 'MultiPolygon', \
                        'GeometryCollection', 'CircularString', \
                        'CompoundCurve', 'CurvePolygon', 'MultiCurve', \
                        'MultiSurface', 'Curve', 'Surface', \
                        'PolyhedralSurface', 'TIN', 'Triangle', 'Circle', \
                        'GeodesicString', 'EllipticalCurve', 'NurbsCurve', \
                        'Clothoid', 'SpiralCurve', 'CompoundSurface', \
                        'BrepSolid', 'AffinePlacement']
        self.eodmsrapi = eodmsrapi
        
    def set_aoi(self, in_aoi):
        """
        Processes the AOI and converts it for use in the RAPI.
        
        @type  aoi: str
        @param aoi: The AOI can either be:
                    - a filename (ESRI Shapefile, KML, GML or GeoJSON)
                    - a WKT format string
                    - the 'geometry' entry from a GeoJSON Feature
                    - a list of coordinates (ex: [(x1, y1), (x2, y2), ...])
        """
        
        if in_aoi is None:
            # print("The AOI is None!")
            return None
            
        # If the AOI is WKT
        if any(word.upper() in in_aoi for word in self.wkt_types):
            # print("The AOI is WKT")
            self.aoi = in_aoi
            return self.aoi
        
        # If the AOI is in JSON format
        if self.eodmsrapi._is_json(in_aoi):
            in_aoi = json.loads(in_aoi)
            
        if isinstance(in_aoi, dict):
            # print("The AOI is JSON")
            self.aoi = self.convert_imageGeom(in_aoi, 'wkt')
            return self.aoi
                
        if isinstance(in_aoi, list):
            # print("The AOI is a list")
            self.aoi = self.convert_imageGeom([in_aoi], 'wkt')
            return self.aoi
            
        # If the AOI is a file
        if os.path.isfile(in_aoi):
            # print("The AOI is a file")
            self.aoi = self.get_polygon(in_aoi)
            return self.aoi
        
        if os.path.isdir(in_aoi):
            # print("The AOI is a folder")
            return None
            
        # If the AOI is a list of coordinates
        if not isinstance(in_aoi, list):
            try:
                in_aoi = eval(in_aoi)
            except SyntaxError as err:
                # print("\n%sWARNING: %s" % (self.eodmsrapi._header, err))
                self.logger.warning("%s" % err)
                return err
        
    def convert_imageGeom(self, coords, output='array'):
        """
        Converts a list of coordinates from the RAPI to a polygon geometry, 
            array of points or as WKT.
        
        @type  coords: list
        @param coords: A list of coordinates from the RAPI results.
        @type  output: str
        @param output: The type of return, can be 'array', 'wkt' or 'geom'.
        
        @rtype:  multiple
        @return: Either a polygon geometry, WKT or array of points.
        """
        
        # print("coords: %s" % type(coords))
        # print("coords: %s" % coords)
        if isinstance(coords, dict):
            
            if 'coordinates' in coords.keys():
                # geo_type = coords['type']
                # print("geo_type: %s" % geo_type)
                # if geo_type == 'MultiPolygon':
                    # coords = coords['coordinates'][0]
                # else:
                    # coords = coords['coordinates']
                # coords = coords['coordinates']
                val = coords['coordinates']
                level = 0
                while isinstance(val, list):
                    val = val[0]
                    level += 1
                #print("val: %s" % val)
                #print("level: %s" % level)
                lst_level = level - 2
                
                # print("lst_level: %s" % lst_level)
                if lst_level > -1:
                    pnt_array = eval("coords['coordinates']" + '[0]'*(lst_level))
                else:
                    pnt_array = coords['coordinates']
                #print("final_lst: %s" % final_lst)
                #answer = input("Press enter...")
            else:
                # print("%sNo coordinates provided." % self.eodmsrapi._header)
                logger.warning("No coordinates provided.")
                return None
        else:
            pnt_array = coords[0]
            
        # print("pnt_array: %s" % pnt_array)
        
        # Get the points from the coordinates list
        pnt1 = pnt_array[0]
        pnt2 = pnt_array[1]
        pnt3 = pnt_array[2]
        pnt4 = pnt_array[3]
        
        # pnt_array = [pnt1, pnt2, pnt3, pnt4]
        
        # print("pnt_array: %s" % pnt_array)
        
        if GDAL_INSTALLED:
            # Create ring
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(pnt1[0], pnt1[1])
            ring.AddPoint(pnt2[0], pnt2[1])
            ring.AddPoint(pnt3[0], pnt3[1])
            ring.AddPoint(pnt4[0], pnt4[1])
            ring.AddPoint(pnt1[0], pnt1[1])

            # Create polygon
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)
            
            # Send specified output
            if output == 'wkt':
                # print("poly.ExportToWkt(): %s" % poly.ExportToWkt())
                return poly.ExportToWkt()
            elif output == 'geom':
                return poly
            else:
                return pnt_array
                
        else:
            if output == 'wkt':
                # Convert values in point array to strings
                pnt_array = [[str(p[0]), str(p[1])] for p in pnt_array]
                
                return "POLYGON ((%s))" % ', '.join([' '.join(pnt) \
                    for pnt in pnt_array])
            else:
                return pnt_array
            
    def convert_fromWKT(self, in_feat):
        """
        Converts a WKT to a polygon geometry.
        
        @type  in_feat: str
        @param in_feat: The WKT of the polygon.
        
        @rtype:  ogr.Geometry
        @return: The polygon geometry of the input WKT.
        """
        
        if GDAL_INSTALLED:
            out_poly = ogr.CreateGeometryFromWkt(in_feat)
        
        return out_poly
            
    def convert_toGeoJSON(self, results):
        
        features = [{"type": "Feature", "geometry": rec['Record Info']\
                    ['geometry'], "properties": rec} for rec in results]
        feature_collection = {"type": "FeatureCollection", 
                            "features": features}
        #print(json.dumps(feature_collection, sort_keys=True, indent=4))
        
        return feature_collection        
        
    def get_polygon(self, in_aoi):
        """
        Extracts the polygon from an AOI file.
        
        @rtype:  str
        @return: The AOI in WKT format.
        """
        
        if GDAL_INSTALLED:
            # Determine the OGR driver of the input AOI
            if in_aoi.find('.gml') > -1:
                ogr_driver = 'GML'
            elif in_aoi.find('.kml') > -1:
                ogr_driver = 'KML'
            elif in_aoi.find('.json') > -1 or in_aoi.find('.geojson') > -1:
                ogr_driver = 'GeoJSON'
            elif in_aoi.find('.shp') > -1:
                ogr_driver = 'ESRI Shapefile'
            else:
                err_msg = "The AOI file type could not be determined."
                #print("%s%s" % (self.eodmsrapi._header, err_msg))
                self.logger.error(err_msg)
                sys.exit(1)
                
            # Open AOI file and extract AOI
            driver = ogr.GetDriverByName(ogr_driver)
            ds = driver.Open(in_aoi, 0)
            
            # Get the layer from the file
            lyr = ds.GetLayer()
            
            # Set the target spatial reference to WGS84
            t_crs = osr.SpatialReference()
            t_crs.ImportFromEPSG(4326)
            
            for feat in lyr:
                # Create the geometry
                geom = feat.GetGeometryRef()
                
                # print("geom: %s" % geom)
                
                # Convert the geometry to WGS84
                s_crs = geom.GetSpatialReference()
                
                # Get the EPSG codes from the spatial references
                epsg_sCrs = s_crs.GetAttrValue("AUTHORITY", 1)
                epsg_tCrs = t_crs.GetAttrValue("AUTHORITY", 1)
                
                if not str(epsg_sCrs) == '4326':
                    if epsg_tCrs is None:
                        print("\nCannot reproject AOI.")
                        sys.exit(1)
                    
                    if not s_crs.IsSame(t_crs) and not epsg_sCrs == epsg_tCrs:
                        # Create the CoordinateTransformation
                        print("\nReprojecting input AOI...")
                        coordTrans = osr.CoordinateTransformation(s_crs, t_crs)
                        geom.Transform(coordTrans)
                        
                        # Reverse x and y of transformed geometry
                        ring = geom.GetGeometryRef(0)
                        for i in range(ring.GetPointCount()):
                            ring.SetPoint(i, ring.GetY(i), ring.GetX(i))
                
                # Convert multipolygon to polygon (if applicable)
                if geom.GetGeometryType() == 6:
                    geom = geom.UnionCascaded()
                
                # Convert to WKT
                aoi_feat = geom.ExportToWkt()
                
        else:
            # Determine the OGR driver of the input AOI
            if in_aoi.find('.gml') > -1 or in_aoi.find('.kml') > -1:
                
                with open(in_aoi, 'rt') as f:
                    tree = ElementTree.parse(f)
                    root = tree.getroot()
                
                if in_aoi.find('.gml') > -1:
                    coord_lst = []
                    for coords in root.findall('.//{http://www.opengis.net/' \
                        'gml}coordinates'):
                        coord_lst.append(coords.text)
                else:
                    coord_lst = []
                    for coords in root.findall('.//{http://www.opengis.net/' \
                        'kml/2.2}coordinates'):
                        coord_lst.append(coords.text)
                        
                pnts_array = []
                for c in coord_lst:
                    pnts = [p.strip('\n').strip('\t').split(',') for p in \
                            c.split(' ') if not p.strip('\n').strip('\t') == '']
                    #print("pnts: %s" % pnts)
                    pnts_array += pnts
                
                # print("pnts_array: %s" % pnts_array)
                
                aoi_feat = "POLYGON ((%s))" % ', '.join([' '.join(pnt[:2]) \
                    for pnt in pnts_array])
                    
                # print("aoi_feat: %s" % aoi_feat)
                # answer = input("Press enter...")
                
            elif in_aoi.find('.json') > -1 or in_aoi.find('.geojson') > -1:
                with open(in_aoi) as f:
                    data = json.load(f)
                
                feats = data['features']
                for f in feats:
                    geo_type = f['geometry']['type']
                    if geo_type == 'MultiPolygon':
                        coords = f['geometry']['coordinates'][0][0]
                    else:
                        coords = f['geometry']['coordinates'][0]
                
                # Convert values in point array to strings
                coords = [[str(p[0]), str(p[1])] for p in coords]
                aoi_feat = "POLYGON ((%s))" % ', '.join([' '.join(pnt) \
                            for pnt in coords])
                            
            elif in_aoi.find('.shp') > -1:
                msg = "Could not open shapefile. The GDAL Python Package " \
                        "must be installed to use shapefiles."
                # print("\n%s%s" % (self.eodmsrapi._header, msg))
                self.logger.warning(msg)
                # sys.exit(1)
                return None
            else:
                # print("%sThe AOI file type could not be determined." % \
                #     self.eodmsrapi._header)
                self.logger.warning(msg)
                # sys.exit(1)
                return None
            
        return aoi_feat
