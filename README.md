# Power BI DAX — Northwind DW Curriculum (DataFabric Academy)

หลักสูตร DAX ที่สอนตามโครงเรื่อง 9EXPERT Version 22 แต่สร้าง **นิสัย semantic model ที่ถูกตั้งแต่ต้น** ด้วย Northwind star schema

| แหล่ง | บทบาท |
| --- | --- |
| [`data/Northwind_DW_DimFact.xlsx`](data/Northwind_DW_DimFact.xlsx) | ไฟล์เดียวที่ Get Data เข้าโมเดล |
| [`docs/lessons/`](docs/lessons/) | **แหล่งความจริง** — ทฤษฎี + ขั้นตอน + สูตร + Lab (โจทย์รวมเฉลย) |
| [`docs/best-practices/`](docs/best-practices/) | ดัชนี BP (แทรกทุกบท) |
| [`dax/measures.dax`](dax/measures.dax) | แคตตาล็อก measure |
| [`dax/calculation-groups.tmdl`](dax/calculation-groups.tmdl) | Time Intelligence calc group |
| สไลด์ 9EXPERT `.pptx` (ถ้ามี) | ภาพ UI / โครงเล่าเท่านั้น — **คอร์สนี้สอนจาก Markdown ไม่พึ่งสไลด์** |

## Setup เร็ว (ชั่วโมงแรก)

1. Get Data → Excel → import Tables: `DimDate`, `DimCustomer`, `DimEmployee`, `DimProduct`, `DimShipper`, `FactSales`
2. **ปิด Auto date/time** (Options → Data Load)
3. Mark `DimDate[Date]` as Date Table
4. Relationships ตามชีต `_Relationships` ใน Excel (OrderDate active; Required/Shipped inactive)
5. ซ่อน `*Key` / FK
6. สร้าง `[Sales Amount] = SUM ( FactSales[SalesAmount] )`
7. แนะนำเปิด **Discourage implicit measures** ตั้งแต่ต้น (จำเป็นก่อนบท Calculation Groups)

รายละเอียด: [docs/lessons/01-star-schema-and-get-data.md](docs/lessons/01-star-schema-and-get-data.md)

## ลำดับบทเรียน

1. [Star schema และ Get Data](docs/lessons/01-star-schema-and-get-data.md)
2. [DAX syntax และ Context](docs/lessons/02-dax-syntax-and-context.md)
3. [Calculated Column](docs/lessons/03-calculated-column.md)
4. [Measures](docs/lessons/04-measures.md)
5. [Aggregation และ Iterators](docs/lessons/05-aggregation-and-iterators.md)
6. [Logical / Text / Date](docs/lessons/06-logical-text-date.md)
7. [RELATED และ Relationships](docs/lessons/07-related-and-relationships.md)
8. [Date Table](docs/lessons/08-date-table.md)
9. [CALCULATE](docs/lessons/09-calculate.md)
10. [Time Intelligence (classic)](docs/lessons/10-time-intelligence.md)
11. [Calculation Groups](docs/lessons/11-calculation-groups.md) ← แทน Dynamic Measure แบบ SWITCH
12. [Field Parameters](docs/lessons/12-field-parameters.md)
13. [What-if](docs/lessons/13-what-if.md)
14. [Visual Calculations](docs/lessons/14-visual-calculations.md) (ภาคผนวก)
15. [VertiPaq checklist](docs/lessons/15-vertipaq-and-performance.md)

## ตรวจคุณภาพข้อมูล

```bash
pip install openpyxl pytest
pytest -q
```

หรือรัน `python scripts/extend_northwind_dw.py` เพื่อรีเฟรช metadata/QA ของ Excel

## สิ่งที่เลิกทำในห้อง

- Get Data จาก `9EXPERT-Dimension` + `9EXPERT-Orders` เป็นโมเดลหลัก
- ก๊อปสูตรสไลด์ที่อ้าง `Orders` / `CUSTOMERS` / `PRODUCTS`
- สร้าง DimDate ด้วย DAX เป็นตารางหลัก
- Dynamic Measure แบบ Enter Data + SWITCH เป็นคำตอบสุดท้าย

ดู [archive/README.md](archive/README.md)

## License / เครดิต

โครงเรื่องและลำดับหัวข้ออ้างอิงหลักสูตร 9Expert Training Power BI DAX Version 22  
โมเดลและเอกสารหลักสูตรนี้จัดทำสำหรับ DataFabric Academy
