import unittest
from aiodoo_datasets.generators.execution.protocol.protocol_statistics import ProtocolStatistics

class TestProtocolStatistics(unittest.TestCase):
    def test_statistics(self):
        stats = ProtocolStatistics()
        self.assertEqual(stats.mapped_plans, 0)
        
        stats.mapped_plans = 1
        stats.mapped_stages = 5
        stats.serialization_count = 2
        stats.protocol_size_bytes = 1024
        
        self.assertEqual(stats.mapped_plans, 1)
        self.assertEqual(stats.mapped_stages, 5)
        self.assertEqual(stats.serialization_count, 2)
        self.assertEqual(stats.protocol_size_bytes, 1024)

if __name__ == '__main__':
    unittest.main()
