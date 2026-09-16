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
