import unittest
import requests
import os
import sys
import subprocess
import time

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestIntegration(unittest.TestCase):
    BASE_URL = "http://localhost:5050"
    
    @classmethod
    def setUpClass(cls):
        """Set up the database before any tests run."""
        # It can take a moment for the services to be fully up.
        time.sleep(5)
        
        print("Initializing database for integration tests...")
        # We need to run the init script inside the container.
        # This is a bit of a workaround for a testing environment.
        try:
            subprocess.run(
                ["sudo", "docker", "exec", "writeguard-v002", "python", "init_db.py"],
                check=True,
                capture_output=True,
                text=True
            )
            print("Database initialized successfully.")
        except subprocess.CalledProcessError as e:
            print("Failed to initialize database.")
            print("Stderr:", e.stderr)
            print("Stdout:", e.stdout)
            raise e

    def test_01_add_memory(self):
        """Test adding a memory."""
        payload = {
            "content": "This is a test memory for the new service.",
            "metadata": {"source": "integration_test_add"}
        }
        response = requests.post(f"{self.BASE_URL}/memory", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('memory_id', data)
        self.assertIn('memory', data)
        self.assertEqual(data['memory']['content'], payload['content'])
        
        # Store the ID for the next test
        TestIntegration.memory_id_to_test = data['memory_id']

    def test_02_get_memory(self):
        """Test retrieving a specific memory."""
        self.assertTrue(hasattr(TestIntegration, 'memory_id_to_test'), "Add memory test must run first.")
        memory_id = TestIntegration.memory_id_to_test
        
        response = requests.get(f"{self.BASE_URL}/memory/{memory_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data['memory']['id'], memory_id)
        self.assertEqual(data['memory']['content'], "This is a test memory for the new service.")

    def test_03_search_memory(self):
        """Test searching for memories."""
        # Add another memory to make search more meaningful
        requests.post(f"{self.BASE_URL}/memory", json={"content": "Another memory about something else."})
        
        payload = {"query": "new service"}
        response = requests.post(f"{self.BASE_URL}/memory/search", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIsInstance(data.get('results'), list)
        self.assertGreater(len(data.get('results', [])), 0)
        # The most relevant result should be the one we added
        self.assertEqual(data['results'][0]['content'], "This is a test memory for the new service.")

if __name__ == '__main__':
    # This allows running the tests in order
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIntegration, sort_tests=True))
    runner = unittest.TextTestRunner()
    runner.run(suite)
