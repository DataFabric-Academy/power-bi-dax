# Power BI DAX — Northwind DW Curriculum (DataFabric Academy)

หลักสูตร DAX ที่สร้างบน **semantic model ที่ถูกต้องตั้งแต่ต้น** ด้วย Northwind star schema พร้อมคำอธิบายแบบ **Mental Model (ภาพจำในใจ)** ที่ช่วยให้ผู้เรียนทุกระดับ (เทียบเท่ามัธยมปลายเข้าใจได้ทันที) โดยยังคงรักษามาตรฐานทางเทคนิคระดับมืออาชีพสำหรับ Data Analyst, Business Analyst และ BI Developer ไว้อย่างครบถ้วน

> 💡 **แผนผังภาพจำในใจ (Mental Model Cheatsheet):**  
> - **Star Schema:** ดวงอาทิตย์ (Fact บันทึกธุรกรรมซ้ำๆ) ล้อมรอบด้วยดาวเคราะห์บริวาร (Dimension สมุดทะเบียนอ้างอิง)  
> - **Grain:** ระดับความละเอียดของกล้องจุลทรรศน์ (1 แถวใน Fact คือ 1 รายการสินค้าในบิล ไม่ใช่ทั้งบิล)  
> - **Filter Context:** แว่นตากรองแสงสี (ผู้ใช้จิ้มเลือกปี/ประเทศ ข้อมูลถูกร่อนเหลือเฉพาะส่วนนั้นก่อนคำนวณ)  
> - **Row Context:** นิ้วชี้ที่ไล่ตรวจทีละบรรทัดในสมุดบัญชี (เกิดขึ้นใน Calculated Column และ Iterators เช่น SUMX)  
> - **CALCULATE:** รีโมทคอนโทรลสั่งเปลี่ยนแว่นกรองสีก่อนคิดเลข (สามารถสั่งเพิ่ม ถอด หรือสลับแว่นได้)  
> - **Calculation Groups:** แผ่นฟิลเตอร์สวมทับหน้าเลนส์กล้อง (สร้างสูตรเวลา เช่น YTD แผ่นเดียว สวมได้กับทุก Measure)  
> - **VertiPaq Engine:** ตู้เก็บเอกสารแยกตามคอลัมน์และบีบอัดรหัสย่อ (ทำให้อ่านข้อมูลเร็วขึ้นหลายสิบเท่า)

| แหล่ง | บทบาท |
| --- | --- |
| [`data/Northwind_DW_DimFact.xlsx`](data/Northwind_DW_DimFact.xlsx) | ไฟล์เดียวที่ Get Data เข้าโมเดล |
| [`docs/lessons/`](docs/lessons/) | **แหล่งความจริง** — ทฤษฎี + ขั้นตอน + สูตร + Lab (โจทย์รวมเฉลย) |
| [`docs/CURRICULUM.md`](docs/CURRICULUM.md) | เป้าหมายการเรียนรู้ · map Microsoft Learn · ลำดับชั่วโมง |
| [`docs/instructor/README.md`](docs/instructor/README.md) | คู่มือผู้สอน |
| [`docs/semantic-model/README.md`](docs/semantic-model/README.md) | Semantic model · MCP · DAX query view |
| [`docs/reference/dax-function-index.md`](docs/reference/dax-function-index.md) | ดัชนีฟังก์ชันตามบท |
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

### Cursor + Power BI Modeling MCP (ผู้สอน / ผู้พัฒนาโมเดล)

โปรเจกต์นี้ลงทะเบียน MCP ระดับ workspace ที่ [`.cursor/mcp.json`](.cursor/mcp.json) ตาม [microsoft/powerbi-modeling-mcp](https://github.com/microsoft/powerbi-modeling-mcp)  
Rule: [`.cursor/rules/powerbi-modeling-mcp.mdc`](.cursor/rules/powerbi-modeling-mcp.mdc)

Project skills จาก [microsoft/skills-for-fabric `powerbi-authoring`](https://github.com/microsoft/skills-for-fabric/tree/main/plugins/powerbi-authoring) อยู่ที่ [`.cursor/skills/`](.cursor/skills/) (เวอร์ชัน 0.3.16 — ดู [SOURCE.md](.cursor/skills/SOURCE.md))

| Skill | ใช้เมื่อ |
| --- | --- |
| `semantic-model-authoring` | แก้ semantic model / DAX / relationships |
| `powerbi-report-planning` | เก็บ requirement ก่อนลงมือทำรายงาน |
| `powerbi-report-design` | ออกแบบ visual / layout / theme |
| `powerbi-report-authoring` | แก้ไฟล์รายงาน PBIR/PBIP |
| `powerbi-report-management` | publish / download รายงานบน Fabric |

1. เปิดโฟลเดอร์นี้ใน Cursor → **Settings → MCP** ตรวจว่า `powerbi-modeling-mcp` เปิดอยู่ (ต้องมี Node.js / `npx`)
2. เชื่อมโมเดลก่อนใช้เครื่องมือ (Desktop / Fabric / PBIP)
3. สำรอง `.pbix` ก่อนให้ agent แก้โมเดล

นักเรียนเรียนจาก Markdown + Excel — **ไม่บังคับ** ติดตั้ง MCP

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
10. [Filter modifiers & Context transition](docs/lessons/16-filter-modifiers-and-context-transition.md) ← แนะนำหลัง 09
11. [Time Intelligence (classic)](docs/lessons/10-time-intelligence.md)
12. [Calculation Groups](docs/lessons/11-calculation-groups.md) ← แทน Dynamic Measure แบบ SWITCH
13. [Field Parameters](docs/lessons/12-field-parameters.md)
14. [What-if](docs/lessons/13-what-if.md)
15. [Visual Calculations](docs/lessons/14-visual-calculations.md) (ภาคผนวก)
16. [VertiPaq checklist](docs/lessons/15-vertipaq-and-performance.md)

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
