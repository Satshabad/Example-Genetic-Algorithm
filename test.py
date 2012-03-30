'''
Created on Mar 29, 2012

@author: satshabad
'''
import unittest
import genetic
import copy

class GeneticTest(unittest.TestCase):
    
    def setUp(self):
        self.qmap = [[1, 2, 3, 4, 5, 4, 3, 2, 1],
                    [2, 3, 4, 5, 6, 5, 4, 3, 2],
                    [3, 4, 5, 6, 7, 6, 5, 4, 3],
                    [4, 5, 6, 7, 8, 7, 6, 5, 4],
                    [5, 6, 7, 8, 9, 8, 7, 6, 5],
                    [4, 5, 6, 7, 8, 7, 6, 5, 4],
                    [3, 4, 5, 6, 7, 6, 5, 4, 3],
                    [2, 3, 4, 5, 6, 5, 4, 3, 2],
                    [1, 2, 3, 4, 5, 4, 3, 2, 1]]
        self.population = [(1, 1), (1, 4), (4, 2), (5, 5), (4, 4)]
        
    def test_Quality(self):
        self.assertEqual(3, genetic.quality(self.population[0], self.qmap))
        
    def test_mutate_chromo(self):
        self.assertNotEqual(self.population[1], genetic.mutate_chromo(self.population[1]))
        
    def test_best_of_population(self):
        self.assertTupleEqual((4, 4), genetic.best_of_population(self.population, self.qmap))
        
    def test_pick_random_by_standard_method(self):
        oldPop = copy.deepcopy(self.population)
        chromo = genetic.pick_random_by_standard_method(self.population, self.qmap)
        self.assertEqual(oldPop, self.population)
        self.assertTrue(chromo in self.population)
        chromo = genetic.pick_random_by_standard_method([], self.qmap)
        self.assertEqual(None, chromo)
    
    def test_cull_population(self):
        oldPop = copy.deepcopy(self.population)
        newPop = genetic.cull_population(self.population, 3, self.qmap)
        self.assertEqual(3, len(newPop))
        self.assertTrue(genetic.best_of_population(oldPop, self.qmap) in newPop)
        
    def test_mate_chromo(self):
        self.assertEqual([(0, 1), (1, 4)], genetic.mate_chromo((0,4), [(0,4), (1,0)], self.qmap))
        
if __name__ == '__main__':
    unittest.main()
