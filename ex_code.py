class CustomSet:
    def __init__(self, elements=None):
        if elements is None:
            elements = []
        self._elements = []
        for el in elements:
            if el not in self._elements:
                self._elements.append(el)

    def is_empty(self):
        return len(self._elements) == 0

    def intersection(self, other_set):
        same_elements = [el for el in self._elements if other_set.contains(el)]
        return CustomSet(same_elements)

    def union(self, other_set):
        union_set = CustomSet(self._elements)
        for el in other_set._elements:
            union_set.add(el)
        return union_set

    def difference(self, other_set):
        different_elements = [el for el in self._elements if not other_set.contains(el)]
        return CustomSet(different_elements)

    def is_disjoint(self, other_set):
        return all(not other_set.contains(el) for el in self._elements)

    def is_same(self, other_set):
        if len(self._elements) != len(other_set._elements):
            return False
        return all(other_set.contains(el) for el in self._elements)

    def is_subset(self, other_set):
        return all(other_set.contains(el) for el in self._elements)

    def add(self, element):
        if element not in self._elements:
            self._elements.append(element)
        return self

    def contains(self, element):
        return element in self._elements

    def __eq__(self, other_set):
        return self.is_same(other_set)