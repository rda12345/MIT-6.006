import rubik
from queue import Queue


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    if start == end:
        return []
    
    parents = ({start: None},{end: None})
    frontiers = [[start],[end]]
    # The maximum depth of the rubik's cube is 14, since we are doing a two
    # sided BFS we need to iterate at most 7 times.
    for i in range(8):
        nexts = ([],[])
        for direction, frontier in enumerate(frontiers):
            for config in frontier:
                # evaluating the possible configurations reachable from config_s by
                # one of the quarter twists
                neigh_configs = [rubik.perm_apply(perm, config) for perm in rubik.quarter_twists]  
                for twist_ind, neigh in enumerate(neigh_configs):
                    if neigh not in parents[direction]:
                        parents[direction][neigh] = (config,rubik.quarter_twists[twist_ind])
                        nexts[direction].append(neigh)
                    # if the neighboring configuration is in the other frontier
                    # then evaluate the list of moves, corresponding to the 
                    # shortest path of moves to reach from the start configuration
                    # to the end.
                    if neigh in parents[(direction + 1) % 2]:
                        result = reconstruct_path(parents,start,end,neigh) 
                        return result
            frontiers[direction] = nexts[direction]      


def reconstruct_path(parents,start,end,collision):
    """
    Reconstructs the path for a two sided BFS.
    
    Input:
        parents: tuple, containing two dictionaries (parents[0],parents[1])
                    parents[0] maps configurations in the path start --> collision
                    to tuples of (parent configuration, quarter twist)
                    parents[1] maps configurations in the path end --> collision
                    to tuples of (parent configuration, quarter twist)
        start: tuple, containing the initial configuration
        end: tuple, ontaining the final configuration
        collision: tuple, containing the collision configuration
    
    Return:
        list, containing the quarter twists associated with the shortest path 
        from start to end configurations
                         
    """
    start_moves, end_moves = [], []
    
    # Tracing back from the collision point of the two shortest path to the
    # start node
    node = collision
    while node !=start:
        twist = parents[0][node][1]
        start_moves.append(twist)
        node = parents[0][node][0]
        
    start_moves.reverse()   
    node = collision
    
    # Tracing back from the collision point of the two shortest path to the
    # end node
    while node != end:
        twist = parents[1][node][1]
        # for the bakward path the permutations are inversed
        end_moves.append(rubik.perm_inverse(twist))
        node = parents[1][node][0]  
        
    start_moves.extend(end_moves)
    return start_moves

def read_moves(moves):
    l = []
    for move in moves:
        l.append(rubik.quarter_twists_names[move])
    return l






    



        
    
    
    
    

