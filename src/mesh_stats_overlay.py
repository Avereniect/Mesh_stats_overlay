import bpy
import bpy_extras
import blf

from bpy.types import ThemePreferences, Operator, AddonPreferences
from mathutils import Vector
from bpy_extras import view3d_utils

# =========================================================
# Preferences
# =========================================================

class Mesh_stats_overlay_preferences(AddonPreferences):
    bl_idname = __package__

    font_size: bpy.props.IntProperty(
        name='Font size',
        default=12
    )

    font_color: bpy.props.FloatVectorProperty(
        name='Font color',
        default=(0.9, 0.9, 0.9),
        min=0.0,
        max=1.0,
        precision = 2,
        subtype='COLOR'
    )

    enable_suffixes: bpy.props.BoolProperty(
        name='Enable suffixes',
        default=True,
        description='Display a one-letter suffix (v, e, t, or f) after counts.'
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, 'font_size')
        layout.prop(self, 'font_color')
        layout.prop(self, 'enable_suffixes')

def register_preferences():
    bpy.utils.register_class(Mesh_stats_overlay_preferences)

def unregister_preferences():
    bpy.utils.unregister_class(Mesh_stats_overlay_preferences)

# =========================================================
# Memory Consumption Overlay
# =========================================================

def attribute_size():
    # TODO: Implement
    pass

#def estimate_memory_usagse_as_vertex_array(mesh: bpy.types.Mesh):
#    triangle_count = len(mesh.loop_triangles)
#    vertex_count = len(mesh.vertices)
#
#    index_count = 3 *  triangle_count # 3 indices per triangle
#    index_array_size = index_count * 4 # 4 bytes per 32-bit index
#
#    attribute_arrays_size = 0
#
#    for attrib in mesh.attributes:
#        # TODO: Complete
#        attribute_array_size = 
#
#        attribute_arrays_size +=
#
#    return index_array_size + attribute_arrays_size

# =========================================================
# Primitive Count Overlay
# =========================================================

def get_text_dimensions(text, font_size, font_id):
	if (bpy.app.version < (3, 4, 0)):
    	blf.size(font_id, font_size, 72)
	else:
    	blf.size(font_id, font_size)
	
	
    return blf.dimensions(font_id, text)

def draw_text(location, text):
    if text is None:
        return

    coords_2d = view3d_utils.location_3d_to_region_2d(bpy.context.region, bpy.context.space_data.region_3d, location)

    font_id = 0
    font_size = bpy.context.preferences.addons[__package__].preferences.font_size
    font_color = bpy.context.preferences.addons[__package__].preferences.font_color

    coords_2d[0] -= get_text_dimensions(text, font_size, font_id)[0] // 2
    coords_2d[1] += int(get_text_dimensions(text, font_size, font_id)[1] * 0.4)

    blf.position(font_id, coords_2d[0], coords_2d[1], 0.0)

	if (bpy.app.version < (3, 4, 0)):
    	blf.size(font_id, font_size, 72)
	else:
    	blf.size(font_id, font_size)

    blf.color(font_id, *font_color, 1.0)
    #blf.enable(font_id, blf.SHADOW)
    #blf.shadow(font_id, 5, 0.0, 0.0, 0.0, 1.0)
    #blf.shadow_offset(font_id, 1, -1)
    blf.draw(font_id, text)
    
def construct_overlay_text(obj):
    U = bpy.context.scene.is_unevaluated_mesh_overlay_enabled
    E = bpy.context.scene.is_evaluated_mesh_overlay_enabled
    
    v = bpy.context.scene.is_vertex_count_overlay_enabled
    e = bpy.context.scene.is_edge_count_overlay_enabled
    t = bpy.context.scene.is_triangle_count_overlay_enabled
    f = bpy.context.scene.is_face_count_overlay_enabled

    if not (v or e or t or f):
        return ''
    
    ret = []

    ctx = bpy.context

    suffixes_enabled = bpy.context.preferences.addons[__package__].preferences.enable_suffixes

    if U:
        tmp = []
        if v:
            tmp.append(str(len(obj.data.vertices)) + 'v' * suffixes_enabled)

        if e:
            tmp.append(str(len(obj.data.edges)) + 'e' * suffixes_enabled)

        if t:
            tmp.append(str(len(obj.data.loop_triangles)) + 't' * suffixes_enabled)

        if f:
            tmp.append(str(len(obj.data.polygons)) + 'f' * suffixes_enabled)

        ret.append(', '.join(tmp).rstrip(' '))

    if E:
        depsgraph = ctx.evaluated_depsgraph_get()
        
        obj_eval = obj.evaluated_get(depsgraph)

        tmp = []
        if v:
            tmp.append(str(len(obj_eval.data.vertices)) + 'v' * suffixes_enabled)

        if e:
            tmp.append(str(len(obj_eval.data.edges)) + 'e' * suffixes_enabled)

        if t:
            tmp.append(str(len(obj_eval.data.loop_triangles)) + 't' * suffixes_enabled)

        if f:
            tmp.append(str(len(obj_eval.data.polygons)) + 'f' * suffixes_enabled)

        ret.append(', '.join(tmp).rstrip(' '))

    return ' | '.join(ret).rstrip(' ')

