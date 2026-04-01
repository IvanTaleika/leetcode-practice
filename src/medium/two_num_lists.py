"""
  Short summary: "Sum two non-empty linked lists representing two non-negative integers digit-by-digit. The digits are
  stored in reverse order."
  Level - medium
  See https://leetcode.com/problems/add-two-numbers/
"""

# Definition for singly-linked list.
from typing import Optional


class ListNode:
  def __init__(self, val=0, next=None):
    self.val = val
    self.next = next


class Solution:
  def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    # `root_node = curr_node = ListNode()` implements the assignment as well, lists always have at least 1 element
    # (despite what their type hints might suggest) and it technically slightly faster.
    # However, this implementation is more versatile
    root_node = None
    curr_node = ListNode()
    n1 = l1
    n2 = l2

    while n1 or n2:
      if not root_node:
        root_node = curr_node

      d1 = n1.val if n1 else 0
      d2 = n2.val if n2 else 0
      sub_s = d1 + d2 + curr_node.val
      n1 = n1.next if n1 else None
      n2 = n2.next if n2 else None
      curr_node.val = sub_s % 10
      if n1 or n2 or sub_s >= 10:
        curr_node.next = ListNode(sub_s // 10)
        curr_node = curr_node.next

    return root_node

  def addTwoNumbersToInt(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> int:
    s = 0
    p = 1
    n1 = l1
    n2 = l2
    while n1 or n2:
      d1 = n1.val if n1 else 0
      d2 = n2.val if n2 else 0
      s += (d1 + d2) * p
      n1 = n1.next if n1 else None
      n2 = n2.next if n2 else None
      p *= 10
    return s
