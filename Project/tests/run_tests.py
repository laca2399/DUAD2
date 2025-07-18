import pytest

if __name__ == "__main__":
    result = pytest.main(["-v", "--tb=short", "--maxfail=3"])
    if result == 0:
        print("✅ All tests passed successfully!")
    else:
        print(f"❌ Some tests failed. Exit code: {result}")
