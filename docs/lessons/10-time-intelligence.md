# 10 — Time Intelligence (classic measures)

**เป้าหมาย:** สร้าง YTD / PY / YoY ด้วย measure แยกต่อ base measure — **ตั้งใจให้เห็น measure explosion** ก่อนย้ายไป Calculation Groups  
**ข้อกำหนด:** Mark as Date Table แล้ว; มี `[Sales Amount]`, `[Sales Quantity]`

---

## ฟังก์ชันที่ใช้บ่อย

| ฟังก์ชัน | ใช้ทำ |
| --- | --- |
| `DATESYTD` / `TOTALYTD` | ปีถึงวันที่ |
| `DATESMTD` / `DATESQTD` | เดือน / ไตรมาสถึงวันที่ |
| `SAMEPERIODLASTYEAR` | ช่วงเทียบปีก่อน |
| `DATEADD` | เลื่อนช่วงเป็นช่วง |
| `DATESINPERIOD` | rolling window |

ทุกตัวต้องอ้างคอลัมน์วันที่ของ Date table ที่ Mark แล้ว: `DimDate[Date]`

> หมายเหตุ: Calendar-based time intelligence (preview) มีบน Learn — คอร์สนี้ใช้ classic + calc group ในบท 11

---

## ชุด Sales Amount

```dax
Sales Amount YTD = TOTALYTD ( [Sales Amount], DimDate[Date] )

Sales Amount PY =
CALCULATE ( [Sales Amount], SAMEPERIODLASTYEAR ( DimDate[Date] ) )

Sales Amount YoY % =
DIVIDE ( [Sales Amount] - [Sales Amount PY], [Sales Amount PY] )

Sales Amount FYTD =
TOTALYTD ( [Sales Amount], DimDate[Date], "09/30" )

Sales Amount Rolling 60d =
CALCULATE (
    [Sales Amount],
    DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ), -60, DAY )
)
```

`"09/30"` = ปีงบที่สิ้นสุด 30 ก.ย. (สอดคล้อง Fiscal ที่เริ่ม 1 ต.ค. ใน DimDate)

---

## ชุด Sales Quantity (ซ้ำแพทเทิร์น)

```dax
Sales Quantity YTD = TOTALYTD ( [Sales Quantity], DimDate[Date] )

Sales Quantity PY =
CALCULATE ( [Sales Quantity], SAMEPERIODLASTYEAR ( DimDate[Date] ) )

Sales Quantity YoY % =
DIVIDE ( [Sales Quantity] - [Sales Quantity PY], [Sales Quantity PY] )
```

นับจำนวน measure: แค่ 2 base × (YTD, PY, YoY%) = 6 ตัว — ยังไม่นับ MTD/QTD/FYTD  
ถ้ามี 20 base measure → ระเบิด → บท 11 แก้ด้วย Calculation Groups

> **Best practice:** รู้ classic TI ก่อน แล้วลดซ้ำด้วย calc group (`SELECTEDMEASURE`)  
> อ้าง: [Time intelligence functions](https://learn.microsoft.com/dax/time-intelligence-functions-dax)

---

## Lab 10 — Classic TI (โจทย์ + เฉลย)

### โจทย์

สำหรับทั้ง Sales Amount และ Sales Quantity สร้าง: YTD, PY, YoY %  
เพิ่ม Sales Amount FYTD (`"09/30"`)  
Matrix: แถวเดือน, ค่า = ชุด TI ของ Sales Amount

### เฉลย

คัดลอกบล็อก Time Intelligence ใน [`dax/measures.dax`](../../dax/measures.dax)

### เกณฑ์ผ่าน

- มี measures ชุด TI หลายตัวชัดเจน (เพื่อเห็น explosion)
- YoY % ใช้ `DIVIDE`

---

**ถัดไป:** [11 — Calculation Groups](11-calculation-groups.md) ← บทหลักที่แทนการสร้าง YTD คนละตัว
