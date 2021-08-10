import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase

from mathutils import Color, Vector


def update_node(self, context):
    if self.operate_type == 'not':
        self.remove_input('value2')
    else:
        self.create_input('SimpleNodeSocketBool', 'value2', 'Boolean')

    self.execute_tree()


class SimpleNodeBoolean(SimpleNodeBase):
    bl_idname = 'SimpleNodeBoolean'
    bl_label = 'Math Boolean'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('and', 'And', ''),
            ('or', 'Or', ''),
            ('not', 'Not', ''),
        ],
        default='and', update=update_node
    )

    def init(self, context):
        self.create_input('SimpleNodeSocketBool', 'value1', 'Boolean')
        self.create_input('SimpleNodeSocketBool', 'value2', 'Boolean')
        self.create_output('SimpleNodeSocketBool', 'output', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')

    def process(self, context, id, path):
        s1 = self.inputs['value1'].get_value()
        s2 = None
        if 'value2' in self.inputs:
            s2 = self.inputs['value2'].get_value()

        s1 = bool(s1)
        s2 = bool(s2)

        if self.operate_type != 'not':
            self.outputs[0].set_value(eval(f'{s1} {self.operate_type} {s2}'))
        else:
            self.outputs[0].set_value(False if s1 else True)


def register():
    bpy.utils.register_class(SimpleNodeBoolean)


def unregister():
    bpy.utils.unregister_class(SimpleNodeBoolean)
