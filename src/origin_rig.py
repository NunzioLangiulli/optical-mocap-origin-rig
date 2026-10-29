# SPDX-License-Identifier: MIT
"""Standalone v7 CAD geometry. All coordinates and tolerances are millimetres."""
import math
import numpy as np
import manifold3d as md
import trimesh

DESIGN_REVISION = 'v7'
PAD_CENTRES = np.array([[0, 0, 24], [150, 0, 24], [0, 150, 24], [0, 0, 174]], float)
INTERMEDIATE_PAD = np.array([100, 0, 24], float)
ALL_PAD_CENTRES = np.vstack([PAD_CENTRES, INTERMEDIATE_PAD])
EXPECTED_BOUNDS = np.array([[-32, -15, 0], [159, 159, 174]], float)
ROOF_APEX = 1 + 5 * math.sqrt(3)
BRACKET_START = 171.2 - 25 * math.sqrt(3)

def box(size, pos):
    return md.Manifold.cube(size).translate(pos)

def cylinder(radius, height, pos, top_radius=None, segments=96):
    return md.Manifold.cylinder(height, radius, radius if top_radius is None else top_radius, segments).translate(pos)

def prism_yz(points, x0, x1):
    return md.Manifold.hull_points(np.array([[x,y,z] for x in (x0,x1) for y,z in points], float))

def marker_support(x, y):
    return cylinder(9, 12.2, (x,y,11.8))

def arm():
    body = box((150,18,12),(0,-9,0)) + cylinder(9,12,(150,0,0))
    channel = [(-5,-.2),(5,-.2),(5,1),(0,ROOF_APEX),(-5,1)]
    return body - prism_yz(channel,16,141) + marker_support(150,0)

def upper_arch(x0, x1, bottom):
    return prism_yz([(-5,bottom),(5,bottom),(5,171.2-5*math.sqrt(3)),(0,171.2),(-5,171.2-5*math.sqrt(3))],x0,x1)

def rig_body():
    body = cylinder(15,16,(0,0,0)) + box((32,16,8),(-32,-8,0))
    body += arm() + arm().rotate((0,0,90)) + marker_support(0,0) + marker_support(100,0)
    tower = box((16,16,171.2),(-32,-8,0)) - upper_arch(-32.2,-19,8)
    points=[]
    for z,xmax,half_y in [(BRACKET_START,-16,8),(171.2,9,9)]:
        points.extend([[x,y,z] for x in (-32,xmax) for y in (-half_y,half_y)])
    bracket=md.Manifold.hull_points(np.array(points,float))
    bracket += box((41,18,2),(-32,-9,171.2))
    bracket -= upper_arch(-33,10,BRACKET_START-.1)
    return body + tower + bracket + cylinder(9,.8,(0,0,173.2))

def thread_cut(clearance=0.20, depth=11.0):
    """Right-hand 1/4-20 UNC-inspired printed clearance profile, not a gauged thread.

    clearance is RADIAL; major and minor diameters increase by twice this value.
    The two 60-degree concepts (thread flank and roof slope) are independent.
    """
    if not 0 <= clearance <= 0.5:
        raise ValueError('Radial clearance must be between 0 and 0.5 mm.')
    pitch=25.4/20
    rmajor=6.35/2+clearance
    rminor=6.35/2-0.541266*pitch+clearance
    count=128
    zs=np.linspace(-.5,depth,int((depth+.5)/pitch*40)+1)
    vertices=[]
    for z in zs:
        for j in range(count):
            theta=j*2*math.pi/count
            q=((z/pitch-theta/(2*math.pi)+.5)%1)-.5
            fraction=np.clip((.4375-abs(q))/.3125,0,1)
            radius=rminor+fraction*(rmajor-rminor)
            vertices.append((radius*math.cos(theta),radius*math.sin(theta),z))
    faces=[]
    for k in range(len(zs)-1):
        for j in range(count):
            a=k*count+j; c=k*count+(j+1)%count
            faces.extend([(a,c,c+count),(a,c+count,a+count)])
    low=len(vertices); vertices.append((0,0,zs[0]))
    high=len(vertices); vertices.append((0,0,zs[-1]))
    for j in range(count):
        nxt=(j+1)%count
        faces.extend([(low,nxt,j),(high,(len(zs)-1)*count+j,(len(zs)-1)*count+nxt)])
    mesh=trimesh.Trimesh(vertices=vertices,faces=faces,process=True)
    if not (mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0):
        raise RuntimeError('Invalid thread cutting mesh.')
    solid=md.Manifold(md.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
    if solid.status()!=md.Error.NoError:
        raise RuntimeError(f'Thread conversion failed: {solid.status()}')
    return solid + cylinder(rmajor+.5,1,(0,0,-.1),top_radius=rminor)

def models(clearance=0.20):
    cut=thread_cut(clearance)
    return {
        'origin_rig_v7': rig_body()-cut,
        'roof_coupon_60deg': (arm() ^ box((24,20,14),(65,-10,-1))).translate((-65,0,0)),
        'thread_coupon_quarter_20': cylinder(6,12,(0,0,0))-cut,
    }

def cleaned_mesh(solid):
    raw=solid.simplify(.02).to_mesh()
    mesh=trimesh.Trimesh(vertices=np.asarray(raw.vert_properties)[:,:3],faces=raw.tri_verts,process=True)
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.remove_unreferenced_vertices()
    return mesh

def mesh_metrics(mesh):
    # Mesh-to-Manifold round trip checks actual exported connectivity.
    m=md.Manifold(md.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
    if m.status()!=md.Error.NoError:
        raise RuntimeError(f'Exported mesh is invalid: {m.status()}')
    metrics=dict(watertight=bool(mesh.is_watertight),consistent_normals=bool(mesh.is_winding_consistent),
        connected_components=len(m.decompose()),dimensions_mm=mesh.extents.tolist(),
        bounds_mm=mesh.bounds.tolist(),volume_cm3=float(mesh.volume/1000),triangles=len(mesh.faces))
    if not (metrics['watertight'] and metrics['consistent_normals'] and metrics['connected_components']==1 and mesh.volume>0):
        raise RuntimeError(f'Mesh validation failed: {metrics}')
    return metrics

def export_stl(solid,path):
    mesh=cleaned_mesh(solid)
    mesh_metrics(mesh)
    mesh.export(path)
    return mesh_metrics(trimesh.load_mesh(path))
