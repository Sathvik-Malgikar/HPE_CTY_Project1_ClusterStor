# conftest.py
import pytest

all_tcs = set()


def pytest_collectstart(collector: pytest.Collector):
    global all_tcs
    for ele in collector.collect():
        if type(ele) == pytest.Function:
            all_tcs.add(ele.name)


def pytest_deselected(items):
    # print(items)
    global all_tcs
    for ele in items:
        if type(ele) == pytest.Function:
            all_tcs.discard(ele.name)


def pytest_collection_finish(session):
    with open('test/selected_test_cases.txt', 'w') as file:
        for tc in all_tcs:
            file.write(tc + '\n')
