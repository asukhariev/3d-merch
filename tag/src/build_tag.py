import cadquery as cq, sys
P=[(77.3328,49.7992),(83.6882,49.7992),(130.121,49.6074),(79.2093,109.134),(73.5525,109.134),(78.0451,68.1531),(73.21,78.5216),(19.8057,211.286),(14.8064,210.971),(34.2971,76.4534),(36.1462,68.0709),(6.35537,108.874),(2.45175,108.874),(0,49.6074),(45.9669,49.7992),(45.9121,0.202637),(109.89,0.202637)]
GAP=float(sys.argv[1]); M=float(sys.argv[2]); T=2.0; R=8.0
s=GAP/44.82; ymax=211.286
pts=[(x*s,(ymax-y)*s) for x,y in P]
W=130.121*s; H=(ymax-0.2026)*s
plate=cq.Workplane().center(W/2,H/2).rect(W+2*M,H+2*M).extrude(T).edges("|Z").fillet(R)
logo=cq.Workplane().polyline(pts).close().extrude(T)
tag=plate.cut(logo)
bb=tag.val().BoundingBox()
print('tag %.0f x %.0f x %.0f mm, logo %.0f x %.0f mm, cap gap %.0f mm, steel %.0f g'%(bb.xlen,bb.ylen,bb.zlen,W,H,GAP,tag.val().Volume()*7.9/1000))
cq.exporters.export(tag,'tag/out/shryftoriz-tag-negative.step');cq.exporters.export(tag,'tag/out/shryftoriz-tag-negative.stl',tolerance=0.01)
cq.exporters.export(tag.section(T/2),'tag/out/shryftoriz-tag-negative.dxf')
import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
face=[f for f in tag.val().Faces() if abs(f.Center().z-T)<1e-3][0]
fig,ax=plt.subplots(figsize=(6,9),dpi=150)
for w in face.Wires():
    p=[w.positionAt(i/600).toTuple() for i in range(601)]
    ax.fill([q[0] for q in p],[q[1] for q in p],color='#c9ccd1' if w.isSame(face.outerWire()) else 'white',ec='#222',lw=1)
import matplotlib.patches as mp
cx,cy=(45.94+22.41)*s,(ymax-0.2026-22.41)*s
ax.add_patch(mp.Circle((cx,cy),13,fill=False,ls='--',ec='#d0342c',lw=1.2));ax.text(cx,cy,'кришка\nØ26',ha='center',va='center',fontsize=8,color='#d0342c')
ax.text(W/2,-M-6,'%.0f mm'%bb.xlen,ha='center');ax.text(W+M+3,H/2,'%.0f mm'%bb.ylen,rotation=90,va='center')
ax.set_aspect('equal');ax.axis('off');ax.set_title('Жетон Шрифторіз · знак вирізаний наскрізь · сталь 2 мм',fontsize=9)
plt.savefig('tag/out/shryftoriz-tag-negative.png',bbox_inches='tight')
