from typing import List, TypeVar, Iterable
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pytest

T = TypeVar('T')

class DeduplicationService:
    MAX_INPUT_SIZE = 10_000  # Ограничение для предотвращения проблем с памятью
    
    @classmethod
    def remove_duplicates(cls, items: Iterable[T]) -> List[T]:
        """
        Удаляет дубликаты с сохранением порядка элементов
        
        Args:
            items: Итерируемая коллекция элементов
            
        Returns:
            Список уникальных элементов в исходном порядке
            
        Raises:
            TypeError: При нехешируемых элементах
            ValueError: При превышении максимального размера
        """
        if len(items) > cls.MAX_INPUT_SIZE:
            raise ValueError(f"Максимальный размер ввода: {cls.MAX_INPUT_SIZE}")
        
        try:
            seen = set()
            return [x for x in items if not (x in seen or seen.add(x))]
        except TypeError as e:
            raise TypeError(f"Элементы должны быть хешируемыми: {str(e)}")

# Тесты
class TestDeduplicationService:
    def test_normal_case(self):
        assert DeduplicationService.remove_duplicates([1,2,2,3]) == [1,2,3]
    
    def test_empty_input(self):
        assert DeduplicationService.remove_duplicates([]) == []
    
    def test_unhashable_items(self):
        with pytest.raises(TypeError):
            DeduplicationService.remove_duplicates([{"a":1}, {"a":1}])

# REST API
app = FastAPI(title="Deduplication API", version="1.0.0")

class DeduplicationRequest(BaseModel):
    items: List[int]  # Можно расширить для поддержки других типов

@app.post(
    "/deduplicate",
    response_model=List[int],
    summary="Удалить дубликаты из списка",
    responses={
        200: {"description": "Успешный ответ"},
        400: {"description": "Некорректный ввод"},
        413: {"description": "Превышен размер ввода"}
    }
)
async def deduplicate_items(request: DeduplicationRequest):
    try:
        return DeduplicationService.remove_duplicates(request.items)
    except (TypeError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST if isinstance(e, TypeError) 
                        else status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(e)
        )
