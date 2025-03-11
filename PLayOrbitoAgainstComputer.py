#%%
from Orbito import Orbito
import os
import copy
import pickle
Orbito.players=['1','2']

#%%

lookUps={}
# Get the list of all files and directories
path = r"LookUps"
dir_list = os.listdir(path)

for string in dir_list:
    test_string = string

    numbers = []
    for char in test_string:
        if char.isdigit():
            numbers.append(char)
    num=int(''.join(numbers))
    path="LookUps/"
    with open( path+ test_string, 'rb') as file: 
        temp=pickle.load(file)
    lookUps[num]=temp


#%%
def playMove(board,action,playerSymbol):
        if len(action)==1:
            indexI=Orbito.hexToDec[action]//len(board)
            indexJ=Orbito.hexToDec[action]%len(board)
            board[indexI][indexJ]=playerSymbol
        else:
            From=Orbito.hexToDec[action[0]]
            indexI=From//len(board)
            indexJ=From%len(board)
            smb= board[indexI][indexJ]
            board[indexI][indexJ]='0'

            To=Orbito.hexToDec[action[1]]
            indexI=To//len(board)
            indexJ=To%len(board)
            board[indexI][indexJ]=smb

            place=Orbito.hexToDec[action[2]]
            indexI=place//len(board)
            indexJ=place%len(board)
            board[indexI][indexJ]=playerSymbol

        return Orbito.rotateBoard(board)

def checkForVerdict(board,playerList):
        
        plr1Won=Orbito.checkIfFourMatches(board,playerList[0])
        plr2Won=Orbito.checkIfFourMatches(board,playerList[1])

        if plr1Won and plr2Won:
            return 'D'
        
        if plr1Won and (not plr2Won):
            return playerList[0]
        
        if plr2Won and (not plr1Won):
            return playerList[1]
        
        for el in board:
            if '0' in el:
                return None

        for _ in range(5):
            board=Orbito.rotateBoard(board)
            plr1Won=Orbito.checkIfFourMatches(board,playerList[0])
            plr2Won=Orbito.checkIfFourMatches(board,playerList[1])
            if plr1Won and (not plr2Won):
                return playerList[0]
            elif plr2Won and (not plr1Won):
                return playerList[1]
            else:
                pass
        
        return 'D'

def showBoard(board,players=['#','$']):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j]=='0':
                    print(Orbito.decToHex[len(board)*i + j],end=' ')
                else:
                    print(players[int(board[i][j])-1],end=' ')
            print('')



# %%
def chkIfSameBoard(board1,board2):
    for i in range(4):
        for j in range(4):
            if board1[i][j]!=board2[i][j]:
                return False
    return True

def rotate90AntiClock(board):
    rotatedBoard = [[0] * 4 for _ in range(4)] 
    for i in range(4):
        for j in range(4):
            rotatedBoard[3 - j][i] = board[i][j]

    return rotatedBoard

def returnAlignedMove(board,unAlignedBoard,unAlignedMove):
    while not chkIfSameBoard(board,unAlignedBoard):
        unAlignedBoard=rotate90AntiClock(unAlignedBoard)
        temp=''
        for char in unAlignedMove:
            num=Orbito.hexToDec[char]
            indexI=num//4
            indexJ=num%4
            rotatedindexI=3-indexJ
            rotatedindexJ=indexI
            rotatedChar=Orbito.decToHex[4*rotatedindexI + rotatedindexJ]
            temp+=rotatedChar
        unAlignedMove=temp   
    return unAlignedMove
# %%

while True:
    turn=int(input('Enter 1 to play first .\n Enter 2 to play Second. \n Enter 3 to End'))
    if turn==3:
        break

    if turn==1:
        zeroRemaining=16
        verdict=None
        board=[['0' for _ in range(4)] for _ in range(4)]
        while verdict==None:
            #showBoard(board)
            action=input('Enter Action')
            board=playMove(board,action,'1')
            verdict=checkForVerdict(board,['1','2'])
            if verdict=='2':
                print('Computer Won')
                break
            if verdict=='1':
                print('You Won')
                break
            if verdict=='D':
                print('Game Ended Draw')
                break
            print('Board after you played')
            showBoard(board)
            zeroRemaining-=1
            state=Orbito.boardTostate(board)
            unalignedBoard=Orbito.stateToBoard(state)
            #print('Unaligned Board')
            #showBoard(unalignedBoard)
            unalignedcompAction=lookUps[zeroRemaining][state][0]
            ComputerFutureVerdict=lookUps[zeroRemaining][state][1]
            alignedMove=returnAlignedMove(board,unalignedBoard,unalignedcompAction)
            #board=playMove(unalignedBoard,unalignedcompAction,'2')
            board=playMove(board,alignedMove,'2')
            print('Board After Computer played ' + alignedMove)
            print('Computer will ' + ComputerFutureVerdict)
            showBoard(board)
            verdict=checkForVerdict(board,['1','2'])
            if verdict=='2':
                print('Computer Won')
                break
            if verdict=='1':
                print('You Won')
                break
            if verdict=='D':
                print('Game Ended Draw')
                break
            zeroRemaining-=1
    
    if turn==2:
        zeroRemaining=16
        verdict=None
        board=[['0' for _ in range(4)] for _ in range(4)]
        while verdict==None:
            #showBoard(board)
            state=Orbito.boardTostate(board)
            unalignedBoard=Orbito.stateToBoard(state)
            #print('Unaligned Board')
            #showBoard(unalignedBoard)
            unalignedcompAction=lookUps[zeroRemaining][state][0]
            ComputerFutureVerdict=lookUps[zeroRemaining][state][1]
            alignedMove=returnAlignedMove(board,unalignedBoard,unalignedcompAction)
            #board=playMove(unalignedBoard,unalignedcompAction,'1')
            board=playMove(board,alignedMove,'1')
            print('Board After Computer played ' + alignedMove)
            print('Computer will ' + ComputerFutureVerdict)
            showBoard(board)
            verdict=checkForVerdict(board,['1','2'])
            if verdict=='1':
                print('Computer Won')
                break
            if verdict=='2':
                print('You Won')
                break
            if verdict=='D':
                print('Game Ended Draw')
                break
            zeroRemaining-=1

            action=input('Enter Action')
            board=playMove(board,action,'2')
            verdict=checkForVerdict(board,['1','2'])
            if verdict=='1':
                print('Computer Won')
                break
            if verdict=='2':
                print('You Won')
                break
            if verdict=='D':
                print('Game Ended Draw')
                break
            print('Board after you played')
            showBoard(board)
            zeroRemaining-=1
        
    showBoard(board)

         
# %%
