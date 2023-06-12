bl_info = {
    "name": "Mesh Stats Overlay",
    "author": "Avereniect",
    "location": "View 3D > Viewport Overlays > Mesh Statistics",
    "version": (1, 3, 0),
    "blender": (2, 80, 0),
    "description": "Adds a viewport overlay which displays object's vertex, edge, triangle, and face counts",
    "category": "3D View",
}

if "bpy" in locals():
    import importlib
    importlib.reload(mesh_stats_overlay)
else:
    from .  import mesh_stats_overlay

import bpy

def register():
    mesh_stats_overlay.register()

def unregister():
    mesh_stats_overlay.unregister()
