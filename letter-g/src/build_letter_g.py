"""Geometric «G» (2025) pendant traced from letter-g/ref/reference.png, crisp straight edges.
Bail like the Shryftoriz pendant: half-cylinder fused on the back of the top bar, bore side-to-side, invisible from the front. usage: build_letter_g.py HEIGHT_MM"""
import sys; sys.path.insert(0,'tools')
import numpy as np, cadquery as cq
from PIL import Image
from scipy import ndimage
from skimage import measure
H=float(sys.argv[1]) if len(sys.argv)>1 else 26.0
T,HOLE_D,WALL,INSET=2.0,1.8,1.5,0.4
a=np.asarray(Image.open('letter-g/ref/reference.png').convert('L'))
m=a<110; m[:40]=False                                    # drop the «2025» caption
lab,n=ndimage.label(m); m=lab==(np.argmax(ndimage.sum(m,lab,range(1,n+1)))+1)
ys,xs=np.nonzero(m); s=H/(ys.max()-ys.min()+1); x0,y1=xs.min(),ys.max()
filled=ndimage.binary_fill_holes(m)
c=max(measure.find_contours(np.pad(filled,2).astype(float),0.5),key=len)
c=measure.approximate_polygon(c,1.6)[:-1]                # straight-edged glyph -> few vertices
outer=[((x-2-x0)*s,(y1-(y-2))*s) for y,x in c]
body=cq.Workplane().polyline(outer).close().extrude(T)
# bail on the back (z<0): half-cylinder + block up to the plate, bore D1.8, walls 1.5 (as pendant/src/build_pendant.py)
RI=HOLE_D/2; R=RI+WALL; ZC=-RI; top=max(p[1] for p in outer); YC=top-0.25-R
xl,xr=[],[]
for i in range(21):
    yy=YC-R+2*R*i/20; row=np.nonzero(m[int(round(y1-yy/s))])[0]; xl.append((row.min()-x0)*s); xr.append((row.max()-x0)*s)
BAIL_L=5.0; cx=body.val().Center().x                     # short bail centred over the centre of mass -> hangs straight
X0,X1=max(max(xl)+INSET,cx-BAIL_L/2),min(min(xr)-INSET,cx+BAIL_L/2); L=X1-X0
bail=cq.Workplane('YZ').workplane(offset=X0).center(YC,ZC).circle(R).extrude(L).union(cq.Workplane().box(L,2*R,-ZC+0.01,centered=False).translate((X0,YC-R,ZC)))
bail=bail.intersect(cq.Workplane().box(60,60,30,centered=(True,True,False)).translate((20,20,-30+0.001)))   # keep only the back half-space
body=body.union(bail).cut(cq.Workplane('YZ').workplane(offset=X0-1).center(YC,ZC).circle(RI).extrude(L+2))
hy=YC; W=(xs.max()-xs.min())*s
v=body.val(); bb=v.BoundingBox()
c=v.Center(); print('CoM x %.2f vs bail centre %.2f |'%(c.x,(X0+X1)/2),end=' '); print('G %.1f x %.1f x %.1f mm | %d vertices | bail L %.1f, bore D%.1f at y=%.1f | steel %.2f g | solids %d'%(bb.xlen,bb.ylen,bb.zlen,len(outer),L,HOLE_D,hy,v.Volume()*7.9/1000,len(v.Solids())))
o='letter-g/out/letter-g-pendant'
cq.exporters.export(body,o+'.step'); cq.exporters.export(body,o+'.stl',tolerance=0.005)
xs_,ys_=zip(*outer); X0,Y1=min(xs_),max(ys_)
open(o+'.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" width="%.2fmm" height="%.2fmm" viewBox="0 0 %.3f %.3f"><path d="M%s Z"/></svg>'%(bb.xlen,bb.ylen,bb.xlen,bb.ylen,' L'.join('%.3f %.3f'%(x-X0,Y1-y) for x,y in outer)))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(3.5,4),dpi=150); ax.fill(xs_,ys_,color='#1d1d1d')
ax.plot([X0,X1],[hy,hy],color='#3c3',lw=1.2,ls='--'); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('%.0f × %.0f × %.1f мм · вушко ззаду, отвір Ø%.1f'%(bb.xlen,bb.ylen,T,HOLE_D),fontsize=8); plt.savefig(o+'.png',bbox_inches='tight')
