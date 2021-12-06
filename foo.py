import sys
import collections
import numpy as np
FILE_NAME = 'maze.txt'

class Node:
    def __init__(self, row, col, dir, c, name, color):
        self.name = name
        self.adjList = []
        self.revList = []
        self.color = color
        self.row = row - 1
        self.col = col - 1
        self.direction = dir
        self.if_circle = True if c == 'C' else False

    def __str__(self):
        return f'[{self.name}, ({self.row + 1}, {self.col + 1})]'

def create_adj_list(node, matrix, transposed_matrix):
    if node.direction == 'N':
        for i in transposed_matrix[node.col]:
            if node.color != i.color and i.row < node.row: node.adjList.append(i)
        return
            
    if node.direction == "S":
        for i in transposed_matrix[node.col]:
            if node.color != i.color and i.row > node.row: node.adjList.append(i)
        return

    if node.direction == 'E':
        for i in matrix[node.row]:
            if node.color != i.color and i.col > node.col: node.adjList.append(i)
        return

    if node.direction == 'W':
        for i in matrix[node.row]:
            if node.color != i.color and i.col < node.col: node.adjList.append(i)
        return

    temp = matrix
    temp = np.array(matrix)

    if node.direction == 'NE':
        diag = np.flipud(temp).diagonal(offset=(node.col - node.row))
        for i in diag:
            if node.color != i.color and i.row < node.row and i.col > node.col: node.adjList.append(i)

    if node.direction == 'NW':
        diag = np.diagonal(temp, offset=(node.col - node.row))
        for i in diag:
            if node.color != i.color and i.row < node.row and i.col < node.col: node.adjList.append(i)

    if node.direction == 'SE':
        diag = np.diagonal(temp, offset=(node.col - node.row))
        for i in diag:
            if node.color != i.color and i.row > node.row and i.col > node.col: node.adjList.append(i)  

    if node.direction == 'SW':
        diag = np.diagonal(np.rot90(temp), offset=-temp.shape[1] + (node.col + node.row) + 1)
        for i in diag:
            if node.color != i.color and i.row > node.row and i.col < node.col: node.adjList.append(i)    


def create_back_adj_list(node, matrix, transposed_matrix):
    if node.direction == "N":
        for i in transposed_matrix[node.col]:
            if node.color != i.color and i.row > node.row: node.revList.append(i)
        return

    if node.direction == "E":
        for i in matrix[node.row]:
            if node.color != i.color and i.col < node.col: node.revList.append(i)
        return

    if node.direction == "S":
        for i in transposed_matrix[node.col]:
            if node.color != i.color and i.row < node.row: node.revList.append(i)
        return

    if node.direction == "W":
        for i in matrix[node.row]:
            if node.color != i.color and i.col > node.col: node.revList.append(i)
        return

    temp = matrix
    temp = np.array(matrix)

    if node.direction == "NW":
        diag = np.diagonal(temp, offset=(node.col - node.row))
        for i in diag:
            if node.color != i.color and i.row > node.row and i.col > node.col: node.revList.append(i)

    if node.direction == "SW":
        diag = np.diagonal(np.rot90(temp), offset=-temp.shape[1] + (node.col + node.row) + 1)
        for i in diag:
            if node.color != i.color and i.row < node.row and i.col > node.col: node.revList.append(i)

    if node.direction == "NE":
        diag = np.diagonal(np.rot90(temp), offset=-temp.shape[1] + (node.col + node.row) + 1)
        for i in diag:
            if node.color != i.color and i.row > node.row and i.col < node.col: node.revList.append(i)

    if node.direction == "SE":
        diag = np.diagonal(temp, offset=(node.col - node.row))
        for i in diag:
            if node.color != i.color and i.row < node.row and i.col < node.col: node.revList.append(i)


def BFS(matrix, visited, rev_visited):

    # create a queue and append the start position to it
    queue = []
    queue.append([matrix[0][0]])

    # initialzie a variable to keep track of whether to iterate
    # forwards or backwards 
    reversed = False
    
    # continue BFS till the queue is empty - keeping track of 
    # whether or not the we are iterating forwards or backwards
    while queue:

        # grab the node at the front of the queue & add
        # that node to the path 
        path = queue.pop(0)
        node = path[-1]

        # determine if one is traversing forward or backwards
        for node in path:
            if node.if_circle:
                reversed = not reversed

        # if we are reversed iterate through reversed adj. list
        if reversed:

            for rev_neighbor in node.revList:
                
                # if the neighbor has not been visited, append it to the queue
                if rev_visited[rev_neighbor] == False: 
                    temp_path = list(path)
                    temp_path.append(rev_neighbor)
                    queue.append(temp_path)
                
                # If the current node is the end of the maze - exit & 
                # return the path from the start pos. to the end.
                if rev_neighbor.name == 'XX':
                    return temp_path

        else:

            # iterate through the node's neighbors, creating a temp var
            # to act as the path - removing the node if the end is not found
            for neighbor in node.adjList:

                # if the neighbor has not been visited, append it to the queue
                if visited[node] == False:
                    temp_path = list(path)
                    temp_path.append(neighbor)
                    queue.append(temp_path)

                # If the current node is the end of the maze - exit & 
                # return the path from the start pos. to the end.
                if neighbor.name == 'XX':
                    temp_path.append(neighbor)
                    return temp_path

        # set visited at the node to true 
        if node.if_circle and reversed:
            visited[node] = True
        elif not node.if_circle and reversed:
            rev_visited[node] = True
        else:
            visited[node] = True

        # reset the reversed variable
        reversed = False

    # if no solution return nothing
    return


if __name__ == '__main__':
    num_rows, num_cols = 0, 0
    matrix = []
    visited = {
        'nodes': [],
        'found': []
    }
    rev_visited = {
        'nodes': [],
        'found': []
    }

    # open and read contents of the file
    with open(FILE_NAME, 'r') as file:

        # read in number of rows and columns
        init_line = file.readline().split()
        num_rows = int(init_line[0])
        num_cols = int(init_line[1])

        # create matrix
        matrix = [[0 for i in range(num_cols)] for j in range(num_rows)]

        # iterate through rest of input file
        for line in file.readlines():
            to_read = line.split()
            row_tmp = int(to_read[0])
            col_tmp = int(to_read[1])
            temp_node = Node(row_tmp, col_tmp, to_read[4], to_read[3], to_read[2] + to_read[4], to_read[2])
            matrix[row_tmp - 1][col_tmp - 1] = temp_node

    # create the graph representation both traversing forwards
    # & traversing backwards if it is a circle
    transposed_matrix = np.transpose(matrix)
    for row in matrix:
        for node in row:
            create_adj_list(node, matrix, transposed_matrix)
            create_back_adj_list(node, matrix, transposed_matrix)

            # dictionaries to keep track of which nodes have been 
            # visited both forwards and backwards
            visited[node] = False
            rev_visited[node] = False
    

    # Call BFS
    sol = BFS(matrix, visited, rev_visited)

    # print the solution
    if sol:
        for i in sol:
            print(f'({i.row + 1}, {i.col + 1})', end=' ')
