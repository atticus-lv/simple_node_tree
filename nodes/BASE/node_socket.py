import bpy
from bpy.props import *
from mathutils import Vector

from ._runtime import cache_socket_links, cache_socket_variables


# some method from rigging_node
class SocketBase():
    compatible_sockets = []

    # reroute method
    ###########################
    @property
    def connected_socket(self):
        '''
        Returns connected socket

        It takes O(len(nodetree.links)) time to iterate thought the links to check the connected socket
        To avoid doing the look up every time, the connections are cached in a dictionary
        The dictionary is emptied whenever a socket/connection/node changes in the nodetree
        accessing links Takes O(len(nodetree.links)) time.
        '''

        def set_valid(socket, is_valid=False):
            if socket.links:
                socket.links[0].is_valid = is_valid

        _nodetree_socket_connections = cache_socket_links.setdefault(self.id_data, {})
        _connected_socket = _nodetree_socket_connections.get(self, None)

        if _connected_socket:
            return _connected_socket

        socket = self

        if socket.is_output:
            while socket.is_linked and socket.links[0].to_node.bl_rna.name == 'Reroute':
                socket = socket.links[0].to_node.outputs[0]
            if socket.is_linked:
                _connected_socket = socket.links[0].to_socket

        else:
            while socket.is_linked and socket.links[0].from_node.bl_rna.name == 'Reroute':
                socket = socket.links[0].from_node.inputs[0]
            if socket.is_linked:
                _connected_socket = socket.links[0].from_socket

                # set link
                if not socket.is_socket_compatible(_connected_socket):
                    set_valid(socket, False)

        cache_socket_links[self.id_data][self] = _connected_socket

        return _connected_socket

    # UI display
    ###################

    # Link valid
    def is_socket_compatible(self, other_socket):
        if other_socket.bl_idname == 'NodeSocketVirtual':
            return True
        return other_socket.bl_idname == self.bl_idname or other_socket.bl_idname in self.compatible_sockets

    @property
    def ui_value(self):
        '''use for output ui display'''
        val = self.get_value()
        if val is None: return 'None'

        if isinstance(val, bpy.types.Object) or isinstance(val, bpy.types.Material) or isinstance(val, bpy.types.World):
            return val.name
        elif isinstance(val, str) or isinstance(val, int):
            return f'{val}'
        elif isinstance(val, float):
            return f'{round(val, 2)}'
        elif isinstance(val, tuple) or isinstance(val, Vector):
            d_val = [round(num, 2) for num in list(val)]
            return f'{d_val}'
        elif isinstance(val, bool):
            return 'True' if val else 'False'
        else:
            return f'{val}'

    # set and get method
    #########################

    def set_value(self, value):
        '''Sets the value of an output socket'''
        cache_socket_variables.setdefault(self.id_data, {})[self] = value

    def get_self_value(self):
        '''returns the stored value of an output socket'''
        val = cache_socket_variables.setdefault(self.id_data, {}).get(self, None)
        return val

    def get_value(self):
        '''
        if the socket is an output it returns the stored value of that socket
        if the socket is an input:
            if it's connected, it returns the value of the connected output socket
            if it's not it returns the default value of the socket
        '''
        _value = ''
        if not self.is_output:
            connected_socket = self.connected_socket

            if not connected_socket:
                _value = self.default_value
            else:
                _value = connected_socket.get_self_value()
        else:
            _value = self.get_self_value()

        return _value


def update_node(self, context):
    try:
        self.node.execute_tree()
    except Exception as e:
        print(e)


class SimpleNodeSocket(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'SimpleNodeSocket'
    bl_label = 'SimpleNodeSocket'

    socket_color = (0.5, 0.5, 0.5, 1)

    compatible_sockets = ['SimpleNodeSocketResult']

    text: StringProperty(default='')
    default_value: IntProperty(default=0, update=update_node)

    @property
    def display_name(self):
        label = self.name
        if self.text != '':
            label = self.text
        if self.is_output:
            label += ': ' + self.ui_value
        return label

    def draw(self, context, layout, node, text):
        col = layout.column(align=1)
        if self.is_linked or self.is_output:
            layout.label(text=self.display_name)
        else:
            col.prop(self, 'default_value', text=self.display_name)  # column for vector

    def draw_color(self, context, node):
        return self.socket_color


# Socket Class
################

class SimpleNodeSocketBool(SimpleNodeSocket, SocketBase):
    bl_idname = 'SimpleNodeSocketBool'
    bl_label = 'SimpleNodeSocketBool'

    socket_color = (0.9, 0.7, 1.0, 1)

    default_value: BoolProperty(default=False, update=update_node)


class SimpleNodeSocketInt(SimpleNodeSocket, SocketBase):
    bl_idname = 'SimpleNodeSocketInt'
    bl_label = 'SimpleNodeSocketInt'

    socket_color = (0, 0.9, 0.1, 1)

    default_value: IntProperty(default=0, update=update_node)


class SimpleNodeSocketFloat(SimpleNodeSocket, SocketBase):
    bl_idname = 'SimpleNodeSocketFloat'
    bl_label = 'SimpleNodeSocketFloat'

    socket_color = (0.5, 0.5, 0.5, 1)

    default_value: FloatProperty(default=0, update=update_node)


class SimpleNodeSocketString(SimpleNodeSocket, SocketBase):
    bl_idname = 'SimpleNodeSocketString'
    bl_label = 'SimpleNodeSocketString'

    socket_color = (0.2, 0.7, 1.0, 1)

    default_value: StringProperty(default='', update=update_node)


class SimpleNodeSocketVector(SimpleNodeSocket, SocketBase):
    bl_idname = 'SimpleNodeSocketVector'
    bl_label = 'SimpleNodeSocketVector'

    socket_color = (0.5, 0.3, 1.0, 1)

    default_value: FloatVectorProperty(name='Vector', default=(0, 0, 0), subtype='NONE',
                                       update=update_node)


class SimpleNodeSocketXYZ(SimpleNodeSocketVector, SocketBase):
    bl_idname = 'SimpleNodeSocketXYZ'
    bl_label = 'SimpleNodeSocketXYZ'

    default_value: FloatVectorProperty(name='Vector', default=(1.0, 1.0, 1.0), subtype='XYZ',
                                       update=update_node)


class SimpleNodeSocketResult(SimpleNodeSocket, SocketBase):
    bl_idname = 'SimpleNodeSocketResult'
    bl_label = 'SimpleNodeSocketResult'

    socket_color = (1, 1, 1, 0.5)

    compatible_sockets = [SimpleNodeSocket.bl_idname,
                          SimpleNodeSocketBool.bl_idname,
                          SimpleNodeSocketInt.bl_idname,
                          SimpleNodeSocketFloat.bl_idname,
                          SimpleNodeSocketString.bl_idname,
                          SimpleNodeSocketXYZ.bl_idname, ]


classes = (
    SimpleNodeSocket,
    SimpleNodeSocketBool,
    SimpleNodeSocketInt,
    SimpleNodeSocketFloat,
    SimpleNodeSocketString,

    SimpleNodeSocketXYZ,
    SimpleNodeSocketResult,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
