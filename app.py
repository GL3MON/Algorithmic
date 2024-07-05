from Algorithmic.pipeline.graph import Graph

graph = Graph()

app = graph.app()

test_cases = open("input.txt", "r").read()
required_output = open("output.txt", "r").read()

question = '''4. Median of Two Sorted Arrays
Hard
Topics
Companies
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

 

Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
 

Constraints:

nums1.length == m
nums2.length == n
0 <= m <= 1000
0 <= n <= 1000
1 <= m + n <= 2000
-106 <= nums1[i], nums2[i] <= 106
'''


from pprint import pprint
inputs = {"question": question, "error":"", "test_cases": test_cases, "required_output": required_output, "regenerate_count":0}
for output in app.stream(inputs, {"recursion_limit": 50}):
    for key, value in output.items():
        pprint(f"Finished running: {key}:")
print("THE FINAL OUTPUT CODE:")
pprint(value["final_code"])
print("THE LOGIC CODE:")
print(value['logic_code'])