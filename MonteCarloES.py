#%%
import random
from Orbito import Orbito

#%%
player1=Orbito('#')
player2=Orbito('$')

#%%
Orbito.initializeStaticVariables()
Orbito.showCurrentBoard()
# %%
player1.playMove('5')
Orbito.showCurrentBoard()
# %%
player2.playMove('AEA')
Orbito.showCurrentBoard()
# %%
player1.playMove('9')
Orbito.showCurrentBoard()
# %%
print(player2.possibleActionInCurrentBoard())
# %%
print(Orbito.currentBoardToState())
# %%
Orbito.showBoard(Orbito.stateToBoard(Orbito.currentBoardToState()))
# %%
player2.playMove('8')
Orbito.showCurrentBoard()
# %%
print(Orbito.checkForVerdict(Orbito.currentBoard))
# %%
