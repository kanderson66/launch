import unittest
from todolist import Todo, TodoList

class TestTodoList(unittest.TestCase):
    def setUp(self):
        self.todo1 = Todo("Buy milk")
        self.todo2 = Todo("Clean room")
        self.todo3 = Todo("Go to the gym")

        self.todos = TodoList("Today's Todos")
        self.todos.add(self.todo1)
        self.todos.add(self.todo2)
        self.todos.add(self.todo3)

    # your tests go here
    def test_length(self):
        self.assertEqual(3, len(self.todos))

    def test_to_list(self):
        self.assertEqual([self.todo1, self.todo2, self.todo3], self.todos.to_list())
    
    def test_first(self):
        self.assertEqual(self.todo1, self.todos.first())
    
    def test_last(self):
        self.assertEqual(self.todo3, self.todos.last())
        
    def test_all_done(self):
        self.assertFalse(self.todos.all_done())

    def test_add_invalid(self):
        with self.assertRaises(TypeError):
            self.todos.add(3)

        with self.assertRaises(TypeError):
            self.todos.add('hi')

        with self.assertRaises(TypeError):
            self.todos.add(self.todo1, self.todo2)

    def test_todo_at(self):
        self.assertEqual(self.todo1, self.todos.todo_at(0))
        self.assertEqual(self.todo2, self.todos.todo_at(1))

        with self.assertRaises(IndexError):
            self.todos.todo_at(5)

        with self.assertRaises(TypeError):
            self.todos.todo_at()

    def test_mark_done_at(self):

        with self.assertRaises(IndexError):
            self.todos.mark_done_at(5)
        
        for idx in range(len(self.todos)):
            self.assertFalse(self.todos.todo_at(idx).done)
            
            self.todos.mark_done_at(idx)
            self.assertTrue(self.todos.todo_at(idx).done)

    def test_mark_undone_at(self):

        with self.assertRaises(IndexError):
            self.todos.mark_done_at(5)
        
        for idx in range(len(self.todos)):
            self.assertFalse(self.todos.todo_at(idx).done)
            
            self.todos.mark_done_at(idx)
            self.assertTrue(self.todos.todo_at(idx).done)

            self.todos.mark_undone_at(idx)
            self.assertFalse(self.todos.todo_at(idx).done)

    def test_mark_all_done(self):
        self.todos.mark_all_done()

        for idx in range(len(self.todos)):
            self.assertTrue(self.todos.todo_at(idx).done)
        
        self.assertTrue(self.todos.all_done())

    def test_remove_at(self):
        with self.assertRaises(TypeError):
            self.todos.remove_at()
            
        with self.assertRaises(IndexError):
            self.todos.remove_at(5)

        original_length = len(self.todos) 
        remove_idx = 1
        original_items = self.todos.to_list()
        self.assertEqual(original_items[remove_idx], self.todos.todo_at(remove_idx))

        self.todos.remove_at(remove_idx)
        self.assertNotEqual(original_length, len(self.todos))

        self.assertNotEqual(original_items[remove_idx], self.todos.todo_at(remove_idx))
        self.assertEqual(original_items[remove_idx + 1], self.todos.todo_at(remove_idx))

    def test_str(self):
        string = (
            "---- Today's Todos ----\n"
            "[ ] Buy milk\n"
            "[ ] Clean room\n"
            "[ ] Go to the gym"
        )
        
        self.assertEqual(string, str(self.todos))

    def test_str_done_todo(self):
        self.todos.mark_done_at(0)
        string = (
            "---- Today's Todos ----\n"
            "[X] Buy milk\n"
            "[ ] Clean room\n"
            "[ ] Go to the gym"
        )
        self.assertEqual(string, str(self.todos))

    def test_str_all_done_todos(self):
        self.todos.mark_all_done()
        string = (
            "---- Today's Todos ----\n"
            "[X] Buy milk\n"
            "[X] Clean room\n"
            "[X] Go to the gym"
        )
        self.assertEqual(string, str(self.todos))

    def test_each(self):
        def mark_done(todo):
            todo.done = True
        self.todos.each(mark_done)
        self.assertTrue(self.todos.all_done())

    def test_select(self):
        self.todos.mark_done_at(1)
        items = self.todos.select(lambda todo: todo.done)
        self.assertEqual([self.todo2], items.to_list())

if __name__ == "__main__":
    unittest.main()