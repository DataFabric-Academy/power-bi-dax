# หลักสูตร DAX และ Semantic Model — Northwind DW

เอกสารนี้สรุป **เป้าหมายการเรียนรู้**, **เส้นทางแนะนำ**, และการ **map กับ Microsoft Learn** สำหรับ repo นี้  
บทเรียนทุกบทได้รับการออกแบบโดยใช้แนวคิด **Mental Model (ภาพจำในใจที่เข้าใจง่าย)** เพื่อให้ผู้เรียนระดับเทียบเท่ามัธยมปลายสามารถเข้าใจที่มาและกลไกการคิดของ DAX ได้อย่างลึกซึ้ง โดยไม่ลดทอน Keyphrase และมาตรฐานการปฏิบัติงานระดับองค์กรสำหรับ Data Analyst, Business Analyst, และ BI Developer  
แหล่งความจริงของสูตรและ Lab ยังคือ [`docs/lessons/`](lessons/) และ [`dax/measures.dax`](../dax/measures.dax)

---

## ผู้เรียนได้อะไรเมื่อจบ

1. สร้าง **Import semantic model** แบบ star schema ที่พร้อม production (integer keys, Date table, explicit measures)
2. เขียน DAX ที่อ่านง่าย: qualify คอลัมน์, `DIVIDE`, Boolean `CALCULATE`, `KEEPFILTERS` / filter modifiers
3. แยก **calculated column vs measure** และเลือก materialize + `SUM` แทน iterator เมื่อเหมาะ
4. ใช้ **role-playing date**, classic Time Intelligence, แล้ว **ลด measure explosion** ด้วย calculation groups
5. ใช้ **field parameters** และ **what-if** ในระดับรายงานโดยไม่ทำลายนิยามธุรกิจในโมเดล
6. ทบทวนด้วย **VertiPaq checklist** และเครื่องมือ (DAX query view, Performance Analyzer, pytest)

---

## โครงเรื่องและแหล่งข้อมูล

| องค์ประกอบ | ที่อยู่ |
| --- | --- |
| ข้อมูลสอน | [`data/Northwind_DW_DimFact.xlsx`](../data/Northwind_DW_DimFact.xlsx) |
| บทเรียน + Lab + เฉลย | [`docs/lessons/`](lessons/) |
| แคตตาล็อก measure | [`dax/measures.dax`](../dax/measures.dax) |
| Calculation group TI | [`dax/calculation-groups.tmdl`](../dax/calculation-groups.tmdl) |
| Best practices | [`docs/best-practices/README.md`](best-practices/README.md) |
| โครงเล่า 9EXPERT V22 | สไลด์ (ถ้ามี) + [`archive/README.md`](../archive/README.md) — **ไม่** copy สูตรจากสไลด์ |

---

## เส้นทางเรียน (ลำดับมาตรฐาน)

| ลำดับ | บท | ชั่วโมงโดยประมาณ | โฟกัส |
| ---: | --- | ---: | --- |
| 1 | [01 Star schema & Get Data](lessons/01-star-schema-and-get-data.md) | 2–3 | Semantic model ตั้งต้น |
| 2 | [02 Syntax & Context](lessons/02-dax-syntax-and-context.md) | 1–2 | Row vs filter context |
| 3 | [03 Calculated column](lessons/03-calculated-column.md) | 2 | Row context, sort by column |
| 4 | [04 Measures](lessons/04-measures.md) | 1–2 | Explicit measures, `DIVIDE` |
| 5 | [05 Aggregation & iterators](lessons/05-aggregation-and-iterators.md) | 2 | `SUMX` สอน → `SUM` production |
| 6 | [06 Logical / text / date](lessons/06-logical-text-date.md) | 1–2 | ฟังก์ชันคอลัมน์ |
| 7 | [07 RELATED & relationships](lessons/07-related-and-relationships.md) | 1–2 | Active/inactive, role-playing |
| 8 | [08 Date table](lessons/08-date-table.md) | 1 | Mark as date table, hierarchy |
| 9 | [09 CALCULATE](lessons/09-calculate.md) | 2–3 | Boolean filter, `USERELATIONSHIP` |
| 10 | [16 Filter modifiers & context transition](lessons/16-filter-modifiers-and-context-transition.md) | 2 | **แนะนำหลัง 09** |
| 11 | [10 Time Intelligence](lessons/10-time-intelligence.md) | 2 | Classic TI (measure explosion) |
| 12 | [11 Calculation groups](lessons/11-calculation-groups.md) | 2–3 | `SELECTEDMEASURE()` |
| 13 | [12 Field parameters](lessons/12-field-parameters.md) | 1 | สลับ field บน visual |
| 14 | [13 What-if](lessons/13-what-if.md) | 1 | Disconnected parameter |
| 15 | [14 Visual calculations](lessons/14-visual-calculations.md) | 0.5 | Optional |
| 16 | [15 VertiPaq checklist](lessons/15-vertipaq-and-performance.md) | 1 | สรุปคอร์ส + QA |

**รวมประมาณ 22–28 ชั่วโมง** ในห้อง (รวม lab) — ปรับตามความเร็วของกลุ่ม

---

## Map กับ Microsoft Learn

| Learning path / module | บทใน repo |
| --- | --- |
| [Use DAX in semantic models](https://learn.microsoft.com/training/paths/dax-power-bi/) (path) | 02–06, 04 |
| [Write DAX formulas](https://learn.microsoft.com/training/modules/dax-power-bi-write-formulas/) | 02 |
| [Create DAX calculations](https://learn.microsoft.com/training/modules/dax-power-bi-create-calculations/) | 03–05, 07 |
| [Modify DAX filter context](https://learn.microsoft.com/training/modules/dax-power-bi-modify-filter/) | 09, **16** |
| [DAX time intelligence](https://learn.microsoft.com/training/modules/dax-power-bi-time-intelligence/) | 08, 10, 11 |
| [Visual calculations](https://learn.microsoft.com/training/modules/power-bi-visual-calculations/) | 14 |
| [Star schema guidance](https://learn.microsoft.com/power-bi/guidance/star-schema) | 01, 15 |
| [Calculation groups](https://learn.microsoft.com/power-bi/transform-model/calculation-groups) | 11 |
| [Field parameters](https://learn.microsoft.com/power-bi/create-reports/power-bi-field-parameters) | 12 |

นักเรียนที่ทำ Learn คู่ขนานสามารถใช้ repo เป็น **lab โมเดลเดียว** (Northwind) แทน dataset หลายชุดในหลักสูตรออนไลน์

---

## เกณฑ์ผ่าน (สรุป)

- โมเดล `.pbix` ผ่าน checklist บท 15 (star, date table, discourage implicit measures, calc group TI)
- Lab ท้ายบทที่บังคับ (01–13, 16 แนะนำ) ทำได้โดยอ้าง [`dax/measures.dax`](../dax/measures.dax) ได้
- รัน `pytest -q` ใน repo ผ่าน (คุณภาพ Excel + sync measure catalog)

---

## ผู้สอน / maintainer

- คู่มือห้องเรียน: [`docs/instructor/README.md`](instructor/README.md)
- Semantic model + MCP + Fabric: [`docs/semantic-model/README.md`](semantic-model/README.md)
- ดัชนีฟังก์ชัน DAX ตามบท: [`docs/reference/dax-function-index.md`](reference/dax-function-index.md)
- Regenerate บทจาก generator: `python scripts/write_lessons.py`
- Refresh metadata Excel: `python scripts/extend_northwind_dw.py`
