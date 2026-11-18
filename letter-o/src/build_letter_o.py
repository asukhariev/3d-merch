"""Letter pendant traced from the reference glyph (high-contrast O + diamond).
The chain is the V: it enters the O and runs straight through a tunnel in the diamond (left tip -> right tip),
in front of the O band, so from the front it reads exactly like the letter.
usage: build_letter_o.py WIDTH_MM"""
import sys, cadquery as cq
W=float(sys.argv[1]) if len(sys.argv)>1 else 24.0
s=W/136.0
A,B=68*s,57.5*s
SIDE,TOPB=max(20*s,1.5),max(9*s,1.5)
a,b=A-SIDE,B-TOPB
DW,DH=19*s*1.15,24*s*1.15                 # diamond a bit larger to host the tunnel
RING_Z0,RING_T=0.0,4.2                    # flat medallion: ring and diamond same thickness
DIA_Z0,DIA_T=0.0,4.2
HOLE_D,HOLE_Z=1.2,2.1                     # one straight channel: ring side, diamond, ring side (3 openings), walls 1.5
dcy=0.0                                   # diamond centred in the O, like the glyph
o=(cq.Workplane().ellipse(A,B).extrude(RING_T).cut(cq.Workplane().ellipse(a,b).extrude(RING_T))).translate((0,0,RING_Z0))
dia=cq.Workplane().polyline([(0,dcy+DH),(DW,dcy),(0,dcy-DH),(-DW,dcy)]).close().extrude(DIA_T).translate((0,0,DIA_Z0))
neck=cq.Workplane().center(0,(dcy+DH+b+0.3)/2).rect(1.6,(b+0.3)-(dcy+DH)+0.8).extrude(RING_T).translate((0,0,RING_Z0))
hole=cq.Workplane('YZ').workplane(offset=-A-2).center(dcy,HOLE_Z).circle(HOLE_D/2).extrude(2*A+4)
body=o.union(neck).union(dia).cut(hole)
v=body.val(); bb=v.BoundingBox()
front_wall=(DIA_Z0+DIA_T)-(HOLE_Z+HOLE_D/2); back_wall=(HOLE_Z-HOLE_D/2)-DIA_Z0
print('O %.1f x %.1f, strokes %.2f/%.2f | diamond %.1f x %.1f x %.1f, tunnel D%.1f walls front %.2f back %.2f | depth %.1f | steel %.2f g | solids %d'%(2*A,2*B,SIDE,TOPB,2*DW,2*DH,DIA_T,HOLE_D,front_wall,back_wall,bb.zlen,v.Volume()*7.9/1000,len(v.Solids())))
n='letter-o/out/letter-o-pendant'
cq.exporters.export(body,n+'.step'); cq.exporters.export(body,n+'.stl',tolerance=0.005)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,(ax,ax2)=plt.subplots(1,2,figsize=(8,5.5),dpi=160,gridspec_kw={'width_ratios':[3,1.2]})
def shape(w,c,ax):
    q=[w.positionAt(i/900).toTuple() for i in range(901)];ax.fill([p[0] for p in q],[p[1] for p in q],color=c,ec='#222',lw=0.8)
# front view: O outline, then diamond on top, chain into the diamond tips
fo=[f for f in o.val().Faces() if abs(f.Center().z-(RING_Z0+RING_T))<1e-3][0]
shape(fo.outerWire(),'#222',ax); [shape(w,'white',ax) for w in fo.innerWires()]
ax.add_patch(plt.Rectangle((-0.8,dcy+DH),1.6,b-(dcy+DH)+0.3,color='#222'))
ax.fill([0,DW,0,-DW],[dcy+DH,dcy,dcy-DH,dcy],color='#222')
ax.plot([-W*0.95,-DW],[B*3,dcy],color='#999',lw=2.2);ax.plot([W*0.95,DW],[B*3,dcy],color='#999',lw=2.2)
ax.set_title('Лице',fontsize=9);ax.set_aspect('equal');ax.axis('off')
# side section through the centre
ax2.add_patch(plt.Rectangle((RING_Z0,-B),RING_T,2*B,color='#bbb'))
ax2.add_patch(plt.Rectangle((DIA_Z0,dcy-DH),DIA_T,2*DH,color='#222'))
ax2.add_patch(plt.Circle((HOLE_Z,dcy),HOLE_D/2,color='white'))
ax2.plot([HOLE_Z,HOLE_Z],[dcy,B*3],color='#999',lw=2.2)
ax2.set_title('Розріз збоку',fontsize=9);ax2.set_aspect('equal');ax2.axis('off');ax2.set_xlim(-3,7)
fig.suptitle('%.0f × %.0f мм · ромб %.1f мм завтовшки · канал Ø%.1f'%(2*A,2*B,DIA_T,HOLE_D),fontsize=9)
plt.savefig(n+'.png',bbox_inches='tight')
