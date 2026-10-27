# poetry run python -m unittest tests.test_app
import unittest
from app import app
import shutil
import os

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

        root = os.path.abspath(os.path.dirname(__file__))
        self.data_path = os.path.join(root, 'data')

        os.makedirs(self.data_path, exist_ok=True)
        
        self.create_document("about.md", "# header\n**bold text**\nnormal text")
        self.create_document("changes.txt", "2008 - Python 3.0 is released.")
        self.create_document("users.yaml", "admin: $2b$12$b1lKI7feVs5V0QlIf.jnKO/Rj5WkvovRwLttEVqA8U6E8i4oGg/OG\npete: $2b$12$Z1J9tIB4BpkvewwX9EWJPOr.LVqp3o0VWKra7uBDuy2wxNmGuWBVO")

    # helper
    def admin_session(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 'admin'
            return c
    
    def create_document(self, name, content=''):
        with open(os.path.join(self.data_path, name), 'w') as file:
            file.write(content)

    def tearDown(self):
        shutil.rmtree(self.data_path, ignore_errors=True)

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        self.assertIn("about.md", response.get_data(as_text=True))
        self.assertIn("changes.txt", response.get_data(as_text=True))

    def test_open_file(self):
        with self.client.get("/changes.txt") as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/plain; charset=utf-8")
            self.assertIn("2008 - Python 3.0 is released.", response.get_data(as_text=True))

    def test_file_not_exist(self):
        with self.client.get("/not_exist.txt") as response:
            self.assertEqual(response.status_code, 302)
        
        with self.client.get(response.headers['Location']) as response:
            self.assertIn("does not exist", response.get_data(as_text=True))

        with self.client.get("/") as response:
            self.assertNotIn("does not exist", response.get_data(as_text=True))
            
    def test_markdown_load(self):
        with self.client.get("/about.md") as response:
            self.assertIn("<h1>", response.get_data(as_text=True))

    def test_edit_file(self):
        client = self.admin_session()
        with client.get("/changes.txt/edit") as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("<textarea", response.get_data(as_text=True))
            self.assertIn('<input type="submit"', response.get_data(as_text=True))
        
    def test_update_data(self):
        client = self.admin_session()
        with client.post("/changes.txt/edit", data={'file_contents': 'hello'}) as response:
            self.assertEqual(response.status_code, 302)

        with client.get(response.headers['Location']) as follow_response:
            self.assertIn("changes.txt has been updated",
                        follow_response.get_data(as_text=True))

        with client.get("/changes.txt") as response:
            self.assertIn("hello", response.get_data(as_text=True))

    def test_new_document(self):
        client = self.admin_session()
        with client.get("/create_doc") as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("Add a new document:", response.get_data(as_text=True))
            self.assertIn('<input type="text"', response.get_data(as_text=True))
        
    def test_create_no_name_doc(self):
        client = self.admin_session()
        with client.post("/create_doc", data={'filename': ''}) as response:
            self.assertEqual(response.status_code, 422)
            self.assertIn("valid extension", response.get_data(as_text=True))

    def test_create_new_doc(self):
        client = self.admin_session()
        with client.post("/create_doc", data={'filename': 'hello.txt'}) as response:
            self.assertEqual(response.status_code, 302)
        
        with client.get(response.headers['Location']) as follow_response:
            self.assertIn("hello.txt has been created",
                        follow_response.get_data(as_text=True))

        with client.get('/') as response:
            self.assertIn("hello.txt", response.get_data(as_text=True))

    def test_delete_file(self):
        client = self.admin_session()
        # check delete button is there
        with self.client.get("/") as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("Delete", response.get_data(as_text=True))

        # delete a file
        with client.post("/changes.txt/delete", follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("changes.txt has been deleted", response.get_data(as_text=True))

        # deleted file is not listed
        with self.client.get("/") as response:
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("changes.txt", response.get_data(as_text=True))

    def test_delete_non_existant_file(self):
        client = self.admin_session()
        with client.post("/not_exist.txt/delete") as response:
            self.assertEqual(response.status_code, 422)
            self.assertIn("not_exist.txt does not exist", response.get_data(as_text=True))

    def test_sign_in(self):
        # homepage has sign in button
        with self.client.get("/") as response:
            self.assertIn("Sign In", response.get_data(as_text=True))

        # sign in page loads correctly
        with self.client.get("/sign_in") as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("<input", response.get_data(as_text=True))
            self.assertIn('<button type="submit"', response.get_data(as_text=True))

        # entering invalid credentials displays error message
        with self.client.post("/sign_in", data={'username': 'fer', 'password': ''}, follow_redirects=True) as response:
            self.assertEqual(response.status_code, 422)
            self.assertIn("Invalid", response.get_data(as_text=True))
            self.assertIn("fer", response.get_data(as_text=True))
            self.assertIn("Sign In", response.get_data(as_text=True))

        # log in to admin successfully
        with self.client.post("/sign_in", data={'username': 'admin', 'password': 'secret'}, follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("Welcome", response.get_data(as_text=True))
            self.assertIn("Signed in as admin", response.get_data(as_text=True))
            self.assertIn("Sign Out", response.get_data(as_text=True))

        # sign out successfully
        with self.client.post("/sign_out", follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("You have been signed out", response.get_data(as_text=True))
            self.assertIn("Sign In", response.get_data(as_text=True))

    def test_restrict_access(self):

        with self.client.get("/changes.txt/edit", follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("Login required", response.get_data(as_text=True))
                
        with self.client.post("/changes.txt/edit", data= {'file_contents': 'empty'}, follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("Login required", response.get_data(as_text=True))
                
        with self.client.get("/create_doc", follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("Login required", response.get_data(as_text=True))
                
        with self.client.post("/create_doc", data= {'filename': 'empty.txt'}, follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("Login required", response.get_data(as_text=True))
                
        with self.client.post("/changes.txt/delete", follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("Login required", response.get_data(as_text=True))

    def test_access_granted(self):
        client = self.admin_session()

        with client.get("/changes.txt/edit", follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("Login required", response.get_data(as_text=True))
                
        with client.post("/changes.txt/edit", data= {'file_contents': 'empty'}, follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("Login required", response.get_data(as_text=True))
                
        with client.get("/create_doc", follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("Login required", response.get_data(as_text=True))
                
        with client.post("/create_doc", data= {'filename': 'empty.txt'}, follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("Login required", response.get_data(as_text=True))
                
        with client.post("/changes.txt/delete", follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("Login required", response.get_data(as_text=True))

    def test_user_file(self):
        with self.client.get("/") as response:
            self.assertNotIn("users.yaml", response.get_data(as_text=True))

        client = self.admin_session()
        with client.get("/") as response:
            self.assertIn("users.yaml", response.get_data(as_text=True))

        with client.get("/users.yaml/edit") as response:
            self.assertNotIn("test: ", response.get_data(as_text=True))

        with client.post("/users.yaml/edit", data= {"file_contents": "admin: $2b$12$b1lKI7feVs5V0QlIf.jnKO/Rj5WkvovRwLttEVqA8U6E8i4oGg/OG\npete: $2b$12$Z1J9tIB4BpkvewwX9EWJPOr.LVqp3o0VWKra7uBDuy2wxNmGuWBVO\ntest: hello"}, follow_redirects=True) as response:
            pass

        # 'hello' gets encrypted
        with client.get("/users.yaml/edit") as response:
            self.assertIn("test: $2b$12$", response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
    