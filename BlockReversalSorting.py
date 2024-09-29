from collections import deque


def main():
    numbers = [int(num) for num in input("Please enter sequence seperated by spaces: ").split(' ')]
    # numbers[1:4] = reversed(numbers[1:4])
    # print(numbers)
    num, num1 = bfs_sort(numbers)
    print(num)
    print(num1)

def inOrder(numbers):
    for num in range(len(numbers) - 1):
        if numbers[num] > numbers[num + 1]:
            return False
    return True

def bfs_sort(numbers):
    searchTree = deque([numbers])
    nodesVisited = 1
    while not(inOrder(searchTree[0])):
        currNode = searchTree.popleft()
        nodesVisited += 1
        for switchIndex in range(len(numbers)):
            startNode = currNode[0:switchIndex]
            for blockLength in range(2, len(numbers) - switchIndex + 1):
                if switchIndex == 0:
                    reversedBlock = currNode[switchIndex + blockLength - 1::-1]
                else:
                    reversedBlock = currNode[switchIndex + blockLength - 1:switchIndex - 1:-1]
                newNode = startNode + reversedBlock + currNode[switchIndex + blockLength:]
                searchTree.append(newNode)
    path = [searchTree[0]]
    branchingFactor = 0
    searchedNodes = nodesVisited
    for i in range(len(numbers) - 1):
        branchingFactor += i
    while nodesVisited != 0:
        offset = nodesVisited % branchingFactor
        nodesVisited //= branchingFactor
    path.reverse()
    return searchedNodes, path

main()