def cykAlgorithm(w,cnf):
    # cyk table
    n = len(w)
    cykTable = [[set([]) for j in range(n)] for i in range(n)]

    # Baris pertama cyk
    for i in range(0,n):
        for head, rule in cnf.items():
            for rhs in rule:
                if len(rhs) == 1 and rhs[0] == w[i]:
                    cykTable[i][i].add(head)

    # Baris kedua, dst
        for j in range(i, -1, -1):     
            for k in range(j, i):  
                for head, rule in cnf.items():
                    for rhs in rule:
                        if len(rhs) == 2 and rhs[0] in cykTable[j][k] and rhs[1] in cykTable[k + 1][i]:
                            cykTable[j][i].add(head)

    # output
    print(cykTable[0][n-1])
    if len(cykTable[0][n-1]) != 0:
        return True
    else:
        return False
