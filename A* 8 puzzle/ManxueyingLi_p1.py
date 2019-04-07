from queue import PriorityQueue

#representing state
class State(object):
    def __init__(self, initial, goal):
        self.initial = list(initial)
        self.goal = list(goal)

    def actions(self, state):
        actions_list = [] #list of all possible actions of this state
        ind_of_zero = state.index("0")

        if ind_of_zero == 0 or ind_of_zero == 1 or ind_of_zero == 2 or ind_of_zero == 3 or ind_of_zero == 4 or ind_of_zero == 5:
            actions_list.append("D")
        if ind_of_zero == 3 or ind_of_zero == 4 or ind_of_zero == 5 or ind_of_zero == 6 or ind_of_zero == 7 or ind_of_zero == 8:
            actions_list.append("U")
        if ind_of_zero == 7 or ind_of_zero == 6 or ind_of_zero == 4 or ind_of_zero == 3 or ind_of_zero == 1 or ind_of_zero == 0:
            actions_list.append("R")
        if ind_of_zero == 8 or ind_of_zero == 7 or ind_of_zero == 5 or ind_of_zero == 4 or ind_of_zero == 2 or ind_of_zero == 1:
            actions_list.append("L")
        return actions_list

    def result(self, state, action):
        after_action = list(state) #list of all possible states after action
        ind_of_zero = state.index("0")
        #swap two tile for each action
        if action == "R":
            after_action[ind_of_zero], after_action[ind_of_zero + 1] = after_action[ind_of_zero + 1], after_action[ind_of_zero]
        if action == "L":
            after_action[ind_of_zero], after_action[ind_of_zero - 1] = after_action[ind_of_zero - 1], after_action[ind_of_zero]
        if action == "D":
            after_action[ind_of_zero], after_action[ind_of_zero + 3] = after_action[ind_of_zero + 3], after_action[ind_of_zero]
        if action == "U":
            after_action[ind_of_zero], after_action[ind_of_zero - 3] = after_action[ind_of_zero - 3], after_action[ind_of_zero]
        return after_action

    def is_goal(self, state):#check if goal is reached
        if state == self.goal:
            return True
        else:
            return False

#representingt node in the search tree
class Node(object):
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.action = action
        self.state = list(state)
        self.parent = parent
        self.path_cost = path_cost

    def __repr__(self):
        return "Node {}".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, state): #expand this node -> move one step further in the search tree
        return [self.child_node(state, action)
                for action in state.actions(self.state)]#return the list of possible states of one step further

    def child_node(self, state, action): #return the child node
        next = state.result(self.state, action)
        return Node(next, self, action, self.path_cost+1)

    def solution_path(self):#the path to get to this node
        node, path = self, []
        cost = 0
        while node:
            if node.action is not None:
                path.append(node.action)
            node = node.parent
            cost += 1
        # print(cost,self.path_cost)
        return list(reversed(path)) #give the path in correct order(from the root to goal)

    def eval_val_lst(self):#the list of values of evaluation functions
            node, eval_lst = self, []
            while node:
                # print("i",node.path_cost + with_linear_conflict(node.state) + Manhattan_dist(node.state))
                if node.action is not None:
                    # print("?")
                    eval_lst.append(eval_func(node))
                node = node.parent

            # print(eval_lst)
            return list(reversed(eval_lst))#give the f(n) in-order(from the root to goal)


