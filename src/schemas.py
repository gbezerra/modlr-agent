from typing import List, Optional, Annotated, Dict
from pydantic import BaseModel, HttpUrl, Field
from enum import Enum


class TableType(str, Enum):
    FACT = "fact"
    DIMENSION = "dimension"
    RAW = "raw"
    MART = "mart"


class Table(BaseModel):
    type: TableType = Field(..., description="Type of the table")
    name: str = Field(..., description="Name of the table")
    columns: List[str] = Field(..., description="List of column names in the table")

class DimensionalModel(BaseModel):
    fact_tables: List[Table] = Field(..., description="List of fact tables")
    dimension_tables: List[Table] = Field(..., description="List of dimension tables")
    relationships: Optional[Dict[str, List[str]]] = Field(None, description="Relationships between tables")