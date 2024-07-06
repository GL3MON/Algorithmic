# Input reading and processing

def read_list_from_input(line):
    return [int(x) for x in line[1:-1].split(',')]

lines = []
while True:
    try:
        line = input()
        if line:
            lines.append(line)
    except EOFError:
        break

nums1 = read_list_from_input(lines[0])
nums2 = read_list_from_input(lines[1])
nums3 = read_list_from_input(lines[2])
nums4 = read_list_from_input(lines[3])


class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        m, n = len(nums1), len(nums2)
        if m > n:
            nums1, nums2, m, n = nums2, nums1, n, m
        imin, imax, half_len = 0, m, (m + n + 1) // 2
        while imin <= imax:
            i = (imin + imax) // 2
            j = half_len - i
            if i < m and nums2[j - 1] > nums1[i]:
                imin = i + 1
            elif i > 0 and nums1[i - 1] > nums2[j]:
                imax = i - 1
            else:
                if i == 0: max_left = nums2[j - 1]
                elif j == 0: max_left = nums1[i - 1]
                else: max_left = max(nums1[i - 1], nums2[j - 1])
                if (m + n) % 2 == 1:
                    return max_left
                if i == m: min_right = nums2[j]
                elif j == n: min_right = nums1[i]
                else: min_right = min(nums1[i], nums2[j])
                return (max_left + min_right) / 2.0

solution = Solution()
print(solution.findMedianSortedArrays(nums1, nums2))
print(solution.findMedianSortedArrays(nums3, nums4))