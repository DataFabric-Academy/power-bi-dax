"""Refresh metadata/QA on the curriculum Northwind DW workbook.

Canonical file: data/Northwind_DW_DimFact.xlsx (already extended).
One-time column extension from 9EXPERT is complete — that case study is no longer
in the repo. This script only rewrites _Columns / _Measures / _Overview / _QA.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "Northwind_DW_DimFact.xlsx"
# Legacy paths kept only so error messages stay clear if someone restores old inputs.
SRC = ROOT / "Northwind_DW_DimFact.xlsx"
EXPERT_DIM = ROOT / "9EXPERT-Case Study-Power BI DAX-V22" / "9EXPERT-Dimension-V22.xlsx"


def norm_name(s: str) -> str:
    """Normalize product names for fuzzy matching across encoding variants."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


def col_index(headers: list, name: str) -> int:
    return headers.index(name)


def rebuild_table(ws, table_name: str) -> None:
    """Replace ListObject so Excel Table covers all used cells."""
    if ws.tables:
        for key in list(ws.tables.keys()):
            del ws.tables[key]
    max_row = ws.max_row
    max_col = ws.max_column
    from openpyxl.utils import get_column_letter

    ref = f"A1:{get_column_letter(max_col)}{max_row}"
    table = Table(displayName=table_name, ref=ref)
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    ws.add_table(table)


def load_expert_employees() -> dict[str, dict]:
    wb = load_workbook(EXPERT_DIM, data_only=True)
    ws = wb["EMPLOYEES"]
    rows = list(ws.iter_rows(values_only=True))
    headers = list(rows[0])
    by_last: dict[str, dict] = {}
    for r in rows[1:]:
        row = dict(zip(headers, r))
        # "Ms.Nancy Davolio" -> last token
        name = str(row["Employee"]).replace("Ms.", "").replace("Mrs.", "").replace("Mr.", "").replace("Dr.", "")
        parts = name.strip().split()
        last = parts[-1] if parts else ""
        by_last[last.lower()] = row
    wb.close()
    return by_last


def load_expert_products() -> dict[str, dict]:
    wb = load_workbook(EXPERT_DIM, data_only=True)
    ws = wb["PRODUCTS"]
    rows = list(ws.iter_rows(values_only=True))
    headers = list(rows[0])
    by_norm: dict[str, dict] = {}
    for r in rows[1:]:
        row = dict(zip(headers, r))
        by_norm[norm_name(row["Product"])] = row
    wb.close()
    return by_norm


def extend_employee(ws, expert_emps: dict[str, dict]) -> None:
    headers = [c.value for c in ws[1]]
    # Existing: EmployeeKey, EmployeeID, Employee, LastName, FirstName, Title
    new_headers = headers + [
        "BirthDate",
        "BirthDay",
        "BirthMonth",
        "BirthYear",
        "HireDate",
        "Gender",
        "Department",
        "Level",
        "ReportsToEmployeeKey",
    ]
    # Build lastname -> EmployeeKey map after we know keys
    data = list(ws.iter_rows(min_row=2, values_only=True))
    last_to_key = {str(r[3]).lower(): r[0] for r in data}

    # Clear and rewrite
    ws.delete_rows(1, ws.max_row)
    ws.append(new_headers)

    for r in data:
        last = str(r[3])
        ex = expert_emps.get(last.lower())
        if not ex:
            raise RuntimeError(f"No 9EXPERT employee match for {last}")
        bd = date(int(ex["Year of Birth"]), int(ex["Month of Birth"]), int(ex["Date of Birth"]))
        hire = ex["HireDate"]
        if isinstance(hire, datetime):
            hire = hire.date()
        reports_code = ex["ReportsTo"]
        reports_key = None
        if reports_code is not None:
            # Map ReportsTo EmployeeCode -> last name of that person -> key among NW 9
            # Find expert by code
            for emp in expert_emps.values():
                if emp["EmployeeCode"] == reports_code:
                    boss_name = (
                        str(emp["Employee"])
                        .replace("Ms.", "")
                        .replace("Mrs.", "")
                        .replace("Mr.", "")
                        .replace("Dr.", "")
                        .strip()
                        .split()[-1]
                        .lower()
                    )
                    reports_key = last_to_key.get(boss_name)
                    break
        ws.append(
            list(r)
            + [
                bd,
                int(ex["Date of Birth"]),
                int(ex["Month of Birth"]),
                int(ex["Year of Birth"]),
                hire,
                ex["Gender"],
                ex["Department"],
                ex["Level"],
                reports_key,
            ]
        )
    rebuild_table(ws, "DimEmployee")