def Manhattan_dist(curr_state):#return only manhattan distance
    dist = 0
    # print(curr_state)
    for i in range(len(curr_state)):
        if(curr_state[i]!= '0'):
            for j in range(len(curr_state)):
                if(curr_state[i] == goal_state[j] and i != j and goal_state[j] != '0'):
                    dist += abs((i//3)-(j//3))+abs((i%3)-(j%3))
                    # print("Manhattan->",curr_state[i],goal_state[j],dist)
    return dist

def with_linear_conflict(curr_state):#return manhattan dis + linear conflict
    # lc = Manhattan_dist(curr_state)
    lc = 0
    row_curr = [[],[],[]]
    row_goal = [[],[],[]]
    col_curr = [[],[],[]]
    col_goal = [[],[],[]]
    permutation = [[0,1],[0,2],[1,2]]#all possible permutations of indeices of any two tiles in a row of three thiles
    for i in range(3):#set list of rows and cols
        row_curr[i].extend(curr_state[i*3:i*3+3])
        row_goal[i].extend(goal_state[i*3:i*3+3])                     
        col_curr[i].extend([curr_state[i],curr_state[i+3],curr_state[i+6]])
        col_goal[i].extend([goal_state[i],goal_state[i+3],goal_state[i+6]])
    # print(row_curr,col_curr)
    already_checked_row = []
    already_checked_col = []
    for i in range(3): #for each row or col
        for j in range(3):
            row_num1,row_num2 = row_curr[i][permutation[j][0]],row_curr[i][permutation[j][1]]#get the two num and their indeices in row
            # row_ind1,row_ind2 = permutation[j][0],permutation[j][1]
            col_num1,col_num2 = col_curr[i][permutation[j][0]],col_curr[i][permutation[j][1]]#do the same for col

            # col_ind1,col_ind2 = permutation[j][0],permutation[j][1]

            # print("r:",row_num1,row_num2,row_ind1,row_ind2)
            # print("c:",col_num1,col_num2,col_ind1,col_ind2)

            # if row_num1 != '0' and row_num2!= '0' and row_num1 not in already_checked_row: #if it is not the blank tile
            #     if row_num1 in row_goal[i] and row_num2 in row_goal[i]: #same two tiles in goal state in same row
            #         if row_goal[i].index(row_num1) > row_goal[i].index(row_num2): #if order reversed
            #             # print("row->",row_num1,row_num2,row_goal[i].index(row_num1),row_goal[i].index(row_num2))
            #             already_checked_row.append(row_num1)
            #             lc += 2
            # if col_num1 != '0' and col_num2 != '0' and col_num1 not in already_checked_col:#if it is not the blank tile
            #     if col_num1 in col_goal[i] and col_num2 in col_goal[i]: #same two tiles in goal state in same col
            #         if col_goal[i].index(col_num1) > col_goal[i].index(col_num2):
            #             # print("col->",col_num1,col_num2,col_goal[i].index(col_num1),col_goal[i].index(col_num2))
            #             already_checked_col.append(col_num1)
            #             lc += 2
            if row_num1 != '0' and row_num2 != '0':  # if it is not the blank tile
                if row_num1 in row_goal[i] and row_num2 in row_goal[i]:  # same two tiles in goal state in same row
                    if row_goal[i].index(row_num1) > row_goal[i].index(row_num2):  # if order reversed
                        # print("row->",row_num1,row_num2,row_goal[i].index(row_num1),row_goal[i].index(row_num2))
                        lc += 2
            if col_num1 != '0' and col_num2 != '0':  # if it is not the blank tile
                if col_num1 in col_goal[i] and col_num2 in col_goal[i]:  # same two tiles in goal state in same col
                    if col_goal[i].index(col_num1) > col_goal[i].index(col_num2):
                        # print("col->",col_num1,col_num2,col_goal[i].index(col_num1),col_goal[i].index(col_num2))
                        lc += 2
    return lc

def eval_func(node):#return the value of evaluation function w/ method given

    if which_eval_func_to_use == "only_manhattan":
       return node.path_cost + Manhattan_dist(node.state)
    elif which_eval_func_to_use == "w_linear_conflicts":
        return node.path_cost + with_linear_conflict(node.state) + Manhattan_dist(node.state)

#A* search algo
def astar(state):

    node = Node(state.initial) #root

    if state.is_goal(node.state): #check if goal is reached
        return node
    queue = []
    frontier = PriorityQueue()
    frontier.put((eval_func(node), node)) #adding to frontier
    queue.append(node.state)
    # print(frontier.queue)
    # print(frontier.queue[0][1])

    # print(node.state not in queue)
    # print((eval_func(node), node) not in frontier.queue)

    explored = set() #stored explored node
    count = frontier.qsize() #count the node generated
    while frontier:#if frontier is not empty
        # print(frontier.queue)
        node_tuple = frontier.get() #get the min node
        # print()
        # print("print",node_tuple)
        node = node_tuple[1]
        # print(node.state,eval_func(node),node.path_cost)       
        if state.is_goal(node.state): #check if goal is reached
            return node,count
        explored.add(tuple(node.state)) #add to the explored set

        count_e = 1
        for child in node.expand(state): #expand the node which is loop through the list of all possible states(child node)
            count_e += 1
            if tuple(child.state) not in explored and child.state not in queue: #new state
            # if tuple(child.state) not in explored and (eval_func(child), child.state) not in visited:
                frontier.put((eval_func(child), child))# add to frontier
                queue.append(child.state)
                # print(state_str(node.state),"\n",eval_func(node),node.path_cost)
                # print("lc",with_linear_conflict(node.state),eval_func(node),Manhattan_dist(node.state),end = "\n++++++++++++++++++++++++\n")
                count += 1
            elif child.state in queue: #check if it can update state that already in the the frontier
                this = frontier.get()
                # print(this)
                if eval_func(child) < int(this[0]):#if f(n) is smaller
                    # print(eval_func(child),int(this[0]))
                    frontier.put((eval_func(child), child)) #add to frontier
                else:
                    frontier.put(this)
        # count += len(node.expand(state))
    # print(node.path_cost)
    return None,count

def state_str(state):#this is just to format output of state for easier debuging :)
    string = ""
    for i in range(len(state)):
        if(i % 3 == 0 and i != 0):
            string += "\n"
        string += str(state[i])
        if i != len(state)-1:
            string += " "
    return string

def test_output(): #also for debuging -> pringting output to terminal :/
    print("input file: ",inFile)
    print(which_eval_func_to_use)
    print(state_str(init_state))
    print()
    print(state_str(goal_state))
    print()
    print(ans.path_cost)
    print(node_count)
    print(' '.join(str(i) for i in lst_solution_path))
    print(' '.join(str(i) for i in lst_eval_funcs))

def output_to_file(f_out): #output to file
    print('\n', file=f_out)
    print(ans.path_cost,file=f_out)
    print(node_count,file=f_out)
    print(' '.join(str(i) for i in lst_solution_path),file=f_out)
    print(' '.join(str(i) for i in lst_eval_funcs),file=f_out)

init_state = []
goal_state = []


#input file name
inFile = "temp.txt"
f = open(inFile,'r')
#output file name
f_outA = open("Output_A.txt",'w') #for output A (only manhattan)
f_outB = open("Output_B.txt",'w') #for putput B (w/ linear conflict)

for i in range(7): #read the file and output init and goal to out file
    curr_line = f.readline()
    line = curr_line.rstrip().split()
    if(i<3): #first 3 line initial state
        init_state.extend(line)
        print(curr_line,file=f_outA,end="")
        print(curr_line,file=f_outB,end="")
    elif(i >3): #line: 4 5 6
        print(curr_line,file=f_outA,end="")
        print(curr_line,file=f_outB,end="")
        goal_state.extend(line)
    else:
        print("\n",file=f_outA,end="")
        print(curr_line,file=f_outB,end="")

# Only manhattan distance as heuristic func
which_eval_func_to_use = "only_manhattan"
state = State(list(init_state), goal_state)
ans,node_count = astar(state)
lst_solution_path = ans.solution_path()
lst_eval_funcs = ans.eval_val_lst()

test_output() # output to terminal
output_to_file(f_outA) #output to file

#manhattan dist + linear conflict as heuristice func
# print(Manhattan_dist(init_state))
# print(with_linear_conflict(init_state))
which_eval_func_to_use = "w_linear_conflicts"
state = State(list(init_state), goal_state)
node = Node(state.initial)
ans,node_count = astar(state)
# print(node.path_cost)
lst_solution_path = ans.solution_path()
lst_eval_funcs = ans.eval_val_lst()
# print(Manhattan_dist(init_state))
# print(with_linear_conflict(init_state))
test_output()
# output_to_file(f_outB)