from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pymysql
import pandas as pd

class SQLQueryToolInput(BaseModel):
    """Input schema for SQLQueryTool."""
    query: str = Field(..., description="The SQL query to execute.")

class SQLQueryTool(BaseTool):
    name: str = "SQL Query Tool"
    description: str = (
        "A tool that executes SQL queries against a MySQL database and returns the results in a readable format."
    )
    args_schema: Type[BaseModel] = SQLQueryToolInput

    def _run(self, query: str) -> str:
        try:
            from main import mysql_connection
            with mysql_connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                
                # Convert results to pandas DataFrame for better formatting
                df = pd.DataFrame(results)
                if df.empty:
                    return "Query executed successfully but returned no results."
                
                # Convert DataFrame to string representation
                return df.to_string()
                
        except pymysql.Error as e:
            return f"Error executing query: {str(e)}"
