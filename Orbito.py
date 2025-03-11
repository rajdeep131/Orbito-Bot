import random
from GameTraining import GameTraining

class Orbito(GameTraining):

    currentBoard=[]
    done=False
    winnerPlayerSymbol=None
    players=[]
    hexToDec={'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15}
    decToHex=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

    def __init__(self,playerSymbol):
        self.playerSymbol=playerSymbol
        Orbito.players.append(self.playerSymbol)
        super().__init__()

    @staticmethod
    def initializeStaticVariables():
        Orbito.currentBoard=[]
        Orbito.done=False
        Orbito.winnerPlayerSymbol=None
        Orbito.initializeBoard()

    @staticmethod
    def initializeBoard(n=4):
        Orbito.currentBoard=[['0' for _ in range(n)] for _ in range(n)]
    
    @staticmethod
    def showBoard(board):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j]=='0':
                    print(Orbito.decToHex[len(Orbito.currentBoard)*i + j],end=' ')
                else:
                    print(board[i][j],end=' ')
            print('')
    
    @staticmethod
    def showCurrentBoard():
        Orbito.showBoard(Orbito.currentBoard)
    
    @staticmethod
    def subBoardToState(arr):
        sm=''
        sign=''
        for i in range(len(arr)):
            if arr[i]=='0':
                sign='0'
            if arr[i]==Orbito.players[0]:
                sign='1'
            if arr[i]==Orbito.players[1]:
                sign='2'
            sm+=sign
        return int(sm)
    
    @staticmethod
    def boardTostate(board):
        A=[board[0][0],board[0][1],board[1][0],board[1][1]]
        B=[board[0][3],board[1][3],board[0][2],board[1][2]]
        C=[board[3][3],board[3][2],board[2][3],board[2][2]]
        D=[board[3][0],board[2][0],board[3][1],board[2][1]]

        state=[Orbito.subBoardToState(A),Orbito.subBoardToState(B),Orbito.subBoardToState(C),Orbito.subBoardToState(D)]
        mx=max(state)
        newState=[]
        while True:
            if state[0]==mx:
               break     
            temp2=state.pop(0)
            state=state+[temp2]
        if state[0]==mx and state[2]==mx:
            if state[1]>state[3]:
                newState=[state[0],state[1],state[2],state[3]]
            if state[3]>state[1]:
                newState=[state[0],state[3],state[2],state[1]]
        
        if state[0]==mx and state[3]==mx:
                newState=[state[3],state[0],state[1],state[2]]
        
        if len(newState)!=0:
            state=newState
        temp=[]
        for el in state:
            length=len(str(el))
            if length==1:
                temp.append('000'+str(el))
            if length==2:
                temp.append('00'+str(el))
            if length==3:
                temp.append('0'+str(el))
            if length==4:
                temp.append(str(el))
        
        return temp[0]+'_'+temp[1]+'_'+temp[2]+'_'+temp[3]
    
    @staticmethod
    def currentBoardToState():
        return Orbito.boardTostate(Orbito.currentBoard)
            
    @staticmethod
    def stateToBoard(state):
        board=[['0' for _ in range(4)] for _ in range(4)]
        stateArr=state.split('_')
        tempArr=[]
        for el in stateArr:
            sm=''
            for i in range(len(el)):
                if el[i]=='0':
                    sm+='0'
                else:
                    sm+=Orbito.players[int(el[i])-1]
            tempArr.append(sm)
        #print(stateArr)
        board[0][0]=tempArr[0][0]
        board[0][1]=tempArr[0][1]
        board[1][0]=tempArr[0][2]
        board[1][1]=tempArr[0][3]

        board[0][3]=tempArr[1][0]
        board[1][3]=tempArr[1][1]
        board[0][2]=tempArr[1][2]
        board[1][2]=tempArr[1][3]

        board[3][3]=tempArr[2][0]
        board[3][2]=tempArr[2][1]
        board[2][3]=tempArr[2][2]
        board[2][2]=tempArr[2][3]

        board[3][0]=tempArr[3][0]
        board[2][0]=tempArr[3][1]
        board[3][1]=tempArr[3][2]
        board[2][1]=tempArr[3][3]

        return board


    @staticmethod
    def rotateBoard(board,mode='antiClockWise'):
        if mode == 'antiClockWise':
            temp=board[0][0]
            board[0][0]=board[0][1]
            board[0][1]=board[0][2]
            board[0][2]=board[0][3]

            board[0][3]=board[1][3]
            board[1][3]=board[2][3]
            board[2][3]=board[3][3]

            board[3][3]=board[3][2]
            board[3][2]=board[3][1]
            board[3][1]=board[3][0]

            board[3][0]=board[2][0]
            board[2][0]=board[1][0]
            board[1][0]=temp

            temp=board[1][1]
            board[1][1]=board[1][2]
            board[1][2]=board[2][2]
            board[2][2]=board[2][1]
            board[2][1]=temp
        return board
    
    @staticmethod 
    def rotateCurrentBoard(mode='antiClockWise'):
        Orbito.rotateBoard(Orbito.currentBoard,mode=mode)
        
    def playMove(self,action):
        if len(action)==1:
            indexI=Orbito.hexToDec[action]//len(Orbito.currentBoard)
            indexJ=Orbito.hexToDec[action]%len(Orbito.currentBoard)
            Orbito.currentBoard[indexI][indexJ]=self.playerSymbol
        else:
            From=Orbito.hexToDec[action[0]]
            indexI=From//len(Orbito.currentBoard)
            indexJ=From%len(Orbito.currentBoard)
            smb= Orbito.currentBoard[indexI][indexJ]
            Orbito.currentBoard[indexI][indexJ]='0'

            To=Orbito.hexToDec[action[1]]
            indexI=To//len(Orbito.currentBoard)
            indexJ=To%len(Orbito.currentBoard)
            Orbito.currentBoard[indexI][indexJ]=smb

            place=Orbito.hexToDec[action[2]]
            indexI=place//len(Orbito.currentBoard)
            indexJ=place%len(Orbito.currentBoard)
            Orbito.currentBoard[indexI][indexJ]=self.playerSymbol

        Orbito.rotateCurrentBoard()
    
    def possibleActionInCurrentBoard(self):
        possSingleAction=[]
        for i in range(len(Orbito.currentBoard)):
            for j in range(len(Orbito.currentBoard)):
                if self.currentBoard[i][j]=='0':
                    action=Orbito.decToHex[len(Orbito.currentBoard)*i + j]
                    possSingleAction.append(action)
        
        possMovingAction=[]
        for i in range(len(Orbito.currentBoard)):
            for j in range(len(Orbito.currentBoard)):
                if self.currentBoard[i][j]!='0' and self.currentBoard[i][j]!=self.playerSymbol:
                    From=Orbito.decToHex[len(Orbito.currentBoard)*i + j]
                    if j!=0 and Orbito.currentBoard[i][j-1]=='0':
                        To=Orbito.decToHex[len(Orbito.currentBoard)*i + (j-1)]
                        possMovingAction.append(From+To)
                    if i!=0 and Orbito.currentBoard[i-1][j]=='0':
                        To=Orbito.decToHex[len(Orbito.currentBoard)*(i-1) + (j)]
                        possMovingAction.append(From+To)
                    if j!=3 and Orbito.currentBoard[i][j+1]=='0':
                        To=Orbito.decToHex[len(Orbito.currentBoard)*i + (j+1)]
                        possMovingAction.append(From+To)
                    if j!=3 and Orbito.currentBoard[i+1][j]=='0':
                        To=Orbito.decToHex[len(Orbito.currentBoard)*(i+1) + (j)]
                        possMovingAction.append(From+To)    
        
        possAction=[]
        for el1 in possSingleAction:
            for el2 in possMovingAction:
                if el2[1]!=el1:
                    possAction.append(el2+el1)
        
        for el in possMovingAction:
            possAction.append(el+el[0])
        
        return possAction+possSingleAction
    
    @staticmethod
    def checkIfFourMatches(board,playerSymbol):
        for i in range(4):
            if board[i][0]==playerSymbol and board[i][1]==playerSymbol and board[i][2]==playerSymbol and board[i][3]==playerSymbol:
                return True
            if board[0][i]==playerSymbol and board[1][i]==playerSymbol and board[2][i]==playerSymbol and board[3][i]==playerSymbol:
                return True
    
        if board[0][0]==playerSymbol and board[1][1]==playerSymbol and board[2][2]==playerSymbol and board[3][3]==playerSymbol:
            return True
    
        if board[0][3]==playerSymbol and board[1][2]==playerSymbol and board[2][1]==playerSymbol and board[3][0]==playerSymbol:
            return True

        return False
    
    @staticmethod
    def checkForVerdict(board):
        
        plr1Won=Orbito.checkIfFourMatches(board,Orbito.players[0])
        plr2Won=Orbito.checkIfFourMatches(board,Orbito.players[1])

        if plr1Won and plr2Won:
            return 'D'
        
        if plr1Won and (not plr2Won):
            return Orbito.players[0]
        
        if plr2Won and (not plr1Won):
            return Orbito.players[1]
        
        for el in board:
            if '0' in el:
                return None

        for _ in range(5):
            board=Orbito.rotateBoard(board)
            plr1Won=Orbito.checkIfFourMatches(board,Orbito.players[0])
            plr2Won=Orbito.checkIfFourMatches(board,Orbito.players[1])
            if plr1Won and (not plr2Won):
                return Orbito.players[0]
            elif plr2Won and (not plr1Won):
                return Orbito.players[1]
            else:
                pass
        
        return 'D'
    
    def moveAndCheckForVerdict(self,action):
        self.playMove(action)
        verdict=Orbito.checkForVerdict(Orbito.currentBoard)
        if verdict=='D':
            Orbito.done=True
        if verdict!='D' and verdict!=None:
            Orbito.winnerPlayerSymbol=verdict

    def takeActionBasedOnPolicy(self):
        state=Orbito.currentBoardToState()
        if self.stateValues.get(state)==None:
            possAction=self.possibleAction()
        else:
            possAction=None
        action=self.suggestActionBasedOnPolicy(state,possAction)
        self.moveAndCheckForVerdict(action)
        return action
    
    @staticmethod
    def returnWinningMove(board,playerSymbol):
        pass
        
    def returnRandomState():
        pass

    

            

        
        



    


        


        


    
