"""Raster -> vector shapes (outer + holes) -> SVG / CadQuery. Shared by letter builds."""
import numpy as np, cadquery as cq
from PIL import Image
from skimage import measure, filters, morphology
from scipy import ndimage

def red_mask(path, thr=60, sigma=1.2):
    a=np.asarray(Image.open(path).convert('RGB')).astype(float)
    m=(a[...,0]-a[...,1])>thr
    m=filters.gaussian(m.astype(float),sigma)>0.5
    return morphology.remove_small_objects(m,max_size=200)

def _smooth(c,k):
    c=c[:-1]
    if len(c)<4*k: return c
    sm=np.array([np.convolve(np.r_[c[-k:,i],c[:,i],c[:k,i]],np.ones(2*k+1)/(2*k+1),'valid') for i in (0,1)]).T
    return measure.approximate_polygon(np.vstack([sm,sm[:1]]),0.5)[:-1]

def shapes(mask, k=4, min_hole=60):
    """returns [(outer_px, [hole_px,...])] in (x,y) image px"""
    out=[]; lab,n=ndimage.label(mask)
    for i in range(1,n+1):
        comp=np.pad(lab==i,2); filled=ndimage.binary_fill_holes(comp)
        outer=max(measure.find_contours(filled.astype(float),0.5),key=len)
        holes=[]; hl,hn=ndimage.label(filled&~comp)
        for j in range(1,hn+1):
            h=hl==j
            if h.sum()<min_hole: continue
            holes.append(max(measure.find_contours(np.pad(h,1).astype(float),0.5),key=len)-1)
        f=lambda c:[(x-2,y-2) for y,x in _smooth(c,k)]
        out.append((f(outer),[f(h) for h in holes]))
    return out

def to_mm(sh, s, x0, y1):
    T=lambda pts:[((x-x0)*s,(y1-y)*s) for x,y in pts]
    return [(T(o),[T(h) for h in hs]) for o,hs in sh]

def solid(sh_mm, z0, t):
    body=None
    for o,hs in sh_mm:
        w=cq.Workplane().polyline(o).close().extrude(t)
        for h in hs:
            if len(h)>=3: w=w.cut(cq.Workplane().polyline(h).close().extrude(t))
        body=w if body is None else body.union(w)
    return body.translate((0,0,z0))

def svg(sh_mm, path, fill='#111'):
    xs=[p[0] for o,_ in sh_mm for p in o]; ys=[p[1] for o,_ in sh_mm for p in o]
    X0,X1,Y0,Y1=min(xs),max(xs),min(ys),max(ys)
    d=lambda pts:'M'+' L'.join('%.3f %.3f'%(x-X0,Y1-y) for x,y in pts)+' Z'
    paths=''.join('<path fill-rule="evenodd" d="%s"/>'%(' '.join([d(o)]+[d(h) for h in hs])) for o,hs in sh_mm)
    open(path,'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="%.2fmm" height="%.2fmm" viewBox="0 0 %.3f %.3f" fill="%s">%s</svg>'%(X1-X0,Y1-Y0,X1-X0,Y1-Y0,fill,paths))
