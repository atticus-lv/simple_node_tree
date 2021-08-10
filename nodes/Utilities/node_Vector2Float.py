import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase
from mathutils import Color, Vector


class SimpleNodeVectorToFloat(SimpleNodeBase):
    bl_idname = 'SimpleNodeVectorToFloat'
    bl_label = 'Vector to Float'

    def init(self, context):
        self.create_output('SimpleNodeSocketFloat', 'value1', 'X')
        self.create_output('SimpleNodeSocketFloat', 'value2', 'Y')
        self.create_output('SimpleNodeSocketFloat', 'value3', 'Z')
        self.create_input('SimpleNodeSocketXYZ', 'input', "Vector")

    def process(self, context, id, path):
        ip = self.inputs['input'].get_value()

        if ip and (isinstance(ip, Vector) or isinstance(ip, list) or isinstance(ip, tuple)):
            for i, output in enumerate(self.outputs):
                output.set_value(ip[i])


def register():
    bpy.utils.register_class(SimpleNodeVectorToFloat)


def unregister():
    bpy.utils.unregister_class(SimpleNodeVectorToFloat)
