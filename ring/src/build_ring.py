"""Ring pendant: the chain runs through the ring (forms the V), the Shryftoriz mark sits inside.
usage: build_ring.py OUTER_D BAND THICK   (mm)"""
import sys, math, cadquery as cq
P=[(77.3328,49.7992),(83.6882,49.7992),(130.121,49.6074),(79.2093,109.134),(73.5525,109.134),(78.0451,68.1531),(73.21,78.5216),(19.8057,211.286),(14.8064,210.971),(34.2971,76.4534),(36.1462,68.0709),(6.35537,108.874),(2.45175,108.874),(0,49.6074),(45.9669,49.7992),(45.9121,0.202637),(109.89,0.202637)]
OD=float(sys.argv[1]) if len(sys.argv)>1 else 26.0
BAND=float(sys.argv[2]) if len(sys.argv)>2 else 1.6
T=float(sys.argv[3]) if len(sys.argv)>3 else 1.5
R_in=OD/2-BAND
cx=sum(x for x,_ in P)/len(P); cy=sum(y for _,y in P)/len(P)          # rough visual centre
far=max(math.hypot(x-cx,y-cy) for x,y in P)
s=(R_in+0.35)/far                                                    # tips sink 0.35 mm into the band
pts=[((x-cx)*s,-(y-cy)*s) for x,y in P]
ring=cq.Workplane().circle(OD/2).circle(R_in).extrude(T)
mark=cq.Workplane().polyline(pts).close().extrude(T)
body=ring.union(mark)
v=body.val(); bb=v.BoundingBox()
print('ring OD %.1f band %.1f thick %.1f | mark %.1f x %.1f mm | steel %.2f g | solids %d'%(OD,BAND,T,(max(p[0] for p in pts)-min(p[0] for p in pts)),(max(p[1] for p in pts)-min(p[1] for p in pts)),v.Volume()*7.9/1000,len(v.Solids())))
n='ring/out/shryftoriz-ring-pendant'
cq.exporters.export(body,n+'.step'); cq.exporters.export(body,n+'.stl',tolerance=0.005); cq.exporters.export(body.section(T/2),n+'.dxf')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
face=[f for f in v.Faces() if abs(f.Center().z-T)<1e-3][0]
fig,ax=plt.subplots(figsize=(5,6.5),dpi=150)
for w in face.Wires():
    q=[w.positionAt(i/800).toTuple() for i in range(801)]
    ax.fill([a[0] for a in q],[a[1] for a in q],color='#c9ccd1' if w.isSame(face.outerWire()) else 'white',ec='#222',lw=1)
# chain as a V through the top of the ring
ax.plot([-22,-0.6],[OD*1.6,OD/2-BAND/2],color='#555',lw=2);ax.plot([22,0.6],[OD*1.6,OD/2-BAND/2],color='#555',lw=2)
ax.text(0,-OD/2-3,'Ø %.0f mm · стрічка %.1f · товщина %.1f'%(OD,BAND,T),ha='center',fontsize=8)
ax.set_aspect('equal');ax.axis('off');plt.savefig(n+'.png',bbox_inches='tight')
