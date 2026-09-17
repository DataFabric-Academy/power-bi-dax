# ดัชนีฟังก์ชัน DAX ตามบทเรียน

อ้างอิงอย่างเป็นทางการ: [DAX function reference](https://learn.microsoft.com/dax/dax-function-reference)  
สูตรตัวอย่างเต็ม: [`dax/measures.dax`](../../dax/measures.dax)

---

## บท 02 — Syntax & context

| ฟังก์ชัน / แนวคิด | ใช้ทำ |
| --- | --- |
| Row context | Calculated column, iterators |
| Filter context | Visual, slicer, `CALCULATE` |

---

## บท 03–06 — Columns

| ฟังก์ชัน | ตัวอย่างใน Northwind |
| --- | --- |
| `IF`, `&&`, `\|\|` | `Reorder`, `PromotionFlag` (บท 06) |
| `LEFT`, `INT` | `PromotionFlag` |
| `&` | `Employee Full` |
| `YEAR`, `DATEDIFF`, `FORMAT` | คอลัมน์อายุ / поколение (บท 03) |

---

## บท 04–05 — Aggregation & iterators

| ฟังก์ชัน | Measure ตัวอย่าง |
| --- | --- |
| `SUM`, `AVERAGE` | `[Sales Amount]`, `[Average Rating]` |
| `COUNTROWS`, `DISTINCTCOUNT`, `DISTINCTCOUNTNOBLANK` | `[Order Lines]`, `[Orders]`, `[#Country]` |
| `SUMX`, `AVERAGEX`, `MAXX` | `[Sales Amount (SUMX)]`, `[Avg Active List Price]` |
| `FILTER` | ภายใน iterator (ไม่ใช่ filter arg ของ `CALCULATE` โดยไม่จำเป็น) |
| `RELATED` | `[Line Cost (from StandardCost)]` |

---

## บท 07 — Relationships

| ฟังก์ชัน | ใช้เมื่อ |
| --- | --- |
| `RELATED` | Row context ฝั่ง many → one |
| `RELATEDTABLE` | Row context ฝั่ง one → many (สอน) |
| `USERELATIONSHIP` | Role-playing date (บท 09) |

---

## บท 08–10 — Date & time intelligence

| ฟังก์ชัน | ใช้ทำ |
| --- | --- |
| `CALENDAR`, `ADDCOLUMNS` | ภาคผนวกฝึก (แล้วลบ) |
| `TOTALYTD`, `DATESYTD` | `[Sales Amount YTD]` |
| `SAMEPERIODLASTYEAR` | `[Sales Amount PY]` |
| `DATESINPERIOD` | `[Sales Amount Rolling 60d]` |
| `DATESMTD`, `DATESQTD`, `DATESYTD` | Calculation group items (บท 11) |

---

## บท 09, 16 — CALCULATE & modifiers

| ฟังก์ชัน | ใช้ทำ |
| --- | --- |
| `CALCULATE` | เปลี่ยน filter context |
| `KEEPFILTERS` | Intersect filter slicer กับเงื่อนไขใหม่ |
| `REMOVEFILTERS` | Denominator / % share |
| `ALLSELECTED` | % ของ visual total |
| `ALL`, `ALLEXCEPT` | Context transition ใน column (สอน) |
| `DIVIDE` | ทุก measure ที่หาร |
| `VAR` / `RETURN` | อ่านง่าย, ไม่คำนวณซ้ำ |

---

## บท 11 — Calculation groups

| ฟังก์ชัน | ใช้ทำ |
| --- | --- |
| `SELECTEDMEASURE()` | Calc item ห่อ base measure |
| `ISNUMERIC ( SELECTEDMEASURE() )` | กัน measure ไม่ใช่ตัวเลข |

---

## บท 12–13 — Report-level

| แนวคิด | หมายเหตุ |
| --- | --- |
| Field parameters | ไม่ใช่ฟังก์ชัน DAX — สร้าง calculated table ใน Desktop |
| What-if parameter | Disconnected table + `SELECTEDVALUE` (บท 13) |

---

## บท 14 — Visual calculations

ฟังก์ชันระดับ visual (เช่น `RUNNINGSUM`) — ไม่อยู่ใน semantic model

---

## บท 15 — ไม่เพิ่มฟังก์ชันใหม่

Checklist + Performance Analyzer + DAX query view (`EVALUATE`)
