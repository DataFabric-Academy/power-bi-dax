# บทเรียน (แหล่งความจริงของคอร์ส — Source of Truth)

เอกสารชุดนี้ออกแบบมาเพื่อสร้างความเข้าใจใน **Power BI Semantic Model & DAX** ตั้งแต่พื้นฐานไปจนถึงระดับสถาปัตยกรรมขั้นสูง โดยใช้ชุดข้อมูลจำลองมาตรฐาน **Northwind DW**

> 💡 **แนวคิดในการเรียนรู้ (Mental Model):**  
> การเรียน DAX ไม่ใช่แค่การจำสูตรคณิตศาสตร์ แต่คือการทำความเข้าใจ **"กลไกการคิดของระบบ" (Evaluation Context)** ถ้าเราเข้าใจว่าคอมพิวเตอร์กำลัง "สวมแว่นกรองข้อมูลแบบไหน" (Filter Context) หรือ "กำลังเอานิ้วชี้อยู่ที่บรรทัดใด" (Row Context) เราจะสามารถเขียนสูตรที่ทำงานได้อย่างถูกต้อง รวดเร็ว และตอบโจทย์ธุรกิจได้อย่างมั่นใจ

เอกสารชุดนี้สอนครบจบในตัว — **ไม่ต้องพึ่งสไลด์** สำหรับสูตรหรือขั้นตอนปฏิบัติ  
สไลด์ (ถ้ามี) ใช้เพื่อดูภาพรวมและโครงสร้างการเล่าเรื่องเท่านั้น

| # | บทเรียน | แนวคิดสำคัญ (Keyphrases & Concepts) | Lab รวมเฉลย |
| ---: | :--- | :--- | :---: |
| 01 | [Star schema และ Get Data](01-star-schema-and-get-data.md) | Star Schema, Fact vs Dim, Grain, Surrogate Key, Explicit Measure | ท้ายบท |
| 02 | [DAX syntax และ Context](02-dax-syntax-and-context.md) | Filter Context, Row Context, Table[Column] vs [Measure] | ท้ายบท |
| 03 | [Calculated Column](03-calculated-column.md) | Row Context, VertiPaq Storage, RAM Footprint, Sort by Column | ท้ายบท |
| 04 | [Measures](04-measures.md) | Dynamic Calculation, Query Time, DIVIDE (Safe Division) | ท้ายบท |
| 05 | [Aggregation และ Iterators](05-aggregation-and-iterators.md) | Aggregators (SUM), Iterators (SUMX), Storage vs Formula Engine | ท้ายบท |
| 06 | [Logical / Text / Date](06-logical-text-date.md) | IF, SWITCH ( TRUE () ), FORMAT, BLANK Handling | ท้ายบท |
| 07 | [RELATED และ Relationships](07-related-and-relationships.md) | Many-to-One, Cross-Filter Direction, Lookup via Relationship | ท้ายบท |
| 08 | [Date Table](08-date-table.md) | Contiguous Dates, Mark as Date Table, Fiscal Calendar | ท้ายบท |
| 09 | [CALCULATE](09-calculate.md) | Context Modification, Boolean Filter, KEEPFILTERS, USERELATIONSHIP | ท้ายบท |
| 10 | [Time Intelligence](10-time-intelligence.md) | TOTALYTD, SAMEPERIODLASTYEAR, Measure Explosion Problem | ท้ายบท |
| 11 | [Calculation Groups](11-calculation-groups.md) | Calculation Items, SELECTEDMEASURE(), Format Strings | ท้ายบท |
| 12 | [Field Parameters](12-field-parameters.md) | Dynamic Dimensions/Measures, Reporting UX, NAMEOF() | ท้ายบท |
| 13 | [What-if](13-what-if.md) | GENERATESERIES, Disconnected Table, Scenario Simulation | ท้ายบท |
| 14 | [Visual Calculations](14-visual-calculations.md) | Visual Matrix Axis, RUNNINGSUM, EXPAND / COLLAPSE | ท้ายบท |
| 15 | [VertiPaq checklist](15-vertipaq-and-performance.md) | Columnar Engine, Dictionary Encoding, Run-Length Encoding, Cardinality | ท้ายบท |
| 16 | [Filter modifiers และ Context transition](16-filter-modifiers-and-context-transition.md) | REMOVEFILTERS, ALLSELECTED, Context Transition in Row Context | ท้ายบท |

- **แคตตาล็อกสูตรทางการ:** [`dax/measures.dax`](../../dax/measures.dax) · [`dax/calculation-groups.tmdl`](../../dax/calculation-groups.tmdl)  
- **ดัชนีแนวทางปฏิบัติที่ดีที่สุด (Best Practices):** [../best-practices/README.md](../best-practices/README.md)
