from typing import List, TypeVar, Iterable, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pytest

T = TypeVar('T')

class DeduplicationService:
    @staticmethod
    def remove_duplicates(items: Iterable[T]) -> List[T]:
        """
        Remove duplicates from container while preserving order
        
        Args:
            items: Iterable container with elements (must be hashable)
            
        Returns:
            List with unique elements in original order
            
        Raises:
            TypeError: If items contain unhashable types
        """
        try:
            seen = set()
            result = []
            for item in items:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            return result
        except TypeError as e:
            raise TypeError(f"Items must be hashable: {str(e)}")

# Unit tests
class TestDeduplicationService:
    def test_remove_duplicates_numbers(self):
        assert DeduplicationService.remove_duplicates([1, 2, 3, 2, 1]) == [1, 2, 3]
    
    def test_remove_duplicates_strings(self):
        assert DeduplicationService.remove_duplicates(['a', 'b', 'a', 'c']) == ['a', 'b', 'c']
    
    def test_remove_duplicates_empty(self):
        assert DeduplicationService.remove_duplicates([]) == []
    
    def test_remove_duplicates_all_same(self):
        assert DeduplicationService.remove_duplicates([1, 1, 1]) == [1]
    
    def test_remove_duplicates_unhashable(self):
        with pytest.raises(TypeError):
            DeduplicationService.remove_duplicates([{'a': 1}, {'b': 2}])

# REST API
app = FastAPI(title="Deduplication Service", version="1.0.0")

class ItemList(BaseModel):
    items: List[int]  # Using int for simplicity, could be generic in real implementation

@app.post("/deduplicate/",
          response_model=List[int],
          summary="Remove duplicates from list",
          responses={
              200: {"description": "List with duplicates removed"},
              400: {"description": "Invalid input provided"}
          })
async def deduplicate_items(item_list: ItemList):
    try:
        return DeduplicationService.remove_duplicates(item_list.items)
    except TypeError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# API Tests
client = TestClient(app)

def test_api_deduplicate():
    response = client.post("/deduplicate/", json={"items": [1, 2, 3, 2, 1]})
    assert response.status_code == 200
    assert response.json() == [1, 2, 3]

def test_api_deduplicate_empty():
    response = client.post("/deduplicate/", json={"items": []})
    assert response.status_code == 200
    assert response.json() == []

def test_api_deduplicate_unhashable():
    response = client.post("/deduplicate/", json={"items": [{"a": 1}, {"a": 1}]})
    assert response.status_code == 400
