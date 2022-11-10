#! /usr/bin/env python3
import sys


# Class for a NFA
class NFA:
    # Constructor
    def __init__(self, name, states, chars, start, finals, graph):
        self.name = name.strip('\n') 
        self.states = states
        self.chars = chars
        self.start = start.strip('*')
        self.finals = set([f.strip('*') for f in finals])
        self.graph = graph

        self.accepted = []
        self.leaf_nodes = 0

    # printer for debugging
    def nfa_print(self):
        print({"name":self.name, "states":self.states, "chars":self.chars, "start":self.start, "finals":self.finals, "graph":self.graph})

    # recursivley trace a NFA for a given string
    def nfa_trace_r(self, string, path, state):
        path.append(state)

        #base case, if string empty path is done and check if accepting
        if len(string) == 0:
            self.leaf_nodes += 1
            if state in self.finals:
                self.accepted.append(path)
        else:
            # if no where to go, state will not be in in graph
            if state not in self.graph:
                return
            for char in self.graph[state]:
                if char == string[0] or char == '~':
                    s = string[1:] if char != '~' else string
                    for next_state in self.graph[state][char]:
                        self.nfa_trace_r(s, path.copy(), next_state)
    
    # base trace funtion
    def nfa_trace(self, string):
        start = self.start
        path = []
        self.nfa_trace_r(string, path, start)
        self.nfa_output(string)

    # print output to a file that is named based on the name given from input file
    def nfa_output(self, string):
        file_name = self.name.split(' ')[0].split('.')[0]
        file_name = f'{file_name}_output.csv'
        fout = open(file_name, 'w')

        fout.write('Input:\n')
        fout.write('-------------------------------------\n')
        fout.write(f'{self.name}\n')
        fout.write(",".join(self.states) + '\n')
        fout.write(",".join(self.chars) + '\n')
        fout.write(f'{self.start}\n')
        fout.write(",".join(self.finals) + '\n')
        for name in self.graph.keys():
            for char in self.graph[name]:
                for state in self.graph[name][char]:
                    fout.write(f'{name},{char},{state}\n')
        fout.write('=====================================\n')
        fout.write('Output:\n')
        fout.write('-------------------------------------\n')
        fout.write(f'Output from {self.name} on {string}\n')
        fout.write(f'Leaf Nodes: {self.leaf_nodes}\n')
        fout.write(f'Number of accepting states: {len(self.accepted)}\n')
        for i, path in enumerate(self.accepted):
            fout.write(f'Path {i}: {path}\n')

        fout.close()

# Read in a graph
def read_graph(fin):
    graph = {}

    while(line := fin.readline().strip('\n,')):
        name, char, state = line.split(',')

        # remove s '*'
        if name[0] == '*':
            name = name[1:]

        if state[0] == '*':
            state = state[1:]

        if name not in graph:
            graph[name] = {char : [state] }
        else:
            if char not in graph[name]:
                graph[name][char] = [state]
            else:
                graph[name][char].append(state)
            
    return graph

# create and return a NFA object
def read_NFA(filename):

    fin = open(filename, 'r')
        # headers
    name = fin.readline().split(',')[0]
    states = fin.readline().strip('\n,').split(',')
    chars = fin.readline().strip('\n,').split(',')
    start = fin.readline().split(',')[0]
    finals = fin.readline().strip('\n,').split(',')

    graph = read_graph(fin)

    fin.close()

    return NFA(name, states, chars, start, finals, graph)

def main():
    # run by giving a filename and the string to trace
    if(len(sys.argv) != 3):
        print("./trace-bwisema3.py $filename $string_to_trace")
        return

    NFA = read_NFA(sys.argv[1])
    NFA.nfa_trace(sys.argv[2])


if __name__ == "__main__":
    main()