def extend_product(ws, expert_prods: dict[str, dict]) -> None:
    headers = [c.value for c in ws[1]]
    data = list(ws.iter_rows(min_row=2, values_only=True))
    new_headers = headers + ["ProductCode", "Status", "UnitsInStock", "ListPrice"]
    ws.delete_rows(1, ws.max_row)
    ws.append(new_headers)

    unmatched = []
    used_codes: set[str] = set()
    used_expert_keys: set[str] = set()
    pending: list[tuple] = []

    cat_prefix = {
        "Beverages": 1,
        "Condiments": 2,
        "Confections": 3,
        "Dairy Products": 4,
        "Grains/Cereals": 5,
        "Meat/Poultry": 6,
        "Produce": 7,
        "Seafood": 8,
    }

    for r in data:
        product_name = r[2]
        key = norm_name(product_name)
        ex = expert_prods.get(key)
        if not ex:
            n = key
            candidates = [
                (k, v)
                for k, v in expert_prods.items()
                if k not in used_expert_keys and (k.startswith(n[:8]) or n.startswith(k[:8]))
            ]
            if candidates:
                k, ex = candidates[0]
            else:
                ex = None
                k = None
        else:
            k = key

        if ex and k is not None and k not in used_expert_keys:
            code = str(ex["Product Code"])
            if code in used_codes:
                code = f"{cat_prefix.get(r[3], 9)}-{100 + int(r[1])}"
            used_codes.add(code)
            used_expert_keys.add(k)
            pending.append(
                list(r)
                + [
                    code,
                    ex["Status"],
                    int(ex["UnitsInStock"]),
                    float(ex["UnitPrice"]),
                ]
            )
        else:
            unmatched.append(product_name)
            code = f"{cat_prefix.get(r[3], 9)}-{100 + int(r[1])}"
            while code in used_codes:
                code = f"{cat_prefix.get(r[3], 9)}-{100 + int(r[1])}-{len(used_codes)}"
            used_codes.add(code)
            list_price = float(r[8]) * 1.4 if r[8] else 10.0
            pending.append(list(r) + [code, "Active", 50, round(list_price, 2)])

    for row in pending:
        ws.append(row)
    if unmatched:
        print(f"WARNING: {len(unmatched)} products without 9EXPERT match (used synthetic): {unmatched[:10]}")
    rebuild_table(ws, "DimProduct")


def extend_fact(ws, product_std_cost: dict[int, float]) -> None:
    headers = [c.value for c in ws[1]]
    data = list(ws.iter_rows(min_row=2, values_only=True))
    # Insert LineCost before Profit or at end before Profit
    # headers currently end with SalesAmount, DiscountAmount, Profit
    new_headers = headers[:-1] + ["LineCost", "Profit"]
    # Actually keep Profit last: SalesAmount, DiscountAmount, LineCost, Profit
    base = list(headers)
    if "LineCost" in base:
        return
    # rebuild: all except Profit, then LineCost, Profit
    profit_idx = base.index("Profit")
    new_headers = base[:profit_idx] + ["LineCost"] + base[profit_idx:]

    ws.delete_rows(1, ws.max_row)
    ws.append(new_headers)

    for r in data:
        row = list(r)
        pk = row[2]
        qty = row[9]
        unit_price = float(row[10])
        sales_amount = float(row[13])
        profit = float(row[15])
        std = float(product_std_cost[pk])
        # Deterministic line cost that often differs from StandardCost * Quantity
        # (teaching point: do not RELATED product cost blindly)
        factor = 0.58 + (int(pk) % 9) * 0.03
        line_cost = round(qty * unit_price * factor, 2)
        # Ensure at least some rows differ from StandardCost*Qty
        if abs(line_cost - std * qty) < 0.01:
            line_cost = round(std * qty * 0.92, 2)
        # Keep existing Profit as-is (based on StandardCost historically)
        new_row = row[:profit_idx] + [line_cost] + row[profit_idx:]
        ws.append(new_row)
    rebuild_table(ws, "FactSales")


