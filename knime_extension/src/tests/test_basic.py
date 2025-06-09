import pytest
import pandas as pd
from util.network_algorithms import create_network
from util.position_algorithms import create_positions


# -------------------------------------------------
# Fixture 1: Simple edge‐list DataFrame
# -------------------------------------------------
@pytest.fixture
def simple_edge_table():
    """
    Returns a pandas DataFrame representing a network:
      A → B (1.0)
      B → C (2.0)
      A → C (3.0)
    """
    df = pd.DataFrame(
        {
            "source": ["A", "B", "A"],
            "target": ["B", "C", "C"],
            "weight": [1.0, 2.0, 3.0],
        }
    )
    assert df.shape == (3, 3)
    return df


@pytest.fixture
def simple_edge_table_string():
    """
    Returns a pandas DataFrame representing a two-mode network:
      A → B friend
      B → C friend
      A → C colleague
    """
    df = pd.DataFrame(
        {
            "source": ["A", "B", "A"],
            "target": ["B", "C", "C"],
            "weight": ["friend", "friend", "colleague"],
        }
    )
    assert df.shape == (3, 3)
    return df


# -------------------------------------------------
# Test: create_positions for a Single Network
# -------------------------------------------------
def test_factory_only_network_position(simple_edge_table):
    settings = {
        "source_label": "source",
        "target_label": "target",
        "weight_label": "weight",
        "two_mode": False,
        "symmetric": False,
        "irreflexive": False,
    }

    net = create_network(simple_edge_table, settings)
    pos_port_obj = create_positions([net], [], "BINARY")
    positions, dims = pos_port_obj.get_uniform_positions()
    print(positions)
    assert dims == {"B_1", "C_1"}
    assert pytest.approx(positions["A"]["B_1"]) == 1.0
    assert pytest.approx(positions["A"]["C_1"]) == 3.0
    assert pytest.approx(positions["B"]["C_1"]) == 2.0
    assert "C" not in positions or positions["C"] == {}
    assert False


def test_factory_only_network_position_string(simple_edge_table_string):
    settings = {
        "source_label": "source",
        "target_label": "target",
        "weight_label": "weight",
        "two_mode": False,
        "symmetric": True,
        "irreflexive": False,
    }

    net = create_network(simple_edge_table_string, settings)
    pos_port_obj = create_positions([net], [], "ONE_HOT")
    temp = pos_port_obj.get_positions()
    print(temp)
    positions, dims = pos_port_obj.get_uniform_positions()
    print(positions)
    assert dims == {"A_friend_1", "A_colleague_2", "B_friend_1", "C_friend_1", "C_colleague_2"}
    assert positions == {
        "A": {"B_friend_1": 1.0, "C_colleague_2": 1.0},
        "B": {"A_friend_1": 1.0, "C_friend_1": 1.0},
        "C": {"B_friend_1": 1.0, "A_colleague_2": 1.0},
    }