LEXICON_TABLE = "lexicon_terms"

COLUMN_CHECKS = {
    "null_check": "SUM(CASE WHEN {column} IS NULL THEN 1 ELSE 0 END)",
    "distinct_check": "COUNT(DISTINCT {column})",
    "min": "MIN({column})",
    "max": "MAX({column})",
}

SQL_CHECK_TEMPLATE = " SELECT '{check}' AS check_name, {check_statement} AS check_result FROM {table} {partition_clause} "


class ColumnQualityCheck:
    def __init__(self, table: str, partition_clause: str | None = None):
        self.table = table
        self.partition_clause = partition_clause
        self.column_checks = COLUMN_CHECKS
        self.sql_check_template = SQL_CHECK_TEMPLATE

    def _generate_sql_query(self, column, checks):
        def _generate_partition_clause(check):
            if self.partition_clause and "partition_clause" not in checks[check]:
                return f"WHERE {self.partition_clause}"
            if not self.partition_clause and "partition_clause" in checks[check]:
                return f"WHERE {checks[check]['partition_clause']}"
            if self.partition_clause and "partition_clause" in checks[check]:
                return f"WHERE {self.partition_clause} AND {checks[check]['partition_clause']}"
            return ""

        checks_sql = "UNION ALL".join(
            self.sql_check_template.format(
                check_statement=self.column_checks[check].format(column=column),
                check=check,
                table=self.table,
                column=column,
                partition_clause=_generate_partition_clause(check),
            )
            for check in checks
        )
        return checks_sql

    def run(self, connection, column: str, checks: dict) -> dict:
        rows = connection.execute(self._generate_sql_query(column, checks)).fetchall()
        return {name: value for name, value in rows}
