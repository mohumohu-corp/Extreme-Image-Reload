import bpy
import os

NONE = "none"
DISABLED = 0
ENABLED = 1
ANIMENABLED = 2

bl_info = {
    "name": "Extreme Image Reload",
    "author": "Yuta Ogasawara",
    "description": "",
    "blender": (3, 3, 0),
    "version": (1, 0, 0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}


class EIRHEADER_OT_toggle(bpy.types.Operator):
    bl_idname = "toggle.extreme_image_reload"
    bl_label = ""
    bl_description = "[Extreme Image Reload] Disable/Enabled/AnimEnabled"
    bl_options = {"REGISTER"}

    def execute(self, context):
        bpy.context.scene.eir_enabled = (1 + bpy.context.scene.eir_enabled) % 3
        return {"FINISHED"}


class UdimTimeStamp(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty(
        name='Timestamp', default=NONE)


class UdimTimeStamps(bpy.types.PropertyGroup):
    last_tile_count: bpy.props.IntProperty()
    timestamps: bpy.props.CollectionProperty(type=UdimTimeStamp)


def combine_udim_path(splitted_uidm_path, label):
    return splitted_uidm_path[0] + label + splitted_uidm_path[1]


def try_reload_udim(image):
    should_reload = False
    udimpath = image.filepath
    splitted = udimpath.split('<UDIM>')

    if len(splitted) != 2:
        return False

    timestamps = image.eir_udim_timestamps.timestamps
    current_tile_count = len(image.tiles)

    if image.eir_udim_timestamps.last_tile_count == current_tile_count:
        i = 0
        for tile in image.tiles:
            path = os.path.abspath(bpy.path.abspath(
                combine_udim_path(splitted, tile.label)))
            timestamp = timestamps[i]
            if os.path.isfile(path):
                current_time_stamp = str(os.path.getmtime(path))
                if timestamp.value != current_time_stamp:
                    should_reload = True
                timestamp.value = current_time_stamp
            else:
                timestamp.value = NONE
            i += 1
    else:
        should_reload = True
        timestamps.clear()
        for tile in image.tiles:
            timestamp = timestamps.add()
            path = os.path.abspath(bpy.path.abspath(
                combine_udim_path(splitted, tile.label)))
            if os.path.isfile(path):
                timestamp.value = str(os.path.getmtime(path))
            else:
                timestamp.value = NONE

    image.eir_udim_timestamps.last_tile_count = current_tile_count

    if should_reload:
        image.reload()
        return True

    return False


def try_reload(image):
    if image.library or image.packed_file:
        return False

    if image.source == 'TILED':
        return try_reload_udim(image)

    if image.source not in {'FILE', 'SEQUENCE'}:
        return False

    path = os.path.abspath(bpy.path.abspath(image.filepath))

    if not os.path.isfile(path):
        image.eir_last_update = NONE
        return False

    time_stamp = str(os.path.getmtime(path))

    if image.eir_last_update == time_stamp:
        return False

    image.eir_last_update = time_stamp
    image.reload()
    return True


def update_view():
    if bpy.context.scene.render.engine not in ['BLENDER_EEVEE', 'BLENDER_WORKBENCH']:
        for w in bpy.data.window_managers['WinMan'].windows:
            for a in w.screen.areas:
                if a.type == 'VIEW_3D':
                    for s in a.spaces:
                        if s.type == 'VIEW_3D' and s.shading.type == 'RENDERED':
                            s.shading.type = 'SOLID'
                            s.shading.type = 'RENDERED'


def reload_images():
    should_redraw = False
    for image in bpy.data.images:
        should_redraw |= try_reload(image)
    return should_redraw


def reload_timer():
    enabled = bpy.context.scene.eir_enabled
    if enabled < ENABLED:
        return 1.0
    if bpy.context.screen.is_animation_playing and enabled < ANIMENABLED:
        return 2.0
    if reload_images():
        update_view()
    return 0.65


classes = (EIRHEADER_OT_toggle, UdimTimeStamp, UdimTimeStamps)


def draw_header_button(self, context):
    layout = self.layout
    enabled = bpy.context.scene.eir_enabled
    toggle_on = ENABLED <= enabled
    layout.alert = ANIMENABLED <= enabled
    self.layout.operator(EIRHEADER_OT_toggle.bl_idname,
                         icon='HIDE_OFF', depress=toggle_on)


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.eir_enabled = bpy.props.IntProperty(
        name='EIR Enabled', default=False)

    bpy.types.Image.eir_last_update = bpy.props.StringProperty(
        name='Last Update', default=NONE)

    bpy.types.Image.eir_udim_timestamps = bpy.props.PointerProperty(
        name="UDIM Timestamps", type=UdimTimeStamps)

    if not bpy.app.timers.is_registered(reload_timer):
        bpy.app.timers.register(reload_timer, persistent=True)

    bpy.types.VIEW3D_HT_header.append(draw_header_button)


def unregister():
    del bpy.types.Scene.eir_enabled
    del bpy.types.Image.eir_last_update
    del bpy.types.Image.eir_udim_timestamps

    if bpy.app.timers.is_registered(reload_timer):
        bpy.app.timers.unregister(reload_timer)

    bpy.types.VIEW3D_HT_header.remove(draw_header_button)

    for c in classes:
        bpy.utils.unregister_class(c)
