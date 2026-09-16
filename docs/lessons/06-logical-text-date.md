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
