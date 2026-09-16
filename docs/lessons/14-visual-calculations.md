# 14 — Visual Calculations (ภาคผนวก)

**เป้าหมาย:** รู้ว่า visual calculation อยู่ชั้นรายงาน ไม่ใช่ semantic model — ใช้เมื่อต้องการ running sum ฯลฯ เฉพาะ visual  
**สถานะ:** Optional — ไม่บังคับสำหรับเกณฑ์จบคอร์สหลัก

อ้างอิง: [Using visual calculations](https://learn.microsoft.com/power-bi/transform-model/desktop-visual-calculations-introduction)

---

## อยู่คนละชั้นกับ Measure / Calc group

| ชั้น | เก็บสูตรที่ | ใช้ซ้ำข้ามหน้า |
| --- | --- | --- |
| Measure / Calc group | Semantic model | ได้ |
| Visual calculation | Visual นั้นเท่านั้น | ไม่ได้ (ต้องสร้างใหม่ต่อ visual) |

ฟังก์ชันตัวอย่างบน visual: `RUNNINGSUM`, `MOVINGAVERAGE`, `PREVIOUS`, `COLLAPSE` ฯลฯ

---

## ขั้นตอนสั้น ๆ

1. สร้าง Matrix: แถว = `DimDate[MonthName]`, ค่า = `[Sales Amount]`
2. เลือก visual → **New calculation**
3. เลือกเทมเพลต Running sum (หรือพิมพ์สูตร)
4. ผลอยู่คอลัมน์ใหม่บน visual — **ไม่โผล่ใน Model view**

เปรียบกับ `[Sales Amount YTD]` หรือ calc item YTD ในโมเดล:

- YTD ในโมเดลตอบ filter/slicer ทั้งรายงานและใช้ซ้ำได้
- Running sum บน visual ผูกกับแกนของ visual นั้น

> **Best practice:** สิ่งที่ใช้ซ้ำและเป็นนิยามธุรกิจ → ใส่โมเดล; สิ่งเฉพาะ ad-hoc บน visual เดียว → visual calculation ได้  
> อ้าง: ลิงก์ Learn ด้านบน

### ภาคผนวกสั้น — DAX UDFs

User-defined functions ใน DAX (GA ตาม roadmap Learn ~กลางปี 2026) ช่วย reuse logic เช่น format string — ยังไม่ใช่แกนคอร์สนี้; รู้ว่ามีเพื่อไม่สับสนกับ visual calc

---

## Lab 14 — Visual Calculations (โจทย์ + เฉลย) — optional

### โจทย์

1. Matrix Month × Sales Amount
2. เพิ่ม visual calculation Running sum บนแกนแถว
3. เปรียบกับ measure/calc item YTD — ระบุว่าคนละชั้น

### เฉลย

New calculation → Running sum บน visual  
คำตอบ: สูตรนี้อยู่ที่ visual ไม่ได้อยู่ใน Model view / ไม่แทนที่ calc group

### เกณฑ์ผ่าน

- ระบุได้ว่าสูตรอยู่ชั้นรายงาน

---

**ถัดไป:** [15 — VertiPaq checklist](15-vertipaq-and-performance.md)
