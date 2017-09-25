import copy

file = open('input.txt','r')
player = file.read(1)
d = file.read(2)
state= file.read()
input_mat = map(list,state.splitlines())
file.close()

maxDepth = int(d)

eval_mat = [[], [99,-8,8,6,6,8,-8,99],[-8,-24,-4,-3,-3,-4,-24,-8],[8,-4,7,4,4,7,-4,8], [6,-3,4,0,0,4,-3,6],
            [6,-3,4,0,0,4,-3,6],[8,-4,7,4,4,7,-4,8], [-8,-24,-4,-3,-3,-4,-24,-8],[99,-8,8,6,6,8,-8,99]]

def isOnBoard(x,y):
    return x>=1 and x<=8 and y>=0 and y<=7

final_lst = list()
def printlog(current,depth,val,alpha, beta):
    #file = open("output.txt","wa")
    curr = current
    d = depth
    eval = val
    a = alpha
    b = beta
    if (a == -1000):
        a = "-Infinity"
    if (b == 1000):
        b = "Infinity"
    if (eval == -1000):
        eval = "-Infinity"
    elif eval == 1000:
        eval = "Infinity"
    final_lst.append(current)
    final_lst.append(',')
    final_lst.append(d)
    final_lst.append(',')
    final_lst.append(eval)
    final_lst.append(',')
    final_lst.append(a)
    final_lst.append(',')
    final_lst.append(b)
    final_lst.append("\n")

def eval_func(matrix_new,tile):
    countX =0
    countO =0
    count =0
    for i in range(1,9):
        for j in range(0,8):
            if(matrix_new[i][j]=='X'):
                countX += eval_mat[i][j]
            if(matrix_new[i][j]=='O'):
                countO += eval_mat[i][j]

    if(tile=='O'):
        count = countX - countO
    else:
        count = countO - countX
    return count

def getDict(key_x,key_y,val,dict_mark):      #dict for marking
    dict_mark[key_x,key_y] = val

def isValidMove(board,tile, xstart, ystart,mark):
    if board[xstart][ystart] =='*' or not isOnBoard(xstart, ystart):
        return False

    if tile =='X':
        otherTile ='O'
    else :
        otherTile ='X'

    for xdir, ydir in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
        x,y = xstart,ystart
        count =0
        x += xdir
        y += ydir
        if not isOnBoard(x, y) or board[x][y] == tile:
            continue
        if isOnBoard(x,y) and board[x][y] == otherTile:
            x += xdir
            y += ydir
        if isOnBoard(x, y) and board[x][y] == '*':
            while isOnBoard(x,y) and board[x][y] != tile:
                count += 1
                x -= xdir
                y -= ydir
                if not isOnBoard(x,y) or board[x][y] == '*':
                    count =0
                    break
                else:
                    continue
        else:
            continue

        tilesToFlip = []
        if not isOnBoard(x,y):
            continue

        elif count>0 and board[x][y]==tile:
            #print count-1
            for i in range(0, count-1):
                x += xdir
                y += ydir
                tilesToFlip.append([x, y])
            #board[x+xdir][y+ydir]='V'
            #print tilesToFlip, x+xdir, y+ydir
            getDict(x+xdir,y+ydir,tilesToFlip,mark)

def copyState(orgState):
    newState= copy.deepcopy(orgState)
    return newState

