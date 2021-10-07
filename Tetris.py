from numpy import array
from random import randint

class Tetris():
    def __init__(self):
      self.board_height = 22  # this includes the 2 hidden layers
      self.board_width = 10
      self.board = array([self.board_width * [0]] * self.board_height)

      self.move = (0, -1), (0, 1), (1, 0)  # left, right, down
      #The Tets spawn in a 2x4 area laying horazontally
      self.ninty_clockwise = 0
      self.Tetraminos = {"I": {0 : [(1, 3), (1, 4), (1, 5), (1, 6)], 90 : [(-1, 2), (0, ), (1, 5), (2, 5)] },
                    "L": [(1, 3), (1, 4), (1, 5), (0, 5)],
                    "J": [(0, 3), (1, 3), (1, 4), (1, 5)],
                    "T": [(1, 3), (1, 4), (0, 4), (1, 5)],
                    "O": [(0, 4), (1, 4), (1, 5), (0, 5)],
                    "S": [(1, 3), (1, 4), (0, 4), (0, 5)],
                    "Z": [(0, 3), (0, 4), (1, 4), (1, 5)]}
      self.Tet_Names = ["I", "L", "J", "T", "O", "S", "Z"]
      self.Current_Tet = "I"
      def Bag_pull(self):
            return(self.Tet_Names[randint(len(self.Tet_Names))])
      def Best_choice(self):
            Tet, rotation = "I", 90
