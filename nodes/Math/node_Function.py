import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase

from mathutils import Color, Vector


def update_node(self, context):
    self.execute_tree()


class SimpleNodeFunctions(SimpleNodeBase):
    bl_idname = 'SimpleNodeFunctions'
    bl_label = 'Functions'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('+', 'Add', ''),
            ('-', 'Subtract', ''),
            ('*', 'Muitiply', ''),
            ('/', 'Divide', ''),
        ],
        default='+', update=update_node
    )

    def init(self, context):
        self.create_input('SimpleNodeSocketFloat', 'value1', 'Value')
        self.create_input('SimpleNodeSocketFloat', 'value2', 'Value')
        self.create_output('SimpleNodeSocketFloat', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')

    def process(self, context, id, path):
        s1 = self.inputs['value1'].get_value()
        s2 = self.inputs['value2'].get_value()

        self.outputs[0].set_value(eval(f'{s1} {self.operate_type} {s2}'))


def register():
    bpy.utils.register_class(SimpleNodeFunctions)


def unregister():
    bpy.utils.unregister_class(SimpleNodeFunctions)
