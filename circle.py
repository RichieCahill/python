"""homework help"""

import logging
import math

import matplotlib.pyplot as plt

visited: set[complex] = set()
segmented: set[tuple[complex, complex]] = set()
colors = []


def fourth(F: complex, A: complex, L: complex, cross_ratio: complex) -> complex:  # noqa N803
    """This function calculates the fourth point of the triangle.

    Args:
        F (complex): the first point of the triangle
        A (complex): the second point of the triangle
        L (complex): the third point of the triangle
        cross_ratio (complex): the cross ratio

    Returns:
        _type_: _description_
    """
    logging.debug(f"Calculating the fourth point of the triangle with points {F}, {A}, {L}")

    if math.isclose(cross_ratio.real, 0):
        error = "CRoss ratio can't be zero lol"
        raise ValueError(error)
    cross_ratio = -cross_ratio
    return (cross_ratio * (F - A) * L - F * (L - A)) / (cross_ratio * (F - A) - L + A)


def line_seg(p: complex, q: complex, color: str) -> None:
    """This function draws a line segment between two points.

    Args:
        p (complex): the first point
        q (complex): the second point
        color (str): the color of the line segment
    """
    logging.debug(f"Drawing line segment between points {p} and {q} with color {color}")
    x = [p.real, q.real]
    y = [p.imag, q.imag]
    plt.plot(x, y, color=color)


def draw_triangle(F: complex, A: complex, L: complex, t: complex) -> None:  # noqa N803
    """This function draws the triangle.

    Args:
        F (complex): the first point of the triangle
        A (complex): the second point of the triangle
        L (complex): the third point of the triangle
        t (complex): the type of triangle
    """
    global segmented  # noqa W0603
    logging.debug(f"Drawing triangle with points {F}, {A}, {L}")

    if t == 1:
        fa_color = "r"
        al_color = "g"
    elif t == 2:
        fa_color = "g"
        al_color = "r"
    else:
        error = "T must be 1 or 2"
        raise ValueError(error)

    if (F, A) not in segmented and (A, F) not in segmented:
        line_seg(p=F, q=A, color=fa_color)
        segmented.add((F, A))

    if (A, L) not in segmented and (L, A) not in segmented:
        line_seg(p=A, q=L, color=al_color)
        segmented.add((A, L))

    if (L, F) not in segmented and (F, L) not in segmented:
        line_seg(p=L, q=F, color="b")
        segmented.add((L, F))


def plotem(x: complex, y: complex, z: complex, cross_ratio: complex, h: int) -> None:
    """This function plots the triangle and calls itself recursively to plot the next triangle.

    Args:
        x (complex): the first point of the triangle
        y (complex): this is the second point of the triangle
        z (complex): this is the third point of the triangle
        cross_ratio (complex): this is the cross ratio
        h (int): this is the height of the triangle
    """
    logging.debug(f"Plotting triangle with points {x}, {y}, {z}")

    global visited  # noqa W0603
    for w in [x, y, z]:
        if w not in visited:
            visited.add(w)
    if h % 2 == 0:
        t = 1
    elif h % 2 == 1:
        t = 2
    else:
        error = "h must be an even or odd number"
        raise ValueError(error)

    draw_triangle(x, y, z, t=t)
    if h < 1:
        h = h + 1
        b = fourth(x, y, z, cross_ratio=cross_ratio)
        if b not in visited:
            visited.add(b)
            plotem(z, x, b, cross_ratio, h)

        b = fourth(z, x, y, cross_ratio=cross_ratio)
        if b not in visited:
            visited.add(b)
            plotem(y, z, b, cross_ratio, h)

        b = fourth(y, z, x, cross_ratio=cross_ratio)
        if b not in visited:
            visited.add(b)
            plotem(x, y, b, cross_ratio, h)
        return


def main() -> None:
    """This is the main function."""
    logging.basicConfig(level=logging.DEBUG)

    fig, ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot
    # (or if you have an existing figure)

    circle1 = plt.Circle((0, 0), 1, fill=False)

    ax = plt.gca()
    ax.cla()  # clear things for fresh plot

    # change default range so that new circles will work
    ax.set_xlim((-1.05, 1.05))
    ax.set_ylim((-1.05, 1.05))
    ax.add_patch(circle1)

    F = 1j
    L = -math.sqrt(2) / 2 - math.sqrt(2) / 2 * 1j
    A = math.sqrt(2) / 2 - math.sqrt(2) / 2 * 1j

    plotem(x=F, y=A, z=L, cross_ratio=1, h=0)

    plt.show()


if __name__ == "__main__":
    main()
