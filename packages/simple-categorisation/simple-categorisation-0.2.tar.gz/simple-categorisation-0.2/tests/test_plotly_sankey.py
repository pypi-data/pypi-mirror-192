from simple_categorisation import Categoriser


def test_plotly_sankey():
    cat = Categoriser()
    cat.add("x < 0.5", lambda x: x < 0.5)
    over_1 = cat.add("x >= 1", lambda x: x >= 1)
    over_1.add("1.2 > x >= 1.1", lambda x: 1.2 > x >= 1.1)
    over_1.add("x > 1.2", lambda x: x >= 1.2)
    result = cat.categorise_list([0.01, 0.6, 1.001, 1.05, 1.1, 1.2, 3])

    parameters = result.plotly_sankey(top_label="Top")

    assert parameters == {
        "node": {
            "label": ["Top", "Unmatched", "x < 0.5", "x >= 1",
                      "Unmatched", "1.2 > x >= 1.1", "x > 1.2"]
        },
        "link": {
            "source": [0, 0, 0, 3, 3, 3],
            "target": [1, 2, 3, 4, 5, 6],
            "value": [1, 1, 5, 2, 1, 2]
        }
    }

    # import plotly.graph_objects as go
    # fig = go.Figure(data=[go.Sankey(parameters)])
    # fig.update_layout(title_text="Example Sankey Diagram", font_size=20)
    # fig.show()
    #
    # assert False
