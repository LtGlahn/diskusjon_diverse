import hentstrekninger
from qgis.core import QgsProject,  QgsVectorLayer, QgsFeature, QgsGeometry, QgsPoint, QgsLineString

def strekning2kart( lenkeliste, lagnavn ):
    
    egenskaper = [ 'field=vegref:string', 
                    'veglenkesekvensid:int', 
                    'startposisjon:double', 
                    'sluttposisjon:double', 
                    'kortform:string' ]
    egenskapdef = '&field='.join( egenskaper) 
    
    minelag = QgsProject.instance().mapLayersByName(lagnavn)
    if len(minelag) > 0: 
        qgislag = minelag[0]
    else: 
        qgislag = QgsVectorLayer('Linestringz'  + 
                                '?crs=epsg:25833&index=yes&' + 
                                egenskapdef, lagnavn, 'memory')
        
        QgsProject.instance().addMapLayer(qgislag)

    qgislag.startEditing() 
    
    egenskap_liste = egenskapdef.split('&') 
    for lenke in lenkeliste: 
        
        feat = QgsFeature()
        eg = []
        for egenskap in egenskap_liste: 
            mykey = egenskap[6:].split(':')[0]
            eg.append( lenke[mykey] )
            
        feat.setAttributes( eg ) 
        
        geom = QgsGeometry.fromWkt(lenke['wkt'] )
        feat.setGeometry(geom)
        
        qgislag.addFeature( feat )
        
    qgislag.updateExtents() 
    qgislag.commitChanges()
    

minelag = QgsProject.instance().mapLayersByName('strekninger')
features = minelag[0].getFeatures()
for feat in features: 
    geom = feat.geometry()
    points = geom.asPolyline()
    
    vvi = hentstrekninger.hentvisveginfo( points[0].x(),  points[0].y(), 
                                points[-1].x(), points[-1].y() ) 
    
    strekning2kart( vvi, 'vvi')
    topo = hentstrekninger.hentstrekning( points[0].x(),  points[0].y(), 
                                points[-1].x(), points[-1].y() )
    
    strekning2kart( topo, 'vegnettbeta')
    
