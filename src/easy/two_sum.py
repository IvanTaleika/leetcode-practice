"""
  Short summary: "Given an array of integers nums and an integer target, return indices of the **two** numbers
  such that they add up to target."
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
  # The classic Leetcode problem
  def twoSum(self, nums: List[int], target: int) -> List[int]:
    search_dict = {}
    for i in range(0, len(nums)):
      diff = target - nums[i]
      if diff in search_dict:
        return [search_dict[diff], i]
      search_dict[nums[i]] = i
    raise ValueError("target not found")

  # The generalization of the problem (which I was trying to solve for some time expecting a sub O(n) complexity).
  # The real complexity is O(n^(N-1))
  def nSum(self, nums: List[int], target: int, n: int) -> List[int]:
    if n < 2:
      raise ValueError("n must be at least 2")

    indexed_nums = sorted((value, index) for index, value in enumerate(nums))
    result = self._n_sum(indexed_nums, target, n, 0)
    if result is None:
      raise ValueError("target not found")
    return result

  def _n_sum(self, nums: List[tuple[int, int]], target: int, n: int, start: int) -> List[int] | None:
    if n == 2:
      left = start
      right = len(nums) - 1
      while left < right:
        total = nums[left][0] + nums[right][0]
        if total == target:
          return [nums[left][1], nums[right][1]]
        if total < target:
          left += 1
        else:
          right -= 1
      return None

    for i in range(start, len(nums) - n + 1):
      if i > start and nums[i][0] == nums[i - 1][0]:
        continue

      sub_result = self._n_sum(nums, target - nums[i][0], n - 1, i + 1)
      if sub_result is not None:
        return [nums[i][1]] + sub_result

    return None


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

n_sum_tests = [
  TestData([2, 7, 11, 15], 9, [0, 1]),
  TestData([1, 2, 3, 4, 5], 9, [1, 2, 3]),
  TestData([1, 0, -1, 0, -2, 2], 0, [0, 1, 2, 5]),
]


for t in n_sum_tests:
  n = len(t.expected)
  actual = sol.nSum(nums=t.nums, target=t.target, n=n)
  assert sum(t.nums[i] for i in actual) == t.target, f"Unexpected sum for test case {t} with n={n}"
  assert len(actual) == n, f"Unexpected result length {actual} for test case {t} with n={n}"
