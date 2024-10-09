import copy
action = (1,2)

i = action[0]
print(i)

X = "X"
O = "O"
EMPTY = None
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xs = 0
    os = 0
    for i in board:
        for a in i:
          if(a == X):
            xs += 1
          if(a == O):
            os += 1
    if((xs == 0 & os == 0) | (xs == os)):
      return X
    else:
      return O
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    r = []
    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
              act = (i, j)
              r.append(act)
    return r       
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #newboard = copy.deepcopy(board,)
    newboard = copy.deepcopy(board)
    print(newboard)
    #print("end1")
    who = player(board)
    if(action != None):
        i = action[0]
        j = action[1]
        if(newboard[i][j] != EMPTY):
            raise Exception("Invalid Move")
        newboard[i][j] = who
    print(newboard)
    return newboard
    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if(winnercheck(board, X)):
      return X
    elif(winnercheck(board, O)):
      return O
    else:
      return None
    #raise NotImplementedError

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty = 0
    for i in board:
      for j in i:
         if(j == EMPTY):
           empty = empty + 1
    w = winner(board)
    if((w != None) | ((empty == 0) & (w == None))):
       return True
    else:
       return False
    #raise NotImplementedError

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if(w == X):
       return 1
    elif(w == O):
       return -1
    else:
       return 0
    #raise NotImplementedError

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    p = player(board)
    if(terminal(board)):
      return None
    elif(p == X):
        score = -2
        for action in actions(board):
          value = min(result(board, action))
          if(value > score):
            score = value
            pick = action
        return pick
    else:
        score = 2
        for action in actions(board):
           value = max(result(board, action))
           if(value < score):
              score = value
              pick = action
        return pick
    #raise NotImplementedError

def min(board):
    v = 2
    if(terminal(board)):
        return utility(board)
    for action in actions(board):
        value = max(result(board, action))
        if(value < v):
          v = value
    return v

def max(board):
    v = -2
    if(terminal(board)):
      return utility(board)
    for action in actions(board):
      value = min(result(board, action))
      if(value > v):
        v = value
    return v

def winnercheck(board, player):
    if((board[0][0] == player) & (board[1][1] == player) & (board[2][2] == player)):
      return 1
    if((board[0][2] == player) & (board[1][1] == player) & (board[2][0] == player)):
      return 1
    for i in board:
      if(islistall(i, player)):
        return 1
    for j in range(3):
        cnt = 0
        for i in board:
          if(i[j] == player):
             cnt = cnt + 1
        if(cnt == 3):
          return 1
    return 0
        

def islistall(a, player):
    cnt = 0
    for j in a:
      if(j == player):
        cnt = cnt + 1
    if(cnt == 3):
       return 1
    else:
       return 0
    
board1 =   [[X, X, O],
            [EMPTY, X, EMPTY],
            [EMPTY, X, O]]
board2 = [[X, O, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, O, EMPTY]]
board3 = [  [X, X, O],
            [O, O, X],
            [X, O, X]]
'''
print("player:",player(board))
#print(actions(board))
action = minimax(board)
print("result:",result(board, action))
print(winner(board))
print(terminal(board))
print(utility(board))
'''
print("terminal", terminal(board3))
print("player:",player(board1))
print(winner(board1))



