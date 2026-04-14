"""
  Short summary: "Given two sorted arrays of size m and n, return the median of the two sorted arrays. Expected complexity: O(n).
  Time complexity: O(log(m+n))."
  Level - hard
  See https://leetcode.com/problems/median-of-two-sorted-arrays/
"""
import dataclasses
from typing import List, Optional


@dataclasses.dataclass(frozen=True)
class TestData:
  nums1: list[int]
  nums2: list[int]
  expected: float


class Solution:
  def findMedianSortedArrays(
      self, nums1: List[int], nums2: List[int]
  ) -> float:
    if len(nums1) > len(nums2):
      # simplify the logic by enforcing that `nums1` is always smaller or equal size to nums2
      return self.findMedianSortedArrays(nums2, nums1)

    m, n = len(nums1), len(nums2)
    left, right = 0, m

    while left <= right:
      partitionA = (left + right) // 2
      partitionB = (m + n + 1) // 2 - partitionA

      maxLeftA = (
        float("-inf") if partitionA == 0 else nums1[partitionA - 1]
      )
      minRightA = float("inf") if partitionA == m else nums1[partitionA]
      maxLeftB = (
        float("-inf") if partitionB == 0 else nums2[partitionB - 1]
      )
      minRightB = float("inf") if partitionB == n else nums2[partitionB]

      if maxLeftA <= minRightB and maxLeftB <= minRightA:
        if (m + n) % 2 == 0:
          return (
              max(maxLeftA, maxLeftB) + min(minRightA, minRightB)
          ) / 2
        else:
          return max(maxLeftA, maxLeftB)
      elif maxLeftA > minRightB:
        right = partitionA - 1
      else:
        left = partitionA + 1

  # this requires both O(m + n) time and memory
  def findMedianSortedArraysSlow(self, nums1: List[int], nums2: List[int]) -> float:
    out = []
    i = 0
    j = 0

    while i < len(nums1) and j < len(nums2):
      if nums1[i] <= nums2[j]:
        out.append(nums1[i])
        i += 1
      else:
        out.append(nums2[j])
        j += 1
    while i < len(nums1):
      out.append(nums1[i])
      i += 1
    while j < len(nums2):
      out.append(nums2[j])
      j += 1

    median = (out[len(out) // 2] + out[int(len(out) / 2 - 0.5)]) / 2
    return median

  # My shot on the task. I was quick to identify that solution is binary search, but I was trying guess the median value,
  # find where this value might have been in the input arrays and go from there. This was both very hard and slow.
  # It's unclear how this compares with the linear solution, cause leetcode tests don't use enough data and the linear
  # solution completes in 0ms
  def findMedianSortedArraysCustom(self, nums1: List[int], nums2: List[int]) -> float:
    if len(nums2) == 0:
      return (nums1[len(nums1) // 2] + nums1[int(len(nums1) / 2 - 0.5)]) / 2
    if len(nums1) == 0:
      return (nums2[len(nums2) // 2] + nums2[int(len(nums2) / 2 - 0.5)]) / 2
    median_i1 = int((len(nums1) + len(nums2)) / 2 - 0.5)
    median_i2 = (len(nums1) + len(nums2)) // 2

    def binary_search(target: List[int], term: int, start: int, end: int, comp) -> int:
      point = (start + end) // 2
      if start == end:
        return point
      comp_res = comp(term, target[point])
      if comp_res >= 0:
        return binary_search(target, term, point + 1, end, comp)
      else:
        return binary_search(target, term, start, point, comp)

      # Failed attempt to implement the fancy search and search for 2 medians at a time.
      # this particular code doesn't work when nums1=nums2=[2,2,4,4] because we find 2 and then try to find m2 between 2 and 3
      # def search_recursively(min: int, max: int, m1: Optional[int] = None, m2: Optional[int] = None):
      #   term = (min + max) // 2
      #   # find `pos` where out[i] > term for all i > `pos`
      #   pos1 = binary_search(nums1, term, 0, len(nums1), lambda v1, v2: v1 - v2 - 0.5)
      #   pos2 = binary_search(nums2, term, 0, len(nums2), lambda v1, v2: v1 - v2 - 0.5)
      #   min_i = pos1 + pos2
      #   # find `pos` where out[i] < term for all i < `pos`
      #   pos1 = binary_search(nums1, term, 0, len(nums1), lambda v1, v2: v1 - v2 + 0.5)
      #   pos2 = binary_search(nums2, term, 0, len(nums2), lambda v1, v2: v1 - v2 + 0.5)
      #   max_i = pos1 + pos2
      #
      #   if min_i <= median_i1 < max_i:
      #     m1 = term
      #   if min_i <= median_i2 < max_i:
      #     m2 = term
      #
      #   if m1 is not None and m2 is not None:
      #     return [m1, m2]
      #   elif min_i >= median_i2:
      #     return search_recursively(min, term, m1, m2)
      #   else:
      #     return search_recursively(term + 1, max, m1, m2)

    def search_recursively(min: int, max: int, target_median):
      term = (min + max) // 2
      # find `pos` where out[i] > term for all i > `pos`
      pos1 = binary_search(nums1, term, 0, len(nums1), lambda v1, v2: v1 - v2 - 0.5)
      pos2 = binary_search(nums2, term, 0, len(nums2), lambda v1, v2: v1 - v2 - 0.5)
      min_i = pos1 + pos2
      # find `pos` where out[i] < term for all i < `pos`
      pos1 = binary_search(nums1, term, 0, len(nums1), lambda v1, v2: v1 - v2 + 0.5)
      pos2 = binary_search(nums2, term, 0, len(nums2), lambda v1, v2: v1 - v2 + 0.5)
      max_i = pos1 + pos2

      if min_i <= target_median < max_i:
        return term
      elif min_i > target_median:
        return search_recursively(min, term, target_median)
      else:
        return search_recursively(term + 1, max, target_median)

    total_min = min(nums1[0], nums2[0])
    total_max = max(nums1[len(nums1) - 1], nums2[len(nums2) - 1])
    median_1 = search_recursively(total_min, total_max + 1, median_i1)
    if median_i1 == median_i2:
      return median_1
    else:
      median_2 = search_recursively(total_min, total_max + 1, median_i2)
      return (median_1 + median_2) / 2


tests = [
  TestData([2, 2, 4, 4], [2, 2, 4, 4], 3),
  TestData([], [1], 1),
  TestData([0, 0], [0, 0], 0),
  TestData([1, 2], [3], 2),
  TestData([1, 2], [3, 4], 2.5),
  TestData([1, 3], [2, 4], 2.5),
]

sol = Solution()

for t in tests:
  actual = sol.findMedianSortedArrays(t.nums1, t.nums2)
  assert actual == t.expected, f"Unexpected result {actual} for test case {t}"
