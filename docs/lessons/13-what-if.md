# 13 — What-if parameters

**เป้าหมาย:** สร้างพารามิเตอร์ตัวเลข (เช่นส่วนลดสมมติ) แล้วผูกกับ measure เพื่อจำลองสถานการณ์  
**ข้อกำหนด:** มี `[Sales Amount]`

อ้างอิง: [Use what-if parameters](https://learn.microsoft.com/power-bi/transform-model/desktop-what-if)

---

## สร้าง Numeric range parameter

1. **Modeling → New parameter → Numeric range**
2. ชื่อ: `Discount Scenario`
3. Data type: Decimal number
4. Min 0 · Max 0.30 · Increment 0.01  
   (หรือ 0–30 แล้วหาร 100 ใน measure — เลือกอย่างใดอย่างหนึ่งให้สม่ำเสมอ)
5. Default 0 · Add slicer to page

Power BI สร้างตารางพารามิเตอร์ + measure ค่าที่เลือก (ชื่อประมาณ `Discount Scenario Value`)

---

## Measure สถานการณ์

ถ้าพารามิเตอร์เป็นสัดส่วน 0–0.30:

```dax
Sales after Scenario Discount =
[Sales Amount] * ( 1 - 'Discount Scenario'[Discount Scenario Value] )
```

ถ้าพารามิเตอร์เป็นเปอร์เซ็นต์ 0–30:

```dax
Sales after Scenario Discount =
[Sales Amount] * ( 1 - DIVIDE ( 'Discount Scenario'[Discount Scenario Value], 100 ) )
```

จัด format เป็นเงินเช่นเดียวกับ Sales Amount

---

## รายงานแนะนำ

- Slicer ของพารามิเตอร์
- Clustered column / Line: `[Sales Amount]` vs `[Sales after Scenario Discount]` ตามเดือน
- Card แสดงส่วนต่าง:

```dax
Scenario Impact =
[Sales after Scenario Discount] - [Sales Amount]
```

> **Best practice:** What-if เป็นตาราง disconnected — ไม่สร้าง relationship ไป Fact  
> อ้าง: [What-if parameters](https://learn.microsoft.com/power-bi/transform-model/desktop-what-if)

---

## Lab 13 — What-if (โจทย์ + เฉลย)

### โจทย์

1. Parameter ส่วนลด 0–30% (หรือ 0–0.30)
2. Measure Sales after Scenario Discount
3. Column chart เทียบกับ Sales Amount — เลื่อน slicer แล้วยอดเปลี่ยน

### เฉลย

ใช้ขั้นตอนและสูตรด้านบน ปรับชื่อตาราง/measure ให้ตรงกับที่ Parameter wizard สร้าง  
ถ้าเลื่อนแล้วไม่เปลี่ยน: ตรวจว่า visual ใช้ measure สถานการณ์ ไม่ใช่คอลัมน์ดิบ และไม่ได้ hardcode ตัวเลขในสูตร

### เกณฑ์ผ่าน

- เลื่อน slicer แล้วยอด scenario เปลี่ยนตาม

---

**ถัดไป:** [14 — Visual Calculations](14-visual-calculations.md) (ภาคผนวก) หรือข้ามไป [15](15-vertipaq-and-performance.md)
