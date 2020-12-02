# TTT V3

import pygame, random


# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Tic Tac Toe')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.player_1 = 'X'
      self.player_2 = 'O'
      self.turn = self.player_1
      self.board_size = 3
      self.board = []
      self.create_board()
      self.filled_count = 0
      self.flashers = []
      
   def create_board(self):
      Tile.set_surface(self.surface)
      width = self.surface.get_width() // self.board_size
      height = self.surface.get_height() // self.board_size
      for row_index in range(0, self.board_size):
         row = []
         for col_index in range(0, self.board_size):
            x = col_index * width
            y = row_index * height
            tile = Tile(x, y, width, height) 
            row.append(tile)
         self.board.append(row)

      

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up(event)

   def handle_mouse_up(self,event):
      for row in self.board:
         for tile in row:
            if tile.select(event.pos,self.turn):
               self.change_turn()
               self.filled_count = self.filled_count + 1

   def change_turn(self):
      if self.turn == self.player_1:
         self.turn = self.player_2
      else:
         self.turn = self.player_1
               
            
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.select_flasher()
      for row in self.board:
         for tile in row:
            tile.draw()
      pygame.display.update() # make the updated surface appear on the display

   def select_flasher(self):
      if self.flashers != []:
         tile = random.choice(self.flashers)
         tile.flash()

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      
      pass

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      
      if self.is_win() or self.is_tie():
         self.continue_game = False

   def is_tie(self):
      tie = False
      if self.filled_count == self.board_size * self.board_size: # and not self.is_win() is not necessary because of the lazy evaluation of self.is_win() or self.is_tie() in decide continue
         tie = True
         for row in self.board:
            for tile in row:
               self.flashers.append(tile)
      return tie
   
   def is_win(self):
      row_win = self.is_row_win()
      col_win = self.is_col_win()
      diag_win = self.is_diag_win()
      win = row_win or col_win or diag_win
      return win
   
   def is_row_win(self):
      row_win = False
      for row in self.board:
         if self.is_list_win(row):
            row_win = True
      return row_win

   def is_col_win(self):
      col_win = False
      for col_index in range(self.board_size):
         col = []
         for row in self.board:
            col.append(row[col_index])
         if self.is_list_win(col):
            col_win = True
      return col_win

   def is_diag_win(self):
      diag_win = False
      diag1 = []
      diag2 = []
      for index in range(self.board_size): 
         diag1.append(self.board[index][index])
         diag2.append(self.board[index][self.board_size-1-index])
      if self.is_list_win(diag1) or self.is_list_win(diag2):
         diag_win = True
      return diag_win

   def is_list_win(self, tile_list):
      # compares the numbers in a_list and returns True 
      # if the numbers are all the same; False otherwise
      first_element = tile_list[0]
      all_the_same = True
      for element in tile_list:
         if element != first_element:
         #if not element.__eq__(first_element):
            all_the_same = False
      if all_the_same:
         self.flashers.extend(tile_list)
      return all_the_same

class Tile:
   # An object in this class represents a Tile in TTT 
   
   border_width = 3
   fg_color = pygame.Color('white')
   surface = None
   font_size = 144
   @classmethod
   def set_surface(cls, surface):
      cls.surface = surface
      
   
   def __init__(self, x, y, width, height):
      # Initializes a Tile.
      # - self is the Dot to initialize

      self.rect = pygame.Rect(x, y, width, height)
      self.content = ''
      self.flashing = False
   
   #def is_equal(self, other_tile):
      #return self.content == other_tile.content and self.content != ''
      
   def __eq__(self, other_tile):
      return self.content == other_tile.content and self.content != ''
      
   def draw(self):
      if self.flashing == True:
         # draw a white rectangle
         pygame.draw.rect(Tile.surface, Tile.fg_color, self.rect)
         self.flashing = False
      else:
         # draw a black rectangle with a white border and the content
         pygame.draw.rect(Tile.surface, Tile.fg_color, self.rect, Tile.border_width)
         self.draw_content()
      
   def draw_content(self):
      text_str = self.content
      my_font = pygame.font.SysFont('', Tile.font_size)
      text_image = my_font.render(text_str, True, Tile.fg_color)
      # Following lines are there to compare the computation of 
      # location done in  Q5 of the Preparation Question
      #r_x = self.rect.x
      #r_y = self.rect.y
      #r_w = self.rect.width
      #r_h = self.rect.height
      #t_w = text_image.get_width()
      #t_h = text_image.get_height()
      #t_x = r_x + (r_w - t_w)//2
      #t_y = r_y + (r_h - t_h)//2
      t_x = self.rect.x + (self.rect.width - text_image.get_width())//2
      t_y = self.rect.y + (self.rect.height - text_image.get_height())//2
      location = (t_x,t_y)
      Tile.surface.blit(text_image, location)
      
   def select(self,position,current_player_symbol):
      # Returns True or False
      selected = False
      if self.rect.collidepoint(position):
         if self.content == '':
            self.content = current_player_symbol
            selected = True
         else:
            self.flashing = True
      return selected
   
   def flash(self):
      self.flashing = True

main()
