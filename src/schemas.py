from typing import List, Optional, Annotated, Dict
from pydantic import BaseModel, HttpUrl, Field
from enum import Enum


class ColumnType(str, Enum):
    STRING = "str"
    INTEGER = "int"
    FLOAT = "float"
    BOOLEAN = "bool"
    DATE = "date"
    DATETIME = "datetime"

class TableType(str, Enum):
    FACT = "fact"
    DIMENSION = "dimension"
    RAW = "raw"
    MART = "mart"

class Column(BaseModel):
    name: str = Field(..., description="Name of the column")
    type: ColumnType = Field(..., description="Data type of the column")
    description: Optional[str] = Field(None, description="Description of the column")
    is_primary_key: Optional[bool] = Field(False, description="Indicates if the column is a primary key")
    is_foreign_key: Optional[bool] = Field(False, description="Indicates if the column is a foreign key")
    references: Optional[str] = Field(None, description="References to another table if it's a foreign key")

class Table(BaseModel):
    name: str = Field(..., description="Name of the table")
    type: TableType = Field(..., description="Type of the table")
    description: Optional[str] = Field(None, description="Description of the table")
    columns: Dict[str, ColumnType] = Field(..., description="Mapping of column names to their data types")

class DimensionalModel(BaseModel):
    fact_tables: List[Table] = Field(..., description="List of fact tables")
    dimension_tables: List[Table] = Field(..., description="List of dimension tables")
    relationships: Optional[Dict[str, List[str]]] = Field(None, description="Relationships between tables")

class RawSchemaSpecs(BaseModel):
    tables: List[Table] = Field(..., description="List of raw input tables")

class Metric(BaseModel):
    name: str = Field(..., description="Name of the metric")
    description: Optional[str] = Field(None, description="Description of the metric")
    formula: Optional[str] = Field(None, description="SQL formula to calculate the metric")
    dimensions: Optional[List[str]] = Field(None, description="Dimensions applicable to the metric")

class MetricsSpecs(BaseModel):
    metrics: List[Metric] = Field(..., description="List of business metrics to be calculated")
