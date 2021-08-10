import bpy
import blf


def dpifac():
    prefs = bpy.context.preferences.system
    return prefs.dpi * prefs.pixel_size / 72


def get_node_location(node):
    node_loc_x = (node.location.x + 1) * dpifac()
    node_loc_y = (node.location.y + 1) * dpifac()
    node_dimension_x = node.dimensions.x
    node_dimension_y = node.dimensions.y

    return node_loc_x, node_loc_y, node_dimension_x, node_dimension_y


def get_node_vertices(nlocx, nlocy, ndimx, ndimy):
    top_left = (nlocx, nlocy)
    top_right = (nlocx + ndimx, nlocy)
    bottom_left = (nlocx, nlocy - ndimy)
    bottom_right = (nlocx + ndimx, nlocy - ndimy)

    return top_left, top_right, bottom_left, bottom_right


def draw_text_2d(color, text, x, y, size=20):
    font_id = 0
    blf.position(font_id, x, y, 0)
    blf.color(font_id, color[0], color[1], color[2], color[3])
    blf.size(font_id, size, 72)
    blf.draw(font_id, text)


def draw_text_on_node(color, text, node, size=15, corner_index=1):
    '''index 0,1,2,3: top_left, top_right, bottom_left, bottom_right'''
    nlocx, nlocy, ndimx, ndimy = get_node_location(node)
    corners = get_node_vertices(nlocx, nlocy, ndimx, ndimy)
    pos = corners[corner_index]

    loc_x, loc_y = bpy.context.region.view2d.view_to_region(pos[0], pos[1], clip=False)
    draw_text_2d(color, text, loc_x, loc_y, size)
