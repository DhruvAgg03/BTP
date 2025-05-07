'''
Code that accepts an adjacenecy matrix as input and returns a matching
It simulates RANKING on a set of alpha,beta graphs
'''

import random
import numpy as np
from math import floor
import concurrent.futures
import csv

class RANKING:
    '''
    alpha<beta<1
    '''
    def __init__(self, alpha, beta, n):
        self.n = n
        self.alpha = alpha
        self.beta = beta
        self.adj = self.generateAdjMatrix(alpha,beta,n)

    def generateAdjMatrix(self,alpha,beta,n):
        # Generates required adjacency matrix from alpa,beta and n
        adj = [[0 for i in range(n)] for j in range(n)]
        lowerBound = floor(alpha*n)-1
        upperBound = floor(beta*n)-1
        for row in range(lowerBound):
            adj[row][row] = 1
            for col in range(lowerBound,upperBound+1):
                adj[row][col] = 1
        for row in range(lowerBound,upperBound+1):
            adj[row][row] = 1
            for col in range(upperBound+1,n):
                adj[row][col] = 1
        for row in range(upperBound+1,n): adj[row][row] = 1
        return adj

    def getPermutation(self,n):
        numbers = list(range(0, n)) 
        random.shuffle(numbers)
        return numbers #returns a list with 0,..n-1 randomly shuffled
    
    def performGreedy(self,adj):
        # performs greedy on a given adjacency matrix and returns the size of the generated matching
        # Assumes that arriving vertices are columns, in given order
        # Arbitrary ranks are same as ranks of rows
        # This implementation is inefficient. Might improve it later - > Currently takes O(n^2)
        # adj gets corrupted on executing this function
        matchCount = 0
        n = len(adj)
        for arrivingVtx in range(n):
            for fixedVtx in range(n):
                if adj[fixedVtx][arrivingVtx] == 1:
                    matchCount += 1
                    # print(f"Matched {arrivingVtx} with {fixedVtx}")
                    for remainingVtx in range(arrivingVtx,n):
                        adj[fixedVtx][remainingVtx] = 2
                    break
        
        return matchCount
    
    def simulateRANKING(self):
        # runs one random instance of RANKING
        arrivalOrder = self.getPermutation(self.n)
        ranks = self.getPermutation(self.n)
        copiedMatrix = list(map(list,self.adj))
        # print(copiedMatrix)
        copiedMatrix = [copiedMatrix[i] for i in ranks] # shuffling rows
        copiedMatrix = [[row[j] for j in arrivalOrder] for row in copiedMatrix] # shuffling columns
        # print(copiedMatrix)
        matchingSize = self.performGreedy(copiedMatrix)
        # print(f"Obtained matching of size {matchingSize}")
        return matchingSize

    def findExpectedValue(self,numRuns):
        # Repeatedly runs simulate RANKING, returns average of all values
        with concurrent.futures.ThreadPoolExecutor() as executor:
            matchingSizes = list(executor.map(lambda _: self.simulateRANKING(), [None] * numRuns))
        expectedSize = sum(matchingSizes) / len(matchingSizes)
        return expectedSize/self.n

if __name__ == "__main__":

    outputFile = "results.csv"
    n = 10000
    numIterations = 2500
    with open(outputFile, mode="a", newline="") as file:
        writer = csv.writer(file)
        file.seek(0, 2)  # Move to the end of the file to check if it's empty
        if file.tell() == 0:
            writer.writerow(["Alpha", "Beta","n","Num Iterations","Avg Value"])  # Write header if file is empty
        
        for alpha in [0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35]:
            for beta in [0.65,0.66,0.67,0.68,0.69,0.70,0.71,0.72,0.73,0.74,0.75]:
                ranking = RANKING(alpha,beta,n)
                avgValue = ranking.findExpectedValue(numIterations)
                print(f"Obtained {avgValue} for {alpha},{beta}")
                writer.writerow([alpha,beta,n,numIterations,avgValue])
                file.flush()
                beta += 0.1
