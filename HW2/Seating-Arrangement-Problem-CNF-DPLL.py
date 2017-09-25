import copy

text = list()
guestlist = list()
dict_friend = dict()
dict_enemy = dict()
keyF = 'F'
keyE = 'E'

file = open('input.txt','r')
text = file.readline().split()
guest = text[0]
table = int(text[1])

for line in file:
    guestlist = line.split()
    if (guestlist == []):
        continue

    elif guestlist[2] == 'F':
        dict_friend[guestlist[0],guestlist[1]]=(keyF)

    elif guestlist[2] == 'E':
        dict_enemy[guestlist[0],guestlist[1]]=(keyE)

file.close()
m = int(guest)
n = int(guest)

def create_matrix(m, n):
    return [[0]*n for _ in xrange(m)]
matR = create_matrix(m,n)

for key,val in dict_friend.iteritems():
        if val == 'F':
            x = int(key[0])
            y = int(key[1])
            matR[x-1][y-1]= 1

for key,val in dict_enemy.iteritems():
        if val == 'E':
            x = int(key[0])
            y = int(key[1])
            matR[x-1][y-1]= -1

#CNF Model
clauses = list()
rule = list()
CNF = set()

#CNF model - RULE 1 AND[(!Xai OR !Xaj)] where 1 <= i<j <= N , OR[(Xai)] if N===1
for i in range(0,m):
    if table == 1:
            rule = list()
            rule.append(str(i + 1) + str("-") + str(1))
            clauses.append(sorted(rule))

    if table > 1:
            rule1 = list()
            for tab in range(0,table):
                rule1.append(str(i+1)+str("-")+str(tab+1))
            clauses.append(sorted(rule1))

            for tab1 in range(0,table):
                for tab2 in range(tab1+1,table):
                    rule1 = list()
                    rule1.append(str("!") +str(i+1)+ str("-") +str(tab1+1))
                    rule1.append(str("!") +str(i+1)+ str("-") +str(tab2+1))
                    clauses.append(sorted(rule1))

CNF = CNF.union(tuple(x)for x in clauses)

#CNF model - RULE 2 AND[(!Xai OR Xbi) AND (Xai OR !Xbi)] where 1 <= i <= N
for i in range(0,m):
    for j in range(0,m):
        if matR[i][j]==1:
            for tab in range(0,table):
                rule2 = list()
                rule2.append(str("!")+str(i+1)+str("-")+str(tab+1))
                rule2.append(str(j+1)+str("-")+str(tab+1))
                clauses.append(sorted(rule2))

            for tab in range(0,table):
                rule2 = list()
                rule2.append(str(i+1)+str("-")+str(tab+1))
                rule2.append(str("!")+str(j+1)+str("-")+str(tab+1))
                clauses.append(sorted(rule2))

CNF = CNF.union(tuple(x) for x in clauses)

#CNF model - RULE 3 AND[(!Xai OR !Xbi)] where 1 <= i <= N
for i in range(0,m):
    for j in range(0,m):
        if matR[i][j]== -1:
            for tab in range(0,table):
                rule3 = list()
                rule3.append(str("!")+str(i+1)+str("-")+str(tab+1))
                rule3.append(str("!")+str(j+1)+str("-")+str(tab+1))
                clauses.append(sorted(rule3))

CNF = CNF.union(tuple(x) for x in clauses)
new = set()
new = CNF
symbols= set()

def inspect_literal(literal):
    if (literal[0]=="!"):
        literal=(literal[1:])
        return literal, False
    else :
        return literal, True

def find_compliment(literal):
    if (literal[0]=="!"):
        literal=(literal[1:])
        return literal
    else :
        literal = (str("!")+literal)
        return literal

def disj(clause):
    temp = set()
    if(len(clause)==1):
        return clause
    for c in clause:
        temp.add(c)
    return temp

for i in new:
    if len(i)==1:
        P, val = inspect_literal(i)
        if val == True:
            symbols = symbols.union(i)
    elif len(i)>1:
        for j in i:
            P, val = inspect_literal(j)
            if val == True:
                symbols.add(j)

def unit_clause_assign(clause, model):
    P, value = None, None
    for literal in clause:
        sym, val = inspect_literal(literal)
        if sym in model:
            if model[sym] == val:
                return None, None
        elif P:
            return None, None
        else:
            P, value = sym, val
    return P, value

def find_unit_clause(clauses, model):
    for clause in clauses:
        P, value = unit_clause_assign(clause, model)
        if P:
            return P, value
    return None, None

def find_pure_symbol(symbols, clauses):
    for s in symbols:
        found_pos, found_neg = False, False
        for c in clauses:
            if not found_pos and s in disj(c):
                found_pos = True
            if not found_neg and ("!")+s in disj(c):
                found_neg = True
        if found_pos != found_neg:
            return s, found_pos
    return None, None

def evaluate(clause,model): #c is in CNF set, model as dictionary
      if model == {}:
          return None
      else:
          count = 0
          for c in disj(clause):
              if c in model:
                  if model[c] == True:
                      return True
                  else:
                      count+=1
              else:
                P = find_compliment(c)
                if P in model:
                      if model[P]== False:
                          return True
                      elif model[P]== True:
                          count+=1
                else:
                     continue
          if (count==len(clause)):
              return False
          else:
              return None

def removeP(P,symbols): #P as set, symbols as set
    symbolsN = copy.copy(symbols)
    new_symbols = set()
    for sym in symbolsN:
            if sym!=P:
                new_symbols.add(sym)
    return new_symbols

def extend_model(model,P,val): #P,val as sets, model as dictionary
    modelC = copy.copy(model)
    modelC[P]=val
    return modelC

def dpll(clauses, symbols, model):
    unknown_clauses = set()
    for c in clauses:
        val = evaluate(c, model)
        if val is False:
            return False
        if val is None:
            unknown_clauses.add(c)

    if not unknown_clauses:
        return model

    P, value = find_pure_symbol(symbols, unknown_clauses)
    if P!= None:
        return dpll(clauses, removeP(P, symbols), extend_model(model, P, value))

    P, value = find_unit_clause(clauses, model)
    if P!= None:
        return dpll(clauses, removeP(P, symbols), extend_model(model, P, value))

    temp = ()
    for sym in symbols:
        if sym != ():
            temp = sym
            break
    return (dpll(clauses, symbols, extend_model(model, temp, False)) or dpll(clauses, symbols, extend_model(model, temp, True)))

mod = dict()
ans = dpll(CNF,symbols,mod)

file = open("output.txt","w")
if ans == False or table==0:
    file.write("no")
    file.close()
else:
    file.write("yes")
    file.write("\n")
    answer = []
    for k,v in ans.iteritems():
        if v == True:
            answer.append(k)
    answer = sorted(answer)
    for a in answer:
        val = a.split("-")
        file.write(val[0]+" "+val[1]+"\n")