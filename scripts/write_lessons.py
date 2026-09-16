# -*- coding: utf-8 -*-
"""Generate standalone lesson markdown (lab = exercise + solution combined)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "docs" / "lessons"


def w(name: str, body: str) -> None:
    path = LESSONS / name
    path.write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def main() -> None:
    LESSONS.mkdir(parents=True, exist_ok=True)

    w(
        "README.md",
        """
# บทเรียน (แหล่งความจริงของคอร์ส)

เอกสารชุดนี้สอนครบในตัว — **ไม่ต้องพึ่งสไลด์** เพื่อสูตรหรือขั้นตอน  
สไลด์ (ถ้ามี) ใช้เป็นภาพ UI / โครงเล่าเรื่องเท่านั้น

| # | บท | Lab รวมเฉลย |
| --- | --- | --- |
| 01 | [Star schema และ Get Data](01-star-schema-and-get-data.md) | ท้ายบท |
| 02 | [DAX syntax และ Context](02-dax-syntax-and-context.md) | ท้ายบท |
| 03 | [Calculated Column](03-calculated-column.md) | ท้ายบท |
| 04 | [Measures](04-measures.md) | ท้ายบท |
| 05 | [Aggregation และ Iterators](05-aggregation-and-iterators.md) | ท้ายบท |
| 06 | [Logical / Text / Date](06-logical-text-date.md) | ท้ายบท |
| 07 | [RELATED และ Relationships](07-related-and-relationships.md) | ท้ายบท |
| 08 | [Date Table](08-date-table.md) | ท้ายบท |
| 09 | [CALCULATE](09-calculate.md) | ท้ายบท |
| 10 | [Time Intelligence](10-time-intelligence.md) | ท้ายบท |
| 11 | [Calculation Groups](11-calculation-groups.md) | ท้ายบท |
| 12 | [Field Parameters](12-field-parameters.md) | ท้ายบท |
| 13 | [What-if](13-what-if.md) | ท้ายบท |
| 14 | [Visual Calculations](14-visual-calculations.md) | ท้ายบท (optional) |
| 15 | [VertiPaq checklist](15-vertipaq-and-performance.md) | ท้ายบท |

แคตตาล็อกสูตร: [`dax/measures.dax`](../../dax/measures.dax) · [`dax/calculation-groups.tmdl`](../../dax/calculation-groups.tmdl)  
ดัชนี Best practice: [../best-practices/README.md](../best-practices/README.md)
""",
    )

    w(
        "01-star-schema-and-get-data.md",
        """
# 01 — Star schema และ Get Data

**เป้าหมาย:** สร้าง semantic model ตั้งต้นที่ถูก — star schema, integer keys, Date table, explicit measure  
**ไฟล์ข้อมูล:** [`data/Northwind_DW_DimFact.xlsx`](../../data/Northwind_DW_DimFact.xlsx)  
**ผลลัพธ์ตอนจบบท:** มีโมเดล 6 ตาราง + relationships + `[Sales Amount]` พร้อม slicer ปีกรองยอดได้

---

## ทำไมต้องเริ่มที่โมเดล ไม่ใช่ที่สูตร

DAX ทำงานบน **filter context** ที่วิ่งตาม relationship  
ถ้าโมเดลเป็น flat / snowflake / คีย์ข้อความ / ไม่มี Date table ที่ถูกต้อง — สูตร Time Intelligence และ CALCULATE จะพังหรือช้าโดยไม่จำเป็น

คอร์สนี้ใช้ **Northwind DW** (star สำเร็จรูป) เป็นโมเดลหลักตลอดหลักสูตร

---

## โครงสร้างข้อมูล (อ่านก่อน Import)

| ตาราง | บทบาท | Grain / หมายเหตุ |
| --- | --- | --- |
| `FactSales` | Fact | **1 แถว = 1 order line** มี `SalesAmount`, `Profit`, `LineCost` (Fixed Decimal) |
| `DimDate` | Date dim | contiguous dates; มีปฏิทิน + Fiscal (เริ่ม 1 ต.ค.) |
| `DimCustomer` | Dim | Country, Segment, Customer |
| `DimEmployee` | Dim | First/Last name, BirthDate, HireDate, Department, Level |
| `DimProduct` | Dim | Category, Supplier (denormalized), ListPrice, Status, ProductCode |
| `DimShipper` | Dim | บริษัทขนส่ง |

ชีตที่ขึ้นต้นด้วย `_` (`_Columns`, `_Measures`, `_Relationships`, `_QA`, …) เป็น **เอกสารสำหรับมนุษย์/pytest** — **อย่า Import** เข้าโมเดล

