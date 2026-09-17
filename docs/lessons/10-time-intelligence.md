# 10 — Time Intelligence (Classic Measures)

**เป้าหมาย:** ใช้งานฟังก์ชันการวิเคราะห์วันเวลาแบบดั้งเดิม (Classic Time Intelligence) เช่น `TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATEADD`, และตระหนักถึงปัญหา "สูตรระเบิดท่วมโมเดล" (Measure Explosion Problem) ซึ่งเป็นที่มาของการเรียนรู้ Calculation Groups ในบทถัดไป  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 08 (Date Table) และบทเรียนที่ 09/16 (CALCULATE) เรียบร้อยแล้ว

---

## Time Intelligence คืออะไร?

ในการดำเนินธุรกิจ ผู้บริหารไม่ได้สนใจแค่ว่า "วันนี้ขายได้เท่าไหร่" แต่ต้องการเห็น **ทิศทางและแนวโน้มเมื่อเปรียบเทียบกับอดีต**  
ภาษา DAX มีกลุ่มฟังก์ชันเฉพาะทางที่เรียกว่า **Time Intelligence Functions** ซึ่งออกแบบมาเพื่ออำนวยความสะดวกในการเลื่อนขยับหรือสะสมช่วงเวลาใน Filter Context โดยอัตโนมัติ

---

## ชุดสูตร Classic Time Intelligence พื้นฐาน

### 1. ยอดสะสมตั้งแต่ต้นปีจนถึงปัจจุบัน (Year-To-Date: YTD)
คำนวณผลรวมยอดขายสะสมตั้งแต่วันที่ 1 มกราคมของปีนั้นๆ วิ่งไล่มาจนถึงวันที่เลือกปัจจุบัน:
```dax
Sales Amount YTD = TOTALYTD ( [Sales Amount], DimDate[Date] )
```

### 2. ยอดขายในช่วงเวลาเดียวกันของปีก่อนหน้า (Prior Year: PY)
ย้อน Filter Context กลับไปในอดีต 1 ปีเต็ม ณ ช่วงวันเดียวกัน:
```dax
Sales Amount PY =
CALCULATE (
    [Sales Amount],
    SAMEPERIODLASTYEAR ( DimDate[Date] )
)
```

### 3. ผลต่างเมื่อเทียบกับปีก่อน (Year-over-Year Growth: YoY)
หามูลค่าการเติบโตเมื่อเทียบกับปีที่แล้ว:
```dax
Sales Amount YoY = [Sales Amount] - [Sales Amount PY]
```

### 4. อัตราการเติบโตคิดเป็นเปอร์เซ็นต์ (YoY %)
คิดเป็นเปอร์เซ็นต์การเติบโตอย่างปลอดภัยด้วยฟังก์ชัน `DIVIDE`:
```dax
Sales Amount YoY % = DIVIDE ( [Sales Amount YoY], [Sales Amount PY] )
```

---

## วิกฤตการณ์ "Measure Explosion" (ปัญหาป่าสูตรดงดิบในโมเดล)

ลองจินตนาการดูว่า ในระบบงานจริงขององค์กร เราไม่ได้มียอดขาย (`[Sales Amount]`) เพียงตัวเดียว แต่เรามีตัวชี้วัดธุรกิจ (Base Measures) หลายตัว เช่น:
1. `[Sales Amount]` (ยอดขาย)
2. `[Total Cost]` (ต้นทุน)
3. `[Profit]` (กำไร)
4. `[Orders]` (จำนวนออเดอร์)
5. `[Quantity]` (ปริมาณชิ้นสินค้า)

หากผู้บริหารต้องการดูมิติเวลาสำหรับทุกตัววัด:
- ค่าปัจจุบัน (Current Year)
- ยอดสะสม (YTD)
- ปีก่อนหน้า (PY)
- ส่วนต่าง (YoY)
- เปอร์เซ็นต์เติบโต (YoY %)

**สิ่งที่เกิดขึ้นคือ:**  
คุณจะต้องเขียนสูตร DAX ทั้งหมด **5 × 5 = 25 สูตร!**  
ถ้าองค์กรมี 20 ตัวชี้วัด คุณจะต้องนั่งเขียนสูตรซ้ำๆ เดิมๆ ถึง **100 สูตร!**  
ทำให้รายการ Measure ในโปรแกรมยาวเป็นกิโลกรัม ดูแลรักษายาก เสี่ยงต่อการพิมพ์ผิด และเปลืองเวลาทำงานอย่างมหาศาล

> 💡 **คิดภาพตามง่ายๆ (Mental Model): ปัญหาแม่พิมพ์ขนมปังแบบแยกชิ้น**  
> ปัญหานี้เปรียบเหมือนร้านเบเกอรี่ที่อยากทำขนมปังปั๊มตรา "ลด 50%"  
> ถ้าใช้วิธีดั้งเดิม ร้านจะต้องไปสั่งหล่อพิมพ์เหล็กรูป "ครัวซองต์ลด 50%", "โดนัทลด 50%", "เค้กลด 50%" แยกทีละชิ้นจนเต็มร้าน  
> ทั้งที่ในความเป็นจริง เราควรมี **"ตรายางปั๊มลด 50% เพียงอันเดียว"** แล้วเอาไปปั๊มลงบนขนมปังชิ้นไหนก็ได้!  
> เครื่องมือตรายางสารพัดประโยชน์นี้ใน Power BI มีชื่อเรียกว่า **Calculation Groups** ซึ่งเราจะได้เรียนรู้ในบทที่ 11 ทันที!

---

## Lab 10 — สร้างชุดสูตร Classic Time Intelligence (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. สร้างชุด Measure สำหรับวิเคราะห์ยอดขายตามกาลเวลา:  
   - `[Sales Amount YTD]`  
   - `[Sales Amount PY]`  
   - `[Sales Amount YoY]`  
   - `[Sales Amount YoY %]` (กำหนดรูปแบบเป็น `0.0%`)
2. สร้างตาราง Matrix:  
   - นำ `DimDate[Year]` และ `DimDate[MonthName]` มาวางที่ Rows  
   - นำ Measure ทั้ง 4 ตัวมาวางที่ Values เพื่อสังเกตการคำนวณตัวเลขสะสมและการเทียบปีก่อนหน้า

### เฉลยสูตร
```dax
Sales Amount YTD = TOTALYTD ( [Sales Amount], DimDate[Date] )

Sales Amount PY =
CALCULATE (
    [Sales Amount],
    SAMEPERIODLASTYEAR ( DimDate[Date] )
)

Sales Amount YoY = [Sales Amount] - [Sales Amount PY]

Sales Amount YoY % = DIVIDE ( [Sales Amount YoY], [Sales Amount PY] )
```

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- ในเดือนมกราคม ยอด `[Sales Amount YTD]` จะต้องเท่ากับ `[Sales Amount]` ของเดือนนั้นพอดี
- เมื่อขึ้นเดือนกุมภาพันธ์ ยอด `[Sales Amount YTD]` จะต้องนำยอดของเดือนมกราคมมารวมสะสมทบยอดขึ้นไปเรื่อยๆ จนถึงสิ้นปี

---

**บทเรียนถัดไป:** [11 — Calculation Groups](11-calculation-groups.md)
