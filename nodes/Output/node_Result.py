import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase
from mathutils import Vector


def set_active_output(self, context):
    if self.set_as_output:
        for node in self.id_data.nodes:
            if node.bl_idname == self.bl_idname and node != self:
                node.set_as_output = False

        # set active output
        bpy.context.window_manager.sp_viewer_node = self.name
        self.execute_tree()


class SimpleNodeResult(SimpleNodeBase):
    """A simple Result node"""
    bl_idname = "SimpleNodeResult"
    bl_label = 'Result'

    default_value: StringProperty(default='Need Update', name='Result Value')
    precision: IntProperty(name='Float Precision', default=3, update=set_active_output)
    # set active and update
    set_as_output: BoolProperty(default=False,
                                update=set_active_output,
                                description='Set as active output')

    def init(self, context):
        self.create_input('SimpleNodeSocketFloat', 'input', 'Input')
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'set_as_output', text='Active Output')

        col.prop(self, 'precision', icon='DOT', emboss=False)
        box = col.box().column(align=1)
        box.prop(self, 'default_value', text='')

    def process(self, context, id, path):
        ip = self.inputs[0].get_value()
        if isinstance(ip, float):
            self.default_value = f'{round(ip, self.precision)}'
        elif isinstance(ip, Vector):
            d_val = [round(num, self.precision) for num in list(ip)]
            self.default_value = F'{tuple(d_val)}'
        else:
            self.default_value = f'{ip}'


def register():
    bpy.utils.register_class(SimpleNodeResult)
    bpy.types.WindowManager.sp_viewer_node = StringProperty(name='Viewer output name')


def unregister():
    bpy.utils.unregister_class(SimpleNodeResult)
    del bpy.types.WindowManager.sp_viewer_node
