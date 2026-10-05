import csv
import io
import math
import os
import tempfile
from typing import Dict, List, Optional

import pandas as pd
from dbfread import DBF
from fastapi import UploadFile

from app.domain.parameter import Parameter
from app.infrastructure.repository import ParameterRepository


class ParameterService:
    REQUIRED_COLUMNS = {"contiss", "pernight", "local", "kilometer"}

    def __init__(self, repository: ParameterRepository):
        self.repository = repository

    @staticmethod
    def _normalize_header(header: object) -> str:
        return "".join(character for character in str(header).casefold() if character.isalnum())

    @classmethod
    def _column_mapping(cls, headers: List[object]) -> Dict[str, object]:
        aliases = {
            "contiss": "contiss",
            "pernight": "pernight",
            "local": "local",
            "kilometer": "kilometer",
            "kilometre": "kilometer",
        }
        mapping: Dict[str, object] = {}
        for header in headers:
            normalized = cls._normalize_header(header)
            canonical = aliases.get(normalized)
            if canonical:
                if canonical in mapping:
                    raise ValueError(f"CSV contains duplicate columns for {canonical}.")
                mapping[canonical] = header

        missing = cls.REQUIRED_COLUMNS - mapping.keys()
        if missing:
            raise ValueError(
                "CSV is missing required columns: " + ", ".join(sorted(missing))
            )
        return mapping

    @staticmethod
    def _row_value(row: dict, header: object):
        value = row.get(header)
        if value is None or pd.isna(value):
            return None
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @classmethod
    def _convert_rows(cls, data: List[dict]) -> List[Parameter]:
        if not data:
            raise ValueError("The uploaded file contains no parameter records.")

        columns = cls._column_mapping(list(data[0].keys()))
        parameters: List[Parameter] = []
        seen_contiss = set()

        for row_number, row in enumerate(data, start=2):
            if all(cls._row_value(row, header) is None for header in columns.values()):
                continue

            contiss_value = cls._row_value(row, columns["contiss"])
            if contiss_value is None:
                raise ValueError(f"Row {row_number}: Contiss is required.")
            contiss = str(contiss_value).strip()
            key = contiss.casefold()
            if key in seen_contiss:
                raise ValueError(f"Row {row_number}: duplicate Contiss value '{contiss}'.")
            seen_contiss.add(key)

            def parse_number(column: str) -> Optional[float]:
                value = cls._row_value(row, columns[column])
                if value is None:
                    return None
                try:
                    number = float(str(value).replace(",", "").strip())
                except (TypeError, ValueError) as error:
                    raise ValueError(
                        f"Row {row_number}: {column} must be a number."
                    ) from error
                if not math.isfinite(number):
                    raise ValueError(f"Row {row_number}: {column} must be a finite number.")
                return number

            parameters.append(
                Parameter(
                    id=None,
                    contiss=contiss,
                    pernight=parse_number("pernight"),
                    local=parse_number("local"),
                    kilometer=parse_number("kilometer"),
                    active=True,
                    created_at=None,
                )
            )

        if not parameters:
            raise ValueError("The uploaded file contains no parameter records.")
        return parameters

    async def process_upload(self, file: UploadFile) -> dict:
        filename = file.filename or ""
        extension = os.path.splitext(filename)[1].lower()
        if extension not in {".csv", ".xlsx", ".xls", ".dbf"}:
            raise ValueError("Unsupported file format. Upload a CSV, Excel, or DBF file.")

        content = await file.read()
        if not content:
            raise ValueError("The uploaded file is empty.")

        if extension == ".csv":
            try:
                text = content.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = content.decode("cp1252")
            reader = csv.DictReader(io.StringIO(text))
            if not reader.fieldnames:
                raise ValueError("CSV must include a header row.")
            data = list(reader)
            if any(None in row for row in data):
                raise ValueError("CSV contains a row with more values than its header.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            try:
                if extension == ".dbf":
                    table = DBF(tmp_path, encoding="cp1252", char_decode_errors="ignore")
                    data = [dict(record) for record in table]
                else:
                    data = pd.read_excel(tmp_path).to_dict("records")
            finally:
                os.remove(tmp_path)

        parameters = self._convert_rows(data)
        return self.repository.bulk_save(parameters)
