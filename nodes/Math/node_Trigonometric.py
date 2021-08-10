import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase
from math import sin, cos, tan, asin, acos, atan


def update_node(self, context):
    self.execute_tree()


class SimpleNodeTrigonometric(SimpleNodeBase):
    bl_idname = 'SimpleNodeTrigonometric'
    bl_label = 'Math Trigonometric'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('sin', 'Sine', ''),
            ('cos', 'Cosine', ''),
            ('tan', 'Tangent', ''),
            ('asin', 'Arcsin', ''),
            ('acos', 'Arccos', ''),
            ('atan', 'Arctangent', ''),
        ],
        default='sin', update=update_node
    )

    def init(self, context):
        self.create_input('SimpleNodeSocketFloat', 'value1', 'Value')
        self.create_output('SimpleNodeSocketFloat', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')

    def process(self, context, id, path):
        s1 = self.inputs['value1'].get_value()

        self.outputs[0].set_value(eval(f'{self.operate_type}({s1})'))


def register():
    bpy.utils.register_class(SimpleNodeTrigonometric)


def unregister():
    bpy.utils.unregister_class(SimpleNodeTrigonometric)
