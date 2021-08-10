import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase
from math import degrees,radians


def update_node(self, context):
    self.execute_tree()


class SimpleNodeConversion(SimpleNodeBase):
    bl_idname = 'SimpleNodeConversion'
    bl_label = 'Math Conversion'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('degrees', 'To Degrees', ''),
            ('radians', 'To Radians', ''),
        ],
        default='degrees', update=update_node
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
    bpy.utils.register_class(SimpleNodeConversion)


def unregister():
    bpy.utils.unregister_class(SimpleNodeConversion)
