import math
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import conint
import pytest

class FactorialService:
    MAX_INPUT = 1000  # Практическое ограничение для предотвращения переполнения
    
    @classmethod
    def calculate_factorials(cls, n: int) -> List[int]:
        """
        Вычисляет первые n факториалов с валидацией ввода
        
        Args:
            n: Натуральное число (1 ≤ n ≤ MAX_INPUT)
            
        Returns:
            Список факториалов от 1! до n!
            
        Raises:
            ValueError: При недопустимом вводе
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Входное значение должно быть натуральным числом")
        if n > cls.MAX_INPUT:
            raise ValueError(f"Максимальное допустимое значение: {cls.MAX_INPUT}")
        
        try:
            return [math.factorial(i) for i in range(1, n+1)]
        except OverflowError:
            raise ValueError("Произошло переполнение при вычислении факториала")

# Тесты
class TestFactorialService:
    def test_normal_case(self):
        assert FactorialService.calculate_factorials(5) == [1, 2, 6, 24, 120]
    
    def test_edge_case(self):
        assert FactorialService.calculate_factorials(1) == [1]
    
    def test_invalid_input(self):
        with pytest.raises(ValueError):
            FactorialService.calculate_factorials(-1)
        with pytest.raises(ValueError):
            FactorialService.calculate_factorials(0)
        with pytest.raises(ValueError):
            FactorialService.calculate_factorials(1001)

# REST API
app = FastAPI(title="Factorial API", version="1.0.0")

@app.get(
    "/factorials/{n}",
    response_model=List[int],
    summary="Получить последовательность факториалов",
    responses={
        200: {"description": "Успешный ответ"},
        400: {"description": "Некорректный ввод"},
        500: {"description": "Внутренняя ошибка сервера"}
    }
)
async def get_factorials(n: conint(gt=0, le=FactorialService.MAX_INPUT)):
    try:
        return FactorialService.calculate_factorials(n)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
