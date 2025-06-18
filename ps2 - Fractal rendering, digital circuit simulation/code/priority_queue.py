#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Priority Queue
"""
import random


class PriorityQueue:
    """Array-based priority queue implementation."""
    def __init__(self):
        """Initially empty priority queue."""
        self.queue = []
        self.min_index = None
    
    def __len__(self):
        # Number of elements in the queue.
        return len(self.queue)
    
    def append(self, key):
        """Inserts an element in the priority queue."""
        if key is None:
            raise ValueError('Cannot insert None in the queue')
        self.queue.append(key)
        key_ind = len(self.queue) - 1
        parent_ind = (key_ind - 1)//2
        
        while parent_ind >= 0:
            self.heapify(parent_ind)
            if self.queue[parent_ind] == key:
                parent_ind = (parent_ind - 1)//2
            else:
                break
            
                
        #self.min_index = None
        
    def heapify(self,ind):
        """
            Min-heapifies the single possible violation of the heap invariant property
            at index ind.
            
            Input
                ind: int, the index of the heap invariant property violation
        """
        left_child_ind, right_child_ind = 2*ind + 1, 2*ind + 2
        #check that the queue isn't empty and the index matches and element in the queue
        if len(self.queue) == 0 or left_child_ind >= len(self.queue):
            return None
        key = self.queue[ind]
        smaller_ind = left_child_ind
        if right_child_ind < len(self.queue):
            if self.queue[left_child_ind] > self.queue[right_child_ind]:
                smaller_ind = right_child_ind
        
  
        if key > self.queue[smaller_ind]:
            #print('check')
            self.queue[ind], self.queue[smaller_ind] = self.queue[smaller_ind], self.queue[ind]
            self.heapify(smaller_ind) 

        
    
    def min(self):
        """The smallest element in the queue."""
        if len(self.queue) == 0:
            return None
        return self.queue[0]
    
    def pop(self):
        """Removes the minimum element in the queue.
    
        Returns:
            The value of the removed element.
        """
        if len(self.queue) == 0:
            return None
        
        #swaping the root and the last last leaf
        self.queue[0], self.queue[len(self.queue) - 1] = self.queue[len(self.queue)-1], self.queue[0]
        #removing the last key
        popped_key = self.queue.pop()
        self.heapify(0)
        
        return popped_key
    
    def check_heap(self):
        for ind, key in enumerate(self.queue):
            if 2*ind + 1 < len(self.queue):
                if key > self.queue[2*ind+1]: return False
            if 2*ind + 2 < len(self.queue):
                if key > self.queue[2*ind+2]: return False 
        return True
    
    #def _find_min(self):
        # Computes the index of the minimum element in the queue.
        #
        # This method may crash if called when the queue is empty.
     #   if self.min_index is not None:
     #       return
     #   return 0        
                
                
if __name__ == '__main__':
    Q = PriorityQueue()
    l = random.sample(range(1, 101), 20)
    for i in l:
        Q.append(i)
    
    
    print(Q.check_heap())
    Q.pop()
    print(Q.check_heap())
    
    #for i in range(len(Q)):
     #   print(Q.pop())
    
    
