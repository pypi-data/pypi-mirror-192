import sys
sys.path.append(r"D:\OneDriveCardiffUniversity\OneDrive - Cardiff University\TopologicPy")
import topologicpy
#from topologicpy import TPVertex
import topologic
tpv = topologicpy.TPVertex
from topologicpy.TPVertex import TPVertex
v = TPVertex(10,20,30)
print("Success 1", v)
print("Success 2", dir(v))
print("Success 3", v.X, v.Y, v.Z, v.Vertex)
