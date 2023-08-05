from __future__ import annotations
from pybi.utils.data_gen import get_global_id, Jsonable
import pandas as pd
import pandas.api.types as pdTypeApis

from typing import Dict, List, Any, Callable, Optional, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from pybi.core.sql import Sql


class DataView(Jsonable):
    def __init__(self, name: str, sql: Sql) -> None:
        super().__init__()
        self._sql = sql
        self.name = name
        self.__excludeLinkages: List[str] = []

    def exclude_source(self, name: str):
        self.__excludeLinkages.append(name)
        return self

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["sqlInfo"] = self._sql
        data["excludeLinkages"] = self.__excludeLinkages
        return data


class DataSource(Jsonable):
    def __init__(self, name: str, data: pd.DataFrame) -> None:
        super().__init__()
        self._data = data
        self.name = name

    def __str__(self) -> str:
        return self.name


class DataSourceView:
    def __init__(self) -> None:
        pass

    def _to_sql(self):
        raise NotImplementedError()


class DataSourceField(DataSourceView):
    def __init__(self, source_name: str, name: str) -> None:
        super().__init__()
        self.source_name = source_name
        self.name = name

    def _to_sql(self):
        return f"select {self.name} from {self.source_name}"


class PyechartsPieItem(DataSourceView):
    def __init__(self, ds_table: DataSourceTable) -> None:
        super().__init__()
        self.ds_table = ds_table

    def __getitem__(self, key):
        from pyecharts import options as opts

        return opts.PieItem("", 0)

    def _to_sql(self):

        if len(self.ds_table.columns) < 2:
            raise Exception("pie data must have 2 fields")

        name = f"{self.ds_table.columns[0]} as name"
        value = f"{self.ds_table.columns[1]} as value"

        return f"select {name} , {value} from ({self.ds_table._to_sql()})"


class DataSourceTable(DataSourceView):
    def __init__(self, source_name: str, columns: List[str]) -> None:
        super().__init__()
        self.source_name = source_name
        self.columns = columns

    def __getitem__(self, field: Union[str, List[str]]):
        if isinstance(field, str):
            return DataSourceField(self.source_name, field)
        return DataSourceTable(self.source_name, field)

    def to_pyecharts_pie_items(self) -> Any:
        return PyechartsPieItem(self)

    def _to_sql(self):
        return f"select {','.join(self.columns)} from {self.source_name}"

    def __str__(self) -> str:
        return self.source_name
