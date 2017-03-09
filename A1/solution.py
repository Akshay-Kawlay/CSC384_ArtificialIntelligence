#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Sokoban warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
import os
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS, sokoban_goal_state #for Sokoban specific classes and problems

#SOKOBAN HEURISTICS
def heur_displaced(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''       
  count = 0
  for box in state.boxes:
    if box not in state.storage:
      count += 1
  return count

def heur_manhattan_distance(state):
#IMPLEMENT--DONE
    '''admissible sokoban heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''      
    #We want an admissible heuristic, which is an optimistic heuristic. 
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum Manhattan distance of the boxes to their closest storage spaces is such a heuristic.  
    #When calculating distances, assume there are no obstacles on the grid and that several boxes can fit in one storage bin.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    
    minManDist = 9999999
    totalManDist = 0
    manDist = 0	
    if state.boxes == None:
      return 0
    for (x1,y1), value in state.boxes.items():
      if state.restrictions == None:
        for (x,y), values in state.storage.items():
          manDist = abs(x-x1)+abs(y-y1)
          if minManDist > manDist:
            minManDist = manDist
        totalManDist += minManDist
        minManDist = 999999
      else:
        for (x0,y0) in state.restrictions[value]:
          manDist = abs(x0-x1)+abs(y0-y1)
          if len(state.restrictions[value]) > 1:
            if minManDist > manDist:
              minManDist = manDist
              totalManDist += minManDist
          else:
            totalManDist += manDist
    
    return totalManDist


# def isBlockAllowed(state):
  
Flag = 0
  
def heur_alternate(state):
#IMPLEMENT
    '''a better sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
    #heur_manhattan_distance has flaws.   
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
      
    #starting with the manhattan heuristics and improving it by adding intelligent pruning
    #f = heur_manhattan_distance(state)
    
    #check for deadlocks    
    #make input adjacency matrix for dijkstra

    w = state.width
    h = state.height

#     DIJKSTRAS WORKS WELL BUT TOO TIME CONSUMING WITH PYTHON PREDEFINED FUNCTION
#     Msize = w*h
#     M = [[1 for x in range(Msize*Msize)] for x in range(Msize*Msize)]
#     #M = [[[None]]*Msize*Msize]*Msize*Msize
#     for (x,y) in state.obstacles:
#       M[x*Msize+y] = [999 for x in range(w*h)]
#     for (x0,y0), i in state.boxes.items():
#       M[x0*Msize+y0] = [999 for x in range(w*h)]
#     (xr,yr) = state.robot
#     M[xr*Msize+yr] = [999 for x in range(w*h)]
#     indices = [0 for x in range(len(state.boxes))]
#     for (x0,y0), i in state.boxes.items():
#       I = x0*Msize + y0
#       indices.append(I)
#     from scipy.sparse.csgraph import dijkstra
#     distances, predecessors = dijkstra(M, indices, return_predecessors=False)
    
    
    #matrix = [[999 for x in range(len(state.storage)+1)] for y in range(len(state.boxes)+1)]
#     dictObsNum = {}
#     for (x1,y1), j in state.storage.items():
#       if (x1,y1) in dictObsNum:
#         continue
#       count = 0
#       if (x1+1,y1) in state.obstacles:
#         count += 1
#       if (x1-1,y1) in state.obstacles:
#         count += 1
#       if (x1,y1+1) in state.obstacles:
#         count += 1
#       if (x1,y1-1) in state.obstacles:
#         count += 1
#       dictObsNum[j] = count
        
    #from scipy.spatial import distance

#IMPLEMENTING HUNGARIAN ALGORITHM BUT AGAIN SLOWER AND COMPUTATIONALLY EXPENSIVE
    
#     for (x0,y0), i in state.boxes.items():
#       for (x1,y1), j in state.storage.items():
#         
#         if state.restrictions == None:
#           #manDist = distance.euclidean(x1,x0) + distance.euclidean(y1,y0)
#           
#           manDist = abs(x1-x0)+abs(y1-y0)
#           #Djk = distances[x0*Msize+y0][x1*Msize+y1]
#           #offset = dictObsNum[j]
#           #print(offset)
#           matrix[i-1][j-1] = manDist #-offset*offset
#           
#         else:
#           found = 0
#           for (x,y) in state.restrictions[i]:
#            if x==x1 and y==y1:
#              found = 1;
#              #manDist = distance.euclidean(x1,x0) + distance.euclidean(y1,y0)
#              manDist = abs(x1-x0)+abs(y1-y0)
#              #Djk = distances[x0*Msize+y0][x1*Msize+y1]
#              #offset = dictObsNum[j]
#              #print(offset)
#              matrix[i-1][j-1] = manDist #- offset*offset
#              break
# 
#     import numpy as np
#     cost = np.array(matrix)
#     from scipy.optimize import linear_sum_assignment
#     row_ind, col_ind = linear_sum_assignment(cost)
#     hungarian = cost[row_ind, col_ind].sum()
#     return hungarian
#     
    
    ###########################################################################
    #IMPLEMENTING SIMPLE PRUNNING AND DEADLOCK CHECKS: FASTER BUT DUMBER
    totalrob = 0
        
    minManDist = 9999999
    totalManDist = 0
    manDist = 0	
    if state.boxes == None:
      return 99999
    for (x1,y1), value in state.boxes.items():
      if (x1,y1) in state.storage:
         return 0
      if x1 == 0 or x1 == w-1:
        return 99999
      if y1 == 0 or y1==h-1:
        return 99999
      if state.restrictions == None:
        for (x,y), values in state.storage.items():
          if(x == 0 and x1==w-1) or (x==w-1 and x1==0) or (y==0 and y1==h-1) or (y==h-1 and y1==0):
            return 99999
          manDist = abs(x-x1)+abs(y-y1)
          if minManDist > manDist:
            minManDist = manDist
        totalManDist += minManDist
        minManDist = 999999
      else:
        for (x0,y0) in state.restrictions[value]:
          if(x0 == 0 and x1==w-1) or (x0==w-1 and x1==0) or (y0==0 and y1==h-1) or (y0==h-1 and y1==0):
            return 99999
          manDist = abs(x0-x1)+abs(y0-y1)
          if len(state.restrictions[value]) > 1:
            if minManDist > manDist:
              minManDist = manDist
              totalManDist += minManDist
          else:
            totalManDist += manDist
            
    return totalManDist+totalrob
      
      
        
  


def fval_function(sN, weight=1.):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
      
    f = sN.gval + weight*sN.hval
    
    return f

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 
    currentTime1 = os.times()[0]
    #remainingTime = timebound
    manDist = heur_manhattan_distance(initial_state)
    costbound = (999999,999999,999999)
    se = SearchEngine('best_first', 'full')
    se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_manhattan_distance)
    state = 0
    found = 0
    timeElapsed = 0
    final = se.search((timebound-timeElapsed), costbound)
    if final != False:
      costbound = (final.gval, 999999,99999)
      found = 1
      state = final
    timeElapsed = os.times()[0] - currentTime1
    
    while(timeElapsed < timebound):
      final = se.search((timebound-timeElapsed), costbound)
      if found:
        found = 1
        if final != False:
          costbound = (final.gval, 99999999, 99999999);
          state = final
      currentTime2 = os.times()[0]
      timeElapsed = (currentTime2-currentTime1)
      
    if found:
      return state
    else:
      return False



