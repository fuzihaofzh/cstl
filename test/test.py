import sys
sys.path.append("cstl")
import cstl
import unittest


class TestAddNumbers(unittest.TestCase):
    def test_tofrom(self):
        vss = [
            [{1:4, 5:6}, {3:5, 7:8, 10:3}],
            {1:2, 3:4, 5:6},
            {1, 2, 3, 4},
            set([1,2,3,4]),
            {1:[3,4,5], 3:[5,4,2], 5:[3,3,5]},
            {1:set([3,4,5]), 3:set([5,4,2]), 5:set([3,3,5])},
        ]
        for vs in vss:
            cv = cstl.frompy(vs)
            v1 = cstl.topy(cv)
            self.assertEqual(vs, v1)

    def test_vecint(self):
        # create a vector of integers
        vec_int = cstl.VecInt()
        vec_int.push_back(1)
        vec_int.push_back(2)
        vec_int.push_back(3)
        self.assertEqual(vec_int[1], 2)
        self.assertEqual(cstl.topy(vec_int), [1,2,3])

    def test_vecstr(self):
        # create a vector of strings
        vec_str = cstl.VecStr()
        vec_str.push_back('hello')
        vec_str.push_back('world')
        self.assertEqual(cstl.topy(vec_str), ['hello', 'world'])

    def test_vecstr(self):
        # create a map from string to int
        map_str_int = cstl.MapStrInt()
        map_str_int['one'] = 1
        map_str_int['two'] = 2
        map_str_int['three'] = 3
        self.assertEqual(cstl.topy(map_str_int), {'one' : 1, 'two' : 2, 'three' : 3})

    def test_compose(self):
        cmsi = cstl.MapStrVecInt()
        v1 = cstl.VecInt([1,2,3])
        v2 = cstl.VecInt([1,5,3])
        v3 = cstl.VecInt([1,6,3])
        cmsi['v1'] = v1
        cmsi['v2'] = v2
        cmsi['v3'] = v3
        self.assertEqual(cstl.topy(cmsi), {'v3': [1, 6, 3], 'v2': [1, 5, 3], 'v1': [1, 2, 3]})

    def test_return_ref(self):
        a = cstl.frompy([[1,2,3], [4,5,6]])
        b1 = a[0]
        b2 = a[0]
        b1[1] = 10
        self.assertEqual(b2[1], 10)


unittest.main()