> **Best practice:** Star schema + integer surrogate keys (`*Key`) แล้วซ่อนจาก Report view  
> อ้าง: [Star schema](https://learn.microsoft.com/power-bi/guidance/star-schema)

---

## ขั้นตอนทีละคลิก

### 1) Get Data

1. เปิด Power BI Desktop → **Get Data → Excel workbook**
2. เลือก `data/Northwind_DW_DimFact.xlsx`
3. ใน Navigator เลือกเฉพาะ **Tables** (ไอคอนตาราง):  
   `DimDate`, `DimCustomer`, `DimEmployee`, `DimProduct`, `DimShipper`, `FactSales`
4. **Load** (หรือ Transform แล้ว Close & Apply ถ้าต้องการตรวจชนิดข้อมูล)

### 2) ปิด Auto date/time

1. **File → Options and settings → Options**
2. **Current File → Data Load → Time intelligence**
3. ยกเลิก **Auto date/time**  
   (แนะนำปิดที่ Global ด้วยถ้าสอนห้องเดียวกันทั้งคอร์ส)

ถ้าไม่ปิด Power BI จะสร้างตารางวันที่ซ่อนต่อคอลัมน์วันที่ → ซ้ำกับ `DimDate` และทำให้ Time Intelligence สับสน

### 3) Relationships

ไป **Model view** ตรวจ/สร้างตามตารางนี้ (ชีต `_Relationships` ใน Excel เป็นแหล่งอ้างอิงเดียวกัน):

| From (many) | To (one) | Active | ความหมาย |
| --- | --- | --- | --- |
| `FactSales[ProductKey]` | `DimProduct[ProductKey]` | Yes | สินค้า |
| `FactSales[CustomerKey]` | `DimCustomer[CustomerKey]` | Yes | ลูกค้า |
| `FactSales[EmployeeKey]` | `DimEmployee[EmployeeKey]` | Yes | พนักงานขาย |
| `FactSales[ShipperKey]` | `DimShipper[ShipperKey]` | Yes | ขนส่ง |
| `FactSales[OrderDateKey]` | `DimDate[DateKey]` | **Yes** | วันที่สั่ง (หลัก) |
| `FactSales[RequiredDateKey]` | `DimDate[DateKey]` | No | วันกำหนดส่ง |
| `FactSales[ShippedDateKey]` | `DimDate[DateKey]` | No | วันส่งจริง |

Cardinality: Many-to-one · Cross-filter: **Single** (Dim → Fact)

### 4) Mark as Date Table

คลิกขวา `DimDate` → **Mark as date table** → คอลัมน์ `Date`  
ต้องเป็นชนิด Date, ไม่มีช่องว่างในช่วงวัน, ไม่ซ้ำ

### 5) ซ่อน Keys / FK

ซ่อนคอลัมน์ที่ `_Columns` ระบุ `Hidden = TRUE` โดยเฉพาะ `*Key` บน Fact และ Dim  
ผู้ใช้รายงานเลือกชื่อธุรกิจ (Customer, ProductName) ไม่ใช่ตัวเลข surrogate

### 6) Measure แรก + Discourage implicit measures

ใน Report view เลือกตาราง `FactSales` → New measure:

```dax
Sales Amount = SUM ( FactSales[SalesAmount] )
```

แนะนำทันที: Model view → โมเดล → เปิด **Discourage implicit measures**  
บังคับให้ทุกตัวเลขบน visual เป็น explicit measure (จำเป็นก่อนบท 11 Calculation Groups)

> **Best practice:** Explicit measures ตั้งแต่ชั่วโมงแรก + ปิด Auto date/time  
> อ้าง: [Import modeling data reduction](https://learn.microsoft.com/power-bi/guidance/import-modeling-data-reduction)

---

## สิ่งที่ต้องจำ

- Grain Fact = order **line** ไม่ใช่ order header
- Supplier อยู่บน `DimProduct` แล้ว — **ไม่มี** ตาราง SUPPLIERS แยก (ไม่สอน snowflake ใน lab)
- `FactSales[LineCost]` **ออกแบบให้ไม่เท่า** `StandardCost * Quantity` — ใช้เทียบในบท 05
- แคตตาล็อก measure เต็ม: [`dax/measures.dax`](../../dax/measures.dax)

---

## Lab 01 — ติดตั้งโมเดล (โจทย์ + เฉลย)

### โจทย์

1. Import 6 ตารางจากไฟล์ใน `data/`
2. ปิด Auto date/time ของไฟล์นี้
3. Mark `DimDate[Date]` as Date Table
4. มี relationship ไป `DimDate` 3 เส้น (1 active, 2 inactive)
5. สร้าง `[Sales Amount]`
6. Card + Slicer `DimDate[Year]` — กรองยอดได้

### เฉลย

- Relationships ตามตารางด้านบน / ชีต `_Relationships`
- สูตร:

```dax
Sales Amount = SUM ( FactSales[SalesAmount] )
```

- ถ้า slicer ปีไม่กรอง: ตรวจว่า active relationship คือ `OrderDateKey` → `DimDate` และ visual ใช้ measure ไม่ใช่คอลัมน์ดิบ

### เกณฑ์ผ่าน

- Model view เห็น star ชัด (Fact กลาง, Dim รอบ)
- มี explicit `[Sales Amount]`
- Slicer ปีจาก `DimDate` กรอง Card ได้

---

**ถัดไป:** [02 — DAX syntax และ Context](02-dax-syntax-and-context.md)
""",
    )

    w(
        "02-dax-syntax-and-context.md",
        """
# 02 — DAX syntax และ Context

**เป้าหมาย:** อ่านและเขียน DAX เป็น `Table[Column]` / `[Measure]` และแยก Row context กับ Filter context ได้  
**ข้อกำหนด:** จบบท 01 แล้ว มี `[Sales Amount]`

---

## ไวยากรณ์พื้นฐาน

| องค์ประกอบ | ตัวอย่าง | กฎ |
| --- | --- | --- |
| อ้างคอลัมน์ | `FactSales[SalesAmount]` | **ต้อง** มีชื่อตาราง |
| อ้าง measure | `[Sales Amount]` | **ห้าม** ใส่ชื่อตารางนำหน้า |
| Comment บรรทัด | `// ...` | |
| Comment บล็อก | `/* ... */` | |

```dax
// ถูก
Sales Amount = SUM ( FactSales[SalesAmount] )

// ผิดแบบที่พบบ่อย — ไม่ชัดว่าเป็นคอลัมน์หรือ measure
// Sales Amount = SUM ( [SalesAmount] )
```

> **Best practice:** Always fully qualify **columns**. Never fully qualify **measures**.  
> อ้าง: [Column and measure references](https://learn.microsoft.com/dax/best-practices/dax-column-measure-references)

---

## Context สองชนิด (หัวใจของ DAX)

### Filter context

มาก่อนที่สูตรจะรัน — จาก:

- แถว/คอลัมน์ของ visual (Matrix, Chart)
- Slicer / Filter pane
- `CALCULATE` ที่เปลี่ยน filter (บท 09)

Card ของ `[Sales Amount]` + Slicer Country = Germany → engine กรอง Fact ตามลูกค้าเยอรมนี แล้วค่อย `SUM`

### Row context

มีเมื่อ DAX “เดินทีละแถว” ของตาราง:

- Calculated column (ทุกแถวของตารางนั้น)
- Iterator: `SUMX`, `AVERAGEX`, `FILTER`, …

ใน calculated column บน `DimEmployee` การเขียน `DimEmployee[BirthYear]` หมายถึงค่าของแถวปัจจุบัน

**Filter context ไม่กลายเป็น Row context อัตโนมัติ** — ต้องใช้ iterator หรือ `RELATED` ตามทิศ relationship (บท 05, 07)

---

## ตัวอย่างแยก context ในห้อง

1. วาง Card `[Sales Amount]` → ได้ยอดทั้งโมเดล (filter context ว่างจาก visual)
2. เพิ่ม Slicer `DimCustomer[Country]` → Card เปลี่ยนตามประเทศ (filter context)
3. สร้าง calculated column `DimProduct[ListPrice]` × 1.07 → คำนวณทีละแถว (row context) เก็บใน VertiPaq

---

## Lab 02 — Syntax และ Context (โจทย์ + เฉลย)

### โจทย์

1. สร้าง measure `[Orders]` = จำนวน order ไม่ซ้ำ (qualify คอลัมน์ให้ถูก)
2. วาง Card `[Sales Amount]` และ `[Orders]` + Slicer Country
3. อธิบายสั้น ๆ (1–2 ประโยคในโน้ตส่วนตัว) ว่า Card ใช้ Filter context อย่างไร

### เฉลย

```dax
Orders = DISTINCTCOUNT ( FactSales[OrderID] )
```

- ถูก: `FactSales[OrderID]` เป็นคอลัมน์ → qualify ตาราง
- ถูก: อ้าง measure อื่นเป็น `[Sales Amount]` ไม่ใช่ `FactSales[Sales Amount]`
- เมื่อเลือก Country บน slicer → filter วิ่ง DimCustomer → FactSales → ทั้งสอง Card คำนวณใหม่ภายใต้ filter เดียวกัน

### เกณฑ์ผ่าน

- สูตรใช้ `FactSales[OrderID]`
- ไม่มี `TableName[Orders]` ตอนอ้าง measure

---

**ถัดไป:** [03 — Calculated Column](03-calculated-column.md)
""",
    )

    w(
        "03-calculated-column.md",
        """
# 03 — Calculated Column

**เป้าหมาย:** สร้างคอลัมน์สำหรับ Slicer / จัดกลุ่ม / Sort by Column เท่านั้น — ไม่ใช้แทน measure  
**ข้อกำหนด:** มี `DimEmployee[BirthDate]`, `BirthYear`, `DimProduct[ListPrice]`

---

## Column vs Measure — เลือกผิดเสียทั้งโมเดล

| ใช้ Calculated Column | ใช้ Measure |
| --- | --- |
| Generation, AgeGroup, PriceRange | ยอดขาย, % Margin, YTD |
| ต้องการ Sort by Column / Slicer / Legend | Ratio ที่เปลี่ยนตาม filter |
| ค่าคงที่ต่อแถวหลัง refresh | ค่าที่ต้องตอบ filter context |

Calculated column **ถูก materialize** เข้า VertiPaq → เพิ่ม RAM  
Measure คำนวณตอน query → ยืดหยุ่นกับ filter

> **Best practice:** Prefer สร้างคอลัมน์ใน Power Query/ETL เมื่อไม่ต้องอิง measure  
> อ้าง: [Calculation options](https://learn.microsoft.com/power-bi/transform-model/desktop-calculations-options) · [Preference for custom columns](https://learn.microsoft.com/power-bi/guidance/import-modeling-data-reduction#preference-for-custom-columns)

---

## Generation บน DimEmployee

ใช้ `BirthYear` ที่ ETL เตรียมไว้ (ไม่ต้อง parse วันที่เอง):

```dax
Generation =
VAR y = DimEmployee[BirthYear]
RETURN
    SWITCH (
        TRUE (),
        y <= 1964, "Baby Boom Generation",
        y <= 1980, "Generation X",
        y <= 1996, "Generation Y",
        y <= 2010, "Generation Z",
        "Generation Alpha"
    )
```

```dax
Generation Sort =
VAR y = DimEmployee[BirthYear]
RETURN
    SWITCH (
        TRUE (),
        y <= 1964, 1,
        y <= 1980, 2,
        y <= 1996, 3,
        y <= 2010, 4,
        5
    )
```

คลิกคอลัมน์ `Generation` → **Sort by column** → `Generation Sort`

---

## AgeGroup (lab — ระวัง TODAY)

```dax
AgeGroup =
VAR Age = DATEDIFF ( DimEmployee[BirthDate], TODAY (), YEAR )
RETURN
    SWITCH (
        TRUE (),
        Age < 25, "Under 25",
        Age < 40, "25-40",
        Age < 50, "41-50",
        "Over 50"
    )
```

```dax
AgeGroupSort =
VAR Age = DATEDIFF ( DimEmployee[BirthDate], TODAY (), YEAR )
RETURN
    SWITCH (
        TRUE (),
        Age < 25, 1,
        Age < 40, 2,
        Age < 50, 3,
        4
    )
```

> **Best practice:** `TODAY()` ใน calculated column ติดค่าตอน **refresh** ไม่ใช่ตอนเปิดรายงานทุกวัน — lab ใช้ได้ แต่ production คำนวณ Age ที่ ETL หรือใช้ measure  
> อ้าง: ลิงก์ Calculation options ด้านบน

---

## PriceRange บน DimProduct

```dax
PriceRange =
SWITCH (
    TRUE (),
    DimProduct[ListPrice] <= 20, "Under 20",
    DimProduct[ListPrice] <= 40, "21-40",
    DimProduct[ListPrice] <= 60, "41-60",
    "Over 60"
)
```

```dax
PriceRangeSort =
SWITCH (
    TRUE (),
    DimProduct[ListPrice] <= 20, 1,
    DimProduct[ListPrice] <= 40, 2,
    DimProduct[ListPrice] <= 60, 3,
    4
)
```

Sort by column เช่นเดียวกับ Generation

---

## Lab 03 — Calculated Columns (โจทย์ + เฉลย)

### โจทย์

1. สร้าง `Generation` + `Generation Sort` แล้ว Sort by Column
2. สร้าง `AgeGroup` + `AgeGroupSort`
3. สร้าง `PriceRange` + `PriceRangeSort`
4. Matrix: แถว = Generation, ค่า = `[Sales Amount]`

### เฉลย

ใช้สูตรในบทนี้ทั้งหมด แล้วตั้ง Sort by Column ให้ครบสามชุด  
ถ้า Generation เรียงตามตัวอักษร (Baby มาก่อน Generation X ผิดยุค) = ยังไม่ได้ Sort by Column

### เกณฑ์ผ่าน

- Generation เรียงตามยุค (Baby Boom → … → Alpha) ไม่ใช่ A–Z
- Matrix แสดงยอดขายตาม Generation ได้

---

**ถัดไป:** [04 — Measures](04-measures.md)
""",
    )

    w(
        "04-measures.md",
        """
# 04 — Measures

**เป้าหมาย:** Explicit measure เป็นค่าเริ่มต้นของทุกตัวเลขบนรายงาน + ใช้ `DIVIDE` + จัด Display folder  
**ข้อกำหนด:** จบบท 01–02

---

## ทำไมต้อง Explicit measure

ลาก `FactSales[SalesAmount]` ขึ้น Values = **implicit measure** (engine สร้าง `SUM` ให้ชั่วคราว)

ปัญหา:

- ชื่อไม่คงที่ / ควบคุม format ยาก
- **Calculation groups ไม่ทำงาน** กับ implicit measure
- นักเรียนก๊อปสูตรอ้างคอลัมน์ดิบแล้วสับสนกับ context

ตั้ง **Discourage implicit measures** ตั้งแต่ต้นคอร์ส

> **Best practice:** สร้าง measure ชัดเจน; เปิด Discourage implicit measures  
> อ้าง: [Create measures](https://learn.microsoft.com/power-bi/transform-model/desktop-tutorial-create-measures) · [Calculation groups](https://learn.microsoft.com/power-bi/transform-model/calculation-groups)

---

## Base measures (คัดลอกได้)

Home table แนะนำ: `FactSales` · Display folder เช่น `Sales`, `Volume`

```dax
Sales Amount = SUM ( FactSales[SalesAmount] )

Sales Quantity = SUM ( FactSales[Quantity] )

Discount Amount = SUM ( FactSales[DiscountAmount] )

Line Cost = SUM ( FactSales[LineCost] )

Profit = SUM ( FactSales[Profit] )

Profit Margin = DIVIDE ( [Profit], [Sales Amount] )

Order Lines = COUNTROWS ( FactSales )

Orders = DISTINCTCOUNT ( FactSales[OrderID] )

Customers = DISTINCTCOUNT ( FactSales[CustomerKey] )
```

หลังมี measure แล้ว **ซ่อนคอลัมน์ฐาน** (`SalesAmount`, `Quantity`, `Profit`, …) จาก Report view — เหลือให้เลือกแค่ measure

> **Best practice:** ใช้ `DIVIDE ( num, den )` แทน `/` เพื่อจัดการหารศูนย์ / BLANK  
> อ้าง: [DIVIDE vs divide operator](https://learn.microsoft.com/dax/best-practices/dax-divide-function-operator)

แคตตาล็อกเต็ม: [`dax/measures.dax`](../../dax/measures.dax)

---

## Format และ Home table

| Measure | Format แนะนำ |
| --- | --- |
| Sales Amount, Line Cost, Profit | Decimal number / Currency |
| Profit Margin | Percentage 1–2 ตำแหน่ง |
| Orders, Customers | Whole number |

---

## Lab 04 — Measures (โจทย์ + เฉลย)

### โจทย์

สร้างและจัด Display folder:

- Sales: Sales Amount, Sales Quantity, Line Cost, Profit, Profit Margin
- Volume: Order Lines, Orders, Customers

ซ่อนคอลัมน์ฐานที่เกี่ยวข้อง

### เฉลย

คัดลอกบล็อกด้านบน (หรือจาก `dax/measures.dax` ตอน Sales / Volume)

```dax
Profit Margin = DIVIDE ( [Profit], [Sales Amount] )
```

อย่าเขียน `[Profit] / [Sales Amount]` เป็นค่าเริ่มต้นของคอร์ส

### เกณฑ์ผ่าน

- Profit Margin ใช้ `DIVIDE`
- ลากคอลัมน์ `SalesAmount` ขึ้น visual ไม่ได้หรือไม่ถูกส่งเสริม (discourage เปิดอยู่)

---

**ถัดไป:** [05 — Aggregation และ Iterators](05-aggregation-and-iterators.md)
""",
    )

    w(
        "05-aggregation-and-iterators.md",
        """
# 05 — Aggregation และ Iterators (SUMX)

**เป้าหมาย:** เข้าใจ Row Context ของ iterator — แล้วเลือก production path เป็น `SUM` ของคอลัมน์ที่ materialize  
**ข้อกำหนด:** มี `[Sales Amount]`, `[Line Cost]` จากบท 04

---

## สองทางไปยอดเดียวกัน (ไม่เสมอไป)

### Production (ค่าเริ่มต้นที่ถูก)

```dax
Sales Amount = SUM ( FactSales[SalesAmount] )
Line Cost = SUM ( FactSales[LineCost] )
```

`SalesAmount` / `LineCost` ถูกคำนวณที่ ETL แล้วเก็บเป็น Fixed Decimal → VertiPaq รวมเร็ว

### Iterator (สอน Row Context)

```dax
Sales Amount (SUMX) =
SUMX (
    FactSales,
    FactSales[UnitPrice] * FactSales[Quantity] * ( 1 - FactSales[Discount] )
)
```

`SUMX` สร้าง row context ทีละแถวของ `FactSales` แล้วรวมผล

บน Northwind ค่า `[Sales Amount]` กับ `[Sales Amount (SUMX)]` ควรใกล้เคียง/ตรงกันถ้า ETL สอดคล้องสูตร

---

## บทเรียนสำคัญ: LineCost ≠ StandardCost × Qty

```dax
Line Cost (from StandardCost) =
SUMX (
    FactSales,
    RELATED ( DimProduct[StandardCost] ) * FactSales[Quantity]
)
```

เปรียบ Card ของ `[Line Cost]` กับ `[Line Cost (from StandardCost)]` — **ตัวเลขต่างกันโดยออกแบบ**

เหตุผลสอน: อย่าสมมติว่า “ต้นทุนบน Fact = ต้นทุนบน Dim × จำนวน” โดยไม่ตรวจโมเดล  
ในธุรกิจจริง LineCost อาจรวม overhead / landed cost

> **Best practice:** Iterator แพงกว่า column aggregation บน VertiPaq — materialize ที่ ETL แล้ว `SUM`  
> อ้าง: [Import modeling data reduction](https://learn.microsoft.com/power-bi/guidance/import-modeling-data-reduction)

---

## FILTER + AVERAGEX

```dax
Avg Active List Price =
AVERAGEX (
    FILTER ( DimProduct, DimProduct[Status] = "Active" ),
    DimProduct[ListPrice]
)

Max Active List Price =
MAXX (
    FILTER ( DimProduct, DimProduct[Status] = "Active" ),
    DimProduct[ListPrice]
)
```

หมายเหตุบท 09: ใน `CALCULATE` ควรเลี่ยง `FILTER ( ทั้งตาราง )` เมื่อ Boolean filter ทำได้ — แต่ iterator ที่ต้องเดินแถวยังใช้ `FILTER` ได้ตามบริบท

---

## Lab 05 — Iterators (โจทย์ + เฉลย)

### โจทย์

1. สร้าง `[Sales Amount (SUMX)]` เทียบ `[Sales Amount]`
2. สร้าง `[Line Cost (from StandardCost)]` เทียบ `[Line Cost]` — ต้อง **ต่าง**
3. สร้าง `[Avg Active List Price]`
4. เขียนหนึ่งประโยคว่าทำไม Line Cost สองแบบไม่เท่ากัน

### เฉลย

ใช้สูตรในบทนี้  
คำตอบสั้น ๆ ที่ถูกต้อง: `FactSales[LineCost]` เป็นต้นทุนบรรทัดที่ materialize แยกจาก `DimProduct[StandardCost] * Quantity` — โมเดลตั้งใจให้ต่างเพื่อฝึกตรวจสอบสมมติฐาน

### เกณฑ์ผ่าน

- เห็นตัวเลข Line Cost สองแบบไม่เท่าบน Card
- อธิบายเหตุผลได้โดยไม่อ้างว่า “สูตรผิด”

---

**ถัดไป:** [06 — Logical / Text / Date](06-logical-text-date.md)
""",
    )

    w(
        "06-logical-text-date.md",
        """
# 06 — Logical, Text, Date

**เป้าหมาย:** ใช้ IF / SWITCH, การต่อข้อความ, และคอลัมน์วันที่บน dimension อย่างถูกชนิดข้อมูล  
**ข้อกำหนด:** มี `DimProduct[ProductCode]`, `UnitsInStock`, `ReorderLevel`, `Status`

---

## Logical — IF / SWITCH / IN

```dax
PromotionFlag =
IF (
    INT ( LEFT ( DimProduct[ProductCode], 1 ) ) IN { 1, 8 },
    0.2,
    0
)
```

```dax
Reorder =
IF (
    DimProduct[UnitsInStock] <= DimProduct[ReorderLevel]
        && DimProduct[Status] = "Active",
    "Reorder",
    "OK"
)
```

ใช้ `&&` / `||` ใน expression; ใน `CALCULATE` filter argument ใช้เครื่องหมายจุลภาคแยกเงื่อนไข (บท 09)

---

## Text

```dax
Employee Full =
DimEmployee[FirstName] & " " & DimEmployee[LastName]
```

ทางเลือก: `COMBINEVALUES ( " ", DimEmployee[FirstName], DimEmployee[LastName] )` เมื่อต้องการคีย์ประกอบที่ปลอดภัยกว่า

---

## Date

คอร์สนี้มี `DimEmployee[BirthDate]` ชนิด Date จาก ETL แล้ว — ใช้ตรง ๆ

ถ้าฝึกประกอบวันที่จากส่วนย่อย:

```dax
BirthDate (from parts) =
DATE ( DimEmployee[BirthYear], DimEmployee[BirthMonth], DimEmployee[BirthDay] )
```

> **Best practice:** คอลัมน์วันที่จริงชนิด Date ที่ ETL ดีกว่าประกอบด้วย DAX ใน production

อย่าใช้ข้อความ `"2024-01-15"` เป็นคอลัมน์วันที่หลักของโมเดล

---

## Lab 06 — Logical / Text / Date (โจทย์ + เฉลย)

### โจทย์

1. คอลัมน์ `Reorder` บน DimProduct
2. คอลัมน์ `PromotionFlag` จาก `LEFT ( ProductCode )`
3. คอลัมน์ `Employee Full`
4. Visual นับสินค้าที่ `Reorder = "Reorder"` (Card หรือตาราง)

### เฉลย

```dax
Reorder =
IF (
    DimProduct[UnitsInStock] <= DimProduct[ReorderLevel]
        && DimProduct[Status] = "Active",
    "Reorder",
    "OK"
)

PromotionFlag =
IF ( INT ( LEFT ( DimProduct[ProductCode], 1 ) ) IN { 1, 8 }, 0.2, 0 )

Employee Full = DimEmployee[FirstName] & " " & DimEmployee[LastName]
```

นับสินค้า Reorder: ใส่ slicer/filter `Reorder = Reorder` แล้ว Card ของ `DISTINCTCOUNT ( DimProduct[ProductKey] )` หรือ measure ชั่วคราว

### เกณฑ์ผ่าน

- สูตร qualify `DimProduct[...]` / `DimEmployee[...]` ครบ
- Visual แยกสินค้าที่ต้องสั่งซื้อเพิ่มได้

---

**ถัดไป:** [07 — RELATED และ Relationships](07-related-and-relationships.md)
""",
    )

    w(
        "07-related-and-relationships.md",
        """
# 07 — RELATED และ Relationships

**เป้าหมาย:** ดึงค่าจาก Dimension ไป Fact ด้วย `RELATED`; เข้าใจ single-direction, active vs inactive  
**ข้อกำหนด:** Relationships จากบท 01 ครบ

---

## RELATED ทำงานเมื่อไหร่

`RELATED ( DimTable[Column] )` ใช้ใน **row context ฝั่ง many** (เช่น calculated column บน Fact) เพื่อเดินไปตาราง one ตาม relationship ที่ **active**

```dax
// บน FactSales (calculated column — demo / slicer บน fact ถ้าจำเป็น)
Customer Name = RELATED ( DimCustomer[Customer] )

Product Category = RELATED ( DimProduct[Category] )

Supplier Name = RELATED ( DimProduct[Supplier] )
```

**ไม่มีตาราง SUPPLIERS แยก** — Supplier ถูก denormalize เข้า `DimProduct` แล้ว

ทิศกลับ (Dim → รวม Fact) ใช้ `RELATEDTABLE` หรือ measure บน Fact ไม่ใช่ `RELATED`

> **Best practice:** ลด hop — denormalize snowflake เข้า dimension เดียวเมื่อเป็นไปได้  
> อ้าง: [Star schema — snowflake](https://learn.microsoft.com/power-bi/guidance/star-schema#snowflake-dimensions)

---

## ทิศทาง Filter

ค่าเริ่มต้นคอร์ส: **Single** (Dimension กรอง Fact)

Bi-directional ใช้เมื่อมีเหตุผลชัด (เช่น many-to-many bridge) — ไม่เปิดทั้งโมเดลเพื่อ “ให้ slicer โผล่”

> **Best practice:** [Relationships active vs inactive](https://learn.microsoft.com/power-bi/guidance/relationships-active-inactive)

---

## Role-playing Date (สามเส้นไป DimDate)

| FK บน Fact | Active | ความหมายธุรกิจ |
| --- | --- | --- |
| `OrderDateKey` | Yes | วิเคราะห์ยอดตามวันสั่ง |
| `RequiredDateKey` | No | วันครบกำหนด |
| `ShippedDateKey` | No | วันส่งของ |

เปิดเส้น inactive ด้วย `USERELATIONSHIP` ใน measure (บท 09)  
ทางเลือกตาม Learn: ทำตารางวันที่ซ้ำ `DimShipDate` — คอร์สนี้ใช้ inactive + measure เพื่อไม่เพิ่มตาราง

---

## Lab 07 — RELATED (โจทย์ + เฉลย)

### โจทย์

1. Calculated columns บน FactSales: `Customer Name`, `Product Category`, `Supplier Name`
2. Table visual: OrderID + สามคอลัมน์ + `[Sales Amount]`
3. **ห้าม** สร้างตาราง SUPPLIERS

### เฉลย

```dax
Customer Name = RELATED ( DimCustomer[Customer] )
Product Category = RELATED ( DimProduct[Category] )
Supplier Name = RELATED ( DimProduct[Supplier] )
```

ถ้า `RELATED` error: ตรวจ relationship Fact→Dim นั้น active และ cardinality many-to-one

### เกณฑ์ผ่าน

- Table แสดงชื่อลูกค้า/หมวด/ซัพพลายเออร์โดยไม่ต้องมีตารางซัพพลายเออร์แยก

---

**ถัดไป:** [08 — Date Table](08-date-table.md)
""",
    )

    w(
        "08-date-table.md",
        """
# 08 — Date Table

**เป้าหมาย:** ใช้ `DimDate` ที่ import แล้ว Mark as Date Table เป็นตารางวันที่หลัก — ไม่สร้างตารางหลักด้วย DAX  
**ข้อกำหนด:** ปิด Auto date/time จากบท 01

---

## คุณสมบัติ Date table ที่ถูกต้อง

1. คอลัมน์ Date ชนิด **Date** (ไม่ใช่ DateTime ที่มีเวลาแปลก)
2. **หนึ่งแถวต่อหนึ่งวัน** — ไม่ซ้ำ
3. ช่วงวัน **contiguous** (ไม่มีวันที่ขาด) ครอบคลุม Fact
4. Mark as Date Table ชี้คอลัมน์นั้น
5. Time intelligence DAX อ้างคอลัมน์นี้ เช่น `DimDate[Date]`

Northwind DW เตรียมครบแล้ว — ตรวจด้วยชีต `_QA` / `pytest`

---

## Hierarchy ที่ใช้ในรายงาน

**ปฏิทิน:** Year → YearQuarter → MonthName → Date  
**Fiscal (เริ่ม 1 ตุลาคม):** FiscalYearLabel → FiscalYearQuarter → FiscalMonthName → Date  

ดูชื่อคอลัมน์จริงใน `_Hierarchies` / `_Columns` ของ Excel

สร้าง hierarchy ใน Model view: ลากคอลัมน์ซ้อนกันใต้ตาราง `DimDate`

> **Best practice:** Import date table + ปิด Auto date/time  
> อ้าง: [Date tables in Power BI Desktop](https://learn.microsoft.com/power-bi/guidance/model-date-tables)

---

## ภาคผนวก — CALENDAR (ฝึกแล้วลบ)

ไม่ใช้เป็นตารางหลักของคอร์ส แต่ฝึกสร้างได้:

```dax
PracticeCalendar =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2023, 1, 1 ), DATE ( 2025, 12, 31 ) ),
    "Year", YEAR ( [Date] ),
    "MonthName", FORMAT ( [Date], "MMMM" ),
    "MonthNumber", MONTH ( [Date] )
)
```

เปรียบกับ `DimDate` ที่ import แล้ว **ลบ** `PracticeCalendar` ก่อนไปบทถัดไป

Fiscal year end สำหรับ `TOTALYTD` ในคอร์สนี้ใช้ `"09/30"` (วันสุดท้ายก่อนปีงบที่เริ่ม ต.ค.) — รายละเอียดบท 10

---

## Lab 08 — Date Table (โจทย์ + เฉลย)

### โจทย์

1. ยืนยัน Mark as Date Table บน `DimDate[Date]`
2. สร้าง hierarchy Calendar และ Fiscal
3. (Optional) สร้าง `PracticeCalendar` แล้วลบออก
4. Matrix drill Year → Month ของ `[Sales Amount]`

### เฉลย

- Mark as Date Table: คลิกขวา DimDate → Mark as date table → `Date`
- Hierarchy ตาม `_Hierarchies`
- Drill บน visual ใช้ปุ่ม Expand / Drill down ของ Matrix

### เกณฑ์ผ่าน

- Drill Year ไป Month ได้ และยอดเปลี่ยนตามระดับ

---

**ถัดไป:** [09 — CALCULATE](09-calculate.md)
""",
    )

    w(
        "09-calculate.md",
        """
# 09 — CALCULATE

**เป้าหมาย:** เปลี่ยน Filter context อย่างถูกวิธี — Boolean filter, `KEEPFILTERS`, `USERELATIONSHIP`; เลี่ยง `FILTER ( ทั้งตาราง )` เมื่อไม่จำเป็น  
**ข้อกำหนด:** มี base measures และ Date relationships

---

## CALCULATE ทำอะไร

```dax
CALCULATE ( <expression>, <filter1>, <filter2>, ... )
```

1. ประเมิน filter arguments
2. แก้ filter context
3. ประเมิน expression ภายใต้ context ใหม่

เป็นสะพานระหว่าง measure กับ “มุมมองใหม่” ของข้อมูล

---

## Boolean filter (ค่าเริ่มต้นที่ถูก)

```dax
Sales Amount EU =
CALCULATE (
    [Sales Amount],
    KEEPFILTERS ( DimCustomer[Country] IN { "Germany", "Italy", "France" } )
)
```

- `DimCustomer[Country] IN { ... }` เป็น filter argument แบบ Boolean → engine optimize ได้ดี
- `KEEPFILTERS` ทำให้เงื่อนไข **ตัดกับ** filter ที่มีอยู่ (เช่น slicer Country) แทนการแทนที่ทั้งหมดในคอลัมน์นั้นแบบหยาบ

เทียบแบบที่ Learn ไม่แนะนำเป็นค่าเริ่มต้น:

```dax
-- เลี่ยงเมื่อ Boolean ทำได้
CALCULATE (
    [Sales Amount],
    FILTER (
        DimCustomer,
        DimCustomer[Country] IN { "Germany", "Italy", "France" }
    )
)
```

> **Best practice:** อย่าใช้ `FILTER ( ตารางทั้งก้อน )` เป็น filter argument เมื่อ Boolean ทำได้ + รู้จัก `KEEPFILTERS`  
> อ้าง: [Avoid FILTER as filter argument](https://learn.microsoft.com/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument) · [KEEPFILTERS](https://learn.microsoft.com/dax/keepfilters-function-dax)

---

## USERELATIONSHIP — เปิดเส้นวันที่ inactive

```dax
Sales Amount (Required Date) =
CALCULATE (
    [Sales Amount],
    USERELATIONSHIP ( FactSales[RequiredDateKey], DimDate[DateKey] )
)

Sales Amount (Shipped Date) =
CALCULATE (
    [Sales Amount],
    USERELATIONSHIP ( FactSales[ShippedDateKey], DimDate[DateKey] )
)

Profit (Shipped Date) =
CALCULATE (
    [Profit],
    USERELATIONSHIP ( FactSales[ShippedDateKey], DimDate[DateKey] )
)
```

ใน Matrix แถว = `DimDate[MonthName]` คอลัมน์/ค่า = Order vs Shipped จะเห็นยอดเลื่อนเดือนตามบทบาทวันที่

---

## VAR ช่วยอ่านและกันคำนวณซ้ำ

```dax
Sales Amount EU Share =
VAR EuSales = [Sales Amount EU]
VAR AllSales = CALCULATE ( [Sales Amount], REMOVEFILTERS ( DimCustomer[Country] ) )
RETURN
    DIVIDE ( EuSales, AllSales )
```

---

## Lab 09 — CALCULATE (โจทย์ + เฉลย)

### โจทย์

1. `[Sales Amount EU]` ด้วย `KEEPFILTERS` + Country IN Germany, Italy, France
2. `[Sales Amount (Shipped Date)]` ด้วย `USERELATIONSHIP`
3. Matrix เปรียบยอดตามเดือน: Order Date (measure ปกติ) vs Shipped Date

### เฉลย

ใช้สูตรในบทนี้ (หรือบล็อก CALCULATE ใน `dax/measures.dax`)  
อย่าใช้ `FILTER ( DimCustomer, ... )` เป็นคำตอบหลัก

### เกณฑ์ผ่าน

- สูตร EU เป็น Boolean + `KEEPFILTERS`
- Matrix แสดงความต่างของเดือนระหว่าง Order กับ Shipped

---

**ถัดไป:** [10 — Time Intelligence](10-time-intelligence.md)
""",
    )

    w(
        "10-time-intelligence.md",
        """
# 10 — Time Intelligence (classic measures)

**เป้าหมาย:** สร้าง YTD / PY / YoY ด้วย measure แยกต่อ base measure — **ตั้งใจให้เห็น measure explosion** ก่อนย้ายไป Calculation Groups  
**ข้อกำหนด:** Mark as Date Table แล้ว; มี `[Sales Amount]`, `[Sales Quantity]`

---

## ฟังก์ชันที่ใช้บ่อย

| ฟังก์ชัน | ใช้ทำ |
| --- | --- |
| `DATESYTD` / `TOTALYTD` | ปีถึงวันที่ |
| `DATESMTD` / `DATESQTD` | เดือน / ไตรมาสถึงวันที่ |
| `SAMEPERIODLASTYEAR` | ช่วงเทียบปีก่อน |
| `DATEADD` | เลื่อนช่วงเป็นช่วง |
| `DATESINPERIOD` | rolling window |

ทุกตัวต้องอ้างคอลัมน์วันที่ของ Date table ที่ Mark แล้ว: `DimDate[Date]`

> หมายเหตุ: Calendar-based time intelligence (preview) มีบน Learn — คอร์สนี้ใช้ classic + calc group ในบท 11

---

## ชุด Sales Amount

```dax
Sales Amount YTD = TOTALYTD ( [Sales Amount], DimDate[Date] )

Sales Amount PY =
CALCULATE ( [Sales Amount], SAMEPERIODLASTYEAR ( DimDate[Date] ) )

Sales Amount YoY % =
DIVIDE ( [Sales Amount] - [Sales Amount PY], [Sales Amount PY] )

Sales Amount FYTD =
TOTALYTD ( [Sales Amount], DimDate[Date], "09/30" )

Sales Amount Rolling 60d =
CALCULATE (
    [Sales Amount],
    DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ), -60, DAY )
)
```

`"09/30"` = ปีงบที่สิ้นสุด 30 ก.ย. (สอดคล้อง Fiscal ที่เริ่ม 1 ต.ค. ใน DimDate)

---

## ชุด Sales Quantity (ซ้ำแพทเทิร์น)

```dax
Sales Quantity YTD = TOTALYTD ( [Sales Quantity], DimDate[Date] )

Sales Quantity PY =
CALCULATE ( [Sales Quantity], SAMEPERIODLASTYEAR ( DimDate[Date] ) )

Sales Quantity YoY % =
DIVIDE ( [Sales Quantity] - [Sales Quantity PY], [Sales Quantity PY] )
```

นับจำนวน measure: แค่ 2 base × (YTD, PY, YoY%) = 6 ตัว — ยังไม่นับ MTD/QTD/FYTD  
ถ้ามี 20 base measure → ระเบิด → บท 11 แก้ด้วย Calculation Groups

> **Best practice:** รู้ classic TI ก่อน แล้วลดซ้ำด้วย calc group (`SELECTEDMEASURE`)  
> อ้าง: [Time intelligence functions](https://learn.microsoft.com/dax/time-intelligence-functions-dax)

---

## Lab 10 — Classic TI (โจทย์ + เฉลย)

### โจทย์

สำหรับทั้ง Sales Amount และ Sales Quantity สร้าง: YTD, PY, YoY %  
เพิ่ม Sales Amount FYTD (`"09/30"`)  
Matrix: แถวเดือน, ค่า = ชุด TI ของ Sales Amount

### เฉลย

คัดลอกบล็อก Time Intelligence ใน [`dax/measures.dax`](../../dax/measures.dax)

### เกณฑ์ผ่าน

- มี measures ชุด TI หลายตัวชัดเจน (เพื่อเห็น explosion)
- YoY % ใช้ `DIVIDE`

---

**ถัดไป:** [11 — Calculation Groups](11-calculation-groups.md) ← บทหลักที่แทนการสร้าง YTD คนละตัว
""",
    )

    w(
        "11-calculation-groups.md",
        """
# 11 — Calculation Groups

**เป้าหมาย:** ลด measure ซ้ำด้วย `SELECTEDMEASURE()` ตาม Microsoft Learn — ใช้แพทเทิร์น Time Intelligence ชุดเดียวกับทุก explicit measure  
**ข้อกำหนด:** จบบท 10; มี `[Sales Amount]` และ `[Sales Quantity]`

อ้างอิงหลัก: [Create calculation groups in Power BI](https://learn.microsoft.com/power-bi/transform-model/calculation-groups)

---

## ทำไมต้องมี (จากบท 10)

YTD / PY / YoY × ทุก base measure = **measure explosion**  
Calculation group = หนึ่งชุด calculation items ที่ **ห่อ** measure ที่ถูกเลือกบน visual

| แนวคิด | ความหมาย |
| --- | --- |
| Calculation group | ตารางพิเศษในโมเดล (เช่น `Time Intelligence`) |
| Calculation item | สูตร เช่น YTD, PY ที่ใช้ `SELECTEDMEASURE()` |
| `SELECTEDMEASURE()` | measure ที่อยู่ใน Values ของ visual ตอนนั้น |

**คนละงานกับ Field parameters (บท 12):** calc group **แปลง** measure เดิม; field parameter **สลับ** ว่าจะเอา field ไหนขึ้น visual

---

## Setup ใน Power BI Desktop

1. ไป **Model view**
2. โฮมริบบอน → **Calculation group**
3. เมื่อถูกถามให้เปิด **Discourage implicit measures** → **Yes**  
   (ถ้ายังไม่เปิดจากบท 01 — เปิดตอนนี้; calc item **ไม่ทำงาน** กับ implicit measure)
4. ชื่อตาราง: `Time Intelligence`  
   ชื่อคอลัมน์: `Time Calculation`
5. สร้าง items ตามด้านล่าง  
   หรือเปิด **TMDL view** แล้วใช้สคริปต์ [`dax/calculation-groups.tmdl`](../../dax/calculation-groups.tmdl)

---

## Calculation items ที่ต้องมี

ห่อด้วย `ISNUMERIC ( SELECTEDMEASURE () )` เพื่อไม่พังเมื่อ Values เป็น measure ข้อความ/title

### Current

```dax
IF (
    ISNUMERIC ( SELECTEDMEASURE () ),
    SELECTEDMEASURE (),
    SELECTEDMEASURE ()
)
```

### MTD / QTD / YTD

```dax
-- YTD (MTD/QTD แทน DATESMTD / DATESQTD)
IF (
    ISNUMERIC ( SELECTEDMEASURE () ),
    CALCULATE ( SELECTEDMEASURE (), DATESYTD ( DimDate[Date] ) ),
    SELECTEDMEASURE ()
)
```

### PY

```dax
IF (
    ISNUMERIC ( SELECTEDMEASURE () ),
    CALCULATE ( SELECTEDMEASURE (), SAMEPERIODLASTYEAR ( DimDate[Date] ) ),
    SELECTEDMEASURE ()
)
```

### YOY

```dax
IF (
    ISNUMERIC ( SELECTEDMEASURE () ),
    SELECTEDMEASURE ()
        - CALCULATE (
            SELECTEDMEASURE (),
            'Time Intelligence'[Time Calculation] = "PY"
        ),
    SELECTEDMEASURE ()
)
```

### YOY% + dynamic format string

สูตร:

```dax
IF (
    ISNUMERIC ( SELECTEDMEASURE () ),
    DIVIDE (
        CALCULATE (
            SELECTEDMEASURE (),
            'Time Intelligence'[Time Calculation] = "YOY"
        ),
        CALCULATE (
            SELECTEDMEASURE (),
            'Time Intelligence'[Time Calculation] = "PY"
        )
    ),
    SELECTEDMEASURE ()
)
```

ตั้ง **Format string** ของ item YOY% เป็น:

```text
#,##0.00%
```

(ใน Model view ที่ calculation item หรือผ่าน TMDL `formatStringDefinition`)

### FYTD

```dax
IF (
    ISNUMERIC ( SELECTEDMEASURE () ),
    TOTALYTD ( SELECTEDMEASURE (), DimDate[Date], "09/30" ),
    SELECTEDMEASURE ()
)
```

---

## ใช้ในรายงาน

**แบบ Matrix**

- Rows: `DimDate[MonthName]` (หรือ hierarchy)
- Columns: `Time Intelligence[Time Calculation]`
- Values: `[Sales Amount]`

สลับ Values เป็น `[Sales Quantity]` — **ห้าม** สร้าง `Sales Quantity YTD` ใหม่

**แบบ Slicer**

- Slicer บน `Time Calculation`
- Values ใส่หลาย measure พร้อมกัน

### ทดสอบใน DAX query view

```dax
EVALUATE
SUMMARIZECOLUMNS (
    DimDate[Year],
    'Time Intelligence'[Time Calculation],
    "Sales", [Sales Amount]
)
```

ตรวจว่าแต่ละ item คืนค่าสมเหตุสมผล

---

## Precedence และ selection (ย่อ)

- ถ้ามีหลาย calculation group ต้องตั้ง **precedence** (ตัวเลขสูงกว่าถูกใช้ก่อนตามเอกสาร AS/PBI)
- กำหนดพฤติกรรมเมื่อไม่เลือก / เลือกหลาย item ได้ผ่าน selection expressions (ดู Learn — คอร์สนี้ใช้ค่าเริ่มต้น + สอนใน Matrix columns)

> **Best practice:** Calculation groups สำหรับแพทเทิร์นซ้ำ; Field parameters สำหรับสลับ field  
> อ้าง: [Calculation groups](https://learn.microsoft.com/power-bi/transform-model/calculation-groups) · [SELECTEDMEASURE](https://learn.microsoft.com/dax/selectedmeasure-function-dax) · [Precedence](https://learn.microsoft.com/analysis-services/tabular-models/calculation-groups#precedence)

---

## แบบที่เลิกใช้เป็นคำตอบสุดท้าย (เคยอยู่ในสไลด์เก่า)

```dax
-- disconnected table + SWITCH — สอนเป็น anti-pattern สำหรับ production
Selected Measure =
SWITCH (
    SELECTEDVALUE ( 'Type'[TypeName] ),
    "Total Sales", [Sales Amount],
    "Total Sales YTD", [Sales Amount YTD],
    [Sales Quantity]
)
```

ใช้ฝึก disconnected table ได้ แต่ **ไม่ scale** และซ้ำกับ measure explosion

---

## Lab 11 — Calculation Groups (โจทย์ + เฉลย)

### โจทย์

1. เปิด Discourage implicit measures
2. สร้าง calc group `Time Intelligence` ตามบทนี้หรือ TMDL
3. Matrix: Month × Time Calculation × Sales Amount
4. เปลี่ยน Values เป็น Sales Quantity โดยไม่สร้าง Quantity YTD ใหม่
5. YOY% แสดงเป็นเปอร์เซ็นต์

### เฉลย

- UI: Model view → Calculation group หรือ apply [`dax/calculation-groups.tmdl`](../../dax/calculation-groups.tmdl)
- Dynamic format YOY%: `#,##0.00%`
- ถ้า item ไม่มีผล: ตรวจว่า Values เป็น explicit measure และ Date table ถูก Mark

### เกณฑ์ผ่าน

- Item เดียวกันใช้ได้ทั้ง `[Sales Amount]` และ `[Sales Quantity]`
- ไม่มี measure ชื่อแบบ `Sales Quantity YTD` แยกสำหรับ lab นี้ (ชุดบท 10 เก็บไว้เทียบก็ได้)

---

**ถัดไป:** [12 — Field Parameters](12-field-parameters.md)
""",
    )

    w(
        "12-field-parameters.md",
        """
# 12 — Field Parameters

**เป้าหมาย:** ให้ผู้ใช้สลับ Dimension / Measure บน visual ได้โดยไม่สร้างหน้า report ซ้ำ  
**ข้อกำหนด:** มีหลาย dimension และ base measures

อ้างอิง: [Let report readers use field parameters](https://learn.microsoft.com/power-bi/create-reports/power-bi-field-parameters)

---

## คนละงานกับ Calculation Groups

| | Calculation group | Field parameter |
| --- | --- | --- |
| คำถามที่ตอบ | “แปลง measure นี้อย่างไร (YTD, PY, …)” | “เอา field ไหนขึ้นแกน/ค่า” |
| กลไก | `SELECTEDMEASURE()` | ตารางพารามิเตอร์ที่ bind ฟิลด์ |
| ตัวอย่าง | Time Intelligence items | สลับ Category ↔ Country; Sales ↔ Profit |

ใช้คู่กันได้: สลับ measure ด้วย field parameter แล้วห่อด้วย calc group Time Intelligence

---

## สร้าง Field parameter

1. **Modeling → New parameter → Fields**
2. ตั้งชื่อ เช่น `Axis Dimension`
3. เพิ่มฟิลด์: `DimProduct[Category]`, `DimCustomer[Country]`, `DimCustomer[Segment]`
4. ติ๊ก **Add slicer to this page** (ถ้าต้องการ)
5. สร้างอีกตัว `Value Measure` จาก `[Sales Amount]`, `[Profit]`, `[Sales Quantity]`

บน visual:

- แกน X / Rows = ฟิลด์จาก `Axis Dimension` (ไม่ใช่คอลัมน์ดิบตรง ๆ)
- Values = ฟิลด์จาก `Value Measure`

ผู้ใช้เลือกที่ slicer ของพารามิเตอร์ → visual เปลี่ยนแกน/ค่า

---

## ข้อควรระวัง

- Field parameter สร้าง calculated table ในโมเดล — อย่าแก้คอลัมน์ภายในมั่วโดยไม่เข้าใจ binding
- ไม่ใช่ที่เก็บสูตร TI — สูตร TI อยู่ที่ measure หรือ calc group
- ต้องเปิด preview feature ในเวอร์ชันเก่าบางตัว (เวอร์ชันปัจจุบันส่วนใหญ่เปิดให้แล้ว)

> **Best practice:** แยก parameter มิติกับ measure จะควบคุม UX ง่ายกว่ากองรวมก้อนเดียว  
> อ้าง: [Field parameters](https://learn.microsoft.com/power-bi/create-reports/power-bi-field-parameters)

---

## Lab 12 — Field Parameters (โจทย์ + เฉลย)

### โจทย์

1. Field parameter มิติ: Category, Country, Segment
2. Field parameter measure: Sales Amount, Profit, Sales Quantity
3. Bar chart สลับได้ทั้งแกนและค่า
4. เขียน 1–2 ประโยคว่าต่างจาก calc group อย่างไร

### เฉลย

- Modeling → New parameter → Fields ตามขั้นตอนด้านบน
- คำตอบสั้น ๆ: calc group แปลงวิธีคำนวณของ measure ที่เลือก; field parameter สลับว่าจะแสดง field ไหนบน visual

### เกณฑ์ผ่าน

- Slicer พารามิเตอร์เปลี่ยนแกนและค่าของ chart ได้จริง
- อธิบายความต่างจาก calc group ได้

---

**ถัดไป:** [13 — What-if](13-what-if.md)
""",
    )

    w(
        "13-what-if.md",
        """
# 13 — What-if parameters

**เป้าหมาย:** สร้างพารามิเตอร์ตัวเลข (เช่นส่วนลดสมมติ) แล้วผูกกับ measure เพื่อจำลองสถานการณ์  
**ข้อกำหนด:** มี `[Sales Amount]`

อ้างอิง: [Use what-if parameters](https://learn.microsoft.com/power-bi/transform-model/desktop-what-if)

---

## สร้าง Numeric range parameter

1. **Modeling → New parameter → Numeric range**
2. ชื่อ: `Discount Scenario`
3. Data type: Decimal number
4. Min 0 · Max 0.30 · Increment 0.01  
   (หรือ 0–30 แล้วหาร 100 ใน measure — เลือกอย่างใดอย่างหนึ่งให้สม่ำเสมอ)
5. Default 0 · Add slicer to page

Power BI สร้างตารางพารามิเตอร์ + measure ค่าที่เลือก (ชื่อประมาณ `Discount Scenario Value`)

---

## Measure สถานการณ์

ถ้าพารามิเตอร์เป็นสัดส่วน 0–0.30:

```dax
Sales after Scenario Discount =
[Sales Amount] * ( 1 - 'Discount Scenario'[Discount Scenario Value] )
```

ถ้าพารามิเตอร์เป็นเปอร์เซ็นต์ 0–30:

```dax
Sales after Scenario Discount =
[Sales Amount] * ( 1 - DIVIDE ( 'Discount Scenario'[Discount Scenario Value], 100 ) )
```

จัด format เป็นเงินเช่นเดียวกับ Sales Amount

---

## รายงานแนะนำ

- Slicer ของพารามิเตอร์
- Clustered column / Line: `[Sales Amount]` vs `[Sales after Scenario Discount]` ตามเดือน
- Card แสดงส่วนต่าง:

```dax
Scenario Impact =
[Sales after Scenario Discount] - [Sales Amount]
```

> **Best practice:** What-if เป็นตาราง disconnected — ไม่สร้าง relationship ไป Fact  
> อ้าง: [What-if parameters](https://learn.microsoft.com/power-bi/transform-model/desktop-what-if)

---

## Lab 13 — What-if (โจทย์ + เฉลย)

### โจทย์

1. Parameter ส่วนลด 0–30% (หรือ 0–0.30)
2. Measure Sales after Scenario Discount
3. Column chart เทียบกับ Sales Amount — เลื่อน slicer แล้วยอดเปลี่ยน

### เฉลย

ใช้ขั้นตอนและสูตรด้านบน ปรับชื่อตาราง/measure ให้ตรงกับที่ Parameter wizard สร้าง  
ถ้าเลื่อนแล้วไม่เปลี่ยน: ตรวจว่า visual ใช้ measure สถานการณ์ ไม่ใช่คอลัมน์ดิบ และไม่ได้ hardcode ตัวเลขในสูตร

### เกณฑ์ผ่าน

- เลื่อน slicer แล้วยอด scenario เปลี่ยนตาม

---

**ถัดไป:** [14 — Visual Calculations](14-visual-calculations.md) (ภาคผนวก) หรือข้ามไป [15](15-vertipaq-and-performance.md)
""",
    )

    w(
        "14-visual-calculations.md",
        """
# 14 — Visual Calculations (ภาคผนวก)

**เป้าหมาย:** รู้ว่า visual calculation อยู่ชั้นรายงาน ไม่ใช่ semantic model — ใช้เมื่อต้องการ running sum ฯลฯ เฉพาะ visual  
**สถานะ:** Optional — ไม่บังคับสำหรับเกณฑ์จบคอร์สหลัก

อ้างอิง: [Using visual calculations](https://learn.microsoft.com/power-bi/transform-model/desktop-visual-calculations-introduction)

---

## อยู่คนละชั้นกับ Measure / Calc group

| ชั้น | เก็บสูตรที่ | ใช้ซ้ำข้ามหน้า |
| --- | --- | --- |
| Measure / Calc group | Semantic model | ได้ |
| Visual calculation | Visual นั้นเท่านั้น | ไม่ได้ (ต้องสร้างใหม่ต่อ visual) |

ฟังก์ชันตัวอย่างบน visual: `RUNNINGSUM`, `MOVINGAVERAGE`, `PREVIOUS`, `COLLAPSE` ฯลฯ

---

## ขั้นตอนสั้น ๆ

1. สร้าง Matrix: แถว = `DimDate[MonthName]`, ค่า = `[Sales Amount]`
2. เลือก visual → **New calculation**
3. เลือกเทมเพลต Running sum (หรือพิมพ์สูตร)
4. ผลอยู่คอลัมน์ใหม่บน visual — **ไม่โผล่ใน Model view**

เปรียบกับ `[Sales Amount YTD]` หรือ calc item YTD ในโมเดล:

- YTD ในโมเดลตอบ filter/slicer ทั้งรายงานและใช้ซ้ำได้
- Running sum บน visual ผูกกับแกนของ visual นั้น

> **Best practice:** สิ่งที่ใช้ซ้ำและเป็นนิยามธุรกิจ → ใส่โมเดล; สิ่งเฉพาะ ad-hoc บน visual เดียว → visual calculation ได้  
> อ้าง: ลิงก์ Learn ด้านบน

### ภาคผนวกสั้น — DAX UDFs

User-defined functions ใน DAX (GA ตาม roadmap Learn ~กลางปี 2026) ช่วย reuse logic เช่น format string — ยังไม่ใช่แกนคอร์สนี้; รู้ว่ามีเพื่อไม่สับสนกับ visual calc

---

## Lab 14 — Visual Calculations (โจทย์ + เฉลย) — optional

### โจทย์

1. Matrix Month × Sales Amount
2. เพิ่ม visual calculation Running sum บนแกนแถว
3. เปรียบกับ measure/calc item YTD — ระบุว่าคนละชั้น

### เฉลย

New calculation → Running sum บน visual  
คำตอบ: สูตรนี้อยู่ที่ visual ไม่ได้อยู่ใน Model view / ไม่แทนที่ calc group

### เกณฑ์ผ่าน

- ระบุได้ว่าสูตรอยู่ชั้นรายงาน

---

**ถัดไป:** [15 — VertiPaq checklist](15-vertipaq-and-performance.md)
""",
    )

    w(
        "15-vertipaq-and-performance.md",
        """
# 15 — VertiPaq checklist และเครื่องมือตรวจ

**เป้าหมาย:** ทบทวนนิสัยโมเดลทั้งคอร์สเป็น checklist ที่ตรวจกับไฟล์ `.pbix` ของตัวเองได้  
**ข้อกำหนด:** ทำ lab หลักบท 01–13 แล้ว

---

## Checklist โมเดล (ติ๊กทีละข้อ)

### Modeling

- [ ] Star schema — Fact กลาง, Dim รอบ; ไม่มี snowflake ที่ไม่จำเป็น
- [ ] Integer surrogate keys; ซ่อน `*Key` / FK จาก Report view
- [ ] ปิด Auto date/time
- [ ] Mark `DimDate[Date]` as Date Table; contiguous dates
- [ ] Relationship single-direction เป็นค่าเริ่มต้น; role-playing date = inactive + `USERELATIONSHIP`
- [ ] เงินเป็น Fixed Decimal; ยอด materialize → `SUM`
- [ ] Explicit measures + **Discourage implicit measures**
- [ ] ลบคอลัมน์ที่ไม่ใช้ (ลด cardinality / ขนาดโมเดล)

### DAX authoring

- [ ] คอลัมน์เป็น `Table[Column]`; measure เป็น `[Measure]`
- [ ] `DIVIDE` แทน `/` เมื่อหาร
- [ ] `CALCULATE` ใช้ Boolean filter; `KEEPFILTERS` เมื่อต้องการ intersection
- [ ] เลี่ยง `FILTER ( ทั้งตาราง )` เมื่อไม่จำเป็น
- [ ] `VAR` เมื่อใช้ผลซ้ำ
- [ ] Calculated column เฉพาะ Slicer/กลุ่ม; ไม่พึ่ง `TODAY()` ใน production

### Dynamics

- [ ] Time patterns ซ้ำ → **Calculation groups** ไม่ใช่ YTD คนละตัวต่อ measure
- [ ] สลับ field บน visual → **Field parameters**
- [ ] What-if เป็น disconnected numeric parameter

---

## เครื่องมือ

| เครื่องมือ | ใช้ทำ |
| --- | --- |
| **Performance Analyzer** | จับเวลา visual / DAX query บนหน้ารายงาน |
| **DAX query view** | ทดสอบ measure และ calc items แบบ `EVALUATE` |
| ชีต `_QA` ใน Excel + `pytest` | ยืนยันคุณภาพไฟล์ข้อมูลต้นทาง |

รันใน repo:

```bash
pip install -r requirements.txt
pytest -q
```

คาดหวัง: tests ผ่านครบ (ปัจจุบัน 21 passed)

> อ้าง: [Import data reduction](https://learn.microsoft.com/power-bi/guidance/import-modeling-data-reduction) · [Star schema](https://learn.microsoft.com/power-bi/guidance/star-schema) · [Best practices index](../best-practices/README.md)

---

## Lab 15 — Checklist (โจทย์ + เฉลย)

### โจทย์

1. เปิด `.pbix` ของคุณ ติ๊ก checklist ด้านบนทุกข้อที่เกี่ยวข้อง
2. รัน `pytest -q` ใน repo เพื่อยืนยัน Excel
3. (แนะนำ) Performance Analyzer บน Matrix ที่มี calc group — บันทึกว่า query กลับมา

### เฉลย

ผ่านเมื่อ:

- Checklist โมเดล/DAX/Dynamics ติ๊กครบตามที่สร้างจริง
- `pytest -q` ผ่าน
- มี calc group Time Intelligence ใช้งานกับอย่างน้อย `[Sales Amount]` และ `[Sales Quantity]`

### เกณฑ์ผ่าน

- ไม่มี lab ที่บังคับ snowflake หรือ hash key บน fact
- Discourage implicit measures เปิดอยู่
- จบคอร์สโดยไม่ต้องพึ่งสูตรจากสไลด์

---

**จบชุดบทเรียน** — ดัชนี: [README](README.md) · BP: [../best-practices/README.md](../best-practices/README.md)
""",
    )

    print("done")


if __name__ == "__main__":
    main()
