import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase
from mathutils import Color, Vector


def update_node(self, context):
    self.execute_tree()


class SimpleNodeVectorInput(SimpleNodeBase):
    bl_idname = 'SimpleNodeVectorInput'
    bl_label = 'Vector Input'

    default_value: FloatVectorProperty(update=update_node)

    def init(self, context):
        self.create_output('SimpleNodeSocketXYZ', 'output', "Output")

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.prop(self, 'default_value', text='')

    def process(self, context, id, path):
        vec = Vector((
            self.default_value[0],
            self.default_value[1],
            self.default_value[2],
        ))
        self.outputs[0].set_value(vec)


def register():
    bpy.utils.register_class(SimpleNodeVectorInput)


def unregister():
    bpy.utils.unregister_class(SimpleNodeVectorInput)
