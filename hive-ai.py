"""A python AI for Hive, by John Yianni
"""

__author__ = "William Dizon"
__license__ = "Simplified BSD License"
__version__ = "0.0.1"
__email__ = "wdchromium@gmail.com"

from hive import *

class GamePieces(object):
    QUANTITIES = {
        Insect.Queen: 1,
        Insect.Ant: 3,
        Insect.Beetle: 1,
        Insect.Grasshopper: 2,
        Insect.Ladybug: 0,
        Insect.Mosquito: 0,
        Insect.Pillbug: 0,
        Insect.Spider: 2
    }
    
    def __init__(self):
        self._pieces = []
        for k, count in self.QUANTITIES.items():
            self._pieces.extend([Tile(Color.White, k) for _ in range(count)])
            self._pieces.extend([Tile(Color.Black, k) for _ in range(count)])
    
    def grab(self, color, insect):
        return self._pieces.pop(self._pieces.index(Tile(color, insect)))
    
    def grab_random(self, color):
        from random import choice
        
        friendly = choice([p for p in self._pieces if p.color == color])
        return self._pieces.pop(self._pieces.index(friendly))

if __name__ == '__main__':
    board = HiveBoard(queen_opening_allowed=True)
    
    gp = GamePieces()

    board.perform(Placement(gp.grab(Color.White, Insect.Queen), (0,0)))
    board.perform(Placement(gp.grab(Color.Black, Insect.Queen), (0,1)))

    from itertools import cycle
    from random import choice
    
    action = {
        Color.White: 'grab',
        Color.Black: 'grab'
        }
    
    cycler = cycle([Color.White, Color.Black])
    player_color = next(cycler)
        
    while board.winner is None:
        if action[player_color] == 'grab':
            try:
                grabbed = gp.grab_random(player_color)
            except IndexError:
                print('placing over')
                action[player_color] = 'move'
                player_color = next(cycler)
            else:
                new_loc = choice(list(board.valid_placements(player_color)))
                board.perform(Placement(grabbed, new_loc))
        elif action[player_color] == 'move':
            try:
                for c in board._pieces:
                    p = board.piece_at(c)
                    v = list(board.valid_moves(c))
                    print(p,v,c)
                    if p.color == player_color and len(v):
                        board.perform(Movement(c, choice(v)))
                        print('performed', p,v,c)
                        player_color = next(cycler)
                else:
                    player_color = next(cycler)
            except IllegalMove as e:
                print(e)
                break
            
            
    print(board)
    