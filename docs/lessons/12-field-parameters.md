# 12 — Field Parameters

**เป้าหมาย:** ให้ผู้ใช้สลับ Dimension / Measure บน visual ได้โดยไม่สร้างหน้า report ซ้ำ  
**ข้อกำหนด:** มีหลาย dimension และ base measures

อ้างอิง: [Let report readers use field parameters](https://learn.microsoft.com/power-bi/create-reports/power-bi-field-parameters)

---

## คนละงานกับ Calculation Groups

| | Calculation group | Field parameter |
| --- | --- | --- |
| คำถามที่ตอบ | “แปลง measure นี้อย่างไร (YTD, PY, …)” | “เอา field ไหนขึ้นแกน/ค่า” |
| กลไก | `SELECTEDMEASURE()` | ตารางพารามิเตอร์ที่ bind ฟิลด์ |
| ตัวอย่าง | Time Intelligence items | สลับ Category ↔ Country; Sales ↔ Profit |

ใช้คู่กันได้: สลับ measure ด้วย field parameter แล้วห่อด้วย calc group Time Intelligence

---

## สร้าง Field parameter

1. **Modeling → New parameter → Fields**
2. ตั้งชื่อ เช่น `Axis Dimension`
3. เพิ่มฟิลด์: `DimProduct[Category]`, `DimCustomer[Country]`, `DimCustomer[Segment]`
4. ติ๊ก **Add slicer to this page** (ถ้าต้องการ)
5. สร้างอีกตัว `Value Measure` จาก `[Sales Amount]`, `[Profit]`, `[Sales Quantity]`

บน visual:

- แกน X / Rows = ฟิลด์จาก `Axis Dimension` (ไม่ใช่คอลัมน์ดิบตรง ๆ)
- Values = ฟิลด์จาก `Value Measure`

ผู้ใช้เลือกที่ slicer ของพารามิเตอร์ → visual เปลี่ยนแกน/ค่า

---

## ข้อควรระวัง

- Field parameter สร้าง calculated table ในโมเดล — อย่าแก้คอลัมน์ภายในมั่วโดยไม่เข้าใจ binding
- ไม่ใช่ที่เก็บสูตร TI — สูตร TI อยู่ที่ measure หรือ calc group
- ต้องเปิด preview feature ในเวอร์ชันเก่าบางตัว (เวอร์ชันปัจจุบันส่วนใหญ่เปิดให้แล้ว)

> **Best practice:** แยก parameter มิติกับ measure จะควบคุม UX ง่ายกว่ากองรวมก้อนเดียว  
> อ้าง: [Field parameters](https://learn.microsoft.com/power-bi/create-reports/power-bi-field-parameters)

---

## Lab 12 — Field Parameters (โจทย์ + เฉลย)

### โจทย์

1. Field parameter มิติ: Category, Country, Segment
2. Field parameter measure: Sales Amount, Profit, Sales Quantity
3. Bar chart สลับได้ทั้งแกนและค่า
4. เขียน 1–2 ประโยคว่าต่างจาก calc group อย่างไร

### เฉลย

- Modeling → New parameter → Fields ตามขั้นตอนด้านบน
- คำตอบสั้น ๆ: calc group แปลงวิธีคำนวณของ measure ที่เลือก; field parameter สลับว่าจะแสดง field ไหนบน visual

### เกณฑ์ผ่าน

- Slicer พารามิเตอร์เปลี่ยนแกนและค่าของ chart ได้จริง
- อธิบายความต่างจาก calc group ได้

---

**ถัดไป:** [13 — What-if](13-what-if.md)
