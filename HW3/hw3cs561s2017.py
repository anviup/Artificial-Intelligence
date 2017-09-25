import copy
fp = open("input11.txt", "r")
content = fp.read().split('******')
queryy = content[0].split("\n")
queryy.remove(str(''))
#print queryy
rules = content[1].split('***')
pd = list()
for r in rules:
    prob = r.split("\n")
    pd.append(prob)

def create_matrix(m, n):
    #print m, n
    return [[0]*n for _ in xrange(m)]

def convert_to_matrix(v):
    v.remove(str(''))
    if str('') in v:
        v.remove(str(''))
    #print v
    t = v[0].split(' | ')[0]
    top_sort = t

    head = v[0].split()
    if len(head) == 1:
        node = create_matrix(1, 1)
        if v[1] == "decision":
            node[0] = float(0.5)
        else:
            node[0] = float(v[1])
        return str(v[0]), node, top_sort

    else:
        ind = v[0].find('|')
        first = v[0][:ind - 1]
        last = v[0][ind + 2:]
        rest = last.split()

        if len(rest) > 0:
            index = list()
            for i in range(1, len(v)):
                index.append(v[i].split())
            node = create_matrix(len(v) - 1, len(rest)+1)
            for i in range(0, len(v) - 1):
                for j in range(0, len(rest)+1):
                    node[i][j] = index[i][j]

        return str(v[0]), node, top_sort

nodes = dict()
bn = dict()
parent = dict()
topological_sort = list()
for i in range(0, len(pd)):
    name, val, ts = convert_to_matrix(pd[i])
    n = name.split(' | ')[0]
    ind = name.split(' | ')
    nodes[name] = val
    bn[n] = val
    if len(ind) == 1:
        parent[n] = 'root'
    else :
        parent[n] = ind[1]
    topological_sort.append(ts)

#print topological_sort

utl_nodes = list()
util = dict()
if len(content)> 2:
    utility = content[2].split('\n')
    utility.remove(str(''))
    if str('') in utility:
        utility.remove(str(''))
    #print utility
    utl_nodes = utility[0].split()
    utl_mat = create_matrix(len(utility)-1,len(utl_nodes)-1)
    for i in range(0,len(utility)-1):
        index = utility[i+1].split()
        for j in range(0,len(utl_nodes)-1):
            utl_mat[i][j]= index[j]
    #print utl_mat
    util[utility[0]] = utl_mat

    for k,v in util.iteritems():
        tmp = k.split(' | ')
        parent[tmp[0]] = tmp[1]
        bn[tmp[0]]= v


def ip(Ynode,sign,evd):
    #print Ynode, sign, evd
    if Ynode in bn:
        Ymat = bn[Ynode]

    if len(Ymat) == 1:
        for y in Ymat:
            Yval = y
        #print Yval
        if sign == '+':
            return float(Yval)
        elif sign == '-':
            return float(1 - Yval)

    else:
        p = parent[Ynode]
        symbols = p.split()
        #print symbols

        sg = list()
        for s in symbols:
            if s in evd:
                pos = evd[s]
                sg.append(pos)
        #print sg

        for y1 in Ymat:
            tmp = y1[1:]
            #print tmp
            if tmp == sg:
                Yval = y1[:1]

        if sign == '+':
            #print float(Yval[0])
            return float(Yval[0])
        elif sign == '-':
            #print (1- float(Yval[0]))
            return 1 - float(Yval[0])


def all_events(variables, e):
    if not variables:
        yield e
    else:
        X, rest = variables[0], variables[1:]
        for e1 in all_events(rest, e):
            for x in ['+','-']:
                yield extend(e1, X, x)


def event_values(evd, variables):
    return tuple([evd[var] for var in variables])


def make_factor(var, e):
    node = bn[var] #matrix corresponding to var - in node
    temp = parent[var]
    parent_list = temp.split()
    variables = [X for X in [var] + parent_list if X not in e]
    cpt = {event_values(e1, variables) : ip(var,e1[var],e1) for e1 in all_events(variables,e)}
    return Factor(variables, cpt)


def pointwise_product(factors):
    return reduce(lambda f, g: f.pointwise_product(g), factors)


def sum_out(var, factors):
    result, var_factors = [], []
    for f in factors:
        (var_factors if var in f.variables else result).append(f)
    result.append(pointwise_product(var_factors).sum_out(var))
    return result

def extend(e,var,val):
    evd = copy.copy(e)
    evd[var]= val
    return evd

class Factor:
    def __init__(self, variables, cpt):
        self.variables = variables
        self.cpt = cpt

    def pointwise_product(self, other):
        variables = list(set(self.variables) | set(other.variables))
        cpt = {event_values(e, variables): self.p(e) * other.p(e)
               for e in all_events(variables, {})}
        return Factor(variables, cpt)

    def sum_out(self, var):
        variables = [X for X in self.variables if X != var]
        cpt = {event_values(e, variables): sum(self.p(extend(e, var, val)) for val in ['+','-'])
               for e in all_events(variables, {})}
        return Factor(variables, cpt)

    def p(self, e):
        return self.cpt[event_values(e, self.variables)]


