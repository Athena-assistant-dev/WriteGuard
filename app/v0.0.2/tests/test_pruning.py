import os
import unittest
import shutil
import hashlib
import sys
from datetime import datetime, timedelta

# Add the parent directory to the Python path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_safe_write import prune_backups, backup_file, get_local_timestamp_safe

class TestPruning(unittest.TestCase):
    def setUp(self):
        self.test_file = "/tmp/pruning_test.txt"
        self.backup_dir = "/tmp/pruning_test_backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        with open(self.test_file, "w") as f:
            f.write("test content")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.backup_dir):
            shutil.rmtree(self.backup_dir)

    def _create_dummy_backup(self, days_ago):
        """Helper to create a dummy backup file with a specific age."""
        # Note: Using datetime.now() directly is okay for testing purposes
        # as we are creating a controlled test environment.
        timestamp = datetime.now() - timedelta(days=days_ago)
        timestamp_str = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        
        rel_path = os.path.relpath(self.test_file, "/")
        path_hash = hashlib.md5(rel_path.encode("utf-8")).hexdigest()[:8]
        base_name = os.path.basename(self.test_file)
        
        backup_name = f"{base_name}_{path_hash}_{timestamp_str}.bak"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        with open(backup_path, "w") as f:
            f.write(f"backup from {days_ago} days ago")
        
        # Manually set the modification time to match the timestamp in the filename
        os.utime(backup_path, (timestamp.timestamp(), timestamp.timestamp()))
        
        return backup_path

    def test_pruning_logic_with_mixed_ages(self):
        """
        Verify that the pruning logic correctly retains and deletes backups
        based on the tiered retention policy with a mix of backup ages.
        """
        # Create a set of backups with varying ages
        # 5 recent backups (should keep 4)
        for i in range(5):
            self._create_dummy_backup(days_ago=i) # 0, 1, 2, 3, 4 days old
        
        # 3 medium-term backups (should keep 2)
        for i in range(3):
            self._create_dummy_backup(days_ago=i + 8) # 8, 9, 10 days old

        # 2 old backups (should keep 1)
        self._create_dummy_backup(days_ago=15)
        self._create_dummy_backup(days_ago=30)
        
        # We have created 5 + 3 + 2 = 10 backups in total
        self.assertEqual(len(os.listdir(self.backup_dir)), 10)

        # Run the pruning function
        prune_backups(self.test_file, self.backup_dir)
        
        # Check that the correct number of backups remain
        remaining_files = os.listdir(self.backup_dir)
        self.assertEqual(len(remaining_files), 4 + 2 + 1, "Should keep 7 backups in total")

        # Optional: Verify that the correct *files* were kept
        remaining_files.sort(reverse=True)
        
        # Expected to keep backups from days 0, 1, 2, 3 (4 recent)
        # Expected to keep backups from days 8, 9 (2 medium)
        # Expected to keep backup from day 15 (1 old)
        
        kept_ages = []
        # Re-calculate the prefix to robustly parse the remaining filenames
        rel_path = os.path.relpath(self.test_file, "/")
        path_hash = hashlib.md5(rel_path.encode("utf-8")).hexdigest()[:8]
        base_name = os.path.basename(self.test_file)
        prefix = f"{base_name}_{path_hash}_"
        now_for_test = datetime.now()

        for f in remaining_files:
            ts_str = f[len(prefix):-len(".bak")]
            ts = datetime.strptime(ts_str, "%Y-%m-%d_%H-%M-%S")
            kept_ages.append((now_for_test - ts).days)
            
        expected_ages = [0, 1, 2, 3, 8, 9, 15]
        self.assertCountEqual(kept_ages, expected_ages, "The ages of the kept backups are not correct")

    def test_pruning_with_fewer_backups_than_limit(self):
        """
        Test that no backups are deleted if the number of backups is
        less than or equal to the retention limit.
        """
        # Create 2 recent, 1 medium, and 1 old backup
        self._create_dummy_backup(days_ago=1)
        self._create_dummy_backup(days_ago=2)
        self._create_dummy_backup(days_ago=8)
        self._create_dummy_backup(days_ago=20)
        
        self.assertEqual(len(os.listdir(self.backup_dir)), 4)

        prune_backups(self.test_file, self.backup_dir)
        
        self.assertEqual(len(os.listdir(self.backup_dir)), 4, "Should not delete any backups")

    def test_pruning_with_only_recent_backups(self):
        """
        Test pruning when all backups are recent.
        """
        # Create 6 recent backups (should keep 4)
        for i in range(6):
            self._create_dummy_backup(days_ago=i)
            
        self.assertEqual(len(os.listdir(self.backup_dir)), 6)
        
        prune_backups(self.test_file, self.backup_dir)
        
        self.assertEqual(len(os.listdir(self.backup_dir)), 4, "Should keep only 4 recent backups")

    def test_pruning_with_no_backups(self):
        """
        Test that the function runs without error when there are no backups.
        """
        self.assertEqual(len(os.listdir(self.backup_dir)), 0)
        
        try:
            prune_backups(self.test_file, self.backup_dir)
        except Exception as e:
            self.fail(f"prune_backups raised an exception with no backups: {e}")
        
        self.assertEqual(len(os.listdir(self.backup_dir)), 0)

if __name__ == "__main__":
    unittest.main()
