import cstl

# create a vector of integers
vec_int = cstl.VecInt()
vec_int.push_back(1)
vec_int.push_back(2)
vec_int.push_back(3)

# create a vector of strings
vec_str = cstl.VecStr()
vec_str.push_back('hello')
vec_str.push_back('world')

# create a map from string to int
map_str_int = cstl.MapStrInt()
map_str_int['one'] = 1
map_str_int['two'] = 2
map_str_int['three'] = 3

# create a map from string to vector of integers
map_str_vec_int = cstl.MapStrVecInt()
map_str_vec_int['vec1'] = vec_int
map_str_vec_int['vec2'] = cstl.VecInt([4, 5, 6])

# access elements
print(vec_int[0])          # 1
print(vec_str[1])          # world
print(map_str_int['two'])  # 2
print(map_str_vec_int['vec1'][2])  # 3