def elimination_ask(evd, ts):
    #evd = copy.copy(e)
    factors = list()
    variables = ts
    for var in reversed(variables):
        factors.append(make_factor(var,evd))
        if var not in evd:
            factors = sum_out(var, factors)
    return pointwise_product(factors).cpt


def generate_combinations(size):
    permutes = list()
    if size==1:
        permutes.append('+')
        permutes.append('-')

    elif size==2:
        permutes.append('++')
        permutes.append('+-')
        permutes.append('-+')
        permutes.append('--')

    elif size ==3:
        permutes.append('+++')
        permutes.append('++-')
        permutes.append('+--')
        permutes.append('---')
        permutes.append('-+-')
        permutes.append('+-+')
        permutes.append('--+')
        permutes.append('-++')

    elif size ==4:
        permutes.append('++++')
        permutes.append('+++-')
        permutes.append('++-+')
        permutes.append('++--')
        permutes.append('+-++')
        permutes.append('+-+-')
        permutes.append('+--+')
        permutes.append('+---')
        permutes.append('-+++')
        permutes.append('-++-')
        permutes.append('-+-+')
        permutes.append('-+--')
        permutes.append('--++')
        permutes.append('--+-')
        permutes.append('---+')
        permutes.append('----')

    return permutes

fileW = open("output.txt","w")

def enumerate_eu(evidence,top_sort):
    probD = elimination_ask(evidence, top_sort)
    # print probD
    utl_parents = utl_nodes[2:]
    # print utl_parents
    tmp = list()
    for u in utl_parents:
        if u not in evidence:
            tmp.append(u)
    # print tmp
    combo_size = len(tmp)
    permutes = list()
    permutes = generate_combinations(combo_size)
    # print permutes
    probN = list()
    sum = 0
    evd = dict()
    for i in range(0, len(permutes)):
        evd = copy.copy(evidence)
        for j in range(0, combo_size):
            #print tmp[j], permutes[i][j]
            evd[tmp[j]] = permutes[i][j]
            #print evd
        probU = ip('utility', '+', evd)
        probN = (elimination_ask(evd, top_sort))
        p = float(probU * probN['+',])
        sum += p
    probEU = (float(sum / probD['+',]))
    return probEU

def calc_query(query,top_sort):
    if query[0] == 'P':
        #print query
        event = dict()
        evidence = dict()
        sent = query[2:len(query)-1]
        index = sent.split(' | ')
        var_evt = index[0].split(', ')
        #print var_evt
        for v in var_evt:
            temp = v.split(' = ')
            event[temp[0]] = temp[1]
        #print event
        if len(index)>1:
            #evidence = dict()
            var_evd = index[1].split(', ')
            #print var_evd
            for v in var_evd:
                temp = v.split(' = ')
                evidence[temp[0]]= temp[1]
                event[temp[0]]= temp[1]
        #print evidence
        #print event
        probD = elimination_ask(evidence,top_sort)
        #print probD
        probN = elimination_ask(event,top_sort)
        #print probN
        probP = float(probN['+',]/probD['+',])
        #print probP
        p = "%.2f" % round((probP+ 0.0001),2)
        fileW.write(str(p))
        fileW.write("\n")

    elif query[0] == 'E':
        #print ("\n")
        #print query
        evidence = dict()
        sent = query[3:len(query) - 1]
        index = sent.split(' | ')
        var_evt = index[0].split(', ')
        for v in var_evt:
            temp = v.split(' = ')
            evidence[temp[0]] = temp[1]
        if len(index) > 1:
            var_evd = index[1].split(', ')
            for v in var_evd:
                temp = v.split(' = ')
                evidence[temp[0]] = temp[1]
        #print evidence
        ans = enumerate_eu(evidence,top_sort)
        k = int(round(ans))
        fileW.write(str(k))
        fileW.write("\n")

    elif query[0] == 'M':
        #print ("\n")
        #print query
        evidence = dict()
        evt = dict()
        sent = query[4:len(query) - 1]
        index = sent.split(' | ')
        event = index[0].split(', ')
        #print event
        if len(index) > 1:
            var_evd = index[1].split(', ')
            for v in var_evd:
                temp = v.split(' = ')
                evidence[temp[0]] = temp[1]
                evt[temp[0]] = temp[1]
        #print evidence

        len_event = len(event)
        permutes = generate_combinations(len_event)
        #print permutes
        eu = list()
        for i in range(0,len(permutes)):
            for j in range(0,len_event):
                evt[event[j]] = permutes[i][j]
            #print evt
            p = enumerate_eu(evt,top_sort)
            eu.append(p)
        #print eu
        maxE = eu[0]
        p = 0
        for e in eu :
            if e > maxE:
                maxE = e
                p = eu.index(e)
        k = int(round(maxE))
        #print k, p
        for i in range(0,len(permutes)):
                if i == p:
                    ans = permutes[i]
        for a in range(0,len(ans)):
            fileW.write(str(ans[a])+str(' '))

        fileW.write(str(k))
        fileW.write("\n")

for q in queryy:
    calc_query(q,topological_sort)

fileW.close()