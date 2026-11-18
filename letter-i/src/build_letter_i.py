"""Letter «і» pendant: serif stem + dot drawn as two flame tongues.
One printable piece: front layer = the letter (flames read as separate), back layer bridges flames to each other and to the stem.
Chain hole goes front-to-back through the flame pair. usage: build_letter_i.py HEIGHT_MM"""
import sys, math, cadquery as cq
H=float(sys.argv[1]) if len(sys.argv)>1 else 36.0
s=H/750.0                                   # reference px (y 45..795) -> mm
T_FRONT,T_BACK=1.5,1.5                      # total 3.0 mm
HOLE_D=1.6
def P(x,y): return (x*s,(795-y)*s)          # px -> mm, y up, base at 0
def flame(cx,cy,L,T,ang):
    """crescent tongue: band along a smile-shaped arc, pointed left tip, blunt right end"""
    pts_top,pts_bot=[],[]
    for i in range(41):
        u=i/40; x=(u-0.5)*L; sag=0.35*T*(2*u-1)**2
        w=T*(0.25+0.75*math.sin(math.pi*min(1,u*1.6)/2))   # tapered left tip
        pts_top.append((x,sag+w/2)); pts_bot.append((x,sag-w/2-0.25*T*(1-(2*u-1)**2)))
    loop=pts_top+pts_bot[::-1]; c,sn=math.cos(ang),math.sin(ang)
    return [P(cx+x*c-y*sn, cy-(x*sn+y*c)) for x,y in loop]
ANG=math.radians(-38)                        # higher on the left, like the reference
f1=flame(178,90,128,46,ANG); f2=flame(148,185,120,44,ANG)
stem=[P(120,262),P(205,262),P(205,772),P(120,772)]
sTop=[P(95,255),P(228,255),P(228,288),P(205,300),P(120,300),P(95,288)]
sBot=[P(118,745),P(205,745),P(245,775),P(245,795),P(100,795),P(100,775)]
def ext(pts,z0,t): return cq.Workplane().polyline(pts).close().extrude(t).translate((0,0,z0))
front=ext(stem,T_BACK,T_FRONT).union(ext(sTop,T_BACK,T_FRONT)).union(ext(sBot,T_BACK,T_FRONT)).union(ext(f1,T_BACK,T_FRONT)).union(ext(f2,T_BACK,T_FRONT))
# back layer: same letter plus a bridge (convex hull of flames + top serif) so everything is one piece
c1=(sum(p[0] for p in f1)/len(f1),sum(p[1] for p in f1)/len(f1)); c2=(sum(p[0] for p in f2)/len(f2),sum(p[1] for p in f2)/len(f2))
hx,hy=(c1[0]+c2[0])/2,(c1[1]+c2[1])/2          # hole sits in the gap, cutting into both flames
disc=cq.Workplane().center(hx,hy).circle(HOLE_D/2+1.5).extrude(T_BACK)
lo=min(p[1] for p in f2); bridge=[(hx-0.9,sTop[0][1]-0.2),(hx+0.9,sTop[0][1]-0.2),(c2[0]+0.9,c2[1]),(c2[0]-0.9,c2[1])]
hull=[(hx+(HOLE_D/2+1.5)*math.cos(a/20*math.pi*2),hy+(HOLE_D/2+1.5)*math.sin(a/20*math.pi*2)) for a in range(20)]
back=disc.union(ext(bridge,0,T_BACK)).union(ext(f1,0,T_BACK)).union(ext(f2,0,T_BACK)).union(ext(stem,0,T_BACK)).union(ext(sTop,0,T_BACK)).union(ext(sBot,0,T_BACK))
hole=cq.Workplane().center(hx,hy).circle(HOLE_D/2).extrude(10).translate((0,0,-1))
body=back.union(front).cut(hole)
v=body.val(); bb=v.BoundingBox()
print('і %.1f x %.1f x %.1f mm | hole D%.1f at (%.1f,%.1f) | steel %.2f g | solids %d'%(bb.xlen,bb.ylen,bb.zlen,HOLE_D,hx,hy,v.Volume()*7.9/1000,len(v.Solids())))
n='letter-i/out/letter-i-pendant'
cq.exporters.export(body,n+'.step'); cq.exporters.export(body,n+'.stl',tolerance=0.005)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(3,6),dpi=160)
ax.fill(*zip(*hull),color='#888'); [ax.fill(*zip(*p),color='#222') for p in (stem,sTop,sBot,f1,f2)]
ax.fill(*zip(*bridge),color='#888');ax.fill(*zip(*hull),color='#888');[ax.fill(*zip(*p),color='#222') for p in (f1,f2)];ax.add_patch(plt.Circle((hx,hy),HOLE_D/2,color='white'));ax.set_aspect('equal');ax.axis('off')
ax.set_title('%.0f × %.0f × %.0f мм · отвір Ø%.1f'%(bb.xlen,bb.ylen,bb.zlen,HOLE_D),fontsize=8)
plt.savefig(n+'.png',bbox_inches='tight')
