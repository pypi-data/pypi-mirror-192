import pytest

from simple_categorisation import Categoriser


@pytest.fixture
def category():
    cat = Categoriser()
    cat.add("x < 0.5", lambda x: x < 0.5)
    over_1 = cat.add("x >= 1", lambda x: x >= 1)
    over_1.add("1.2 > x >= 1.1", lambda x: 1.2 > x >= 1.1)
    over_1.add("x > 1.2", lambda x: x >= 1.2)
    return cat


def test_summary(category):
    result = category.categorise_list([0.01, 0.6, 1.001, 1.05, 1.1, 1.2, 3])
    summarised = result.summarise()

    assert summarised == {
        "categories": [
            {"category_name": "x < 0.5", "matches": 1},
            {
                "category_name": "x >= 1", "matches": 5,
                "categories": [
                    {"category_name": "1.2 > x >= 1.1", "matches": 1},
                    {"category_name": "x > 1.2", "matches": 2},
                    {"unmatched_items": 2}
                ]
            },
            {"unmatched_items": 1}
        ]
    }


def test_summary_with_bespoke_function(category):
    result = category.categorise_list([0.01, 0.6, 1.001, 1.05, 1.1, 1.2, 3])
    summarised = result.summarise(lambda x: x)

    assert summarised == {
        "categories": [
            {
                "category_name": "x < 0.5",
                "matches": [0.01]
            },
            {
                "category_name": "x >= 1",
                "matches": [1.001, 1.05, 1.1, 1.2, 3],
                "categories": [
                    {
                        "category_name": "1.2 > x >= 1.1",
                        "matches": [1.1]
                    },
                    {
                        "category_name": "x > 1.2",
                        "matches": [1.2, 3]
                    },
                    {
                        "unmatched_items": [1.001, 1.05]
                    }
                ]
            },
            {
                "unmatched_items": [0.6]
            }
        ]
    }
