import bpy
from bpy.props import *
from ...nodes.BASE.node_base import SimpleNodeBase

from mathutils import Color, Vector


def update_node(self, context):
    if self.operate_type in {'normalized', 'length'}:
        self.remove_input('value2')
    else:
        self.create_input('SimpleNodeSocketXYZ', 'value2', 'Vector')

    if self.operate_type in {'dot', 'length'}:
        self.remove_output('output_vector')
        self.create_output('SimpleNodeSocketFloat', 'output_value', 'Output')
    else:
        self.remove_output('output_value')
        self.create_output('SimpleNodeSocketXYZ', 'output_vector', 'Output')

    self.execute_tree()


class SimpleNodeVectorMath(SimpleNodeBase):
    bl_idname = 'SimpleNodeVectorMath'
    bl_label = 'Vector Math'

    operate_type: EnumProperty(
        name='Type',
        items=[
            ('+', 'Add', ''),
            ('-', 'Subtract', ''),
            ('dot', 'Dot Product', ''),
            ('cross', 'Cross Product', ''),
            ('project', 'Project', ''),
            ('normalized', 'Normalized', ''),
            ('length', 'Length', ''),
        ],
        default='+', update=update_node
    )

    def init(self, context):
        self.create_input('SimpleNodeSocketXYZ', 'value1', 'Vector')
        self.create_input('SimpleNodeSocketXYZ', 'value2', 'Vector')
        self.create_output('SimpleNodeSocketXYZ', 'output_vector', "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operate_type', text='')

    def process(self, context, id, path):
        s1 = self.inputs['value1'].get_value()
        s2 = None
        if 'value2' in self.inputs:
            s2 = self.inputs['value2'].get_value()

        if self.operate_type == '+':
            self.outputs[0].set_value(s1 + s2)
        elif self.operate_type == '-':
            self.outputs[0].set_value(s1 - s2)
        elif self.operate_type == 'dot':
            self.outputs[0].set_value(s1.dot(s2))
        elif self.operate_type == 'cross':
            self.outputs[0].set_value(s1.cross(s2))
        elif self.operate_type == 'project':
            self.outputs[0].set_value(s1.project(s2))
        elif self.operate_type == 'normalized':
            self.outputs[0].set_value(s1.normalized())
        elif self.operate_type == 'length':
            self.outputs['output_value'].set_value(s1.length)


def register():
    bpy.utils.register_class(SimpleNodeVectorMath)


def unregister():
    bpy.utils.unregister_class(SimpleNodeVectorMath)
