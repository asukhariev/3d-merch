"""Letter pendant traced from the reference glyph: a high-contrast O with a diamond hanging inside.
The chain itself forms the V above. usage: build_letter_o.py WIDTH_MM THICK_MM"""
import sys, cadquery as cq
W=float(sys.argv[1]) if len(sys.argv)>1 else 24.0
T=float(sys.argv[2]) if len(sys.argv)>2 else 2.0
s=W/136.0                                   # reference px -> mm
A,B=68*s,57.5*s                              # outer half-axes
SIDE,TOPB=20*s,9*s                           # stroke contrast: thick sides, thin top/bottom
MIN=1.5                                      # JLC3DP metal minimum wall
TOPB=max(TOPB,MIN); SIDE=max(SIDE,MIN)
a,b=A-SIDE,B-TOPB                            # inner half-axes
DW,DH=19*s,24*s                              # diamond half-width / half-height
dcy=b-1.2*s*10-DH                             # diamond hangs just under the inner top
NECK=MIN
o=cq.Workplane().ellipse(A,B).extrude(T).cut(cq.Workplane().ellipse(a,b).extrude(T))
dia=cq.Workplane().polyline([(0,dcy+DH),(DW,dcy),(0,dcy-DH),(-DW,dcy)]).close().extrude(T)
neck=cq.Workplane().center(0,(dcy+DH+b+0.3)/2).rect(NECK,(b+0.3)-(dcy+DH)+0.6).extrude(T)
body=o.union(dia).union(neck)
v=body.val()
print('O %.1f x %.1f mm, strokes side %.2f / top %.2f, diamond %.1f x %.1f, neck %.1f, thick %.1f, steel %.2f g, solids %d'%(2*A,2*B,SIDE,TOPB,2*DW,2*DH,NECK,T,v.Volume()*7.9/1000,len(v.Solids())))
n='letter-o/out/letter-o-pendant'
cq.exporters.export(body,n+'.step'); cq.exporters.export(body,n+'.stl',tolerance=0.005); cq.exporters.export(body.section(T/2),n+'.dxf')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
face=[f for f in v.Faces() if abs(f.Center().z-T)<1e-3][0]
fig,ax=plt.subplots(figsize=(4.5,6),dpi=160)
outer=face.outerWire()
for w in face.Wires():
    q=[w.positionAt(i/900).toTuple() for i in range(901)]
    ax.fill([p[0] for p in q],[p[1] for p in q],color='#222' if w.isSame(outer) else 'white',ec='#222',lw=0.8)
gap=(a*0.55)
ax.plot([-W*0.9,-gap],[B*3.2,b*0.55],color='#888',lw=2.5);ax.plot([W*0.9,gap],[B*3.2,b*0.55],color='#888',lw=2.5)
ax.text(0,-B-3,'%.0f × %.0f mm · товщина %.1f · ланцюжок = «V»'%(2*A,2*B,T),ha='center',fontsize=8)
ax.set_aspect('equal');ax.axis('off');plt.savefig(n+'.png',bbox_inches='tight')
