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