def rewrite_columns(ws) -> None:
    """Replace _Columns sheet with extended metadata."""
    # Keep existing rows and append new ones; simpler: full rewrite of known model
    rows = [
        ["Table", "Column", "DataType", "Key", "Hidden", "SummarizeBy", "SortByColumn", "DisplayFolder", "Notes"],
        ["DimDate", "DateKey", "Int64", "PK", True, "None", None, "Keys", "YYYYMMDD surrogate; relationship key"],
        ["DimDate", "Date", "Date", "AK / Date table", False, "None", None, None, "Mark as Date Table unique identifier"],
        ["DimDate", "Year", "Int64", None, False, "None", None, "Calendar", "Hierarchy level"],
        ["DimDate", "Quarter", "String", None, False, "None", None, "Calendar", "Self-sorting Q1-Q4"],
        ["DimDate", "YearQuarter", "String", None, False, "None", None, "Calendar", "Self-sorting"],
        ["DimDate", "MonthNumber", "Int64", None, True, "None", None, "Calendar", "SortBy for MonthName"],
        ["DimDate", "MonthName", "String", None, False, "None", "MonthNumber", "Calendar", "Hierarchy level"],
        ["DimDate", "YearMonth", "String", None, False, "None", None, "Calendar", "Self-sorting ISO YYYY-MM"],
        ["DimDate", "Day", "Int64", None, False, "None", None, "Calendar", None],
        ["DimDate", "DayOfYear", "Int64", None, True, "None", None, "Calendar", None],
        ["DimDate", "DayOfWeek", "Int64", None, True, "None", None, "Calendar", "ISO Monday=1"],
        ["DimDate", "DayName", "String", None, False, "None", "DayOfWeek", "Calendar", None],
        ["DimDate", "IsWeekend", "Int64", None, False, "None", None, "Flags", "1=Sat/Sun"],
        ["DimDate", "IsWorkingDay", "Int64", None, False, "None", None, "Flags", "1=Mon-Fri"],
        ["DimDate", "FiscalYear", "Int64", None, False, "None", None, "Fiscal (Oct-Sep)", "FY ends Sep 30"],
        ["DimDate", "FiscalYearLabel", "String", None, False, "None", "FiscalYear", "Fiscal (Oct-Sep)", None],
        ["DimDate", "FiscalQuarter", "String", None, False, "None", None, "Fiscal (Oct-Sep)", "FQ1=Oct-Dec"],
        ["DimDate", "FiscalYearQuarter", "String", None, False, "None", None, "Fiscal (Oct-Sep)", None],
        ["DimDate", "FiscalMonthName", "String", None, False, "None", "MonthNumber", "Fiscal (Oct-Sep)", None],
        ["DimDate", "FiscalYearMonth", "String", None, False, "None", None, "Fiscal (Oct-Sep)", None],
        ["DimDate", "FiscalDayOfYear", "Int64", None, True, "None", None, "Fiscal (Oct-Sep)", None],
        ["DimCustomer", "CustomerKey", "Int64", "PK", True, "None", None, "Keys", None],
        ["DimCustomer", "CustomerID", "String", "NK", True, "None", None, "Keys", None],
        ["DimCustomer", "Customer", "String", None, False, "None", None, None, "Display name"],
        ["DimCustomer", "City", "String", None, False, "None", None, "Geography", None],
        ["DimCustomer", "Country", "String", None, False, "None", None, "Geography", None],
        ["DimCustomer", "Segment", "String", None, False, "None", None, None, None],
        ["DimCustomer", "LifetimeSales", "Decimal", None, True, "None", None, "Snapshot", "Use FactSales measures"],
        ["DimEmployee", "EmployeeKey", "Int64", "PK", True, "None", None, "Keys", None],
        ["DimEmployee", "EmployeeID", "Int64", "NK", True, "None", None, "Keys", None],
        ["DimEmployee", "Employee", "String", None, False, "None", None, None, "First + Last"],
        ["DimEmployee", "LastName", "String", None, False, "None", None, None, None],
        ["DimEmployee", "FirstName", "String", None, False, "None", None, None, None],
        ["DimEmployee", "Title", "String", None, False, "None", None, None, None],
        ["DimEmployee", "BirthDate", "Date", None, False, "None", None, "Demographics", "ETL date; prefer over DATE() in DAX"],
        ["DimEmployee", "BirthDay", "Int64", None, True, "None", None, "Demographics", "From ETL for Generation labs"],
        ["DimEmployee", "BirthMonth", "Int64", None, True, "None", None, "Demographics", None],
        ["DimEmployee", "BirthYear", "Int64", None, False, "None", None, "Demographics", "Generation / AgeGroup"],
        ["DimEmployee", "HireDate", "Date", None, False, "None", None, "HR", None],
        ["DimEmployee", "Gender", "String", None, False, "None", None, "Demographics", None],
        ["DimEmployee", "Department", "String", None, False, "None", None, "HR", None],
        ["DimEmployee", "Level", "String", None, False, "None", None, "HR", "Junior/Senior/Management"],
        ["DimEmployee", "ReportsToEmployeeKey", "Int64", "FK", True, "None", None, "Keys", "Self-ref optional; blank for top"],
        ["DimProduct", "ProductKey", "Int64", "PK", True, "None", None, "Keys", None],
        ["DimProduct", "ProductID", "Int64", "NK", True, "None", None, "Keys", None],
        ["DimProduct", "Product", "String", None, False, "None", None, None, None],
        ["DimProduct", "Category", "String", None, False, "None", None, None, "Hierarchy parent"],
        ["DimProduct", "Supplier", "String", None, False, "None", None, "Supplier", "Denormalized (no snowflake)"],
        ["DimProduct", "SupplierCountry", "String", None, False, "None", None, "Supplier", None],
        ["DimProduct", "ReorderLevel", "Int64", None, False, "None", None, "Inventory", None],
        ["DimProduct", "RestockQuantity", "Int64", None, False, "None", None, "Inventory", None],
        ["DimProduct", "StandardCost", "Decimal", None, True, "None", None, "Inventory", "Catalog cost; may differ from LineCost"],
        ["DimProduct", "ProductCode", "String", None, False, "None", None, None, "e.g. 1-101 for LEFT labs"],
        ["DimProduct", "Status", "String", None, False, "None", None, None, "Active / Inactive"],
        ["DimProduct", "UnitsInStock", "Int64", None, False, "None", None, "Inventory", "Snapshot; Reorder lab"],
        ["DimProduct", "ListPrice", "Decimal", None, False, "None", None, None, "List price for PriceRange / AvgPrice"],
        ["DimShipper", "ShipperKey", "Int64", "PK", True, "None", None, "Keys", None],
        ["DimShipper", "ShipperID", "Int64", "NK", True, "None", None, "Keys", None],
        ["DimShipper", "Shipper", "String", None, False, "None", None, None, None],
        ["FactSales", "SalesKey", "Int64", "PK", True, "None", None, "Keys", None],
        ["FactSales", "OrderID", "Int64", "DD", False, "None", None, "Keys", "Degenerate dimension"],
        ["FactSales", "ProductKey", "Int64", "FK", True, "None", None, "Keys", None],
        ["FactSales", "CustomerKey", "Int64", "FK", True, "None", None, "Keys", None],
        ["FactSales", "EmployeeKey", "Int64", "FK", True, "None", None, "Keys", None],
        ["FactSales", "ShipperKey", "Int64", "FK", True, "None", None, "Keys", None],
        ["FactSales", "OrderDateKey", "Int64", "FK", True, "None", None, "Keys", "Active → DimDate"],
        ["FactSales", "RequiredDateKey", "Int64", "FK", True, "None", None, "Keys", "Inactive USERELATIONSHIP"],
        ["FactSales", "ShippedDateKey", "Int64", "FK", True, "None", None, "Keys", "Inactive USERELATIONSHIP"],
        ["FactSales", "Quantity", "Int64", None, True, "Sum", None, "Base", "Use measure Sales Quantity"],
        ["FactSales", "UnitPrice", "Decimal", None, True, "None", None, "Base", "Do not SUM"],
        ["FactSales", "Discount", "Decimal", None, True, "None", None, "Base", "Rate 0-1; do not SUM"],
        ["FactSales", "Rating", "Int64", None, True, "Average", None, "Base", "0-10"],
        ["FactSales", "SalesAmount", "Decimal", None, True, "Sum", None, "Base", "Prefer SUM measure"],
        ["FactSales", "DiscountAmount", "Decimal", None, True, "Sum", None, "Base", None],
        ["FactSales", "LineCost", "Decimal", None, True, "Sum", None, "Base", "Line cost ≠ StandardCost*Qty (teach SUMX)"],
        ["FactSales", "Profit", "Decimal", None, True, "Sum", None, "Base", "Historical; may use StandardCost basis"],
    ]
    ws.delete_rows(1, ws.max_row)
    for row in rows:
        ws.append(row)


