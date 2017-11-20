ASCII_BOARD_TPL = """
+---+---+---+
|   |   |   |
|   |   |   |
|   |   |   |
+---+---+---+
|   |   |   |
|   |   |   |
|   |   |   |
+---+---+---+
|   |   |   |
|   |   |   |
|   |   |   |
+---+---+---+
""".strip()

class Sudoku(object):
  def __init__(self, matrix):
    self.board, self.rows, self.columns, self.boxes = self.init_board(matrix)

  @property
  def ascii(self):
    flattened = [val for sublist in self.board for val in sublist]
    return ASCII_BOARD_TPL.replace(' ', '%d') % tuple(flattened)


  '''
  Checks if matrix has a valid row/column/box configurations
  matrix - the puzzle to be checked
  val - value to be inserted in to puzzle
  var - the (x, y) position in matrix where val is inserted
  r - set of unused values for each row
  c - set of unused values for each column
  b - set of unused values for each 3x3 box
  '''

  def row_legal(self, val, var):
      if val in self.rows[var[0]]:
         return True
      else:
         return False

  def col_legal(self, val, var):
      if val in self.columns[var[1]]:
         return True
      else:
         return False

  def box_legal(self, val, var):
      if val in self.boxes[var[0]//3][var[1]//3]:
          return True
      else:
          return False

  def is_legal(self, val, var):
      if self.row_legal(val, var) and \
         self.col_legal(val, var) and \
         self.box_legal(val, var):
          return True
      else:
          return False

  '''
  Checks if sudoku puzzle is completed
  Dummy entries are assigned to "0"
  '''

  def is_complete(self):
      for i in range(9):
          for j in range(9):
              if self.board[i][j] == 0:
                  return False
      return True

  '''
  Returns a list of tuples [x,y] that need
  to be filled in, in order to complete the puzzle
  '''

  def unassigned_vars(self):
      varus=[]
      for i in range(9):
          for j in range(9):
              if self.board[i][j] == 0:
                  varus.append([i,j])
      return varus

  '''
  produces
  rows - list of sets, of possible assignment values
  cols - list of sets, of possible assignment values
  boxes - 2d list of sets, of possible assignment values
  from given matrix
  '''
  def init_board(self, matrix):
      rows = [{1,2,3,4,5,6,7,8,9} for i in range(9)]
      cols = [{1,2,3,4,5,6,7,8,9} for i in range(9)]
      boxes = [[{1,2,3,4,5,6,7,8,9} for i in range(3)]
               for j in range(3)]
      board = [[0 for i in range(9)] for j in range(9)]
      for i in range(81):
        x = i//9
        y = i%9
        board[x][y] = matrix[i]
        rows[x].discard(board[x][y])
        cols[y].discard(board[x][y])
        boxes[x//3][y//3].discard(board[x][y])
      return board, rows, cols, boxes

  def fill_square(self, val, var):
      self.board[var[0]][var[1]] = val
      self.rows[var[0]].discard(val)
      self.columns[var[1]].discard(val)
      self.boxes[var[0]//3][var[1]//3].discard(val)

  def undo_square(self, val, var):
      self.board[var[0]][var[1]] = 0
      self.rows[var[0]].add(val)
      self.columns[var[1]].add(val)
      self.boxes[var[0]//3][var[1]//3].add(val)

  '''
  Checks if any variable in our constraint problem
  has no more choices,
  returns True to let forward
  checker know, not to proceed with the assignment
  returns False if there is still hope of solving
  '''

  def bad_row(self, var):
      for i in range(9):
          if self.board[var[0]][i] == 0:
              set_intersection = self.rows[var[0]] & \
                                  self.columns[i] & \
                                  self.boxes[var[0]//3][i//3]
              if len(set_intersection) == 0:
                  return True
      return False

  def bad_col(self, var):
      for i in range(9):
          if self.board[i][var[1]] == 0:
              set_intersection = self.rows[i] & \
                                  self.columns[var[1]] & \
                                  self.boxes[i//3][var[1]//3]
              if len(set_intersection) == 0:
                  return True
      return False

  def bad_box(self, var):
      for i in range(3):
          for j in range(3):
              if self.board[(var[0]//3)*3 + i][(var[1]//3)*3 + j] == 0:
                  set_intersection = self.rows[(var[0]//3)*3 + i] & \
                                     self.columns[(var[1]//3)*3 + j] & \
                                     self.boxes[var[0]//3][var[1]//3]
                  if len(set_intersection) == 0:
                      return True
      return False

  def bad_move(self, var):
      if self.bad_row(var) or \
         self.bad_col(var) or \
         self.bad_box(var):
          return True
      else:
          return False


  '''
  First heuristic
  Ranks variables based on which ones can take the least amount of values
  smaller values are prioritized first
  '''
  def constrained_vars(self, varus):
      most_constrained_varus = []
      min_constrained = float("inf")
      for var in varus:
          cur_constraints = len(self.rows[var[0]] & \
                                self.columns[var[1]] & \
                                self.boxes[var[0]//3][var[1]//3])
          if cur_constraints < min_constrained:
              most_constrained_varus = [var]
              min_constrained = cur_constraints
          elif cur_constraints == min_constrained:
              most_constrained_varus.append(var)
      return most_constrained_varus


  '''
  Second heuristic
  Ranks variables based on how many other variables are affected
  larger values are prioritized first
  '''
  def constraining_vars(self, varus):
      most_constraining_varus = []
      max_constraining = float("-inf")
      for var in varus:
          num_zeros = 0
          for i in range(9):
              if self.board[var[0]][i] == 0:
                  num_zeros += 1
              if self.board[i][var[1]] == 0:
                  num_zeros += 1
          for i in range(3):
              for j in range(3):
                  if self.board[var[0]//3 + i][var[1]//3 + j] == 0:
                      num_zeros += 1
          num_zeros -= 3
          if num_zeros > max_constraining:
              most_constraining_varus = [var]
              max_constraining = num_zeros
          elif num_zeros == max_constraining:
              most_constraining_varus.append(var)
      return most_constraining_varus

  '''
  Third heuristic
  Ranks values for each variable base on how many other variables are affected
  smaller values are prioritized first
  '''
  def least_constraining_vals(self, var):
      least_constraining_vals = (self.rows[var[0]] & \
                                  self.columns[var[1]] & \
                                  self.boxes[var[0]//3][var[1]//3])
      total_squares_affected = []
      for val in least_constraining_vals:
          tot_affected = 0
          for i in range(9):
              if self.board[var[0]][i] == 0:
                  s = self.rows[var[0]] & \
                      self.columns[i] & \
                      self.boxes[var[0]//3][i//3]
                  if val not in s:
                      tot_affected += 1
              if self.board[i][var[1]] == 0:
                  s = self.rows[i] & \
                      self.columns[var[1]] & \
                      self.boxes[i//3][var[1]//3]
                  if val not in s:
                      tot_affected += 1
          for i in range(3):
              for j in range(3):
                  if self.board[(var[0]//3)*3 + i][(var[1]//3)*3 + j] == 0:
                      s = self.rows[(var[0]//3)*3 + i] & \
                          self.columns[(var[1]//3)*3 + j] & \
                          self.boxes[var[0]//3][var[1]//3]
                      if val not in s:
                          tot_affected += 1
          total_squares_affected.append(tot_affected)
     
      sorted_vals = [x for (x, y) in sorted(zip(least_constraining_vals,
                                                total_squares_affected),
                                            key=lambda tup: tup[1])]
      return sorted_vals


  '''
  Backtracking search with forward checking and 3 heursitics
  '''

  def solve(self):
      if self.is_complete():
        return self
      varus = self.unassigned_vars()
      most_constrained_varus = self.constrained_vars(varus)
      most_constraining_varus = self.constraining_vars(most_constrained_varus)
      for var in most_constrained_varus:
          vals = self.least_constraining_vals(var)
          for val in vals:
              if self.is_legal(val, var):
                 self.fill_square(val, var)
                 if self.bad_move(var):
                     self.undo_square(val, var)
                     continue
                 result = self.solve()
                 if result:
                     return result
                 self.undo_square(val, var)
          return False
      return False