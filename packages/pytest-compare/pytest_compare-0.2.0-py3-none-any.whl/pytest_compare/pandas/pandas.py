from abc import ABC
from typing import Optional, List, Union

import pandas as pd

from pytest_compare.base import CompareBase


class CompareDataFrameBase(CompareBase, ABC):
    def __init__(self, expected: Union[pd.DataFrame, pd.Series]):
        """Initialize the class.

        Args:
            expected (Union[pd.DataFrame, pd.Series]): First dataframe.
        """
        if not isinstance(expected, pd.DataFrame) and not isinstance(
            expected, pd.Series
        ):
            raise TypeError(
                f"Dataframe must be a pandas DataFrame or Series, not {type(expected)}"
            )

        self._expected = expected


class CompareDataFrame(CompareDataFrameBase):
    """Compare two dataframes"""

    def __init__(self, expected: pd.DataFrame, columns: Optional[List[str]] = None):
        """Initialize the class.

        Args:
            expected (pd.DataFrame): Dataframe to compare.
            columns (Optional[List[str]], optional): Columns to compare. If None, all columns are compared. Defaults to None.
        """
        if columns and not isinstance(columns, list):
            raise TypeError(f"Columns must be a list, not {type(columns)}")

        super().__init__(expected)
        self._columns = columns

    def compare(self, actual) -> bool:
        """Compare two dataframes.

        Args:
            actual (pd.DataFrame): Dataframe to compare.

        Returns:
            bool: True if the first dictionary is a subset of the second
                dictionary, False otherwise.
        """
        if not isinstance(actual, pd.DataFrame):
            raise TypeError(f"Dataframe must be a pandas DataFrame, not {type(actual)}")

        if not self._columns:
            return actual.equals(self._expected)
        else:
            return actual[self._columns].equals(self._expected[self._columns])


class CompareDataFrameColumns(CompareDataFrameBase):
    """Compare two dataframe columns"""

    def compare(self, actual) -> bool:
        """Compare two dataframe columns.

        Args:
            actual (pd.DataFrame): Dataframe to compare.

        Returns:
            bool: True if columns are identical, False otherwise.
        """
        if not isinstance(actual, pd.DataFrame):
            raise TypeError(f"Dataframe must be a pandas DataFrame, not {type(actual)}")

        return actual.columns.equals(self._expected.columns)


class CompareSeries(CompareDataFrameBase):
    """Compare two series"""

    def __init__(self, expected: pd.Series):
        """Initialize the class.

        Args:
            expected (pd.Series): Series to compare.
        """
        super().__init__(expected)

    def compare(self, actual) -> bool:
        """Compare two series.

        Args:
            actual (pd.Series): Series to compare.

        Returns:
            bool: True if the first dictionary is a subset of the second
                dictionary, False otherwise.
        """
        if not isinstance(actual, pd.Series):
            raise TypeError(f"Series must be a pandas Series, not {type(actual)}")
        return actual.equals(self._expected)