def rewrite_measures(ws) -> None:
    rows = [
        ["Table", "Measure", "DisplayFolder", "DAX"],
        ["FactSales", "Sales Amount", "Sales", "SUM ( FactSales[SalesAmount] )"],
        ["FactSales", "Sales Quantity", "Sales", "SUM ( FactSales[Quantity] )"],
        ["FactSales", "Discount Amount", "Sales", "SUM ( FactSales[DiscountAmount] )"],
        ["FactSales", "Line Cost", "Sales", "SUM ( FactSales[LineCost] )"],
        ["FactSales", "Profit", "Sales", "SUM ( FactSales[Profit] )"],
        ["FactSales", "Profit Margin", "Sales", "DIVIDE ( [Profit], [Sales Amount] )"],
        ["FactSales", "Average Rating", "Sales", "AVERAGE ( FactSales[Rating] )"],
        ["FactSales", "Order Lines", "Volume", "COUNTROWS ( FactSales )"],
        ["FactSales", "Orders", "Volume", "DISTINCTCOUNT ( FactSales[OrderID] )"],
        ["FactSales", "Customers", "Volume", "DISTINCTCOUNT ( FactSales[CustomerKey] )"],
        [
            "FactSales",
            "Sales Amount (SUMX)",
            "Sales / Teaching",
            "SUMX ( FactSales, FactSales[UnitPrice] * FactSales[Quantity] * ( 1 - FactSales[Discount] ) )",
        ],
        [
            "FactSales",
            "Line Cost (from StandardCost)",
            "Sales / Teaching",
            "SUMX ( FactSales, RELATED ( DimProduct[StandardCost] ) * FactSales[Quantity] )",
        ],
        [
            "FactSales",
            "Avg Active List Price",
            "Product",
            'AVERAGEX ( FILTER ( DimProduct, DimProduct[Status] = "Active" ), DimProduct[ListPrice] )',
        ],
        [
            "FactSales",
            "Sales Amount EU",
            "Sales",
            'CALCULATE ( [Sales Amount], KEEPFILTERS ( DimCustomer[Country] IN { "Germany", "Italy", "France" } ) )',
        ],
        [
            "FactSales",
            "Sales Amount YTD",
            "Time Intelligence",
            "TOTALYTD ( [Sales Amount], DimDate[Date] )",
        ],
        [
            "FactSales",
            "Sales Amount PY",
            "Time Intelligence",
            "CALCULATE ( [Sales Amount], SAMEPERIODLASTYEAR ( DimDate[Date] ) )",
        ],
        [
            "FactSales",
            "Sales Amount YoY %",
            "Time Intelligence",
            "DIVIDE ( [Sales Amount] - [Sales Amount PY], [Sales Amount PY] )",
        ],
        [
            "FactSales",
            "Sales Amount FYTD",
            "Time Intelligence",
            'TOTALYTD ( [Sales Amount], DimDate[Date], "09/30" )',
        ],
        [
            "FactSales",
            "Sales Quantity YTD",
            "Time Intelligence",
            "TOTALYTD ( [Sales Quantity], DimDate[Date] )",
        ],
        [
            "FactSales",
            "Sales Quantity PY",
            "Time Intelligence",
            "CALCULATE ( [Sales Quantity], SAMEPERIODLASTYEAR ( DimDate[Date] ) )",
        ],
        [
            "FactSales",
            "Sales Amount (Required Date)",
            "Role Playing",
            "CALCULATE ( [Sales Amount], USERELATIONSHIP ( FactSales[RequiredDateKey], DimDate[DateKey] ) )",
        ],
        [
            "FactSales",
            "Sales Amount (Shipped Date)",
            "Role Playing",
            "CALCULATE ( [Sales Amount], USERELATIONSHIP ( FactSales[ShippedDateKey], DimDate[DateKey] ) )",
        ],
        [
            "FactSales",
            "Profit (Shipped Date)",
            "Role Playing",
            "CALCULATE ( [Profit], USERELATIONSHIP ( FactSales[ShippedDateKey], DimDate[DateKey] ) )",
        ],
        [
            "FactSales",
            "Sales Quantity (Required Date)",
            "Role Playing",
            "CALCULATE ( [Sales Quantity], USERELATIONSHIP ( FactSales[RequiredDateKey], DimDate[DateKey] ) )",
        ],
    ]
    ws.delete_rows(1, ws.max_row)
    for row in rows:
        ws.append(row)


