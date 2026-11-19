"""«О» kateevision as a STAMP pendant: ink the striped face and print it.
Takes the traced pendant (glyph_pendant.py output: 2 mm plate + back bail), adds raised horizontal stripes on the
front face and mirrors everything so the print reads like the reference. usage: build_stamp.py [PERIOD_MM RIDGE_MM RELIEF_MM]"""
import sys, cadquery as cq
P,RIDGE,RELIEF=[float(a) for a in sys.argv[1:4]] if len(sys.argv)>3 else (1.5,0.8,0.8)
T=2.0
base=cq.importers.importStep('letter-o-stripes/out/letter-o-stripes-pendant.step')
bb=base.val().BoundingBox()
plate=base.intersect(cq.Workplane().box(200,200,T,centered=(True,True,False)).translate((0,0,0)))
face=plate.translate((0,0,RELIEF)).intersect(cq.Workplane().box(200,200,RELIEF,centered=(True,True,False)).translate((0,0,T)))
bars=None; y=bb.ymin+0.6
while y<bb.ymax-0.3:
    b=cq.Workplane().center((bb.xmin+bb.xmax)/2,y+RIDGE/2).rect(bb.xlen+2,RIDGE).extrude(RELIEF).translate((0,0,T))
    bars=b if bars is None else bars.union(b); y+=P
ridges=face.intersect(bars)
body=base.union(ridges).mirror('YZ',basePointVector=((bb.xmin+bb.xmax)/2,0,0))
v=body.val(); b2=v.BoundingBox()
print('stamp %.1f x %.1f x %.1f mm | stripes period %.1f ridge %.1f gap %.1f relief %.1f | steel %.2f g | solids %d'%(b2.xlen,b2.ylen,b2.zlen,P,RIDGE,P-RIDGE,RELIEF,v.Volume()*7.9/1000,len(v.Solids())))
o='letter-o-stripes/out/letter-o-stripes-stamp'
cq.exporters.export(body,o+'.step'); cq.exporters.export(body,o+'.stl',tolerance=0.005)
