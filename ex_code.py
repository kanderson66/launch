

class Element:
    def __init__(self, datum, next_element=None):
        self.datum = datum
        self.next = next_element
    
    def is_tail(self):
        return not self.next

class SimpleLinkedList:
    def __init__(self):
        self.lst = []
    
    @property
    def size(self):
        return len(self.lst)

    @property
    def head(self):
        return None if self.is_empty() else self.lst[-1]

    def is_empty(self):
        return not len(self.lst)
    
    def push(self, datum):
        self.lst.append(Element(datum, self.head))

    def peek(self):
        return None if self.is_empty() else self.head.datum
    
    def pop(self):
        if len(self.lst) > 1:
            self.lst[-2].next = None
        return self.lst.pop().datum

    @staticmethod
    def from_list(lst):
        llst = SimpleLinkedList()

        if lst:
            for item in lst[::-1]:
                llst.push(item)

        return llst
    
    def to_list(self):
        lst = []
        if not self.head:
            return []

        element = Element(self.head.datum, self.head.next)

        while not element.is_tail():
            lst.append(element.datum)
            element = element.next
        lst.append(element.datum)
        return lst

    def reverse(self):
        lst = self.to_list()
        lst.reverse()
        return self.__class__.from_list(lst)
