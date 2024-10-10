import heapq
import time
from collections import deque


# Function to check if a permutation is sorted
def is_sorted(perm):
    return perm == sorted(perm)


# Function to reverse a sublist in the permutation
def reverse_segment(perm, i, j):
    new_perm = perm[:i] + perm[i:j + 1][::-1] + perm[j + 1:]
    return new_perm

# BFS function
def bfs_sort_by_reversal(start_perm):
    # Initialize the goal state
    queue = deque([(start_perm, [])])

    visited = set()
    visited.add(tuple(start_perm))

    total_states_visited = 0
    max_queue_size = 0
    start_time = time.time()

    # BFS
    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        current_perm, current_path = queue.popleft()
        total_states_visited += 1

        # If current_perm is sorted then return the solution
        if is_sorted(current_perm):
            end_time = time.time()
            return {
                "moves": current_path,
                "total_states_visited": total_states_visited,
                "max_queue_size": max_queue_size,
                "cpu_time": end_time - start_time
            }

        # Generate all possible children (reversing any segment of the permutation)
        n = len(current_perm)
        for i in range(n):
            for j in range(i + 1, n):
                new_perm = reverse_segment(current_perm, i, j)
                if tuple(new_perm) not in visited:
                    visited.add(tuple(new_perm))
                    queue.append((new_perm, current_path + [(i, j)]))  # Record the move

def inOrder(numbers):
    for num in range(len(numbers) - 1):
        if numbers[num] > numbers[num + 1]:
            return False
    return True

def dls(numbers):
    limit = 1
    result, path, nodes = dls_sort(numbers, limit)
    total_nodes = nodes
    while not(result):
        limit += 1
        result, path, nodes = dls_sort(numbers, limit)
        total_nodes += nodes
    return {
        "moves": path,
        "total_states_visited": nodes,
        "result": True
    }


def dls_sort(numbers, limit):
    if inOrder(numbers):
        return True, [numbers], 1
    if limit == 0:
        return False, [], 1
    cutoff = False
    nodesVisited = 0
    for switchIndex in range(len(numbers)):
        for blockLength in range(2, len(numbers) - switchIndex + 1):
            newNode = numbers.copy()
            newNode[switchIndex:switchIndex + blockLength] = reversed(newNode[switchIndex:switchIndex + blockLength])
            result, path, nodes = dls_sort(newNode, limit-1)
            nodesVisited += nodes
            if len(path) == 0:
                cutoff = True
            if result:
                path.append(numbers)
                return result, path, nodesVisited
    if cutoff:
        return False, [], nodesVisited
    return False, numbers, nodesVisited

def heuristic(numbers):
    h = 0
    for i in range(len(numbers) - 1):
        diff = numbers[i] - numbers[i + 1]
        if diff != 1 and diff != -1:
            h += 1
    return h / 2

def astar_sort(numbers):
    queue = []
    n = len(numbers)
    heapq.heappush(queue, (heuristic(numbers), [numbers]))
    nodesVisited = 0
    start_time = time.time()
    while queue:
        item = heapq.heappop(queue)
        if is_sorted(item[1][-1]):
            end_time = time.time()
            return {"path": item[1], "nodes": nodesVisited,"time": end_time - start_time, "queue_size": len(queue)}
        for i in range(n):
            for j in range(i + 1, n):
                nodesVisited += 1
                new_perm = reverse_segment(item[1][-1], i, j)
                heapq.heappush(queue, (item[0] + heuristic(new_perm), item[1] + [new_perm]))
                heapq.heapify(queue)



if __name__ == "__main__":
    # Example input: 1 3 5 7 9 2 4 6 8 10
    input_perm = list(map(int, input("Enter the permutation: ").split()))

    # Run bfs_sort_by_reversal
    result = bfs_sort_by_reversal(input_perm)
    #
    # # Print results
    print("Breadth First Search")
    print(f"Number of Moves to Sort: {len(result['moves'])}")
    print("The path from start state to the goal state:")
    path = input_perm.copy()
    print(input_perm)
    for move in result['moves']:
        path = reverse_segment(path, move[0], move[1])
        print(path)
        # print(f"Reverse segment from {move[0]} to {move[1]}")

    print(f"The total number of states visited was {result['total_states_visited']}")
    print(f"The max size of the queue was {result['max_queue_size']}")
    print(f"The total CPU time was {result['cpu_time']:.4f} seconds")

    result = astar_sort(input_perm)
    print("\n\nA*-Search")
    print(f"Number of Moves to Sort: {len(result['path']) - 1}")
    print("The path from start state to the goal state:")
    path = input_perm.copy()
    for move in result['path']:
        print(move)
        # print(f"Reverse segment from {move[0]} to {move[1]}")

    print(f"The total number of states visited was {result['nodes']}")
    print(f"The max size of the queue was {result['queue_size']}")
    print(f"The total CPU time was {result['time']:.4f} seconds")

    start = time.time()
    result = dls(input_perm)
    end = time.time()
    print("\n\nIterative Deepening Search")
    print(f"Number of Moves to Sort: {len(result['moves']) - 1}")
    print("The path from start state to the goal state:")
    path = input_perm.copy()
    for move in reversed(result['moves']):
        print(move)
        # print(f"Reverse segment from {move[0]} to {move[1]}")

    print(f"The total number of states visited was {result['total_states_visited']}")
    print(f"The total CPU time was {end - start:.4f} seconds")