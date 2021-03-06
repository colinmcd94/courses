# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    if board.is_game_over():
        return -1000
    score = board.longest_chain(board.get_current_player_id()) * 10
    score+= sum([2**(len(chain)-1) for chain in board.chain_cells(board.get_current_player_id())])
    score-= sum([2**(len(chain)-1) for chain in board.chain_cells(board.get_other_player_id())])
    return score
    

## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.

def mux(opt1, opt2, bool):
        if bool:
            return opt1
        else:
            return opt2


def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		              is_terminal_fn=is_terminal):



    def negamax(board_x, depth_x, alpha, beta, me=1,evaluator=eval_fn, next_moves=get_next_moves_fn, is_term=is_terminal_fn):
        if depth_x == 0 or is_term(depth_x,board_x):
            return (evaluator(board_x),None)
        bestValue = (NEG_INFINITY,None)
        childNodes = next_moves(board_x)
        for child in childNodes:
            val = -1*negamax(child[1], depth_x-1, -1*beta, -1*alpha,me+1)[0]
            if val==1000 and me%2==0:
                return (val,child[0])
            if val>bestValue[0]:
                bestValue=(val,child[0])
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return bestValue

    best_val=negamax(board,depth,NEG_INFINITY,INFINITY,0)  
    print "MINIMAX: Decided on column %s with rating %d" % (best_val[1], best_val[0])
    return best_val[1]




    
    

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
                        run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def better_evaluate(board):
    me=board.get_current_player_id()
    other=board.get_other_player_id()
    if board.is_game_over():
        return -1000
    if board.is_win() == me:
        return 1000

    def get(r,c):
        try:
            a = board.get_cell(r,c)
        except:
            a = board.get_other_player_id()
        boolean = a != board.get_other_player_id()
        return boolean

    def h(r,c):
        try:
            boolean = board.get_height_of_column(c)==r
        except:
            boolean = False
        return boolean

    def check(r,c):
        return h(r,c) and get(r,c)

    score=0

    """
    chains = [chain for chain in board.chain_cells(board.get_current_player_id()) if len(chain)>2]
    if not chains:
        pass
    else:
        for chain in chains:
            
            row_l = chain[0][0]
            row_r = chain[2][0]
            col_l = chain[0][1]
            col_r = chain[2][1]
            row_diff = row_r-row_l
            col_diff = col_r-col_l

            #AUGMENT SCORE
            if row_diff and col_diff:
                if row_diff * col_diff>0:
                    if get(row_l+1,col_l+1)!=other and get(row_l-1,col_l-1)!=other:
                        score+=50
                    if get(row_r+1,col_r+1)!=other and get(row_r-1,col_r-1)!=other:
                        score+=50
                else:
                    if get(row_l-1,col_l+1)!=other and get(row_l+1,col_l-1)!=other:
                        score+=50
                    if get(row_r+1,col_r-1)!=other and get(row_r-1,col_r+1)!=other:
                        score+=50
            elif row_diff:
                if get(row_l+1,col_l)!=other and get(row_l-1,col_l)!=other:
                    score+=50
                if get(row_r+1,col_r)!=other and get(row_r-1,col_r)!=other:
                    score+=50
            elif col_diff:
                if get(row_l,col_l+1)!=other and get(row_l,col_l-1)!=other:
                    score+=50
                if get(row_r,col_r+1)!=other and get(row_r,col_r-1)!=other:
                    score+=50
            
            if row_diff and col_diff:
                if row_diff * col_diff>0:
                    if check(row_l+1,col_l+1) or check(row_l-1,col_l-1):
                        return 1000
                    if check(row_r+1,col_r+1) or check(row_r-1,col_r-1):
                        return 1000
                else:
                    if check(row_l-1,col_l+1) or check(row_l+1,col_l-1):
                        return 1000
                    if check(row_r+1,col_r-1) or check(row_r-1,col_r+1):
                        return 1000
            elif row_diff:
                if check(row_l+1,col_l) or check(row_l-1,col_l):
                    return 1000
                if check(row_r+1,col_r) or check(row_r-1,col_r):
                    return 1000
            elif col_diff:
                if check(row_l,col_l+1) or check(row_l,col_l-1):
                    return 1000
                if check(row_r,col_r+1) or check(row_r,col_r-1):
                    return 1000 
            """


    score =  board.longest_chain(board.get_current_player_id()) * 100
    score += sum([3**len(chain) for chain in board.chain_cells(board.get_current_player_id()) if len(chain)>1])
    score -= sum([3**len(chain) for chain in board.chain_cells(board.get_other_player_id()) if len(chain)>1])
    for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= 8*abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += 8*abs(3-col)
    return score

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
#your_player = lambda board: run_search_function(board,
                                                #search_fn=alpha_beta_search,
                                                #eval_fn=better_evaluate,
                                                #timeout=20)

your_player = lambda board: alpha_beta_search(board, depth=6,
                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (True)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "4"
WHAT_I_FOUND_INTERESTING = "The implementation"
WHAT_I_FOUND_BORING = "Looking into the built in code to figure out what exactly is returned by get_all_next_moves (specify that it returns the column played and the new board)"
NAME = "Colin McDonnell"
EMAIL = "colinmcd@mit.edu"

