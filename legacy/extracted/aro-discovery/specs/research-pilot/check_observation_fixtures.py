"""Exact finite reference cases for the draft observation contract."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product

Path = tuple[int, int]
VALUES = (-1, 0, 1)
INFEASIBLE = float("inf")


@dataclass(frozen=True)
class Fixture:
    first_controls: tuple[int, ...]
    paths: tuple[Path, ...]
    prefix_gain: int
    terminal_zero: bool = False

    def state(self, first: int, path: Path) -> int:
        return first + self.prefix_gain * path[0]

    def loss(self, first: int, second: int, path: Path) -> int | float:
        final_state = self.state(first, path) + second + path[1]
        if self.terminal_zero and final_state != 0:
            return INFEASIBLE
        return abs(final_state)


def policy_enumeration(case: Fixture, observation: str) -> int | float:
    """Enumerate all policies constant on each observable class."""
    values: list[int | float] = []
    for first in case.first_controls:
        if observation == "state":
            keys = [case.state(first, path) for path in case.paths]
        elif observation == "prefix":
            keys = [path[0] for path in case.paths]
        else:
            assert observation == "open"
            keys = [0] * len(case.paths)
        cells = sorted(set(keys))
        for actions in product(VALUES, repeat=len(cells)):
            policy = dict(zip(cells, actions, strict=True))
            values.append(
                max(
                    case.loss(first, policy[key], path)
                    for path, key in zip(case.paths, keys, strict=True)
                )
            )
    return min(values)


def measured_state_bellman(case: Fixture) -> int | float:
    """Solve the suffix minimax game separately at each reachable state."""
    first_values = []
    for first in case.first_controls:
        states_and_suffixes: dict[int, set[int]] = {}
        for prefix, suffix in case.paths:
            state = first + case.prefix_gain * prefix
            states_and_suffixes.setdefault(state, set()).add(suffix)
        worst_state = max(
            min(
                max(
                    INFEASIBLE
                    if case.terminal_zero and state + action + suffix != 0
                    else abs(state + action + suffix)
                    for suffix in suffixes
                )
                for action in VALUES
            )
            for state, suffixes in states_and_suffixes.items()
        )
        first_values.append(worst_state)
    return min(first_values)


def main() -> None:
    cases = {
        "strict_gain": (Fixture(VALUES, ((-1, 0), (1, 0)), 1), (1, 0, 0)),
        "correlated_hidden_disturbance": (
            Fixture((0,), ((-1, -1), (1, 1)), 0),
            (1, 1, 0),
        ),
        "independent_hidden_disturbance": (
            Fixture((0,), ((-1, -1), (-1, 1), (1, -1), (1, 1)), 0),
            (1, 1, 1),
        ),
        "terminal_feasibility": (
            Fixture(VALUES, ((-1, 0), (1, 0)), 1, terminal_zero=True),
            (INFEASIBLE, 0, 0),
        ),
    }
    for name, (case, expected) in cases.items():
        open_value = policy_enumeration(case, "open")
        state_value = policy_enumeration(case, "state")
        prefix_value = policy_enumeration(case, "prefix")
        bellman_value = measured_state_bellman(case)
        assert (open_value, state_value, prefix_value) == expected, name
        assert bellman_value == state_value, name
        print(f"{name}: open={open_value}, state={state_value}, prefix={prefix_value}, "
              f"state_bellman={bellman_value}")


if __name__ == "__main__":
    main()
