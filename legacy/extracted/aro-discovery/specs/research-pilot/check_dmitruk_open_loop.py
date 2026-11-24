"""Certify the open-loop benchmark in Dmitruk (2022), Example 1, PDF p. 12.

The two coefficient sets separate literal transcription from a reconstruction
using the continuous model (A2, PDF p. 15) and the sampling period
(A3, PDF pp. 8–9). The reconstructed decimal coefficients are explicit inputs.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as F

Vector = tuple[F, F]


def dynamics(cosine: F, sine: F, vector: Vector) -> Vector:
    x, y = vector
    return cosine * x + sine * y, -sine * x + cosine * y


def guaranteed_reward(cosine: F, sine: F, input_x: F) -> F:
    horizon = 120
    initial = (F(0), F(1))
    input_effect = (input_x, sine)
    columns = []
    for _ in range(horizon):
        columns.append(input_effect)
        input_effect = dynamics(cosine, sine, input_effect)
        initial = dynamics(cosine, sine, initial)

    # The paper uses the same column for control and disturbance, with
    # independent disturbances in [-1/2, 1/2]. The extrema use support sums.
    support_x = sum((abs(x) for x, _ in columns), F(0)) / 2
    support_y = sum((abs(y) for _, y in columns), F(0)) / 2
    lower_x, upper_x = 2 + support_x, 10 - support_x
    actions = [F(1) if y >= 0 else F(-1) for _, y in columns]
    nominal_x = initial[0] + sum(
        (x * action for (x, _), action in zip(columns, actions, strict=True)), F(0)
    )
    needed = lower_x - nominal_x
    assert needed > 0, "the example certificate expects an active lower bound"

    # Starting from the unconstrained optimum, add the required x gain
    # in order of increasing y loss per unit gain.
    options = sorted(
        (abs(y / x), index)
        for index, ((x, y), action) in enumerate(zip(columns, actions, strict=True))
        if x * action < 0
    )
    multiplier = F(0)
    for price, index in options:
        capacity = 2 * abs(columns[index][0])
        gain = min(needed, capacity)
        actions[index] *= 1 - 2 * gain / capacity
        needed -= gain
        if needed == 0:
            multiplier = price
            break

    assert needed == 0
    assert all(abs(action) <= 1 for action in actions)
    nominal_x = initial[0] + sum(
        (x * action for (x, _), action in zip(columns, actions, strict=True)), F(0)
    )
    assert lower_x <= nominal_x <= upper_x
    reward = initial[1] - support_y + sum(
        (y * action for (_, y), action in zip(columns, actions, strict=True)), F(0)
    )

    # Adding the nonnegative slack multiplier to the objective gives an
    # upper bound. Its box maximum matches the feasible worst-case reward.
    upper_bound = (
        initial[1] - support_y + multiplier * (initial[0] - lower_x)
        + sum((abs(y + multiplier * x) for x, y in columns), F(0))
    )
    assert upper_bound == reward
    return reward


def display(value: F, places: int) -> str:
    with localcontext() as ctx:
        ctx.prec = 36
        return format(Decimal(value.numerator) / Decimal(value.denominator), f".{places}f")


def main() -> None:
    printed = guaranteed_reward(F("0.9950"), F("0.0998"), F("0.0050"))
    # h=0.1, A_h uses cos(h) and sin(h), B_h = (1-cos(h), sin(h)).
    cosine = F("0.9950041652780258")
    sine = F("0.09983341664682815")
    reconstructed = guaranteed_reward(cosine, sine, 1 - cosine)
    assert display(printed, 6) == "1.495710"
    assert display(reconstructed, 6) == "1.501102"
    print("A4 Example 1 (maximize guaranteed terminal reward, open loop)")
    print("Printed coefficient value:", display(printed, 12))
    print("Reconstructed coefficient value:", display(reconstructed, 12))
    print("Both have exact feasible and upper-bound certificates for their input coefficients.")


if __name__ == "__main__":
    main()
