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
