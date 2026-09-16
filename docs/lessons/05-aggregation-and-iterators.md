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
