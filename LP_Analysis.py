from scipy.optimize import linprog
from numpy import e as e
from numpy import log as lg
def getDesecVarBounds(n):
    bounds = []
    for _ in range(2*n):
        bounds.append((0,None))
    return bounds

def getObjectiveCoeffs(n):
    coeffs = []
    for _ in range(n):
        coeffs.append(1)
    for _ in range(n):
        coeffs.append(0)
    return coeffs

def getConstraintVector(n,epsilon):
    constraintCoeffs = []
    for _ in range(n):
        constraintCoeffs.append(epsilon*(2+lg(n))-1)
    for _ in range(n):
        constraintCoeffs.append(2*n*(n-1)*epsilon)
    return constraintCoeffs

def getConstraintRow_type1(n,t):
    constraint = []
    for i in range(n):
        constraint.append(-1 if i ==t else 0)

    for i in range(n):
        constraint.append(-1 if i < t else 0)
    return constraint

def getConstraintRow_type2(n,t):
    constraint = []
    for i in range(n):
        constraint.append(-1 if i<=t else 0)
    for i in range(n):
        constraint.append(n if i<=t else 0)
    return constraint

def constructConstraintMatrix(n):
    A = []
    for t in range(n):
        A.append(getConstraintRow_type1(n,t))
    for t in range(n):
        A.append(getConstraintRow_type2(n,t))
    return A

def solve(n,epsilon):
    try:
        c = getObjectiveCoeffs(n)
        A_ub = constructConstraintMatrix(n)
        b_ub = getConstraintVector(n,epsilon)
        results = linprog(c=c,A_ub=A_ub,b_ub=b_ub,bounds = getDesecVarBounds(n))
        if results.status == 0: 
            print(f'Achieved competitive ratio = {results.fun/n}')
        return results.fun/n
    except Exception as e:
        print("Could not solve lin prog")
        print(e)
        return None


if __name__=="__main__":
    output = [['n','e=0','e=0.0001','e=0.001','e=0.01','e=0.1']]
    for n in range(3,100):
        print(f"Testing for n = {n}")
        row = [n,solve(n,0),solve(n,0.0001),solve(n,0.001),solve(n,0.01),solve(n,0.1)]
        output.append(row)
    import csv
    with open('output.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output)
