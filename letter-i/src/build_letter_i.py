"""Letter «і» pendant traced from the reference (letter-i/ref/reference.png): serif stem + dot as two flame tongues.
Front face = the traced glyph exactly (flames read as separate). Back half = small bridges so it prints as ONE piece.
Chain hole goes front-to-back through the gap between the flames, biting into both. usage: build_letter_i.py HEIGHT_MM"""
import sys, numpy as np, cadquery as cq
from PIL import Image
from skimage import measure, filters
from scipy.spatial.distance import cdist
H=float(sys.argv[1]) if len(sys.argv)>1 else 36.0
T_FRONT,T_BACK,HOLE_D,WALL=2.1,2.1,1.2,1.5   # 4.2 thick: side channel D1.2 + 1.5 walls
im=filters.gaussian(np.asarray(Image.open('letter-i/ref/reference.png').convert('L')).astype(float),1.5,preserve_range=True)
lab=measure.label(im<90); regs=[r for r in measure.regionprops(lab) if r.area>300 and r.bbox[1]>50]   # skip the neighbouring O
regs.sort(key=lambda r:r.bbox[0]); y0=min(r.bbox[0] for r in regs); y1=max(r.bbox[2] for r in regs); s=H/(y1-y0)
cx=np.mean([r.centroid[1] for r in regs if r.area>20000])
def outline(r):
    m=np.pad(lab==r.label,2); c=max(measure.find_contours(m.astype(float),0.5),key=len)
    k=9; c=c[:-1]; c=np.array([np.convolve(np.r_[c[-k:,i],c[:,i],c[:k,i]],np.ones(2*k+1)/(2*k+1),'valid') for i in (0,1)]).T
    c=measure.approximate_polygon(np.vstack([c,c[:1]]),0.6)[:-1]
    return [((x-2-cx)*s,(y1-(y-2))*s) for y,x in c]
f1,f2,stem=[outline(r) for r in regs]
def ext(pts,z0,t): return cq.Workplane().polyline(pts).close().extrude(t).translate((0,0,z0))
glyph=lambda z0,t: ext(stem,z0,t).union(ext(f1,z0,t)).union(ext(f2,z0,t))
# hole: midpoint of the closest pair between the two flames
A,B=np.array(f1),np.array(f2); d=cdist(A,B); i,j=np.unravel_index(d.argmin(),d.shape); hx,hy=(A[i]+B[j])/2
R=1.2   # back-side bridge disc joining the two flames
# bridge: lower flame -> top of stem, at the closest pair
S=np.array(stem); d2=cdist(B,S); k,l=np.unravel_index(d2.argmin(),d2.shape); p,q=B[k],S[l]
n=np.array([-(q-p)[1],(q-p)[0]]); n=n/np.linalg.norm(n)*0.9
bridge=[tuple(p+n),tuple(q+n),tuple(q-n),tuple(p-n)]
p=(p+(np.mean(B,0)-p)*0.3); q=q-(np.array([q[0],q[1]])-np.mean(S[S[:,1]>S[:,1].max()-2],0))*0.0
bridge=[tuple(B[k]+n+(np.mean(B,0)-B[k])*0.25),tuple(S[l]+n+np.array([0,-0.6])),tuple(S[l]-n+np.array([0,-0.6])),tuple(B[k]-n+(np.mean(B,0)-B[k])*0.25)]
back=glyph(0,T_BACK).union(cq.Workplane().center(hx,hy).circle(R).extrude(T_BACK)).union(ext(bridge,0,T_BACK))
body=back.union(glyph(T_BACK,T_FRONT)).cut(cq.Workplane().add(cq.Solid.makeCylinder(HOLE_D/2,40,cq.Vector(-20,hy,T_BACK),cq.Vector(1,0,0))))   # horizontal, side-to-side through both flames
v=body.val(); bb=v.BoundingBox()
print('і %.1f x %.1f x %.1f mm | hole D%.1f | gap flame-stem %.2f mm | steel %.2f g | solids %d'%(bb.xlen,bb.ylen,bb.zlen,HOLE_D,d2.min(),v.Volume()*7.9/1000,len(v.Solids())))
o='letter-i/out/letter-i-pendant'
cq.exporters.export(body,o+'.step'); cq.exporters.export(body,o+'.stl',tolerance=0.005)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,(a1,a2)=plt.subplots(1,2,figsize=(5,6),dpi=160)
for ax,ttl,back_on in ((a1,'Лице',False),(a2,'Зворот',True)):
    if back_on: ax.fill(*zip(*bridge),color='#888'); ax.add_patch(plt.Circle((hx,hy),R,color='#888'))
    [ax.fill(*zip(*g),color='#222') for g in (stem,f1,f2)]
    ax.axhline(hy,color='#3c3',lw=1.2,ls='--'); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(ttl,fontsize=8)
fig.suptitle('%.0f × %.0f × %.0f мм · канал Ø%.1f збоку (пунктир)'%(bb.xlen,bb.ylen,bb.zlen,HOLE_D),fontsize=8)
plt.savefig(o+'.png',bbox_inches='tight')
