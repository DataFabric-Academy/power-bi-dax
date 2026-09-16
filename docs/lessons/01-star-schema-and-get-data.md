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
