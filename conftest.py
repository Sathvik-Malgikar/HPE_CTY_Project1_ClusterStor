# conftest.py
import pytest

EXEC_MODE = "GUI"  #  "GUI" or "CLI"


def pytest_collection_finish(session):
    """
    Called after test collection has been performed.

    This function is called after test collection has been performed.
    It writes the names of selected test cases to a file named
    'selected_test_cases.txt' in the 'test' directory.

    Parameters:
        session (pytest.Session): The pytest session object.

    Returns:
        None

    Raises:
        None
    """
    print(session.items)
    with open('test/selected_test_cases.txt', 'w') as file:
        for item in session.items:
            file.write(item.name + '\n')
