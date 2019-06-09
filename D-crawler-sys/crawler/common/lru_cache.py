__all__=(
    "LRUCache",
)

class LRUCache:
    '''
        LRU_Cache (Least Recently Used)
    
        可以用一先构造一个有限大小的栈stack，node在栈所在位置表示了它入栈的时间
        为了在O(1)时间内push到顶部或pop底部元素，应该使用双向链表
    
        但是问题是key相同的node在stack中不能重复出现
        也就是说put时，要先检查stack中是否有这个node，如果有，则要把它移动到stack顶部，否则直接入栈
        如果不进行优化，复杂度是O(n)，主要是搜索元素比较耗时
    
        为了在要求的O(1)时间内做到，应该想到 hash table（python里对应的是dict或者set）
        
        dict里存{key:node(key,val)}，stack存dict中的node（的引用）
        因为在python中可以说所有可变对象都都可以当引用来用，所以很方便；但如果是C++中，则应该使用指针
    
        因为可以通过dict迅速定位node，所以时间复杂度是O(1)
        
    '''
    def __init__(self, capacity: int):
        self.time = 0
        self.node_in_cache = {}
        self.stack = CacheStack()
        self.stack_size = 0
        self.capacity = capacity
 
    def get(self, key):
        # 查看是否在缓存中
        node = self.node_in_cache.get(key)
        if node is None:
            return None # 如果没找到，返回 None 
        # 移动结点
        self.stack.move_node_to_top(node)
        return node.val
 
    def put(self, key, value) -> None:
        if(self.capacity <= 0):
            return
        # 查看是否在缓存中
        node = self.node_in_cache.get(key)
        if node:
            # 如果在缓存中，移动结点
            self.stack.move_node_to_top(node)
            node.val = value
        else:
            # 如果栈满了，应该清除栈底元素botton_node
            # 这意味着同时在stack和dict中删除bottom_node
            if self.stack_size+1 > self.capacity:
                tmp = self.stack.get_bottom_node()
                if tmp:
                    self.stack.remove_bottom_node()
                    self.node_in_cache.pop(tmp.key)
                    self.stack_size -= 1
            # 如果不在，则应该在字典中加入相应结点
            node = Node(key, value)
            self.node_in_cache[key] = node
            # 元素入栈
            self.stack.move_node_to_top(node)
            self.stack_size += 1

class Node:
    # 在python中属性少，但是实例多的时候可以考虑使用__slots__优化
    __slots__=('up','down','key','val')
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.up = None
        self.down = None
 
    def down_insert(self, node):
        if node:
            node.down = self.down
            if self.down:
                self.down.up = node
            node.up = self
            self.down = node
 
    def remove(self):
        u, d = self.up, self.down
        if u:
            u.down = d
        if d:
            d.up = u
 
 
class CacheStack:
    def __init__(self):
        self.top = Node(None, None)
        self.bottom = Node(None, None)
        self.top.down_insert(self.bottom)
 
    def move_node_to_top(self, node):
        if node is self.bottom or node is self.top:
            return
        node.remove()
        self.top.down_insert(node)
 
    def get_bottom_node(self):
        return None if self.bottom.up is self.top else self.bottom.up
 
    def remove_bottom_node(self):
        if self.bottom.up is self.top:
            return
        self.bottom.up.remove()
             
 