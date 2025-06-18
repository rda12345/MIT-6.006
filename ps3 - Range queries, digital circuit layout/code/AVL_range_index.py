#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AVL_range_index
"""

class BSTNode(object):
    """A node in a BST tree"""
    def __init__(self,k):
        """ Creates a node.
            
            Args:
                parent: BSTNode, the node's parent
                key: float, the node's key
            
            Parms:
                left: BSTNode, the left child node.
                right: BSTNode, the right child node.
        """
        self.key = k
        self.left = None
        self.right = None
        self.parent = None 
        
    def __str__(self):
        return str(self.key)
    
        
    
    def find(self,k):
        """Finds and returns the node with key k from the subtree rooted at this node."""
        if self.key == k:
            return self
        elif k < self.key:
            if self.left is None:
                return None
            else:
                return self.left.find(k)
        else:
            if self.right is None:
                return None
            else:
                return self.right.find(k)
    
    def find_min(self):
        """Finds and returns the minimum element of the BST rooted at the node"""
        # Base case:
        if self.left is None:
            return self
        else: 
            return self.left.find_min()
    
    def find_max(self):
        """Finds and returns the minimum element of the BST rooted at the node"""
        # Base case:
        if self.right == None:
            return self
        else: 
            return self.right.find_max()
    
    def insert(self,node):
        """Inserts a node into the subtree rooted at this node.
            (it is assumed each key is distinct)
        
        Args: 
            node: BSTNode, the node to be inserted
        
        Returns:
            node: the inserted node
        """
        if node.key < self.key:
            if self.left is not None:
                return self.left.insert(node)
            node.parent = self
            self.left = node
            return node

        elif node.key > self.key:          
            if self.right is not None:
                return self.right.insert(node)
            node.parent = self
            self.right = node
            return node
        return self
            
    def next_larger(self):
        """Finds the node with the next larger key"""
        # Base case: the right childe of the node is None
        if self.right == None:
            if self == self.parent.right:
                raise NameError('This is the largest key')
            else:
                return self.parent
        else: 
            return self.right.find_min()
        
    def next_smaller(self):
        """Finds the node with the next smaller key"""
        # Base case: the right childe of the node is None
        if self.left == None:
            if self == self.parent.left:
                raise NameError('This is the smallest key')
            else:
                return self.parent
        else: 
            return self.left.find_max()    
    
        
                
    def delete(self):
      """Deletes this node from the BST.
      """
      if self.left is None or self.right is None:
        if self is self.parent.left:
          self.parent.left = self.left or self.right
          if self.parent.left is not None:
            self.parent.left.parent = self.parent
        else:
          self.parent.right = self.left or self.right
          if self.parent.right is not None:
            self.parent.right.parent = self.parent
        return self
      else:
        s = self.next_larger()
        # NOTE: deleting before swapping the keys so the BST RI is never violated.
        deleted_node = s.delete()
        self.key, s.key = s.key, self.key
        return deleted_node
        
    def check_ri(self):
        """
        Checks the representation invariant (RI) of the AVL tree. 
        Namely, that the tree is a binary search tree:
        node.left.key < node.key && node.right.key > node.key for every node
        in the tree.
        
        """
        # Base case: if the node is a leaf it satisfies the representation invariant
        if self.left == None and self.right == None:
            return True
        elif self.left == None and self.right.key > self.key:
            return self.right.check_ri()
        elif self.right == None and self.left.key < self.key:
            return self.left.check_ri()
        elif self.right.key > self.key and self.left.key < self.key:
            return self.left.check_ri() and self.right.check_ri()
        else: 
            return False

class BST(object):
    """Creates a binary search tree"""
    
    def __init__(self,node_class = BSTNode):
        """Creates and emptly BST"""        
        self.node_class = node_class
        self.root = None
        
    def min(self):
        if self.root is None:
            return None
        else:
            return self.root.find_min()
            
     
    def insert(self, key):
        node = self.node_class(key)
        if self.root is None:
           self.root = node
           return node
        else:
            return self.root.insert(node)
            
            
    def find(self,key):
        return self.root and self.root.find(key)
   
    
    def check_ri(self):
        return self.root and self.root.check_ri()
    #COMPLETE        
    def delete(self,key):
        node = self.find(key)
        if node:
            if node == self.root:
                pseudo_root = self.node_class(None)
                pseudo_root.left = self.root 
                self.root.parent = pseudo_root
                deleted_node = node.delete()
                self.root = pseudo_root.left
                return deleted_node
            else:
                return node.delete()
        else:
            return None
        
    def successor(self,key):
        node = self.find(key)
        return node and node.next_larger()        
  

l = []         
def inorder(node):
    if node != None:     
       #print(node.key)
       inorder(node.left)
       l.append(node.key)
       inorder(node.right)
       
       
       

            
class AVLNode(BSTNode):
    
    def __init__(self,key):
        """Create as a node which will be inserted into the AVL tree"""
        BSTNode.__init__(self,key)  
        self.height = 0
        
    def update_subtree_info(self):
        """Updates the nodes info"""
        self.height = self.updated_height()
    
    def updated_height(self):
        """Updates the node's height"""
        return 1 + max((self.left and self.left.height) or -1,
                       (self.right and self.right.height) or -1)
        
        
    def check_ri(self):
        """Checks the representation invariant of the AVL node"""
        if self.height != self.updated_height():
            raise NameError('RI is violated by wrong node height')
        if abs(height(self.left)-height(self.right)) >= 2:
            raise NameError('RI violated by unbalanced node height')
        BSTNode.check_ri(self)

   

