"""Lisovsky «Ф» (Lviv, 1923) pendant traced from letter-f/ref/reference.png.
Flat piece, chain channel runs side-to-side through the top stem. usage: build_letter_f.py HEIGHT_MM"""
import sys; sys.path.insert(0,'tools')
import numpy as np, cadquery as cq, trace as tr
H=float(sys.argv[1]) if len(sys.argv)>1 else 30.0
T,HOLE_D=4.2,1.2   # side channel D1.2 + 1.5 walls
m=tr.red_mask('letter-f/ref/reference.png'); m[900:]=False          # drop the signature below
ys,xs=np.nonzero(m); s=H/(ys.max()-ys.min()); x0=(xs.min()+xs.max())/2
sh=tr.to_mm(tr.shapes(m,k=5),s,x0,ys.max())
body=tr.solid(sh,0,T)
# hole in the top stem: centred, just below its top serif
top=ys.min(); row=np.nonzero(m[top+int(1.5/s)])[0]; hx=((row.min()+row.max())/2-x0)*s; hy=H-max(1.6,HOLE_D/2+1.5); stem_w=(row.max()-row.min())*s
body=body.cut(cq.Workplane().add(cq.Solid.makeCylinder(HOLE_D/2,stem_w+4,cq.Vector(hx-stem_w/2-2,hy,T/2),cq.Vector(1,0,0))))   # horizontal through the top stem
v=body.val(); bb=v.BoundingBox()
print('Ф %.1f x %.1f x %.1f mm | top stem %.1f mm wide, side channel D%.1f, walls front/back %.2f | steel %.2f g | solids %d'%(bb.xlen,bb.ylen,bb.zlen,stem_w,HOLE_D,(T-HOLE_D)/2,v.Volume()*7.9/1000,len(v.Solids())))
o='letter-f/out/letter-f-pendant'
cq.exporters.export(body,o+'.step'); cq.exporters.export(body,o+'.stl',tolerance=0.005); tr.svg(sh,o+'.svg')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(4,5),dpi=150)
for ol,hs in sh:
    ax.fill(*zip(*ol),color='#7a2018'); [ax.fill(*zip(*h),color='white') for h in hs]
ax.plot([hx-stem_w,hx+stem_w],[hy,hy],color='#3c3',lw=1.2,ls='--'); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('%.0f × %.0f × %.0f мм · канал Ø%.1f збоку'%(bb.xlen,bb.ylen,bb.zlen,HOLE_D),fontsize=8); plt.savefig(o+'.png',bbox_inches='tight')
