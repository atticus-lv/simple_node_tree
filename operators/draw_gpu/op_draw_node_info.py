import bpy
import blf
import bgl

from bpy.props import BoolProperty

from ...nodes.BASE.node_base import cache_executed_nodes
from ...nodes.BASE._runtime import cache_node_times

from .utils import draw_text_on_node


def draw_callback_nodeoutline(self, context):
    # is executing
    result_node = context.space_data.edit_tree.nodes.get(context.window_manager.sp_viewer_node)
    if not result_node: return

    # set bgl
    bgl.glLineWidth(1)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glHint(bgl.GL_LINE_SMOOTH_HINT, bgl.GL_NICEST)

    # color
    white = (1, 1, 1, self.alpha * 2)
    green = (0, 1, 0, self.alpha * 2)
    red = (1, 0, 0, self.alpha * 2)

    node_list = [node for node in context.space_data.edit_tree.nodes if node in cache_executed_nodes]
    # draw time
    for node in node_list:
        if node.id_data in cache_node_times:
            if node in cache_node_times[node.id_data]:
                times = cache_node_times[node.id_data][node]
                t = times['Execution'] if node.bl_idname != 'RenderNodeGroup' else times['Group']
                t = t * 1000
                if t < 0.1:
                    col = white
                elif t < 1:
                    col = green
                else:
                    col = red
                draw_text_on_node(col, f"{t:.2f}ms", node, size=17, corner_index=0)

    # restore
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glDisable(bgl.GL_LINE_SMOOTH)


class SP_OT_DrawNodeInfo(bpy.types.Operator):
    """Draw the executing node's information"""
    bl_idname = "sp.draw_node_info"
    bl_label = "Draw Info"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'TIMER':
            # show draw
            if context.scene.SP_Drawing:
                if self.alpha < 0.5:
                    self.alpha += 0.02  # show

            # close draw
            else:
                if self.alpha > 0:
                    self.alpha -= 0.02  # fade
                    return {'RUNNING_MODAL'}
                # remove timer / handles
                context.window_manager.event_timer_remove(self._timer)
                bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if True in {context.area.type != 'NODE_EDITOR',
                    context.space_data.edit_tree is None,
                    context.space_data.edit_tree.bl_idname not in {'SimpleNodeTree', 'SimpleNodeTreeGroup'}}:
            self.report({'WARNING'}, "NodeEditor not found, cannot run operator")
            return {'CANCELLED'}

        # init draw values
        self.alpha = 0
        # set statue
        context.scene.SP_Drawing = True
        # add timer and handles
        self._timer = context.window_manager.event_timer_add(0.01, window=context.window)
        self._handle = bpy.types.SpaceNodeEditor.draw_handler_add(draw_callback_nodeoutline, (self, context),
                                                                  'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def draw_header(self, context):
    if context.area.ui_type == 'SimpleNodeTree' and context.space_data.node_tree is not None:
        layout = self.layout
        layout.separator(factor=0.5)

        if context.scene.SP_Drawing is True:
            layout.prop(context.scene, 'SP_Drawing', text='Stop', toggle=1, icon='CANCEL')
        else:
            layout.operator("sp.draw_node_info", icon='INFO')


def register():
    bpy.types.Scene.SP_Drawing = BoolProperty(default=False)
    bpy.utils.register_class(SP_OT_DrawNodeInfo)

    bpy.types.NODE_MT_editor_menus.append(draw_header)


def unregister():
    del bpy.types.Scene.SP_Drawing
    bpy.utils.unregister_class(SP_OT_DrawNodeInfo)

    bpy.types.NODE_MT_editor_menus.remove(draw_header)
