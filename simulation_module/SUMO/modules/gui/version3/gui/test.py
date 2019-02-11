import StatusWindow
import NavigationWindow

s_path_of_net_xml = "./test_map/Davenport.net.xml"
s_window_title = "Status Window"
n_max_window_width = 1000
n_max_window_height = 600
n_cell_width = 10
n_edge_length_scale = 1
is_cells_mode_on = False
is_minimap_mode_on = True

sw = StatusWindow.StatusWindow(s_path_of_net_xml)
sw.set_window_title(s_window_title)
sw.set_window_max_dimensions(n_max_window_width,n_max_window_height)
sw.set_edge_length_scale(n_edge_length_scale)
sw.set_cell_width(n_cell_width)
sw.set_cells_mode(is_cells_mode_on)
sw.set_minimap_mode(is_minimap_mode_on)

nw = NavigationWindow.NavigationWindow(sw)





