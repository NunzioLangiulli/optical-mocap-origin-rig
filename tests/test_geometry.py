# SPDX-License-Identifier: MIT
"""Regression tests for exported geometry and critical solid/void locations."""
import sys,unittest
from pathlib import Path
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import origin_rig as rig

class GeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solid=rig.models()['origin_rig_v7']

    def material_at(self,xyz):
        probe=rig.box((.1,.1,.1),np.array(xyz)-.05)
        return (self.solid ^ probe).volume()>.0009

    def test_printable_exports_and_bounds(self):
        expected={'origin_rig_v7':[191,174,174],'roof_coupon_60deg':[24,18,12],'thread_coupon_quarter_20':[12,12,12]}
        for name,size in expected.items():
            m=trimesh.load_mesh(ROOT/'models'/(name+'.stl'))
            rig.mesh_metrics(m)
            np.testing.assert_allclose(m.extents,size,atol=.001)

    def test_marker_faces_and_axes(self):
        vectors=rig.PAD_CENTRES[1:]-rig.PAD_CENTRES[0]
        np.testing.assert_allclose(vectors@vectors.T,np.eye(3)*150**2)
        for x,y,z in rig.ALL_PAD_CENTRES:
            self.assertTrue(self.material_at((x,y,z-.15)))
            self.assertFalse(self.material_at((x,y,z+.15)))
        for x,y in [(0,0),(150,0),(0,150),(100,0)]:
            for z in [17,20,23]:
                self.assertTrue(self.material_at((x+8.8,y,z)))

    def test_channels_are_open_and_top_pad_is_backed(self):
        for p in [(70,0,2),(0,70,2),(-31,0,80),(-24,0,80),(0,0,5)]:
            self.assertFalse(self.material_at(p))
        for p in [(70,0,11),(0,70,11),(150,5,6),(5,150,6),(-17,0,80),(0,8.8,173.1)]:
            self.assertTrue(self.material_at(p))

    def test_intermediate_pad_and_motive_triangle(self):
        np.testing.assert_allclose(rig.INTERMEDIATE_PAD, [100,0,24])
        o=rig.PAD_CENTRES[0]
        a=rig.INTERMEDIATE_PAD-o
        b=rig.PAD_CENTRES[2]-o
        self.assertEqual(float(a@b),0.)
        np.testing.assert_allclose([np.linalg.norm(a),np.linalg.norm(b)],[100,150])
        # New pedestal is backed by the existing roof; underside stays open.
        self.assertTrue(self.material_at((100,0,11)))
        self.assertFalse(self.material_at((100,0,2)))
        # The extra support has no wider cap or lateral overhang.
        self.assertFalse(self.material_at((100,9.2,20)))

    def test_source_matches_released_geometry(self):
        reference=trimesh.load_mesh(ROOT/'models'/'origin_rig_v7.stl')
        rebuilt=rig.cleaned_mesh(self.solid)
        np.testing.assert_allclose(rebuilt.bounds,reference.bounds,atol=.001)
        # Boolean reordering can change triangulation under the 0.02-mm simplifier.
        # Compare geometry within explicit tolerances, not binary STL identity.
        self.assertLess(abs(rebuilt.volume-reference.volume),10.)  # < 0.01 cm3
        # Symmetric difference detects shape changes that preserve the volume.
        m=rig.md.Manifold(rig.md.Mesh(np.asarray(reference.vertices,dtype=np.float32),np.asarray(reference.faces,dtype=np.uint32)))
        delta=(self.solid-m).volume()+(m-self.solid).volume()
        self.assertLess(delta,30.)  # < 0.03 cm3; STL simplification tolerance is 0.02 mm

if __name__=='__main__': unittest.main()