alst = ['a','b','c','d','e','f','g','h']
#recursive DFS
def dfs(state,player,depth,level,aplha,beta,current,parent):

    if(level==1):
        evaluate= -1000
    else:
        evaluate = 1000

    markX={}
    markO={}

    if depth == maxDepth:
        evaluate = (eval_func(state,player))
        #print current,depth,evaluate,aplha,beta
        printlog(current,depth,evaluate,aplha,beta)
        return evaluate,state

    if(level==1):
        temp = -1000
        st_new = copyState(state)

        if player == 'X':
            for i in range(1, 9):
                for j in range(0,8):
                    if state[i][j]=='O':
                        isValidMove(state,player,i,j,markX)

            if not (parent == 'pass' and bool(markX) == 0):
                #print current, depth, temp, aplha, beta
                printlog(current,depth,temp,aplha,beta)

            if (bool(markX)== 0):   #pass cond.
                if parent=='pass':
                    evaluate = eval_func(state,'O')
                    #print current, depth, evaluate, aplha, beta
                    printlog(current,depth,evaluate,aplha,beta)
                    return evaluate, state
                next = 'pass'
                (eval,st) = dfs(st_new,'O',depth+1,0,aplha,beta,next,current)
                if temp < eval:
                    temp = eval
                if temp >= beta:
                    #print current, depth, temp, aplha, beta
                    printlog(current,depth,temp,aplha,beta)
                    return temp,st_new
                if aplha < temp:
                    aplha = temp
                #print current, depth, temp, aplha, beta
                printlog(current,depth,temp,aplha,beta)

            else:
             for key,val in sorted(markX.iteritems()):
                retainedState = copyState(state)
                next = alst[key[1]] + str(key[0])
                retainedState[key[0]][key[1]]= 'X'
                for i in val:
                    retainedState[i[0]][i[1]] = 'X'

                (eval,st) = dfs(retainedState,'O',depth+1,0,aplha,beta,next,current)
               # print 150, temp, eval
                if temp < eval:
                    temp = eval
                if temp >= beta:
                    #print current, depth, temp, aplha, beta
                    printlog(current, depth, temp, aplha, beta)
                    return temp,st_new
                if aplha < temp:
                    aplha = temp
                    st_new = copyState(retainedState)
                #print current, depth, temp, aplha, beta
                printlog(current, depth, temp, aplha, beta)

        else:
            for i in range(1, 9):
                for j in range(0,8):
                    if state[i][j]=='X':
                        isValidMove(state,player,i,j,markO)

            if not (parent == 'pass' and bool(markO) == 0):
                #print current, depth, temp, aplha, beta
                printlog(current, depth, temp, aplha, beta)

            if (bool(markO)== 0):
                if (parent=='pass'):
                    evaluate = eval_func(state,'X')
                    #print current, depth, evaluate, aplha, beta
                    printlog(current, depth, evaluate, aplha, beta)
                    return evaluate, state
                next = 'pass'
                (eval,st) = dfs(st_new,'X',depth+1,0,aplha,beta,next,current)
                #print 206, temp, eval
                if temp < eval:
                    temp = eval
                if temp >= beta:
                    #print current, depth, temp, aplha, beta
                    printlog(current, depth, temp, aplha, beta)
                    return temp,st_new
                if aplha < temp:
                    aplha = temp
                #print current, depth, temp, aplha, beta
                printlog(current, depth, temp, aplha, beta)

            else:
                for key,val in sorted(markO.iteritems()):
                    retainedState = copyState(state)
                    next = alst[key[1]] + str(key[0])
                    retainedState[key[0]][key[1]]= 'O'
                    for i in val:
                        retainedState[i[0]][i[1]] = 'O'

                    (eval,st) = dfs(retainedState,'X',depth+1,0,aplha,beta,next,current)
                    #print temp,eval
                    if temp < eval:
                        temp = eval
                    if temp >= beta:
                        #print current, depth, temp, aplha, beta
                        printlog(current, depth, temp, aplha, beta)
                        return temp, st_new
                    if aplha < temp:
                        aplha = temp
                        st_new = copyState(retainedState)
                    #print current, depth, temp, aplha, beta
                    printlog(current, depth, temp, aplha, beta)

    if (level == 0):
        temp = 1000
        st_new = copyState(state)

        if player == 'X':
            for i in range(1, 9):
                for j in range(0, 8):
                    if state[i][j] == 'O':
                        isValidMove(state, player, i, j, markX)

            if not (parent == 'pass' and bool(markX) == 0):
                #print current, depth, temp, aplha, beta
                printlog(current, depth, temp, aplha, beta)

            if (bool(markX) == 0):  # pass cond.
                if (parent=='pass'):
                    evaluate = eval_func(state,'O')
                    #print current, depth, evaluate, aplha, beta
                    printlog(current, depth, evaluate, aplha, beta)
                    return evaluate, state
                next = 'pass'
                (eval, st) = dfs(st_new,'O',depth+1,1,aplha,beta,next,current)
                #print 30 temp,eval
                if temp > eval:
                    temp = eval
                if temp <= aplha:
                     #print current, depth, temp, aplha, beta
                     printlog(current, depth, temp, aplha, beta)
                     return temp, st_new
                if beta > temp:
                    beta = temp
                #print current, depth, temp, aplha, beta
                printlog(current, depth, temp, aplha, beta)

            else:
                for key, val in sorted(markX.iteritems()):
                    retainedState = copyState(state)
                    next = alst[key[1]] + str(key[0])
                    retainedState[key[0]][key[1]] = 'X'
                    for i in val:
                        retainedState[i[0]][i[1]] = 'X'

                    (eval, st) = dfs(retainedState,'O',depth+1,1,aplha,beta,next,current)
                    #print 350, temp,eval
                    if temp > eval:
                        temp = eval
                    if temp <= aplha:
                        #print current, depth, temp, aplha, beta
                        printlog(current, depth, temp, aplha, beta)
                        return (temp, st_new)
                    if beta > temp:
                        beta = temp
                        st_new = copyState(retainedState)
                    #print current, depth, temp, aplha, beta
                    printlog(current, depth, temp, aplha, beta)

        else:
            for i in range(1, 9):
                for j in range(0, 8):
                    if state[i][j] == 'X':
                        isValidMove(state, player, i, j, markO)

            if not (parent == 'pass' and bool(markO) == 0):
                #print current, depth, temp, aplha, beta
                printlog(current, depth, temp, aplha, beta)

            if (bool(markO) == 0):
                if (parent=='pass'):
                    evaluate = eval_func(state,'X')
                    #print current, depth, evaluate, aplha, beta
                    printlog(current, depth, evaluate, aplha, beta)
                    return evaluate, state
                next = 'pass'
                (eval, st) = dfs(st_new, 'X', depth+1,1,aplha,beta,next,current)
                #print 403, temp, eval
                if temp > eval:
                    temp = eval
                if temp <= aplha:
                     #print current, depth, temp, aplha, beta
                     printlog(current, depth, temp, aplha, beta)
                     return (temp, st_new)
                if beta > temp:
                    beta = temp
                #print current, depth, temp, aplha, beta
                printlog(current, depth, temp, aplha, beta)

            else:
                for key, val in sorted(markO.iteritems()):
                    retainedState = copyState(state)
                    next = alst[key[1]] + str(key[0])
                    retainedState[key[0]][key[1]] = 'O'
                    for i in val:
                        retainedState[i[0]][i[1]] = 'O'
                    (eval, st) = dfs(retainedState, 'X', depth+1,1,aplha,beta,next,current)
                    #print 500, temp, eval
                    if temp > eval:
                        temp = eval
                    if temp <= aplha:
                         #print current, depth, temp, aplha, beta
                         printlog(current, depth, temp, aplha, beta)
                         return (temp, st_new)
                    if beta > temp:
                        beta = temp
                        st_new = copyState(retainedState)
                    #print current, depth, temp, aplha, beta
                    printlog(current, depth, temp, aplha, beta)

    #print current, depth, evaluate, aplha, beta
    return (temp,st_new)

aplha = -1000
beta = 1000
level =1 #max
depth = 0
(val,st) = dfs(input_mat,player,depth,level,aplha,beta,'root','null')

file = open('output.txt','w')
for i in st:
    if not("".join(map(str,i))== ""):
        file.write("".join(map(str,i)))
        file.write("\n")
file.write("Node,Depth,Value,Alpha,Beta")
file.write("\n")
for i in range(0,len(final_lst)):
    file.write(str(final_lst[i]))
file.close()