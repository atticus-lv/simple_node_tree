import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase

from mathutils import Color, Vector


def update_node(self, context):
    if self.operate_type in {'=', '>', '<'}:
        if self.operate_type == '=': self.create_input('SimpleNodeSocketFloat', 'epsilon', 'Epsilon')
        self.create_output('SimpleNodeSocketBool', 'bool_output', 'OutBool')
    else:
        self.remove_input('epsilon')
        self.remove_output('bool_output')

    self.execute_tree()


class SimpleNodeComparison(SimpleNodeBase):
    bl_idname = 'SimpleNodeComparison'
    bl_label = 'Comparison'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('>', 'Greater than', ''),
            ('<', 'Less than', ''),
            ('=', 'Compare', ''),
            ('max', 'Maximum', ''),
            ('min', 'Minimum', ''),
        ],
        default='>', update=update_node
    )

    def init(self, context):
        self.create_input('SimpleNodeSocketFloat', 'value1', 'Value')
        self.create_input('SimpleNodeSocketFloat', 'value2', 'Value')
        self.create_output('SimpleNodeSocketFloat', 'output', "Output")
        self.create_output('SimpleNodeSocketBool', 'bool_output', "OutBool")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')

    def process(self, context, id, path):
        s1 = self.inputs['value1'].get_value()
        s2 = self.inputs['value2'].get_value()

        if self.operate_type == '>':
            ans = 1 if s1 > s2 else 0
            ans_bool = True if ans == 1 else False
            self.outputs['output'].set_value(ans)
            self.outputs['bool_output'].set_value(ans_bool)

        elif self.operate_type == '<':
            ans = 1 if s1 < s2 else 0
            ans_bool = True if s1 < s2 else False
            self.outputs['output'].set_value(ans)
            self.outputs['bool_output'].set_value(ans_bool)

        elif self.operate_type == '=':
            e = self.inputs['epsilon'].get_value()
            ans = 1 if abs(s1 - s2) < abs(e) else 0
            ans_bool = True if ans == 1 else False
            self.outputs['output'].set_value(ans)
            self.outputs['bool_output'].set_value(ans_bool)

        elif self.operate_type == 'max':
            self.outputs['output'].set_value(max(s1, s2))

        elif self.operate_type == 'min':
            self.outputs['output'].set_value(min(s1, s2))


def register():
    bpy.utils.register_class(SimpleNodeComparison)


def unregister():
    bpy.utils.unregister_class(SimpleNodeComparison)
