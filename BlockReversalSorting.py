from re import search


def main():
    numbers = [int(num) for num in input("Please enter sequence seperated by spaces: ").split(' ')]
    num, num1 = bfs_sort(numbers)
    print(num)
    print(num1)

def inOrder(numbers):
    for num in range(len(numbers) - 1):
        if numbers[num] > numbers[num + 1]:
            return False
    return True

def bfs_sort(numbers):
    searchTree = [numbers]
    nodesVisited = 1
    while not(inOrder(searchTree[0])):
        currNode = searchTree.pop(0)
        nodesVisited += 1
        for blockLength in range(2, len(numbers) + 1):
            for switchIndex in range(len(numbers) - blockLength + 1):
                newNode = currNode[0:switchIndex]
                reversedBlock = currNode[switchIndex:switchIndex + blockLength]
                reversedBlock.reverse()
                newNode += reversedBlock
                newNode += currNode[switchIndex + blockLength:]
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