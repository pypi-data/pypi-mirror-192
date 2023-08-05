from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, NamedTuple

from .geometry import Region, Size, Spacing

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from .widget import Widget

ArrangeResult: TypeAlias = "tuple[list[WidgetPlacement], set[Widget]]"
DockArrangeResult: TypeAlias = "tuple[list[WidgetPlacement], set[Widget], Spacing]"


class WidgetPlacement(NamedTuple):
    """The position, size, and relative order of a widget within its parent."""

    region: Region
    margin: Spacing
    widget: Widget
    order: int = 0
    fixed: bool = False


class Layout(ABC):
    """Responsible for arranging Widgets in a view and rendering them."""

    name: ClassVar[str] = ""

    def __repr__(self) -> str:
        return f"<{self.name}>"

    @abstractmethod
    def arrange(
        self, parent: Widget, children: list[Widget], size: Size
    ) -> ArrangeResult:
        """Generate a layout map that defines where on the screen the widgets will be drawn.

        Args:
            parent: Parent widget.
            size: Size of container.

        Returns:
            An iterable of widget location
        """

    def get_content_width(self, widget: Widget, container: Size, viewport: Size) -> int:
        """Get the optimal content width by arranging children.

        Args:
            widget: The container widget.
            container: The container size.
            viewport: The viewport size.

        Returns:
            Width of the content.
        """
        if not widget._nodes:
            width = 0
        else:
            # Use a size of 0, 0 to ignore relative sizes, since those are flexible anyway
            placements, _, _ = widget._arrange(Size(0, 0))
            width = max(
                [
                    placement.region.right + placement.margin.right
                    for placement in placements
                ],
                default=0,
            )
        return width

    def get_content_height(
        self, widget: Widget, container: Size, viewport: Size, width: int
    ) -> int:
        """Get the content height.

        Args:
            widget: The container widget.
            container: The container size.
            viewport: The viewport.
            width: The content width.

        Returns:
            Content height (in lines).
        """
        if not widget._nodes:
            height = 0
        else:
            # Use a height of zero to ignore relative heights
            placements, _, _ = widget._arrange(Size(width, 0))
            height = max(
                [
                    placement.region.bottom + placement.margin.bottom
                    for placement in placements
                ],
                default=0,
            )

        return height