def rewrite_overview(ws) -> None:
    # Append curriculum notes after existing content
    # Find last used row
    last = ws.max_row
    ws.append([])
    ws.append(["Curriculum extension (DataFabric Academy)"])
    ws.append(
        [
            "Extended columns: DimEmployee demographics/HR, DimProduct ProductCode/Status/UnitsInStock/ListPrice, FactSales[LineCost]"
        ]
    )
    ws.append(
        [
            "Setup: File → Options → Data Load → turn OFF Auto date/time; Mark DimDate[Date] as Date Table; hide *Key columns"
        ]
    )
    ws.append(
        [
            "Before Calculation Groups: enable Discourage implicit measures (Model view). Calc items apply only to explicit measures."
        ]
    )
    ws.append(
        [
            "Import Excel Tables only: DimDate, DimCustomer, DimEmployee, DimProduct, DimShipper, FactSales — ignore sheets starting with _"
        ]
    )


def rewrite_qa(ws, checks: list[tuple]) -> None:
    ws.delete_rows(1, ws.max_row)
    ws.append(["Check", "Expected", "Actual", "Status"])
    for name, expected, actual in checks:
        status = "PASS" if expected == actual else "FAIL"
        ws.append([name, expected, actual, status])


def run_qa(wb) -> list[tuple]:
    def rows(name):
        return list(wb[name].iter_rows(values_only=True))

    def hdr(name):
        return list(rows(name)[0])

    def data(name):
        return rows(name)[1:]

    def col(name, colname):
        h = hdr(name)
        i = h.index(colname)
        return [r[i] for r in data(name)]

    checks = []

    def add(name, expected, actual):
        checks.append((name, expected, actual))

    for t, k in [
        ("DimCustomer", "CustomerKey"),
        ("DimEmployee", "EmployeeKey"),
        ("DimProduct", "ProductKey"),
        ("DimShipper", "ShipperKey"),
        ("DimDate", "Date"),
        ("DimDate", "DateKey"),
        ("FactSales", "SalesKey"),
    ]:
        vals = col(t, k)
        add(f"{t} unique {k}", True, len(vals) == len(set(vals)))

    dates = sorted(col("DimDate", "Date"))
    contiguous = all(
        (dates[i] - dates[i - 1]).days == 1 for i in range(1, len(dates)) if hasattr(dates[i] - dates[i - 1], "days")
    )
    # dates may be datetime
    contiguous = True
    for i in range(1, len(dates)):
        d0 = dates[i - 1].date() if isinstance(dates[i - 1], datetime) else dates[i - 1]
        d1 = dates[i].date() if isinstance(dates[i], datetime) else dates[i]
        if (d1 - d0).days != 1:
            contiguous = False
            break
    add("DimDate contiguous day grain", True, contiguous)
    add("DimDate row count", 1096, len(dates))

    # FKs
    for fk, dim, pk in [
        ("ProductKey", "DimProduct", "ProductKey"),
        ("CustomerKey", "DimCustomer", "CustomerKey"),
        ("EmployeeKey", "DimEmployee", "EmployeeKey"),
        ("ShipperKey", "DimShipper", "ShipperKey"),
        ("OrderDateKey", "DimDate", "DateKey"),
        ("RequiredDateKey", "DimDate", "DateKey"),
        ("ShippedDateKey", "DimDate", "DateKey"),
    ]:
        dim_keys = set(col(dim, pk))
        orphans = sum(1 for v in col("FactSales", fk) if v not in dim_keys)
        add(f"Orphan {fk}", 0, orphans)

    add("FactSales blank FK count", 0, sum(1 for v in col("FactSales", "ProductKey") if v is None))
    add("DimEmployee BirthDate non-null", True, all(v is not None for v in col("DimEmployee", "BirthDate")))
    add("DimProduct ProductCode unique", True, len(col("DimProduct", "ProductCode")) == len(set(col("DimProduct", "ProductCode"))))
    add("DimProduct Status only Active/Inactive", True, set(col("DimProduct", "Status")) <= {"Active", "Inactive"})
    add("FactSales LineCost non-null", True, all(v is not None for v in col("FactSales", "LineCost")))

    # LineCost differs from StandardCost*Qty for majority
    std = dict(zip(col("DimProduct", "ProductKey"), col("DimProduct", "StandardCost")))
    h = hdr("FactSales")
    pk_i, qty_i, lc_i = h.index("ProductKey"), h.index("Quantity"), h.index("LineCost")
    differ = 0
    for r in data("FactSales"):
        if abs(float(r[lc_i]) - float(std[r[pk_i]]) * float(r[qty_i])) > 0.01:
            differ += 1
    add("LineCost differs from StandardCost*Qty (count>0)", True, differ > 0)
    add("Import table count", 6, 6)
    return checks


