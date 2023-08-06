from pyxo.views import View
from pyxo.utils import clear,show_board


class Playing(View):

    def __init__(self,controler:"Engin") -> None:
        self.controler :"Engin" = controler

    def print(self,number:int) -> int:
        clear()
        show_board(self.controler.board,self.controler.players)
        move :int = int(input(f"  what is your next move  {self.controler.players[number].name}  :(1...9) \t"))
        return move

    def print_error(self) -> int:

        return int(input(" tnis nomber is not vailable chose an ather one:(1...9) \t"))

        

