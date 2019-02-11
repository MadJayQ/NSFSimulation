# Author: Quentin Goss
# Last Modified: 9/3/18

from graphics import *

class NavigationWindow:
  
  def __init__(self,status_window):
    self.n_border_padding = 10
    self.n_button_size = 20
    self.n_button_padding = 3
    self.s_window_title = 'Navigation'
    self.n_scroll_amount = 100
    self.l_buttons = []
    self.status_window = status_window
    
    # Status window
    self.status_window.initialize()
    self.status_window.update()
    
    n_height = self.n_border_padding * 2 + self.n_button_padding * 2 + self.n_button_size * 3
    n_width = n_height
    self.window = GraphWin(self.s_window_title,n_width,n_height)
    
    for row in range(3):
      for col in range(3):
        # Top left point
        if col != 1 and row != 1:
          continue
        elif col == 1 and row == 1:
          continue
        n_top_left_x = self.n_border_padding + col * self.n_button_size
        if col > 0:
          n_top_left_x += col * self.n_button_padding
          
        n_top_left_y = self.n_border_padding + row * self.n_button_size
        if row > 0: 
          n_top_left_y += row * self.n_button_padding
          
        p_top_left = Point(n_top_left_x,n_top_left_y)
        
        # Bottom right point
        n_bottom_right_x = n_top_left_x + self.n_button_size
        n_bottom_right_y = n_top_left_y + self.n_button_size
        p_bottom_right = Point(n_bottom_right_x,n_bottom_right_y)
        
        rect = Rectangle(p_top_left,p_bottom_right)
        rect.setFill("light blue")
        self.l_buttons.append(rect)
        
        rect.draw(self.window)
      # end for
    # end for
    
    text_up = Text(self.l_buttons[0].getCenter(),'/\\')
    text_up.draw(self.window)
    
    text_left = Text(self.l_buttons[1].getCenter(),'<')
    text_left.draw(self.window)
    
    text_right = Text(self.l_buttons[2].getCenter(),'>')
    text_right.draw(self.window)
    
    text_down = Text(self.l_buttons[3].getCenter(),'\\/')
    text_down.draw(self.window)
    
    
    # Get original boundaries for status window
    x = [0,self.status_window.get_window_width()]
    y = [self.status_window.get_window_height(),0]
    #print([x,y])
    
    try:
      # Handle buttons
      while True:
        mouse = self.window.getMouse()
        #print([mouse.x,mouse.y])
        # Up
        if self.l_buttons[0].getP1().x < mouse.x < self.l_buttons[0].getP2().x and self.l_buttons[0].getP1().y < mouse.y < self.l_buttons[0].getP2().y:
          y[0] += self.n_scroll_amount
          y[1] += self.n_scroll_amount
          self.status_window.setCoords(x[0],y[0],x[1],y[1])
        # Left
        elif self.l_buttons[1].getP1().x < mouse.x < self.l_buttons[1].getP2().x and self.l_buttons[1].getP1().y < mouse.y < self.l_buttons[1].getP2().y:
          x[0] += self.n_scroll_amount
          x[1] += self.n_scroll_amount
          self.status_window.setCoords(x[0],y[0],x[1],y[1])
        # Right
        if self.l_buttons[2].getP1().x < mouse.x < self.l_buttons[2].getP2().x and self.l_buttons[2].getP1().y < mouse.y < self.l_buttons[2].getP2().y:
          x[0] -= self.n_scroll_amount
          x[1] -= self.n_scroll_amount
          self.status_window.setCoords(x[0],y[0],x[1],y[1])
        # Down
        if self.l_buttons[3].getP1().x < mouse.x < self.l_buttons[3].getP2().x and self.l_buttons[3].getP1().y < mouse.y < self.l_buttons[3].getP2().y:
          y[0] -= self.n_scroll_amount
          y[1] -= self.n_scroll_amount
          self.status_window.setCoords(x[0],y[0],x[1],y[1])

      # end while True
    except:
      self.status_window.finalize()
  # end def __init__(self)
# end class NavigationWindow
