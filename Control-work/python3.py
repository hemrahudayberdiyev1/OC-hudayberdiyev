from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pytest
import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedListService:
    @staticmethod
    def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Reverse a linked list using recursion with depth limit
        
        Args:
            head: Head node of the linked list
            
        Returns:
            New head of the reversed list
            
        Raises:
            RecursionError: If recursion depth exceeds limit
        """
        sys.setrecursionlimit(1000)  # Set reasonable recursion limit
        
        def _reverse(current: Optional[ListNode], prev: Optional[ListNode]) -> Optional[ListNode]:
            if not current:
                return prev
            next_node = current.next
            current.next = prev
            return _reverse(next_node, current)
        
        try:
            return _reverse(head, None)
        except RecursionError:
            raise RecursionError("Recursion depth exceeded - list too long")

    @staticmethod
    def list_to_linked_list(items: List[int]) -> Optional[ListNode]:
        """Convert Python list to linked list"""
        if not items:
            return None
        head = ListNode(items[0])
        current = head
        for val in items[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    @staticmethod
    def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
        """Convert linked list to Python list"""
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result

# Unit tests
class TestLinkedListService:
    def test_reverse_list_empty(self):
        assert LinkedListService.reverse_list(None) is None
    
    def test_reverse_list_single(self):
        node = ListNode(1)
        reversed_head = LinkedListService.reverse_list(node)
        assert reversed_head.val == 1
        assert reversed_head.next is None
    
    def test_reverse_list_multiple(self):
        head = LinkedListService.list_to_linked_list([1, 2, 3, 4])
        reversed_head = LinkedListService.reverse_list(head)
        assert LinkedListService.linked_list_to_list(reversed_head) == [4, 3, 2, 1]
    
    def test_reverse_list_recursion_limit(self):
        long_list = list(range(1, 1001))
        head = LinkedListService.list_to_linked_list(long_list)
        with pytest.raises(RecursionError):
            LinkedListService.reverse_list(head)

# REST API
app = FastAPI(title="Linked List Service", version="1.0.0")

class ListInput(BaseModel):
    items: List[int]

@app.post("/reverse-list/",
          response_model=List[int],
          summary="Reverse a linked list",
          responses={
              200: {"description": "Reversed list"},
              400: {"description": "Invalid input or recursion error"}
          })
async def reverse_list_endpoint(input_data: ListInput):
    try:
        head = LinkedListService.list_to_linked_list(input_data.items)
        reversed_head = LinkedListService.reverse_list(head)
        return LinkedListService.linked_list_to_list(reversed_head)
    except RecursionError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# API Tests
client = TestClient(app)

def test_api_reverse_list():
    response = client.post("/reverse-list/", json={"items": [1, 2, 3, 4]})
    assert response.status_code == 200
    assert response.json() == [4, 3, 2, 1]

def test_api_reverse_empty():
    response = client.post("/reverse-list/", json={"items": []})
    assert response.status_code == 200
    assert response.json() == []

def test_api_reverse_long_list():
    response = client.post("/reverse-list/", json={"items": list(range(1, 1001))})
    assert response.status_code == 400
