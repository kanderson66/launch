class CustomSet:
    def __init__(self, lst=[]):
        self.items = []
        self.add_items(lst)
    
    def is_empty(self):
        return len(self.items) == 0

    def contains(self, num):
        return num in self.items

    def is_subset(self, other):
        for item in self.items:
            if item not in other.items:
                return False
        return True

    def is_disjoint(self, other):
        for item in self.items:
            if item in other.items:
                return False
        return True

    def is_same(self, other):
        if len(self) != len(other):
            return False
        return self.is_subset(other)

    def add(self, num):
        if num not in self.items:
            self.items.append(num)
    
    def add_items(self, lst):
        for item in lst:
            self.add(item)

    def intersection(self, other):
        return CustomSet([item for item in self.items if item in other.items])
    
    def difference(self, other):
        return CustomSet([item for item in self.items if item not in other.items])
    
    def union(self, other):
        result = CustomSet(self.items)
        result.add_items(other.items)

        return result

    def __eq__(self, other):
        return self.is_same(other)
    
    def __len__(self):
        return len(self.items)
