from collections.abc import MutableMapping

class Node:
    """Node contains a key value pair {key(str): value}
    Each node obj will be element in linked list

    Attributes:
    key- str key to be used for data retrevial
    value- stored data
    _next- pointer to next Node in linked list
    """
    def __init__(self, key, val, _next=None):
        self.key = key
        self.val = val
        self.next = _next


class LinkedList:
    """Linked List class- connected list of Node class objects. Each row of hashtable
    contains a linked list to store data in separate chaining

    Atributes:
    root = first Node of linked list

    Methods:
    add- args: key, val- if key is present- update val, if key not present-
      add Node with key,val to end of linked list
    get- arg: key, default_val- returns value if key value pair present in list, else returns default val
    delete- arg: key- removes item from list then reconnects nodes to fill in gap
    str- return string representation of linked list [Node]->[Node]->[Node]...

    """
    def __init__(self):
        self.root = None


    def add(self, key, val):
        #If key exists in Linked List, update val
        cur = self.root
        while cur:
            if cur.key == key:
                cur.val = val
                break
            cur = cur.next

        #If not, create a new node at beginning of linked list
        new_node = Node(key, val, self.root)
        self.root = new_node


    def get(self, key, default=0):
        #If key in linked list, return val
        cur = self.root
        
        while cur:
            if cur.key == key:
                return cur.val
            cur = cur.next

        #If not return default val
        return default
    

    def delete(self, key):
        #If key in linked list, drop Node (set prev item point to cur.next)
        cur = self.root
        prev = None

        while cur:
            if cur.key == key:
                if prev:
                    prev.next = cur.next
                else:
                    self.root = cur.next
                return None
            prev = cur
            cur = cur.next

        #If not, raise KeyError    
        raise KeyError(key)


    def __str__(self):
        result = ''
        cur = self.root
        while cur:
            result += f"[{cur.key}: {cur.val}] -> "
            cur = cur.next
        result += "END"
        return result


class Hashtable(MutableMapping):
    """Hashtable with separate chaining collision rule

    Attributes:
    _items- single list of LinkedList objs- list of length capacity
    _size- number of entries in hash table- starts at 0
    capacity- max size of hashtable- adjusted when table grows
    _default_value- default value of hash table entries
    _load_factor- what proportion of table will be filled before rehash implemented
    _growth_factor- multiplies hash table size when load factor reached

    Methods:
    hash- hash function takes key as input and returns integer which ise use to calculate
            index placement position in hashtable (index = hash val % capacity)
    __setitem__ - arg: key, val- input key, val Node obj at end of LinkedList in index position 
                    given by hash function
    __getitem__ - arg: key- return value if key is present in table, else raises KeyError
    __delitem__ - arg: key- delete key value pair Node obj from hashtable
    rehash- when load factor proportion is reached, saves table data, 
            creates a new bigger table (multiple origional table) by growth factor and 
            inserts old values into new table
    __len__- returns current size (number of Nodes contained in table) of hashtable
    """
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        self._items = [LinkedList() for i in range(capacity)]
        self._size = 0
        self.capacity = capacity
        self._default_value = default_value
        self._load_factor = load_factor
        self._growth_factor = growth_factor


    def _hash(self, key):
        """
        This method takes in a string and returns an integer value.
        This particular hash function uses Horner's rule to compute a large polynomial.
        See https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf
        DO NOT CHANGE THIS FUNCTION
        """
        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val


    def __setitem__(self, key, val):
        #Identify linked list to add item
        index = self._hash(key) % self.capacity
        index_ll = self._items[index]

        #If key not in list- add item
        if not index_ll.get(key, None):
            self._size += 1
        index_ll.add(key, val)
        
        #Rehash when load_factor surpassed
        if self._size / self.capacity > self._load_factor:
            self.rehash()


    def __getitem__(self, key):
        #Identify linked list that contains key
        index = self._hash(key) % self.capacity
        index_ll = self._items[index]
        val = index_ll.get(key, self._default_value)

        #Return value if key in linked list- else return default val
        return val if val is not None else self._default_value
    

    def __delitem__(self, key):
        #Identify linked list then implement delete method to delete item
        index = self._hash(key) % self.capacity
        self._items[index].delete(key)
        self._size -= 1
    

    def rehash(self):
        # Save the old table and create a new one with updated capacity
        orig_hash = self._items
        self.capacity *= self._growth_factor
        self._items = [LinkedList() for i in range(self.capacity)]

        # Reset size and re-insert items
        self._size = 0
        for ll in orig_hash:
            cur = ll.root
            while cur:
                self[cur.key] = cur.val
                cur = cur.next


    def __len__(self):
        return self._size


    def __iter__(self):
        """
        You do not need to implement __iter__ for this assignment.
        This stub is needed to satisfy `MutableMapping` however.)

        Note, by not implementing __iter__ your implementation of Markov will
        not be able to use 3things that depend upon it,
        that shouldn't be a problem but you'll want to keep that in mind.
        """
        raise NotImplementedError("__iter__ not implemented")