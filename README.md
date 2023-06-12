# Mesh Statistics Overlay
This Blender add-on is meant to make it easy to check the number of vertices,
edges, triangles, and/or faces that each individual object in your scene has.

The add-on support Blender 2.80. - 3.5.x

![The ](https://i.imgur.com/ApXsZT6.png)

## Usage
The add-on's functionality is found from the 3D Viewport Overlay's menu in the
Mesh statistics section.  

## Viewport Settings
* **Unevaluated** - Shows mesh statistics for the raw mesh
* **Evaluated** - Shows mesh statistics for the mesh with modifiers applied
* **Selected Only** - Shows mesh statistics only for selected objects instead of
  all objects  

One of **Unevaluated** should be **Evaluated** enabled for the following
settings to be enabled.

* **Vertex count** - Display the number of vertices in the mesh
* **Edge count** - Display the number of edges in the mesh
* **Triangle count** - Display the number of triangles in the mesh
* **Face count** - Display the number of faces in the mesh

## Add-on Preferences
* **Font size** - Size of font used to draw overlays
* **Font color** - Color of font used to draw overlays
* **Enable suffixes** - Display a one-letter suffix after count overlays to
  indicate which primitive the number corresponds to.

## Building
Compress the src directory to a `.zip` file to build the add-on. The `pack.sh`
script makes this convenient for *nix systems.