class AVL(BST):
    
    
    def __init__(self, node_class = AVLNode):
        """Initiates an AVL tree"""
        BST.__init__(self,node_class)
        
        
        
    def insert(self,key):
        """Inserts a node to the AVL tree and rebalances the tree"""
        inserted_node = BST.insert(self, key)
        self.rebalance(inserted_node)
        return inserted_node
        
        
    def delete(self,key):
        """Deletes a node with node.key = key from the tree"""
        deleted_node = BST.delete(self, key)
        self.rebalance(deleted_node.parent)
        return deleted_node
        
    def rebalance(self,node):
        """Rebalances the tree by right and left rotations. 
        """
        #We begin the procedure from the leafs to the root.    
        while node is not None:
            node.update_subtree_info()

            #There are two cases 
            #case 1: the left child of node x is heavier than the right child.
            #       inserting into the left child may violate the AVL tree
            if height(node.left) >= 2 + height(node.right):
                if height(node.left) >= height(node.right):
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            
            #case 2: analogous to case 1 but with left -> right
            if height(node.right) >= 2 + height(node.left):
                if height(node.right) >= height(node.left):
                    
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)   
            #updating the node (going up the tree towards the root)
            node = node.parent
        
         
           
    def left_rotate(self,y):
        """Performs a left rotation w.r.t node y"""
        x = y.right
        x.parent = y.parent
        if y.parent == None:
            self.root = x
        else:
            if y.parent.left == y:
                y.parent.left = x
            else:
                y.parent.right = x
        y.parent = x
        y.right = x.left
        if y.right is not None:
           y.right.parent = y
        x.left = y
        #update the information
        x.update_subtree_info()
        y.update_subtree_info()
        
    def right_rotate(self,x):
        """Performs a right rotation w.r.t node y"""
        y = x.left
        y.parent = x.parent
        if y.parent == None:
            self.root = y
        else:
            if x.parent.left == x:
                x.parent.left = y
            else:
                x.parent.right = y
        x.parent = y
        x.left = y.right
        if x.left is not None:
           x.left.parent = x
        y.right = x
        #update the information
        x.update_subtree_info()
        y.update_subtree_info()
        
        
def height(node):
    """Returns the height of the the node"""
    if node is None:
        return -1
    else: 
        return node.height
    
    
    
    
