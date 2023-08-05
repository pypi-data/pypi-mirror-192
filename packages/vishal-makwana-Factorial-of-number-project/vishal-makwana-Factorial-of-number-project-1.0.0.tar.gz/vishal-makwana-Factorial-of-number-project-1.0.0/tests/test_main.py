import pytest
import sys
sys.path.append(r"C:\Users\vishal.makwana\2023-nirma-college-1\vishal_makwana\Python\Day-21\Day-21_1\Src")
from Src.Package.main import factorial

def test_factorial_1():
    """Test the case-1"""
    assert factorial(5) == 120

def test_factorial_2():
    """Test the case-2"""
    assert factorial(10) == 3628800

def test_factorial_3():
    """Test the case-2"""
    assert factorial(11) == 39916800