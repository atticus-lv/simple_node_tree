import bpy

from bpy.props import *
from ._runtime import (runtime_info, cache_node_dependants, cache_executed_nodes,
                       cache_socket_links, cache_socket_variables, cache_node_group_outputs,
                       logger, MeasureTime)


# some method comes from rigging_nodes
class SimpleNodeBase(bpy.types.Node):
    bl_label = "SimpleNode"

    last_ex_id: StringProperty()

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname in {'SimpleNodeTree', 'SimpleNodeTreeGroup'}

    ## BASE METHOD
    #########################################

    def copy(self, node):
        if self.bl_idname == 'SimpleNodeResult': self.label = self.name
        if hasattr(self, 'set_as_output'): self.set_as_output = False
        print(f"Copied {self.name} from {node.name}")

    def free(self):
        """Remove Node"""
        print("Removed node", self.name)

    ## INITIAL METHOD
    #########################################

    def create_input(self, socket_type, socket_name, socket_label, default_value=None):
        if self.inputs.get(socket_name):
            return None

        input = self.inputs.new(socket_type, socket_name)
        input.text = socket_label

        if default_value: input.default_value = default_value

    def remove_input(self, socket_name):
        input = self.inputs.get(socket_name)
        if input:
            self.inputs.remove(input)

    def create_output(self, socket_type, socket_name, socket_label, default_value=None):
        if self.outputs.get(socket_name):
            return None

        output = self.outputs.new(socket_type, socket_name)
        output.text = socket_label

        if default_value: output.default_value = default_value

    def remove_output(self, socket_name):
        output = self.outputs.get(socket_name)
        if output:
            self.outputs.remove(output)

    ## STATE METHOD
    #########################################

    def draw_buttons(self, context, layout):
        pass

    ## UPDATE METHOD
    #########################################

    # This is build-in method
    def update(self):
        if runtime_info['updating'] is True:
            return


    def get_dependant_nodes(self):
        '''returns the nodes connected to the inputs of this node'''
        dep_tree = cache_node_dependants.setdefault(self.id_data, {})

        if self in dep_tree:
            return dep_tree[self]
        nodes = []
        for input in self.inputs:
            connected_socket = input.connected_socket
            if connected_socket and connected_socket not in nodes:
                nodes.append(connected_socket.node)
        dep_tree[self] = nodes

        return nodes

    def execute_dependants(self, context, id, path):
        '''Responsible of executing the required nodes for the current node to work'''
        for x in self.get_dependant_nodes():
            self.execute_other(context, id, path, x)

    def execute(self, context, id, path):
        if self.last_ex_id == id: return

        self.last_ex_id = id

        with MeasureTime(self, 'Dependants'):
            self.execute_dependants(context, id, path)
        with MeasureTime(self, 'Group'):
            self.process_group(context, id, path)
            if self not in cache_executed_nodes: cache_executed_nodes.append(self)
        with MeasureTime(self, 'Execution'):
            self.process(context, id, path)
            if self not in cache_executed_nodes: cache_executed_nodes.append(self)

        logger.debug(f'Execute: <{self.name}>')

    def path_to_node(self, path):
        node_tree = bpy.data.node_groups.get(path[0])
        for x in path[1:-1]:
            node_tree = node_tree.nodes.get(x).node_tree
        node = node_tree.nodes.get(path[-1])
        return node

    def execute_other(self, context, id, path, other):
        if hasattr(other, 'execute'):
            other.execute(context, id, path)
        else:
            if other.bl_rna.identifier == 'NodeGroupInput':
                if len(path) < 2:
                    raise ValueError(f'trying to setup the values of a nodegroup input on the upper level')
                node = self.path_to_node(path)
                assert node, f'{path} cannot be resolved to a node'
                for i, output in enumerate(other.outputs):
                    if output.bl_rna.identifier != 'NodeSocketVirtual':
                        if self.id_data.bl_idname == 'SimpleNodeTreeGroup':
                            other_socket = node.inputs[i]
                            output.set_value(other_socket.get_value())

            elif other.bl_rna.identifier == 'NodeGroupOutput':
                nodes = set()
                for input in other.inputs:
                    if input.bl_rna.identifier != 'NodeSocketVirtual':
                        connected_socket = input.connected_socket

                        if connected_socket and connected_socket not in nodes:
                            node = connected_socket.node
                            self.execute_other(context, id, path, node)
                            nodes.add(node)

    # update the build-in values with update the hole tree
    def execute_tree(self):
        cache_executed_nodes.clear()
        if runtime_info['executing']:
            return

        if bpy.context.scene.sp_viewer_tree is not None:
            bpy.context.scene.sp_viewer_tree.execute(bpy.context)

    def process(self, context, id, path):
        """node method"""
        pass

    def process_group(self, context, id, path):
        """group node method"""
        pass


def register():
    bpy.utils.register_class(SimpleNodeBase)


def unregister():
    bpy.utils.unregister_class(SimpleNodeBase)
