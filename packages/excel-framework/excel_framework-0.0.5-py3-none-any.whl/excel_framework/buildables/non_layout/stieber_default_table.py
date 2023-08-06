from dataclasses import dataclass
from overrides import override
from typing import TypeVar, Generic, ClassVar
from ...buildables.layout.table import Table, TableColumn
from ...styling.color import Colors, Color
from ...styling.style import Style, TextStyle, Fill
from ...styling.border import BorderSide, Border, BorderStyle
from ...internals.buildable import Buildable

T = TypeVar("T")

@dataclass(frozen=True)
class StieberDefaultTable(Buildable, Generic[T]):
    columns: list[TableColumn[T]]
    data: list[T]

    column_name_text_style: ClassVar[TextStyle] = TextStyle(font_color=Colors.white)
    column_name_fill: ClassVar[Fill] = Fill(Color("FF000060"))
    border: ClassVar[Border] = Border(all=BorderSide(Colors.black, BorderStyle.THIN))

    @override
    def build(self) -> 'Buildable':
        return Table(
            columns=self.columns,
            data=self.data,
            column_name_style=Style(
                self.column_name_fill,
                self.column_name_text_style,
                child_border=self.border
            ),
            data_style=Style(child_border=self.border)
        )
