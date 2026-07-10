import unittest
from aiodoo_datasets.generators.execution.export.export_statistics import ExportStatistics

class TestExportStatistics(unittest.TestCase):
    def test_statistics(self):
        stats = ExportStatistics()
        stats.exported_files = 3
        stats.jsonl_records = 10
        stats.export_duration = 1.5
        
        self.assertEqual(stats.exported_files, 3)
        self.assertEqual(stats.jsonl_records, 10)
        self.assertEqual(stats.export_duration, 1.5)

if __name__ == '__main__':
    unittest.main()
