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
