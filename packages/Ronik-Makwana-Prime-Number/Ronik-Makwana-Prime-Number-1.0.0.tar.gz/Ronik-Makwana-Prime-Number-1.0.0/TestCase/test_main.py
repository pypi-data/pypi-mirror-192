import pytest
import sys
sys.path.append(r"C:\\Users\\ronik.makwana\\Desktop\\Python_Training\\Day-21\\prime_number\\Src")
from Package.main import prime_number

def test_case_1():
    """Test the case-1"""
    assert prime_number(11) == True

def test_case_2():
    """Test the case-2"""
    assert prime_number(210) == False

def test_case_3():
    """Test the case-2"""
    assert prime_number(37) == True