class RangeNode(AVLNode):
    
    def __init__(self,key):
        """Creates a node which will be inserted in the range index"""
        AVLNode.__init__(self,key)  
        self.tree_size =  1
        
    def update_subtree_info(self):
        """Updates the nodes info"""
        AVLNode.update_subtree_info(self)
        self.tree_size = self.updated_tree_size()
        
    def updated_tree_size(self):
        """Updates the tree_size based at the node"""
        return (1 + ((self.left and self.left.tree_size) or 0) + ((self.right and self.right.tree_size) or 0) )
    
        
        
    def check_ri(self):
        """Checks the representation invariant of the Range index"""
        if self.tree_size != self.updated_tree_size():
            raise NameError('RI is violated by wrong tree size')
        AVLNode.check_ri(self)
        
        
    def rank(self,key):
        """Returns the number of keys smaller or equal to key"""
        if key < self.key:
            if self.left is not None:
                return self.left.rank(key)
            else: 
                return 0
        
        if self.left:
            # add all the nodes of the self.left, the node itself and go to the next node
            lrank = 1 + self.left.tree_size
        else:
            lrank = 1
        if key > self.key and self.right is not None:
            lrank = lrank + self.right.rank(key)
        
        return lrank
            
                
        
    def lca(self,low_key,high_key):
        """Returns the lowest common node of nodes with keys low_key and high_key
            return a RangeNode instance of None if the range is not in the tree
        """
        if low_key <= self.key <= high_key:
            return self
        elif self.left and high_key < self.key: 
            return self.left.lca(low_key,high_key)
        elif self.right and low_key > self.key:
            return self.right.lca(low_key,high_key)
        else:
            return None
        
    def list(self, low_key, high_key, result):
        """Returns a list with all the nodes with keys in the range [low_key,high_key]"""
        if low_key <= self.key <= high_key:
            result.append(self)
        if (self.left is not None) and self.key >= low_key:
            self.left.list(low_key,high_key,result)
        if (self.right is not None) and self.key <= high_key:
            self.right.list(low_key,high_key,result) 
        
        
        
class RangeTree(AVL):
    
    def __init__(self,node_class = RangeNode):
      """Initiates an empty range tree"""
      AVL.__init__(self,node_class)
      
          
    def rank(self,key):
        """Returns the number of keys smaller or equal to key"""
        if self.root is not None:
            return self.root.rank(key)
        else:
            return 0
        
        
    def lca(self,low_key,high_key):
        """Returns the lowest common node of nodes with keys low_key and high_key
            return a RangeNode instance of None if the range is not in the tree
        """
        if self.root is not None:
            return self.root.lca(low_key,high_key)
        
        
    def list(self, low_key, high_key):
        """Returns a list with all the nodes with keys in the range [low_key,high_key]"""
        range_list = []
        if self.root:
            lca = self.root.lca(low_key,high_key)
            if lca is not None:
                lca.list(low_key,high_key,range_list)
        return range_list
    
    

class AvlRangeIndex(object):
  """Tree-based range index implementation."""
  def __init__(self):
     """Initializing an empty AVL range index """     
     self.tree = RangeTree()
    

    
  
  def add(self, key):
    """Inserts a key in the range index."""
    if key is None:
        raise ValueError('Cannot insert nil in the index')
    self.tree.insert(key)
  
  def remove(self, key):
    """Removes a key from the range index."""
    self.tree.delete(key)
  
  def list(self, low_key, high_key):
    """List of values for the keys that fall within [low_key, high_key]."""
    return [node.key for node in self.tree.list(low_key,high_key)]
  
  def count(self, low_key, high_key):
    """Number of keys that fall within [first_key, last_key]."""
    check_low = self.tree.find(low_key)
    check_high = self.tree.find(high_key)
    # (Following the assingment questions) if both the first and last key
    # exist in the index or the first exists while the last doesn't
    if (check_low and check_high) or (check_low and not check_high):
        return self.tree.rank(high_key) -self.tree.rank(low_key) + 1 
    # The complementary: if both the first and last key
    # don't exist in the index or the last exists while the first doesn't
    else:
        return self.tree.rank(high_key) -self.tree.rank(low_key)


    
      
if __name__ == '__main__':
    
    ### RangeTree check
    tree = RangeTree()
    keys = [10,9,11,13]
    for key in keys:
        tree.insert(key)
        tree.check_ri()
  
    ##rank
    l = [8,9,9.1,10,10.5,11,12,13,14]
    for k in l:
        print('-----------------')
        print(f'k: {k}')
        print(tree.rank(k))
    
    ##lca and list check
    l = [(1,8),(9,11),(8,14),(11.1,13),(13,14),(14,15)]
    for tup in l:
        result = []
        low_key, high_key = tup
        print('------------------')
        print(f'(low_key,high_key): {low_key},{high_key}')
        print(f'lca = {tree.lca(low_key,high_key)}')
        l = tree.list(low_key,high_key)
        print(f'list: {[node.key for node in l]}')

    
    
    
