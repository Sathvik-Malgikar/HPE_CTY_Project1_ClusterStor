# conftest.py
import pytest

all_tcs = set()


def pytest_collectstart(collector: pytest.Collector):
    """
    Called when test collection starts.

    This function is called at the start of test collection.
    It iterates through collected items and adds the names of
    test cases to a global set if they are of type pytest.Function.

    Parameters:
        collector (pytest.Collector): The test collector object.

    Returns:
        None

    Raises:
        None
    """
    global all_tcs
    for ele in collector.collect():
        if type(ele) == pytest.Function:
            all_tcs.add(ele.name)


def pytest_deselected(items):
    """
    Called for deselected test items.

    This function is called for deselected test items.
    It removes the names of deselected test cases from
    the global set if they are of type pytest.Function.

    Parameters:
        items (list): The list of deselected test items.

    Returns:
        None

    Raises:
        None
    """
    global all_tcs
    for ele in items:
        if type(ele) == pytest.Function:
            all_tcs.discard(ele.name)


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
    with open('test/selected_test_cases.txt', 'w') as file:
        for tc in all_tcs:
            file.write(tc + '\n')
