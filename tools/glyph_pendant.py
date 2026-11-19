"""Generic letter pendant from a reference image: trace glyph (with counters), flat face, and a short
Shryftoriz-style bail on the back (half-cylinder, bore side-to-side) centred over the centre of mass.
usage: glyph_pendant.py NAME MODE X0 Y0 X1 Y1 HEIGHT_MM [CLOSE_PX] [SMOOTH]
MODE: red | dark | ink (anything not near-white/blue background)"""
import sys; sys.path.insert(0,'tools')
import numpy as np, cadquery as cq, trace as tr
from PIL import Image
from scipy import ndimage
from skimage import morphology
name,mode=sys.argv[1],sys.argv[2]; X0,Y0,X1,Y1=map(int,sys.argv[3:7]); H=float(sys.argv[7])
CLOSE=int(sys.argv[8]) if len(sys.argv)>8 else 0; K=int(sys.argv[9]) if len(sys.argv)>9 else 3; CONVEX=len(sys.argv)>10 and sys.argv[10]=='convex'
T,HOLE_D,WALL,BAIL_L,INSET=2.0,1.8,1.5,5.0,0.4
a=np.asarray(Image.open(f'{name}/ref/reference.png').convert('RGB')).astype(int)[Y0:Y1,X0:X1]
R_,G_,B_=a[...,0],a[...,1],a[...,2]
m={'red':(R_-G_>70)&(R_>150),'dark':a.mean(-1)<110,'ink':(a.mean(-1)<200)&~((B_>R_+30))}[mode]
if CLOSE: m=morphology.binary_closing(m,morphology.disk(CLOSE))
m=morphology.remove_small_holes(m,max_size=400)
lab,n=ndimage.label(m); m=lab==(np.argmax(ndimage.sum(m,lab,range(1,n+1)))+1)
if CONVEX:   # round letters: clean convex outline (drops texture bumps / UI overlaps), keep the counters
    holes=ndimage.binary_fill_holes(m)&~m; holes=morphology.remove_small_objects(holes,max_size=400)
    m=morphology.convex_hull_image(m)&~morphology.binary_erosion(holes,morphology.disk(0))
ys,xs=np.nonzero(m); s=H/(ys.max()-ys.min()+1); x0,y1=xs.min(),ys.max()
sh=tr.to_mm(tr.shapes(m,k=K),s,x0,y1); body=tr.solid(sh,0,T)
cx=body.val().Center().x; col=int(round(cx/s+x0))
run=np.nonzero(m[:,col])[0]; top=run.min(); seg=top
while seg+1<m.shape[0] and m[seg+1,col]: seg+=1
solid_mm=(seg-top+1)*s
RI=HOLE_D/2; R=RI+WALL; ZC=-RI
top_mm=(y1-top)*s; YC=top_mm-0.25-R

xl,xr=[],[]
for i in range(21):
    r=int(round(y1-(YC-R+2*R*i/20)/s)); row=m[r]
    if True:
        nz=np.nonzero(row)[0]
        if len(nz): xl.append((nz.min()-x0)*s); xr.append((nz.max()-x0)*s)
        continue
    if True:
        l=col
        while l>0 and row[l-1]: l-=1
        rr=col
        while rr<len(row)-1 and row[rr+1]: rr+=1
        xl.append((l-x0)*s); xr.append((rr-x0)*s)
bx0,bx1=max(max(xl)+INSET,cx-BAIL_L/2),min(min(xr)-INSET,cx+BAIL_L/2); L=bx1-bx0
bail=cq.Workplane('YZ').workplane(offset=bx0).center(YC,ZC).circle(R).extrude(L).union(cq.Workplane().box(L,2*R,-ZC+0.01,centered=False).translate((bx0,YC-R,ZC)))
bail=bail.intersect(cq.Workplane().box(200,200,30,centered=(True,True,False)).translate((50,50,-30+0.001)))
body=body.union(bail).cut(cq.Workplane('YZ').workplane(offset=bx0-1).center(YC,ZC).circle(RI).extrude(L+2))
v=body.val(); bb=v.BoundingBox()
print('%s %.1f x %.1f x %.1f mm | top stroke %.1f mm | bail L %.1f at x %.1f (CoM %.1f) | steel %.2f g | solids %d'%(name,bb.xlen,bb.ylen,bb.zlen,solid_mm,L,(bx0+bx1)/2,cx,v.Volume()*7.9/1000,len(v.Solids())))
o=f'{name}/out/{name}-pendant'
cq.exporters.export(body,o+'.step'); cq.exporters.export(body,o+'.stl',tolerance=0.005); tr.svg(sh,o+'.svg')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(3.5,4),dpi=150)
for ol,hs in sh: ax.fill(*zip(*ol),color='#1d1d1d'); [ax.fill(*zip(*h),color='white') for h in hs]
ax.add_patch(plt.Rectangle((bx0,YC-R),L,2*R,fill=False,ec='#3c3',ls='--')); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('%.0f × %.0f × %.0f мм · вушко ззаду Ø%.1f'%(bb.xlen,bb.ylen,T,HOLE_D),fontsize=8); plt.savefig(o+'.png',bbox_inches='tight')
