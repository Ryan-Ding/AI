import unittest
import os
from MP1.Graph import Graph

dir_path = os.path.dirname(os.path.realpath(__file__))

class GraphTestCase(unittest.TestCase):

    def test_parse_single_dot_file(self):
        graph = Graph(dir_path + "/mediumMaze.txt")
        self.assertEqual(graph.goals, [(1,59)])
        self.assertEqual(graph.start_position, (21,1))


if __name__ == '__main__':
    unittest.main()
