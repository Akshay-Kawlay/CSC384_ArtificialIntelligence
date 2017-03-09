#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def neighbour_constraint(V, V1, tenner_csp):
    scope = [V, V1]
    V_dom = V.domain()
    V1_dom = V1.domain()
    sat_tuples = []
    
    for (a,b) in itertools.product(V_dom, V1_dom):
        if a != b:
            sat_tuples.append((a,b))
    
    con = Constraint('C-neq', scope)
    con.add_satisfying_tuples(sat_tuples)
    tenner_csp.add_constraint(con)

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    n_grid, last_row = initial_tenner_board
    tenner_csp = CSP('Tenner1')
    variable_array = []
    Domain = [0,1,2,3,4,5,6,7,8,9]
    
    #add variables
    N = len(n_grid)
    for i in range(N):
        var_row = []
        for j in range(10):
            V = Variable("V({},{})".format(i,j))
            if n_grid[i][j] == -1:
                V.add_domain_values(Domain)
            else:
                V.add_domain_values([n_grid[i][j]])
            tenner_csp.add_var(V)
            var_row.append(V)
            
        variable_array.append(var_row)
        
    #add constraints
    
    #neighbourhood constraints
    for i in range(N):
        for j in range(10):

            V = variable_array[i][j]
            
            if i!= N-1 and j!= 0:
                V1 = variable_array[i+1][j-1]
                neighbour_constraint(V, V1, tenner_csp)
                
            if i!= N-1:
                V2 = variable_array[i+1][j]
                neighbour_constraint(V, V2,tenner_csp)

            if i!= N-1 and j!= 9:
                V3 = variable_array[i+1][j+1]
                neighbour_constraint(V, V3, tenner_csp)
            
            #row constraint
            for k in range(10):
                if k>j:
                    Vk = variable_array[i][k]
                    neighbour_constraint(V,Vk,tenner_csp)
                    
    
    #sum constraints
    for j in range(10):
        scope = []
        var_domains = []
        for i in range(N):
            scope.append(variable_array[i][j])
            var_domains.append(variable_array[i][j].domain())
        sat_tuples = []
        for column in itertools.product(*var_domains):
            s = last_row[j]
            if sum(column) == s:
                sat_tuples.append(column)
        
        con = Constraint('C-sum', scope)
        con.add_satisfying_tuples(sat_tuples)
        tenner_csp.add_constraint(con)
    
    return tenner_csp, variable_array
            


def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular,
       model_2 has a combination of n-nary 
       all-different constraints and binary not-equal constraints: all-different 
       constraints for the variables in each row, binary constraints for  
       contiguous cells (including diagonally contiguous cells), and n-nary sum 
       constraints for each column. 
       Each n-ary all-different constraint has more than two variables (some of 
       these variables will have a single value in their domain). 
       model_2 should create these all-different constraints between the relevant 
       variables.
    '''
    
    n_grid, last_row = initial_tenner_board
    tenner_csp = CSP('Tenner2')
    variable_array = []
    Domain = [0,1,2,3,4,5,6,7,8,9]
    
    #add variables
    N = len(n_grid)
    for i in range(N):
        var_row = []
        for j in range(10):
            V = Variable("T({},{})".format(i,j))
            if n_grid[i][j] == -1:
                V.add_domain_values(Domain)
            else:
                V.add_domain_values([n_grid[i][j]])
            tenner_csp.add_var(V)
            var_row.append(V)
            
        variable_array.append(var_row)
     
    #add constraints
    
    #neighbourhood constraints
    for i in range(N):
        scope = []
        var_domains = []
        for j in range(10):
            V = variable_array[i][j]
            
            if i!= N-1 and j!= 0:
                V1 = variable_array[i+1][j-1]
                neighbour_constraint(V, V1, tenner_csp)
             
            if i!= N-1:
                V2 = variable_array[i+1][j]
                neighbour_constraint(V, V2,tenner_csp)

            if i!= N-1 and j!= 9:
                V3 = variable_array[i+1][j+1]
                neighbour_constraint(V, V3, tenner_csp)
            
            if j!= 9:
                V4 = variable_array[i][j+1]
                neighbour_constraint(V, V4, tenner_csp)
        
        
    #n-ary all diff constraints
    for i in range(N):
        scope = []
        var_domains = []
        single_domain_vars = []
        tempD = list(Domain)
        for j in range(10):
            scope.append(variable_array[i][j])
            if n_grid[i][j]==-1:
                var_domains.append(tempD)
            else:
                single_domain_vars.append(n_grid[i][j])

        for d in single_domain_vars:
            for d_list in var_domains:
                if d in d_list:
                    d_list.remove(d)
        
        sat_tuples = []
        flag = 0
        sat_tuples += itertools.permutations(var_domains[0], len(var_domains[0]))            
        new_tuples = []
        for tup in sat_tuples:
            ptr = 0
            temp_tup = tup
            temp_tup = list(temp_tup)
            for j in range(10):
                if n_grid[i][j]!=-1:
                    temp_tup.insert(ptr, n_grid[i][j])
                    ptr=ptr+1
                else:
                    ptr=ptr+1
            temp_tup = tuple(temp_tup)
            new_tuples.append(temp_tup)
        con = Constraint('C-aldif', scope)
        con.add_satisfying_tuples(new_tuples)
        tenner_csp.add_constraint(con)

    #sum constraints
    for j in range(10):
        scope = []
        var_domains = []
        for i in range(N):
            scope.append(variable_array[i][j])
            var_domains.append(variable_array[i][j].domain())
        sat_tuples = []
        for column in itertools.product(*var_domains):
            s = last_row[j]
            if sum(column) == s:
                sat_tuples.append(column)
        
        con = Constraint('C', scope)
        con.add_satisfying_tuples(sat_tuples)
        tenner_csp.add_constraint(con)
    
    return tenner_csp, variable_array
