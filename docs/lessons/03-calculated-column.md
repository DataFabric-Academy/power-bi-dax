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
