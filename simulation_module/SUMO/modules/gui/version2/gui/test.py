import StatusWindow
import NavigationWindow

s_path_of_net_xml = "../flpoly.net.xml"
s_window_title = "Status Window"
n_cell_width = 10
n_edge_length_scale = 1
is_cells_mode_on = False
is_minimap_mode_on = True

nw = NavigationWindow.NavigationWindow()

if False:
  sw = StatusWindow.StatusWindow(s_path_of_net_xml)
  sw.set_window_title(s_window_title)
  sw.set_edge_length_scale(n_edge_length_scale)
  sw.set_cell_width(n_cell_width)
  sw.set_cells_mode(is_cells_mode_on)
  sw.set_minimap_mode(is_minimap_mode_on)
  sw.build()




