"""«Обід» lettering traced to vector (SVG) and extruded. Thin hairlines are thickened to a printable minimum.
At the top of the ascender after «О» the piece is thickened into a boss with a side-to-side chain channel.
usage: build_obid.py WIDTH_MM"""
import sys; sys.path.insert(0,'tools')
import numpy as np, cadquery as cq, trace as tr
from scipy import ndimage
from skimage import morphology
W=float(sys.argv[1]) if len(sys.argv)>1 else 60.0
T,BOSS_T,HOLE_D,MIN_STROKE=2.0,4.2,1.2,0.9
m=tr.red_mask('obid/ref/reference.png',thr=50)
ys,xs=np.nonzero(m); s=W/(xs.max()-xs.min())
from skimage import filters
m=filters.gaussian(m.astype(float),0.3/s)>0.4                     # even, smooth thickening of hairlines
m=morphology.remove_small_objects(m,max_size=int((0.8/s)**2))     # drop specks that would fall off
lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1)); keep=np.argmax(sizes)+1
dropped=n-1; m=lab==keep                                            # one piece only
ys,xs=np.nonzero(m); x0,y1=xs.min(),ys.max()
sh=tr.to_mm(tr.shapes(m,k=5),s,x0,y1)
body=tr.solid(sh,0,T)
# ascender after «О»: topmost point of the glyph in the left half
cols=np.nonzero(m[:, :m.shape[1]//2].any(0))[0]
top_y=ys.min(); tx=np.nonzero(m[top_y])[0].mean()
by=top_y+int(2.2/s); row=np.nonzero(m[by,int(tx-3/s):int(tx+3/s)])[0]+int(tx-3/s); bx=row.mean()
BX,BY=(bx-x0)*s,(y1-by)*s; R=2.4
boss=cq.Workplane().center(BX,BY).circle(R).extrude(BOSS_T).translate((0,0,(T-BOSS_T)/2))
boss=boss.edges().fillet(0.8)
body=body.union(boss).cut(cq.Workplane().add(cq.Solid.makeCylinder(HOLE_D/2,2*R+2,cq.Vector(BX-R-1,BY,T/2),cq.Vector(1,0,0))))
v=body.val(); bb=v.BoundingBox()
print('Обід %.1f x %.1f x %.1f mm | dropped %d loose bits | boss D%.1f x %.1f, side channel D%.1f | steel %.2f g | solids %d'%(bb.xlen,bb.ylen,bb.zlen,dropped,2*R,BOSS_T,HOLE_D,v.Volume()*7.9/1000,len(v.Solids())))
o='obid/out/obid'
cq.exporters.export(body,o+'.step'); cq.exporters.export(body,o+'.stl',tolerance=0.01); tr.svg(sh,o+'.svg',fill='#c4122f')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5,5.5),dpi=150)
for ol,hs in sh:
    ax.fill(*zip(*ol),color='#c4122f'); [ax.fill(*zip(*h),color='white') for h in hs]
ax.add_patch(plt.Circle((BX,BY),R,fill=False,color='#333',lw=1)); ax.plot([BX-R-2,BX+R+2],[BY,BY],color='#3c3',lw=1.2,ls='--')
ax.set_aspect('equal'); ax.axis('off'); ax.set_title('%.0f × %.0f мм · %.0f мм, біля петлі %.1f мм · канал Ø%.1f збоку'%(bb.xlen,bb.ylen,T,BOSS_T,HOLE_D),fontsize=8)
plt.savefig(o+'.png',bbox_inches='tight')
