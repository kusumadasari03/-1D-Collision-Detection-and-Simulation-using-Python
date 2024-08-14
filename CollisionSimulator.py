# Reference taken from the Course book Data Structures and Algorithms in Python by Goodrich
# A Minimum Heap Class is defined 
class MinHeap:

    def __init__(self):
        self.storage = []  #Heap is stored in form of list
    
    def __len__(self):
        return len(self.storage)
   
    def parent(self,i):  #index corresponding to parent of a node provided its index i
        return  (i-1)// 2
   
    def left(self,i): #index corresponding to left child of a node provided its index i
        return 2*i + 1
   
    def right(self,i): #index corresponding to right child of a node provided its index i
        return 2*i + 2
   
    def has_left(self,i): #checks whether given node has a left child or not
        return self.left(i) < len(self.storage) # index beyond end of list?
   
    def has_right(self,i): #checks whether given node has a right child or not
        return self.right(i) < len(self.storage) # index beyond end of list?
   
    def swap(self,i,j): # Swaps the elements on the i'th and j'th index of the heap 
        self.storage[i], self.storage[j] = self.storage[j], self.storage[i]
    
    def upheapify(self,i): # a node with given index i is upheaped and brought up to its correct position
        parent = self.parent(i)
        while i>0 and self.storage[i] < self.storage[parent]:
            self.swap(i,parent) #swap happens if parent is bigger
            i = parent
            parent = self.parent(i)
    
    def downheapify(self,i): # a node with given index j is downheaped and brought down to its correct position
        while self.has_left(i):
            left = self.left(i)
            small_child = left # although right may be smaller
            if self.has_right(i):
                right = self.right(i)
                if self.storage[right] < self.storage[left]: #checks which which child is smaller and with who to swap
                    small_child = right
            if self.storage[small_child] > self.storage[i]:
                break
            else:
                self.swap(i, small_child) #swap happena if child is smaller
                i = small_child

    def is_empty(self): #checks if a given heap is empty
        return len(self.storage)==0

    def insert(self,value): # Insertion of an element in the heap and the element if upheaped to its correct position
        self.storage.append(value)
        self.upheapify(len(self.storage)-1)  # upheap newly added position

    def min(self): # returns the element on the top of the heap
        if self.is_empty():
            raise 'Priority queue is empty'
        item = self.storage[0]
        return item
    
    def remove_min(self): # Returns the element on the top of the heap and removes it from the Minimum Heap
        if self.is_empty():
            raise 'Priority queue is empty'
        self.swap(0,len(self.storage)-1) # put minimum item at the end
        item = self.storage.pop() # and remove it from the list;
        self.downheapify(0) # then fix new root
        return item

def time_calc(i,x,v): # returns the time taken in a collision between the i'th and i+1'th object
    if i < (len(x) - 1):
        if v[i+1] >= v[i] : # Conditio for valid collision
            return False
        else : 
            d = x[i+1] - x[i]
            v_app = v[i] - v[i+1]
            return float(d/v_app) 
    else:
        return False

def final_velocity_calc(i,m,v): #returns the velocity of i'th and i+1'th object after undergoing collision
    if i < (len(v) - 1):
        if v[i+1] >= v[i] : 
            return False
        else:
            v_1_f = float(((m[i]-m[i+1])*v[i] + 2*m[i+1]*v[i+1])/(m[i]+m[i+1]))
            v_2_f = float((2*m[i]*v[i] - (m[i]-m[i+1])*v[i+1])/(m[i]+m[i+1]))
            output = (v_1_f,v_2_f)
            return output
    else:
        return False

def x_calc(i,x,v): #Returns the position of i'th and i+1'th object after undergoing a colision
    if i < (len(x) - 1):
        if v[i+1] >= v[i] :
            return False
        else : 
            x_collision = float((((v[i]*x[i+1])-(v[i+1]*x[i])) / (v[i]-v[i+1])))
            return x_collision
    else:
        return False

def listCollisions(M,x,v,m,T):
    heap = MinHeap() #Heap
    time_array = [] # List containing the times of collision to be executed to eliminate the redundant tuples existing in the Heap/checker list
    time_last = [0]*len(M) # List containing the last time at which the objects collided 
    answer = [] # output list
    collision_counter = 0
    t_last = 0 # Time at which last collsion occured
    for i in range (0,len(M)-1): #initial heap is Created
        t = time_calc(i,x,v)
        time_array.append(t)
        if t != False :
            position = x_calc(i,x,v)
            heap.insert((t,i,position))

    while len(heap)>0 and collision_counter < m and heap.min()[0]<T: #Condition for the collisions to occur
        if len(heap) > 0:
            min_col = heap.remove_min() # Minimum time collision extracted from heap
        else:
            break
        if min_col[0] == time_array[min_col[1]]: # Condition for valid collision
            t_last = min_col[0] # last time of collision updated
            index = min_col[1] # index of the object whose collsion is executed
            time_last[index] = t_last # last collision executed updated in the list
            time_last[index+1] = t_last
            x[index] = min_col[2] # position list updated
            x[index+1] = min_col[2]
            vel = final_velocity_calc(min_col[1],M,v)
            v[index] = vel[0] # velocity list updated
            v[index+1] = vel[1]
            answer.append((round(min_col[0],4),round(min_col[1],4),round(min_col[2],4))) # output list updated with executed collision
            collision_counter += 1
            # objects on left and right of the colliding objects are analysed since their collision times will change
            if index-1 >= 0:  # Analyzing the i-1'th object
                if v[index] >= v[index-1] : # condition for valid collision
                    t_prev = False
                else : 
                    x_prev_init = x[index-1] + (v[index-1]*(t_last-time_last[index-1]))  # position of i-1'th object before collision
                    d = x[index] - x_prev_init
                    v_app = v[index-1] - v[index]
                    t_prev = t_last +  float(d/v_app) # time at which collision will happen
                    x_prev_final = float(((v[index-1]*x[index]-v[index]*x_prev_init)/(v[index-1]-v[index])))  # position of i-1'th and i'th object after collision
                    heap.insert((t_prev,index-1,x_prev_final)) # updated collision tuple for i-1'th object is updated in Heap
                    time_array[index-1] = t_prev  #corrected collision time for i-1'th object updated in checker list          
            
            if index+2 < len(x): # Analyzing the i+2'th object
                if v[index+2] >= v[index+1] : # condition for valid collision
                    t_next = False
                else : 
                    x_next_init = x[index+2] + v[index+2]*(t_last-time_last[index+2]) # position of i+2'th object before collision
                    d = x_next_init - x[index+1]
                    v_app = v[index+1] - v[index+2]
                    t_next = t_last + float(d/v_app) # time at which collision will happen
                    x_next_final = float(((v[index+1]*x_next_init-v[index+2]*x[index+1])/(v[index+1]-v[index+2]))) # position of i+1'th and i+2'th object after collision
                    heap.insert((t_next,index+1,x_next_final)) # updated collision tuple for i-1'th object is updated in Heap
                    time_array[index+1] = t_next #corrected collision time for i+1'th object updated in checker list    
        else: #Invalid collision
            continue #Move ahead to the next possible collision in the heap
    return answer # Return the Output List