def draw_callback(self):
    if not bpy.context.space_data.overlay.show_overlays:
        return

    if bpy.context.scene.is_selected_mesh_overlay_enabled:
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH' and obj.visible_get():
                draw_text(obj.location, construct_overlay_text(obj))
    else:
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and obj.visible_get():
                draw_text(obj.location, construct_overlay_text(obj))


draw_handler = None

def register_overlay_draw_handler():
    global draw_handler
    draw_handler = bpy.types.SpaceView3D.draw_handler_add(draw_callback, (None,), 'WINDOW', 'POST_PIXEL')

    # Immediately refresh the UI
    # bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

def unregister_overlay_draw_handler():
    global draw_handler
    if draw_handler is not None:
        bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')
        draw_handler = None

# =========================================================
# Menu entries
# =========================================================

def draw_ui_callback(self, context):

    if context.object.mode != 'OBJECT':
        return

    scene = context.scene

    layout = self.layout
    layout.label(text='Mesh statistics')
    columns = layout.row()
    
    l_column = columns.column()
    r_column = columns.column()

    l_column.prop(context.scene, 'is_unevaluated_mesh_overlay_enabled', text='Unevaluated')
    l_column.prop(context.scene, 'is_evaluated_mesh_overlay_enabled', text='Evaluated')
    l_column.label(text=' ')
    l_column.prop(context.scene, 'is_selected_mesh_overlay_enabled', text='Selcted Only')

    r_column.enabled = scene.is_unevaluated_mesh_overlay_enabled or scene.is_evaluated_mesh_overlay_enabled

    r_column.prop(context.scene, 'is_vertex_count_overlay_enabled', text='Vertex count')
    r_column.prop(context.scene, 'is_edge_count_overlay_enabled', text='Edge count')
    r_column.prop(context.scene, 'is_triangle_count_overlay_enabled', text='Triangle count')
    r_column.prop(context.scene, 'is_face_count_overlay_enabled', text='Face count')

def register_ui_callback():
    bpy.types.Scene.is_unevaluated_mesh_overlay_enabled = bpy.props.BoolProperty(description='Show statistics for raw mesh')
    bpy.types.Scene.is_evaluated_mesh_overlay_enabled = bpy.props.BoolProperty(description='Show statistics for mesh with modifiers applied')
    
    bpy.types.Scene.is_selected_mesh_overlay_enabled = bpy.props.BoolProperty(description='Show overlay for selected objects only', default=True)

    bpy.types.Scene.is_vertex_count_overlay_enabled = bpy.props.BoolProperty(description='Show vertex counts')
    bpy.types.Scene.is_edge_count_overlay_enabled = bpy.props.BoolProperty(description='Show edge counts')
    bpy.types.Scene.is_triangle_count_overlay_enabled = bpy.props.BoolProperty(description='Show triangle counts')
    bpy.types.Scene.is_face_count_overlay_enabled = bpy.props.BoolProperty(description='Show face counts')

    bpy.types.VIEW3D_PT_overlay_object.append(draw_ui_callback)

def unregister_ui_callback():
    bpy.types.VIEW3D_PT_overlay_object.remove(draw_ui_callback)

    del bpy.types.Scene.is_unevaluated_mesh_overlay_enabled
    del bpy.types.Scene.is_evaluated_mesh_overlay_enabled

    del bpy.types.Scene.is_selected_mesh_overlay_enabled

    del bpy.types.Scene.is_vertex_count_overlay_enabled
    del bpy.types.Scene.is_edge_count_overlay_enabled
    del bpy.types.Scene.is_triangle_count_overlay_enabled
    del bpy.types.Scene.is_face_count_overlay_enabled

# =========================================================
# Other
# =========================================================

def register():
    register_preferences()
    register_ui_callback()
    register_overlay_draw_handler()

def unregister():
    unregister_overlay_draw_handler()
    unregister_ui_callback()
    unregister_preferences()

