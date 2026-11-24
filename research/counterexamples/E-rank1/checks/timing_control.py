"""One-prefix rank-one control: a policy must survive both hidden suffixes."""

import json
from fractions import Fraction as F


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    # Fixed T=2,r=1,n=d=1,m=2. First block is zero, E0=A0=A1=0.
    # B1=(1,-1), E1=1, H=-1,h=0,c=1. Both paths share w0=0.
    suffixes = [F(-1), F(1)]
    common = [F(3, 2), F(1, 2)]
    terminals = [common[0] - common[1] + suffix for suffix in suffixes]
    require(terminals == [0, 2], "unexpected common-action terminal states")
    require(all(0 <= value <= 2 for value in terminals), "q=2 witness failed")

    # At q=1, hard row from suffix -1 plus cost row from suffix +1.
    rows = [([F(-1), F(1)], F(-1)), ([F(1), F(-1)], F(0))]
    left = [sum((row[0][i] for row in rows), F(0)) for i in range(2)]
    right = sum((row[1] for row in rows), F(0))
    require(left == [0, 0] and right == -1, "q=1 contradiction failed")

    illegal = [[F(1), F(0)], [F(0), F(1)]]
    illegal_terminals = [
        action[0] - action[1] + suffix for action, suffix in zip(illegal, suffixes, strict=True)
    ]
    require(illegal_terminals == [0, 0], "illegal oracle control not discriminating")
    prefix_keys = [(F(0),), (F(0),)]
    require(
        prefix_keys[0] == prefix_keys[1] and illegal[0] != illegal[1],
        "illegal policy not rejected for same-prefix action mismatch",
    )
    print(
        json.dumps(
            {
                "check_id": "E-hidden-suffix-control",
                "rank_L": 1,
                "complete_paths": [["0", "-1"], ["0", "1"]],
                "prefix_count": 1,
                "measured_states": ["0", "0"],
                "q2_common_witness": list(map(str, common)),
                "q2_terminal_states": list(map(str, terminals)),
                "q1_certificate": {
                    "weights": ["1", "1"],
                    "weighted_left": list(map(str, left)),
                    "weighted_right": str(right),
                },
                "q0_oracle_only_terminal_states": list(map(str, illegal_terminals)),
                "same_prefix_different_actions_rejected": True,
                "scope": "one fixed correlated two-path instance, not a general theorem",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
