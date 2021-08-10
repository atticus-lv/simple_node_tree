import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase


def update_node(self, context):
    self.execute_tree()


class SimpleNodeFloatInput(SimpleNodeBase):
    bl_idname = 'SimpleNodeFloatInput'
    bl_label = 'Float Input'

    default_value: FloatProperty(update=update_node)

    def init(self, context):
        self.create_output('SimpleNodeSocketFloat', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'default_value', text='')

    def process(self, context, id, path):
        self.outputs[0].set_value(self.default_value)


def register():
    bpy.utils.register_class(SimpleNodeFloatInput)


def unregister():
    bpy.utils.unregister_class(SimpleNodeFloatInput)
