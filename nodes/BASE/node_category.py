import nodeitems_utils


class SimpleNodeCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in {'SimpleNodeTree', 'SimpleNodeTreeGroup'}


node_categories = [
    SimpleNodeCategory("INPUT", "Input", items=[
        nodeitems_utils.NodeItem('SimpleNodeFloatInput'),
        nodeitems_utils.NodeItem('SimpleNodeVectorInput'),
    ]),

    SimpleNodeCategory("MATH", "Math", items=[
        nodeitems_utils.NodeItem("SimpleNodeFunction"),
        nodeitems_utils.NodeItem("SimpleNodeTrigonometric"),
        nodeitems_utils.NodeItem("SimpleNodeComparison"),
        nodeitems_utils.NodeItem("SimpleNodeConversion"),
        nodeitems_utils.NodeItem("SimpleNodeBoolean"),
        nodeitems_utils.NodeItem("SimpleNodeVectorMath"),
    ]),

    SimpleNodeCategory("UTILS", "Utils", items=[
        nodeitems_utils.NodeItem("SimpleNodeVectorToFloat"),
        nodeitems_utils.NodeItem("SimpleNodeFloatToVector"),
    ]),

    SimpleNodeCategory("OUTPUT", "Output", items=[
        nodeitems_utils.NodeItem("SimpleNodeResult"),

    ]),

]


def register():
    try:
        nodeitems_utils.unregister_node_categories("SimpleNodeCategory")
    except Exception:
        pass
    nodeitems_utils.register_node_categories("SimpleNodeCategory", node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories("SimpleNodeCategory")
