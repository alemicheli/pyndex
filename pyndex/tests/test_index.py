import pytest
from pyndex.core.index import Index
from unittest.mock import Mock
import wrds


def test_index_integer_years():
    with pytest.raises(TypeError):
        year = "A"
        mock_wrds = Mock(spec=wrds.sql.Connection)
        index = Index.from_wrds(mock_wrds, "A", "3000")


def test_calendar_integer_years():
    with pytest.raises(TypeError):
        year = "A"
        index = Index.get_calendar("A")


def test_index_wrds_connection():
    with pytest.raises(TypeError):
        index = Index.from_wrds("WRDS_Connection", 2000, "3000")


def test_index_unsupported_index():
    with pytest.raises(ValueError):
        mock_wrds = Mock(spec=wrds.sql.Connection)
        index = Index.from_wrds(mock_wrds, 2000, "5000")