def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 
    currentTime1 = os.times()[0]
    costbound = (9999999, 99999999, 999999999);
    se = SearchEngine('custom', 'full')
    se.init_search(initial_state, goal_fn=sokoban_goal_state, fval_function=fval_function)
    state = 0
    found = 0
    timeElapsed = 0
    final = se.search((timebound-timeElapsed), costbound)
    if final != False:
      manDist = heur_manhattan_distance(final)
      costbound = (final.gval,999999, 9999999)
      found = 1
      state = final
    timeElapsed = os.times()[0] - currentTime1
    while(timeElapsed < timebound):
      final = se.search((timebound-timeElapsed), costbound)
      if found and final != False:
        found = 1
        costbound = (final.gval, 999999, 999999);
        state = final
      currentTime2 = os.times()[0]
      timeElapsed = (currentTime2-currentTime1)
  
    if found:
      return state
    else: 
      return False



if __name__ == "__main__":
  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")  
  print("Running A-star")     

  for i in range(0, 10): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")  
    print("PROBLEM {}".format(i))
    
    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    se.init_search(s0, goal_fn=sokoban_goal_state, heur_fn=heur_displaced)
    final = se.search(timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)    
    counter += 1

  if counter > 0:  
    percent = (solved/counter)*100

  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 

  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit 
  print("Running Anytime Weighted A-star")   

  for i in range(0, 10):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    weight = 10
    final = anytime_weighted_astar(s0, heur_fn=heur_displaced, weight=weight, timebound=timebound)

    if final:
      final.print_path()   
      solved += 1 
    else:
      unsolved.append(i)
    counter += 1      

  if counter > 0:  
    percent = (solved/counter)*100   
      
  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 



