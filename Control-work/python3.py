from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import pytest

class LinkedListService:
    MAX_RECURSION_DEPTH = 1000  # Защита от переполнения стека
    
    class ListNode:
        def __init__(self, val=0, next=None):
            self.val = val
            self.next = next
    
    @classmethod
    def reverse_list(cls, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Рекурсивно разворачивает связный список
        
        Args:
            head: Начало связного списка
            
        Returns:
            Развернутый связный список
            
        Raises:
            RecursionError: При превышении глубины рекурсии
        """
        sys.setrecursionlimit(cls.MAX_RECURSION_DEPTH)
        
        def _reverse(node: Optional[ListNode], prev: Optional[ListNode]) -> Optional[ListNode]:
            if not node:
                return prev
            next_node = node.next
            node.next = prev
            return _reverse(next_node, node)
        
        try:
            return _reverse(head, None)
        except RecursionError:
            raise RecursionError(f"Превышена максимальная глубина рекурсии: {cls.MAX_RECURSION_DEPTH}")

# Тесты
class TestLinkedListService:
    def test_normal_case(self):
        node3 = LinkedListService.ListNode(3)
        node2 = LinkedListService.ListNode(2, node3)
        node1 = LinkedListService.ListNode(1, node2)
        
        reversed_head = LinkedListService.reverse_list(node1)
        assert reversed_head.val == 3
        assert reversed_head.next.val == 2
        assert reversed_head.next.next.val == 1
    
    def test_empty_list(self):
        assert LinkedListService.reverse_list(None) is None

# REST API
app = FastAPI(title="LinkedList API", version="1.0.0")

class LinkedListRequest(BaseModel):
    items: List[int]

@app.post(
    "/reverse",
    response_model=List[int],
    summary="Развернуть связный список",
    responses={
        200: {"description": "Успешный ответ"},
        400: {"description": "Некорректный ввод"},
        500: {"description": "Ошибка при развороте"}
    }
)
async def reverse_list(request: LinkedListRequest):
    # Конвертация списка в связный список
    if not request.items:
        return []
    
    head = LinkedListService.ListNode(request.items[0])
    current = head
    for val in request.items[1:]:
        current.next = LinkedListService.ListNode(val)
        current = current.next
    
    # Разворот
    try:
        reversed_head = LinkedListService.reverse_list(head)
    except RecursionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))
    
    # Конвертация обратно в список
    result = []
    while reversed_head:
        result.append(reversed_head.val)
        reversed_head = reversed_head.next
    
    return result
