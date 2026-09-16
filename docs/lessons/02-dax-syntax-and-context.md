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
