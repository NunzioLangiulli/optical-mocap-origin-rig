# SPDX-License-Identifier: MIT
"""Orthographic preview of the exact released STL, with illustrative markers."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont

def render(mesh, path, az=43,el=29, markers=True, version='v3'):
    import trimesh
    meshes=[mesh]; colors=[(103,114,130)]
    if markers:
        for xyz,c in [((0,0,30),(180,180,180)),((150,0,30),(220,50,50)),((0,150,30),(40,160,90)),((0,0,180),(40,110,220)),((100,0,30),(220,150,30))]:
            sphere=trimesh.creation.icosphere(subdivisions=3,radius=6)
            sphere.apply_translation(xyz); meshes.append(sphere); colors.append(c)
    az,el=np.radians([az,el]); view=np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])
    right=np.array([-np.sin(az),np.cos(az),0]); up=np.cross(view,right)
    transform=np.stack([right,up,view],axis=1)
    allverts=np.concatenate([m.vertices for m in meshes])@transform
    lo=allverts[:,:2].min(axis=0); hi=allverts[:,:2].max(axis=0)
    W,H=1400,1300; scale=min(1180/(hi[0]-lo[0]),980/(hi[1]-lo[1]))
    center=(lo+hi)/2
    canvas=np.full((H,W,3),(245,246,248),dtype=np.uint8)
    depth=np.full((H,W),-np.inf,dtype=np.float32)
    light=(view*.7+up*.7+right*.2); light/=np.linalg.norm(light)
    for m,color in zip(meshes,colors):
        vertices=m.vertices@transform
        vertices[:,0]=(vertices[:,0]-center[0])*scale+W/2
        vertices[:,1]=-(vertices[:,1]-center[1])*scale+H/2+15
        shades=np.clip(.50+.50*np.maximum(0,m.face_normals@light),.25,1)
        for face,shade in zip(m.faces,shades):
            p=vertices[face]; x0,y0=np.maximum(np.floor(p[:,:2].min(axis=0)).astype(int),0)
            x1,y1=np.minimum(np.ceil(p[:,:2].max(axis=0)).astype(int),[W-1,H-1])
            den=(p[1,1]-p[2,1])*(p[0,0]-p[2,0])+(p[2,0]-p[1,0])*(p[0,1]-p[2,1])
            if abs(den)<1e-9 or x1<x0 or y1<y0: continue
            yy,xx=np.mgrid[y0:y1+1,x0:x1+1]; xx=xx+.5; yy=yy+.5
            a=((p[1,1]-p[2,1])*(xx-p[2,0])+(p[2,0]-p[1,0])*(yy-p[2,1]))/den
            c=((p[2,1]-p[0,1])*(xx-p[2,0])+(p[0,0]-p[2,0])*(yy-p[2,1]))/den
            d=1-a-c; z=a*p[0,2]+c*p[1,2]+d*p[2,2]
            old=depth[y0:y1+1,x0:x1+1]
            mask=(a>=-1e-6)&(c>=-1e-6)&(d>=-1e-6)&(z>old)
            old[mask]=z[mask]; canvas[y0:y1+1,x0:x1+1][mask]=(np.array(color)*shade).astype(np.uint8)
    im=Image.fromarray(canvas); draw=ImageDraw.Draw(im)
    font=ImageFont.load_default(size=24)
    title=ImageFont.load_default(size=36)
    if markers:
        for xyz,label in [((0,0,30),'O'),((150,0,30),'X'),((0,150,30),'Y'),((0,0,180),'Z'),((100,0,30),'M100')]:
            projected=np.asarray(xyz)@transform
            x=(projected[0]-center[0])*scale+W/2+25
            y=-(projected[1]-center[1])*scale+H/2-25
            draw.text((x,y),label,font=title,fill='#182333',stroke_width=1,stroke_fill='#f5f6f8')
    def text(y,value,font=font): draw.text((W/2,y),value,font=font,fill='#252b33',anchor='mt')
    text(30,'OPTICAL MOCAP ORIGIN RIG '+version+' | '+('TOP VIEW' if markers else 'UNDERSIDE AND REAR'),title)
    text(90,'Downward X/Y channels | Rear-facing Z channel | Cylindrical marker supports')
    text(1210,'O-X / O-Y / O-Z: 150 mm | O-M100: 100 mm | 1/4-20 UNC')
    text(1250,'All five sites illustrated; use the marker subset for your system. Untested print.')
    im.save(path)

if __name__=='__main__':
    import trimesh
    root=Path(__file__).resolve().parents[1]
    out=root/'docs'/'images'; out.mkdir(parents=True,exist_ok=True)
    mesh=trimesh.load_mesh(root/'models'/'origin_rig_v7.stl')
    render(mesh,out/'origin-rig-v7.png',version='v7')
    render(mesh,out/'underside-and-rear.png',az=220,el=-24,markers=False,version='v7')
