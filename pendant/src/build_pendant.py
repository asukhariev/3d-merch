import cadquery as cq, glob
from OCP.gp import gp_GTrsf, gp_Mat
from OCP.BRepBuilderAPI import BRepBuilderAPI_GTransform
comp=cq.importers.importStep(glob.glob('source/*.step')[0]).vals()[0]
plate=sorted(comp.Solids(),key=lambda s:-s.Volume())[0]
S=23.5/plate.BoundingBox().ylen
g=gp_GTrsf(); g.SetVectorialPart(gp_Mat(S,0,0, 0,S,0, 0,0,1))
plate=cq.Shape.cast(BRepBuilderAPI_GTransform(plate.wrapped,g,True).Shape())
top=plate.BoundingBox().ymax
RI,WALL,INSET=0.9,1.5,0.15; R=RI+WALL      # bore 2.0, outer 5.0
ZC=-RI                                  # outer front flush with the front face, front wall over bore = 1.5
YC=top-0.25-R
xl,xr=[],[]
for i in range(41):
    y=YC-R+2*R*i/40
    c=cq.Workplane().add(plate).intersect(cq.Workplane().box(40,0.02,3,centered=(False,True,False)).translate((-5,y,-1))).val().BoundingBox()
    xl.append(c.xmin);xr.append(c.xmax)
X0,X1=max(xl)+INSET,min(xr)-INSET;L=X1-X0
outer=cq.Workplane('YZ').workplane(offset=X0).center(YC,ZC).circle(R).extrude(L).val()
outer=outer.fuse(cq.Workplane().box(L,2*R,1.0-ZC,centered=False).translate((X0,YC-R,ZC)).val())
outer=outer.intersect(cq.Workplane().box(40,40,20,centered=(True,True,False)).translate((10,10,1.0-20)).val())
bore=cq.Workplane('YZ').workplane(offset=X0-1).center(YC,ZC).circle(RI).extrude(L+2).val()
body=plate.fuse(outer).cut(bore).clean()
b=body.BoundingBox();c=body.Center()
print('solids',len(body.Solids()),'YC %.2f ZC %.2f X0 %.2f X1 %.2f L %.2f'%(YC,ZC,X0,X1,L))
print('bbox %.2f x %.2f, z %.2f..%.2f, mass %.2f g, CoM %.2f %.2f'%(b.xlen,b.ylen,b.zmin,b.zmax,body.Volume()*8.0/1000,c.x,c.y))
cq.exporters.export(cq.Workplane().add(body),'pendant/out/pendant_d18.step')
cq.exporters.export(cq.Workplane().add(body),'pendant/out/pendant_d18.stl',tolerance=0.004,angularTolerance=0.05)
