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