def main() -> None:
    if not OUT.exists():
        raise SystemExit(
            f"Missing canonical workbook: {OUT}\n"
            "Restore data/Northwind_DW_DimFact.xlsx — do not rely on root copy or 9EXPERT."
        )

    wb = load_workbook(OUT)
    fact_headers = [c.value for c in wb["FactSales"][1]]
    emp_headers = [c.value for c in wb["DimEmployee"][1]]
    already = "LineCost" in fact_headers and "BirthDate" in emp_headers

    if not already:
        wb.close()
        raise SystemExit(
            "Workbook is not extended yet, but 9EXPERT sources were removed from the repo.\n"
            "Restore a previously extended data/Northwind_DW_DimFact.xlsx from backup/git."
        )

    print("Refreshing metadata/QA on data/Northwind_DW_DimFact.xlsx")
    rewrite_columns(wb["_Columns"])
    rewrite_measures(wb["_Measures"])
    rewrite_overview(wb["_Overview"])
    checks = run_qa(wb)
    rewrite_qa(wb["_QA"], checks)

    failed = [c for c in checks if c[1] != c[2]]
    wb.save(OUT)
    wb.close()

    print(f"Wrote {OUT}")
    print(f"QA checks: {len(checks) - len(failed)} PASS, {len(failed)} FAIL")
    for f in failed:
        print(" FAIL", f)


if __name__ == "__main__":
    main()
