"""Cursor template."""

from __future__ import annotations

import curses
import logging
import sys


def configure_logger(level: str = "INFO") -> None:
    """Configure the logger.

    Args:
        level (str, optional): The logging level. Defaults to "INFO".
    """
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


class Cursor:
    """Cursor class."""

    def __init__(self) -> None:
        """Init."""
        self.x_position = 0
        self.y_position = 0
        self.height = 0
        self.width = 0

    def set_height(self, height: int) -> None:
        """Set height.

        Args:
            height (int): The height of the curses window.
        """
        self.height = height

    def set_width(self, width: int) -> None:
        """Set width.

        Args:
            width (int): The width of the curses window.
        """
        self.width = width

    def x_bounce_check(self, cursor: int) -> int:
        """X bounce check.

        Args:
            cursor (int): The current cursor position.

        Returns:
            int: The bounced cursor position.
        """
        cursor = max(0, cursor)
        return min(self.width - 1, cursor)

    def y_bounce_check(self, cursor: int) -> int:
        """Y bounce check.

        Args:
            cursor (int): The current cursor position.

        Returns:
            int: The bounced cursor position.
        """
        cursor = max(0, cursor)
        return min(self.height - 1, cursor)

    def set_x(self, x: int) -> None:
        """Set x.

        Args:
            x (int): The new x position.
        """
        self.x_position = self.x_bounce_check(x)

    def set_y(self, y: int) -> None:
        """Set y.

        Args:
            y (int): The new y position.
        """
        self.y_position = self.y_bounce_check(y)

    def get_x(self) -> int:
        """Get x.

        Returns:
            int: The current x position.
        """
        return self.x_position

    def get_y(self) -> int:
        """Get y.

        Returns:
            int: The current y position.
        """
        return self.y_position

    def move_up(self) -> None:
        """Move up."""
        self.set_y(self.y_position - 1)

    def move_down(self) -> None:
        """Move down."""
        self.set_y(self.y_position + 1)

    def move_left(self) -> None:
        """Move left."""
        self.set_x(self.x_position - 1)

    def move_right(self) -> None:
        """Move right."""
        self.set_x(self.x_position + 1)

    def move_home(self) -> None:
        """Move home."""
        self.set_x(0)

    def move_end(self) -> None:
        """Move end."""
        self.set_x(self.width - 1)

    def page_up(self) -> None:
        """Page up."""
        self.set_y(0)

    def page_down(self) -> None:
        """Page down."""
        self.set_y(self.height - 1)

    def navigation(self, key: int) -> None:
        """Navigation.

        Args:
            key (int): The last key pressed.
        """
        action = {
            curses.KEY_DOWN: self.move_down,
            curses.KEY_UP: self.move_up,
            curses.KEY_RIGHT: self.move_right,
            curses.KEY_LEFT: self.move_left,
            curses.KEY_PPAGE: self.page_up,
            curses.KEY_NPAGE: self.page_down,
            curses.KEY_HOME: self.move_home,
            curses.KEY_END: self.move_end,
        }

        action.get(key, lambda: None)()


def debug_menu(std_screen: curses.window, key: int) -> None:
    """Debug menu.

    Args:
        std_screen (curses.window): The curses window.
        key (int): The last key pressed.
    """
    height, width = std_screen.getmaxyx()
    width_height = f"Width: {width}, Height: {height}"
    std_screen.addstr(height - 4, 0, width_height, curses.color_pair(5))

    key_pressed = f"Last key pressed: {key}"[: width - 1]
    if key == 0:
        key_pressed = "No key press detected..."[: width - 1]
    std_screen.addstr(height - 3, 0, key_pressed)

    for i in range(8):
        std_screen.addstr(height - 2, i * 3, f"{i}██", curses.color_pair(i))


def status_bar(std_screen: curses.window, cursor: Cursor, width: int, height: int) -> None:
    """Status bar.

    Args:
        std_screen (curses.window): The curses window.
        cursor (Cursor): The cursor object.
        width (int): The width of the curses window.
        height (int): The height of the curses window.
    """
    std_screen.attron(curses.A_REVERSE)
    std_screen.attron(curses.color_pair(3))

    status_bar = f"Press 'q' to exit | STATUS BAR | Pos: {cursor.get_x()}, {cursor.get_y()}"
    std_screen.addstr(height - 1, 0, status_bar)
    std_screen.addstr(height - 1, len(status_bar), " " * (width - len(status_bar) - 1))

    std_screen.attroff(curses.color_pair(3))
    std_screen.attroff(curses.A_REVERSE)


def set_color() -> None:
    """Set color."""
    curses.start_color()
    curses.use_default_colors()
    for i in range(curses.COLORS):
        curses.init_pair(i + 1, i, -1)


def draw_menu(std_screen: curses.window) -> None:
    """Draw menu.

    Args:
        std_screen (curses.window): The curses window.
    """
    # Clear and refresh the screen for a blank canvas
    std_screen.clear()
    std_screen.refresh()

    set_color()

    key = 0
    cursor = Cursor()

    # Loop where k is the last character pressed
    while key != ord("q"):
        std_screen.clear()
        height, width = std_screen.getmaxyx()

        cursor.set_height(height)
        cursor.set_width(width)

        cursor.navigation(key)

        status_bar(std_screen, cursor, width, height)

        debug_menu(std_screen, key)

        std_screen.move(cursor.get_y(), cursor.get_x())

        std_screen.refresh()

        key = std_screen.getch()


def main() -> None:
    """Main function."""
    curses.wrapper(draw_menu)


if __name__ == "__main__":
    main()
