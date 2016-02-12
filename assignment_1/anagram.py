#!/usr/bin/python
import sys

word_arr = list(sys.argv[1])
word_arr.sort()
final_sol = list()

def find_anagram(word_arr,sol_list):
    len_arr = len(word_arr)
    if len_arr == 0:
        final_sol.append("".join(sol_list))
        return

    for i in range(len_arr):
        sol_list.append(word_arr[i])
        c = word_arr.pop(i)
        find_anagram(word_arr, sol_list)
        word_arr.insert(i,c)
        sol_list.pop(-1)
sol_list = list()

find_anagram(word_arr,sol_list)

output_file = open('anagram_out.txt', "w+")
for i,c in enumerate(final_sol):
    output_file.write(c + "\n")

#print final_sol