"""      
    ### RangeNode check
    #root = RangeNode(10)
    #root.update_subtree_info()
    #print(root.tree_size)
    
    
    #root.insert(RangeNode(9))
    #root.left.update_subtree_info()
    #root.insert(RangeNode(11))
    #root.right.update_subtree_info()
    
    #root.insert(RangeNode(13))
    #root.right.right.update_subtree_info()
    
    
    #root.right.update_subtree_info()
    #root.update_subtree_info()
    #print(root.tree_size)
    #print(root.right.tree_size)
    #print(root.right.right)    
    
    ##check_ri
    #keys = [10,9,11,13]
    #for key in keys:
     #   print(f'key: {key}')
      #  print(f'tree size: {root.find(key).tree_size}')
      #   root.find(key).check_ri()
    
    ##rank
    #keys = [10,9,11,13]
    #for key in keys:
     #  print(f'key: {key}')
      # print(f'rank: {root.find(key).rank(14)}')
       
    ##lca and list check
    #l = [(1,8),(9,11),(8,14),(11.1,13),(13,14),(14,15)]
    #for tup in l:
        #result = []
        #low_key, high_key = tup
        #print('------------------')
        #print(f'(low_key,high_key): {low_key},{high_key}')
        #print(f'lca = {root.find(10).lca(low_key,high_key)}')
        #root.find(10).list(low_key,high_key,result)
        #print([node.key for node in result])

    

    
    
    ### AVL check
    #tree = AVL()
    #keys = [10,11,18,6,2]
    #for key in keys:
     #   tree.insert(key)

    ## insert check
    #l = []    
    #inorder(tree.root)
    #print(f'tree transversal: {l}')
    #for key in keys:
     #   node = tree.find(2)
      #  node.check_ri()
    
 
    ## delete check
    #tree.delete(10)
    #tree.delete(11)
    #tree.delete(0)
    #l = []    
    #inorder(tree.root)
    #print(f'tree transversal: {l}')
    #for key in keys:
     #   node = tree.find(2)
      #  node.check_ri()
    
    #print(f'RI check: {tree.check_ri()}')
    
    
    ### BST check
    #tree = BST()
    #tree.insert(10)
    #tree.insert(11)
    #tree.insert(18)
    #tree.insert(6)
    #tree.insert(2)
    
    ## insert check
    #print(tree.check_ri())    
    
    ## find check
    #print(tree.find(11))
    #print(tree.find(1))
    
    ## min check
    #print(tree.min())
    
    ## successor check
    #print(tree.successor(6))
    #print(tree.successor(18))
 
    ## delete check
    #tree.delete(10)
    #tree.delete(11)
    #tree.delete(0)
    #l = []    
    #inorder(tree.root)
    #print(f'tree transversal: {l}')
    #print(f'RI check: {tree.check_ri()}')
    


    ### BSTNode check                    
    root = BSTNode(None,10)
    root.insert(BSTNode(9))
    root.insert(BSTNode(11))
    root.insert(BSTNode(13))
    root.insert(BSTNode(6))
    root.insert(BSTNode(12))
    

    ## insert check
    
    l = []    
    inorder(root)
    print(f'tree transversal: {l}')
    print(f'RI check: {root.check_ri()}')
    
    ## delete check
   
    print(f'deleted node: {root.left.key}')
    root.left.delete()
    print(f'deleted node: {root.left.key}')
    root.left.delete()
    l = []
    inorder(root)
    print(f'tree transversal: {l}')
    print(f'RI check: {root.check_ri()}')

    
    ## find check
    #print(root.find(6))
    #print(root.find(55))
    # find_min check
    print(f'minimum: {root.find_min()}')
    print(f'maximum: {root.find_max()}')
    
    
    # next_greatest check
    print(f'root.key = {root}')
    print(f'next larger: {root.next_larger()}')
    
    # next_smallest check
    print(f'next smaller: {root.next_smaller()}')
    """
    
    
    
    




