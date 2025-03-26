import math
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import conint
import pytest
from unittest.mock import patch

class FactorialService:
    @staticmethod
    def calculate_factorials(n: int) -> List[int]:
        """
        Calculate first n factorials with input validation
        
        Args:
            n: Positive integer representing number of factorials to calculate
            
        Returns:
            List of factorials from 1! to n!
            
        Raises:
            ValueError: If n is not a positive integer or too large
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Input must be a positive integer")
        
        if n > 10000:  # Practical limit to prevent excessive computation
            raise ValueError("Input too large - maximum allowed is 10000")
        
        try:
            return [math.factorial(i) for i in range(1, n+1)]
        except OverflowError:
            raise ValueError("Factorial computation overflow")

# Unit tests
class TestFactorialService:
    def test_calculate_factorials_normal_case(self):
        assert FactorialService.calculate_factorials(5) == [1, 2, 6, 24, 120]
    
    def test_calculate_factorials_edge_case(self):
        assert FactorialService.calculate_factorials(1) == [1]
    
    def test_calculate_factorials_invalid_input(self):
        with pytest.raises(ValueError):
            FactorialService.calculate_factorials(-5)
        with pytest.raises(ValueError):
            FactorialService.calculate_factorials(0)
        with pytest.raises(ValueError):
            FactorialService.calculate_factorials(1.5)
    
    def test_calculate_factorials_large_input(self):
        with pytest.raises(ValueError):
            FactorialService.calculate_factorials(10001)
    
    @patch('math.factorial')
    def test_calculate_factorials_overflow(self, mock_factorial):
        mock_factorial.side_effect = OverflowError
        with pytest.raises(ValueError):
            FactorialService.calculate_factorials(1000)

# REST API
app = FastAPI(title="Factorial Service", version="1.0.0")

@app.get("/factorials/{n}", 
         response_model=List[int],
         summary="Get first n factorials",
         responses={
             200: {"description": "Successful response with factorials"},
             400: {"description": "Invalid input provided"},
             500: {"description": "Internal server error"}
         })
async def get_factorials(n: conint(gt=0, le=10000)):
    try:
        return FactorialService.calculate_factorials(n)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# API Tests
from fastapi.testclient import TestClient

client = TestClient(app)

def test_api_get_factorials():
    response = client.get("/factorials/5")
    assert response.status_code == 200
    assert response.json() == [1, 2, 6, 24, 120]

def test_api_invalid_input():
    response = client.get("/factorials/-5")
    assert response.status_code == 400

def test_api_large_input():
    response = client.get("/factorials/10001")
    assert response.status_code == 400
