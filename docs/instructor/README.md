# คู่มือผู้สอน — Power BI DAX (Northwind DW)

เอกสารนี้สำหรับ **วิทยากร / maintainer** ไม่บังคับนักเรียน

---

## ก่อนเปิดคอร์ส

1. Clone repo และติดตั้ง Python deps: `pip install -r requirements.txt`
2. รัน `pytest -q` — ต้องผ่านทั้ง QA Excel และ sync `dax/measures.dax` ↔ `_Measures`
3. เตรียม `data/Northwind_DW_DimFact.xlsx` ให้นักเรียน (หรือชี้ path ใน repo)
4. (แนะนำ) สร้าง `.pbix` solution ของตัวเองโดยทำ Lab 01–11 — ใช้ demo ในห้อง
5. Cursor + [Power BI Modeling MCP](../../.cursor/mcp.json): สำรอง `.pbix` ก่อนให้ agent แก้โมเดล

---

## สิ่งที่ **ไม่** สอน (ตั้งใจ)

| หัวข้อ | เหตุผล | อ้าง |
| --- | --- | --- |
| Get Data จาก 9EXPERT Orders/Dimension | โมเดลไม่เหมาะ production | [`archive/README.md`](../../archive/README.md) |
| Dynamic measure แบบ Enter Data + SWITCH | แทนด้วย calc group / field parameter | บท 11–12 |
| Snowflake SUPPLIERS แยก | Northwind denormalize แล้ว | บท 07 |
| Copy สูตรจากสไลด์ที่อ้าง `Orders` | สูตรไม่ตรงโมเดล | README หลัก |

---

## จุดที่นักเรียนมักสะดุด

| บท | อาการ | คำแนะนำ |
| --- | --- | --- |
| 01 | Slicer ปีไม่กรอง | ตรวจ active relationship `OrderDateKey`; ใช้ measure ไม่ใช่ column |
| 02 | สับสน `[SalesAmount]` vs `FactSales[SalesAmount]` | ย้ำ qualify column / ไม่ qualify measure |
| 05 | Line Cost สอง measure เท่ากัน | ข้อมูลออกแบบให้ **ไม่เท่า** — รัน pytest / อ่าน lab |
| 09 | EU measure เป็นศูนย์ | ตรวจชื่อประเทศใน DimCustomer ตรง `{ Germany, Italy, France }` |
| 10–11 | Calc group ไม่ทำงาน | เปิด **Discourage implicit measures**; ใช้ explicit measure |
| 11 | YOY% format ผิด | ใช้ dynamic format string ใน TMDL ตาม [`dax/calculation-groups.tmdl`](../../dax/calculation-groups.tmdl) |
| 16 | % of visual ได้ 100% ทุกแถว | ใช้ `ALLSELECTED` บนคอลัมน์แกน ไม่ใช่ `ALL` ทั้งตาราง |

---

## โครงสร้างชั่วโมง (ตัวอย่าง 3 วัน)

| วัน | บท | หมายเหตุ |
| --- | --- | --- |
| 1 AM | 01–03 | เน้นโมเดล + column |
| 1 PM | 04–06 | measures + iterators แนวสอน |
| 2 AM | 07–09 | relationships + CALCULATE |
| 2 PM | 16 + 10 | filter modifiers แล้ว classic TI |
| 3 AM | 11–12 | calc group + field params |
| 3 PM | 13, 15 (+14 optional) | what-if, checklist, Q&A |

---

## Demo visuals ที่แนะนำ

- **บท 01:** Card `[Sales Amount]` + Slicer `DimDate[Year]`
- **บท 05:** สอง Card `[Line Cost]` vs `[Line Cost (from StandardCost)]`
- **บท 09:** Matrix เดือน — Order vs Shipped measures
- **บท 11:** Matrix + calc group slicer `Time Calculation` × หลาย base measures
- **บท 12:** Bar chart + field parameter slicers

---

## การบำรุง repo

| งาน | คำสั่ง / ไฟล์ |
| --- | --- |
| แก้เนื้อหาบท (batch) | แก้ `scripts/write_lessons.py` → `python scripts/write_lessons.py` |
| แก้ measure catalog | แก้ `dax/measures.dax` + `scripts/extend_northwind_dw.py` (`rewrite_measures`) → `python scripts/extend_northwind_dw.py` |
| ตรวจคุณภาพ | `pytest -q` |
| ดัชนีหลักสูตร | [`docs/CURRICULUM.md`](../CURRICULUM.md) |

เมื่อเพิ่ม measure ใหม่: **ต้อง** sync ทั้ง `measures.dax` และ `_Measures` มิฉะนั้น `test_measures_catalog` จะ fail

---

## การประเมินผล (rubrics สั้น)

- **โมเดล (40%):** star, hidden keys, date table, relationships ถูก
- **DAX (40%):** lab ผ่านเกณฑ์ท้ายบท; สูตร qualify ถูก; ใช้ `DIVIDE` / Boolean CALCULATE
- **Dynamics (20%):** calc group TI ใช้ได้; อธิบายความต่าง field parameter vs calc group

Optional: ให้นักเรียนส่ง `.pbix` + screenshot Matrix calc group
