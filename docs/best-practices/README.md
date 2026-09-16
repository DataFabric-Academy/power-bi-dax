# Best practices — ดัชนีสำหรับคอร์ส DAX (Northwind DW)

Best practice **ไม่ใช่บทท้าย** — แทรกเป็น callout ในทุกบทเรียน  
อ้างอิงหลักจาก Microsoft Learn

## Modeling / VertiPaq

| หลัก | ทำอะไร | Learn |
| --- | --- | --- |
| Star schema | Fact + Dimension; อย่า snowflake โดยไม่จำเป็น | [Star schema](https://learn.microsoft.com/power-bi/guidance/star-schema) |
| Integer surrogate keys | Relationship ใช้ `*Key` จำนวนเต็ม แล้วซ่อน FK | [Surrogate keys](https://learn.microsoft.com/power-bi/guidance/star-schema#surrogate-keys) |
| ปิด Auto date/time | ใช้ `DimDate` ที่ Mark as Date Table | [Disable auto date/time](https://learn.microsoft.com/power-bi/guidance/import-modeling-data-reduction#disable-auto-date-time) |
| Explicit measures | สร้าง measure ไม่ลากคอลัมน์ตัวเลขขึ้น Values | [Create measures](https://learn.microsoft.com/power-bi/transform-model/desktop-tutorial-create-measures) |
| Discourage implicit measures | เปิดก่อน Calculation Groups | [Calculation groups](https://learn.microsoft.com/power-bi/transform-model/calculation-groups) |
| Fixed Decimal สำหรับเงิน | Materialize `SalesAmount` / `LineCost` แล้ว `SUM` | [Data reduction](https://learn.microsoft.com/power-bi/guidance/import-modeling-data-reduction) |
| Single-direction filters | Bi-directional เมื่อจำเป็นเท่านั้น | [Relationships](https://learn.microsoft.com/power-bi/guidance/relationships-active-inactive) |

## DAX authoring

| หลัก | ทำอะไร | Learn |
| --- | --- | --- |
| Qualify columns | เสมอ `Table[Column]` | [Column and measure references](https://learn.microsoft.com/dax/best-practices/dax-column-measure-references) |
| Never qualify measures | ใช้ `[Measure]` ไม่ใช่ `Table[Measure]` | 同上 |
| `DIVIDE` | แทน `/` เมื่อหาร | [DIVIDE vs /](https://learn.microsoft.com/dax/best-practices/dax-divide-function-operator) |
| Boolean filter ใน CALCULATE | อย่า `FILTER ( ทั้งตาราง )` เมื่อ Boolean ได้ | [Avoid FILTER as filter argument](https://learn.microsoft.com/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument) |
| `KEEPFILTERS` | คง filter เดิมเมื่อต้องการ intersection | [KEEPFILTERS](https://learn.microsoft.com/dax/keepfilters-function-dax) |
| `VAR` | คำนวณครั้งเดียว อ่านง่าย | DAX basics |
| Calculated column | เฉพาะ Slicer / จัดกลุ่ม — ไม่ใส่ `TODAY()` | [Calculation options](https://learn.microsoft.com/power-bi/transform-model/desktop-calculations-options) |
| Prefer Power Query for columns | Calc column จาก DAX compress ด้อยกว่า M | [Preference for custom columns](https://learn.microsoft.com/power-bi/guidance/import-modeling-data-reduction#preference-for-custom-columns) |

## Calculation groups & dynamics

| หลัก | ทำอะไร | Learn |
| --- | --- | --- |
| `SELECTEDMEASURE()` | แพทเทิร์น Time Intelligence ใช้ซ้ำได้ทุก measure | [Create calculation groups](https://learn.microsoft.com/power-bi/transform-model/calculation-groups) |
| `ISNUMERIC ( SELECTEDMEASURE() )` | กัน error กับ measure ข้อความ / title | 同上 Considerations |
| Dynamic format string | เช่น YOY% เป็น `%` โดยไม่เปลี่ยนเป็น text | [Dynamic format strings](https://learn.microsoft.com/power-bi/create-reports/desktop-dynamic-format-strings) |
| Field parameters | **สลับ** field บน visual — คนละงานกับ calc group ที่ **แปลง** measure | [Field parameters](https://learn.microsoft.com/power-bi/create-reports/power-bi-field-parameters) |
| Precedence | เมื่อมีหลาย calc group | [Precedence](https://learn.microsoft.com/analysis-services/tabular-models/calculation-groups#precedence) |

## Callout template (ใช้ในบทเรียน)

```markdown
> **Best practice:** …
> อ้าง: [ลิงก์ Learn]
```

## สิ่งที่คอร์สนี้ตั้งใจสอน “แล้วค่อยเลิกใช้”

| แบบฝึก | ทำไมสอน | คำตอบ production |
| --- | --- | --- |
| `SUMX` คูณราคา | เข้าใจ Row Context | Materialize + `SUM` |
| Measure YTD คนละตัวต่อ base measure | เห็น measure explosion | Calculation group |
| Enter Data + `SWITCH` “Selected Measure” | Disconnected table | Calculation group / Field parameter |
| สร้าง `DimDate` ด้วย `CALENDAR` | เข้าใจ Date table | Import `DimDate` สำเร็จรูป |
