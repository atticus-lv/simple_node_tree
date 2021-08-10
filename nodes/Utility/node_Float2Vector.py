import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase
from mathutils import Color, Vector


class SimpleNodeFloatToVector(SimpleNodeBase):
    bl_idname = 'SimpleNodeFloatToVector'
    bl_label = 'Float to Vector'

    def init(self, context):
        self.create_input('SimpleNodeSocketFloat', 'value1', 'Boolean')
        self.create_input('SimpleNodeSocketFloat', 'value2', 'Boolean')
        self.create_input('SimpleNodeSocketFloat', 'value3', 'Boolean')
        self.create_output('SimpleNodeSocketXYZ', 'output', "Output")

    def process(self, context, id, path):
        s1 = self.inputs['value1'].get_value()
        s2 = self.inputs['value2'].get_value()
        s3 = self.inputs['value3'].get_value()

        vec = Vector((s1, s2, s3))

        self.outputs[0].set_value(vec)


def register():
    bpy.utils.register_class(SimpleNodeFloatToVector)


def unregister():
    bpy.utils.unregister_class(SimpleNodeFloatToVector)
