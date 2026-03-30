"""
  Short summary: "Given an array of integers nums and an integer target, return indices of the !two! numbers such that they add up to target."
  Level - easy
  See https://leetcode.com/problems/two-sum/description/
"""
import dataclasses
from typing import List


@dataclasses.dataclass(frozen=True)
class TestData:
  nums: list[int]
  target: int
  expected: list[int]


class Solution:
  def twoSum(self, nums: List[int], target: int) -> List[int]:
    search_dict = {}
    for i in range(0, len(nums)):
      diff = target - nums[i]
      if diff in search_dict:
        return [search_dict[diff], i]
      search_dict[nums[i]] = i
    raise ValueError("target not found")


tests = [
  TestData([2, 7, 11, 15], 9, [0, 1]),
  TestData([3, 2, 4], 6, [1, 2]),
  TestData([3, 3], 6, [0, 1]),
  TestData([3, 2, 3], 6, [0, 2]),
]

sol = Solution()
for t in tests:
  actual = sol.twoSum(nums=t.nums, target=t.target)
  assert actual == t.expected, f"Unexpected result {actual} for test case {t}"
