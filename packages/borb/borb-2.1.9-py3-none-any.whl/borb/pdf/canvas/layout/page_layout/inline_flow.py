#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement aggregates other LayoutElements
and lays them out on consecutive lines. If a line is full, it overflows
into the next line.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement


class InlineFlow(LayoutElement):
    """
    This implementation of LayoutElement aggregates other LayoutElements
    and lays them out on consecutive lines. If a line is full, it overflows
    into the next line.
    """

    def __init__(self):
        super(InlineFlow, self).__init__()
        self._content: typing.List[LayoutElement] = []

    def add(self, e: LayoutElement) -> "InlineFlow":
        """
        This function adds a LayoutElement to this InlineFlow
        :param e:   the LayoutElement to be added
        :return:    self
        """
        if isinstance(e, InlineFlow):
            for child_e in e._content:
                self.add(child_e)
        else:
            self._content.append(e)
        return self

    def extend(self, es: typing.List[LayoutElement]) -> "InlineFlow":
        """
        This function adds a typing.List of LayoutElement(s) to this InlineFlow
        :param es:   the LayoutElements to be added
        :return:    self
        """
        for e in es:
            self.add(e)
        return self

    @staticmethod
    def _get_min_content_box(e: LayoutElement) -> Rectangle:
        from borb.pdf.canvas.layout.table.table import TableCell

        c: TableCell = TableCell(e)
        c._calculate_min_and_max_layout_box()
        return Rectangle(Decimal(0), Decimal(0), c._min_width, c._max_height)

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:

        # all lines
        layout_lines: typing.List[typing.List[LayoutElement]] = [[]]
        layout_lines_height: typing.List[Decimal] = [Decimal(0)]

        # current line
        layout_line_width: Decimal = Decimal(0)

        # distribute content over lines
        for e in self._content:
            cbox: Rectangle = InlineFlow._get_min_content_box(e)
            w: Decimal = cbox.get_width()
            h: Decimal = cbox.get_height()
            if layout_line_width + w > available_space.get_width() or (
                e.__class__.__name__ == "LineBreakChunk"
            ):
                e._previous_layout_box = Rectangle(
                    available_space.get_x(), Decimal(0), w, h
                )
                layout_lines.append([e])
                layout_lines_height.append(h)
                layout_line_width = w
            else:
                e._previous_layout_box = Rectangle(
                    available_space.get_x() + layout_line_width, Decimal(0), w, h
                )
                layout_lines[-1].append(e)
                layout_line_width += w
                layout_lines_height[-1] = max(layout_lines_height[-1], h)

        # set height on all elements
        y: Decimal = available_space.get_y() + available_space.get_height()
        for i, line in enumerate(layout_lines):
            y -= layout_lines_height[i]
            for e in line:
                e._previous_layout_box = Rectangle(
                    e._previous_layout_box.get_x(),
                    y,
                    e._previous_layout_box.get_width(),
                    layout_lines_height[i],
                )

        # calculate total dimensions
        return Rectangle(
            available_space.get_x(),
            available_space.get_y()
            + available_space.get_height()
            - sum(layout_lines_height),
            available_space.get_width(),
            sum(layout_lines_height),
        )

    def _paint_content_box(self, page: "Page", content_box: Rectangle) -> None:
        for e in self._content:
            e.paint(page, e.get_previous_layout_box())
