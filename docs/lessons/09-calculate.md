# 09 — CALCULATE

**เป้าหมาย:** เชี่ยวชาญฟังก์ชันที่สำคัญที่สุดในภาษา DAX: `CALCULATE`, เข้าใจกลไกการเปลี่ยน Filter Context, ใช้งานเงื่อนไขแบบ Boolean Filter ได้อย่างมีประสิทธิภาพ, ใช้ `KEEPFILTERS` เพื่อรักษาตัวกรองเดิม, และเปิดใช้งานสะพานสำรองด้วย `USERELATIONSHIP`  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 08 เรียบร้อยแล้ว และมีโมเดล Date Table ที่สมบูรณ์

---

## CALCULATE คืออะไร และทำหน้าที่อะไร?

ถ้าเปรียบเทียบภาษา DAX เป็นร่างกายมนุษย์... **`CALCULATE` คือหัวใจที่สูบฉีดเลือดไปเลี้ยงทุกส่วน!**  
สูตร DAX ระดับสูงเกือบทั้งหมดล้วนทำงานโดยมี `CALCULATE` อยู่เบื้องหลัง

```dax
CALCULATE ( <สูตรคำนวณ Expression>, <ตัวกรองที่ 1>, <ตัวกรองที่ 2>, ... )
```

**ขั้นตอนการทำงาน 3 สเต็ปของ CALCULATE:**
1. **ประเมินตัวกรองใหม่:** คำนวณเงื่อนไขของ Filter Arguments ที่ส่งเข้ามา
2. **แก้ไข Filter Context:** นำตัวกรองใหม่นี้ไปเพิ่ม, สลับ, หรือแทนที่ตัวกรองเดิมที่หน้ารายงาน
3. **คำนวณผลลัพธ์:** สั่งให้ `<Expression>` เริ่มคำนวณภายใต้สภาพแวดล้อม Filter Context ที่ถูกเปลี่ยนใหม่แล้ว

> 💡 **คิดภาพตามง่ายๆ (Mental Model): รีโมทคอนโทรลสั่งเปลี่ยนแว่นกรองสี**  
> จำภาพ "แว่นตากรองแสงสี" จากบทที่ 02 ได้ไหมครับ?  
> ปกติแล้ว ผู้ใช้รายงานจะเป็นคนสวมแว่นกรองสีผ่านการคลิก Slicer บนหน้าจอ  
> แต่ฟังก์ชัน `CALCULATE` เปรียบเสมือน **"รีโมทคอนโทรลมหัศจรรย์ในมือของโปรแกรมเมอร์"**  
> ที่สั่งการว่า: *"เดี๋ยวก่อนนะ! ไม่ว่าตอนนี้ผู้ใช้จะสวมแว่นสีอะไรอยู่ ขอให้ถอดแว่นนั้นออกชั่วคราว แล้วสวมแว่นสีที่ระบุไว้ในสูตรนี้แทน จากนั้นคำนวณตัวเลขออกมา พอคิดเสร็จค่อยคืนแว่นเดิมให้ผู้ใช้"*

---

## Boolean Filter: กฎการเขียนตัวกรองที่เร็วและถูกต้องที่สุด

วิธีส่งเงื่อนไขเข้าไปใน `CALCULATE` ที่ดีที่สุดและประมวลผลได้เร็วที่สุด คือการเขียนเป็นนิพจน์ตรรกะแบบ **Boolean Filter**:

```dax
Sales Amount EU =
CALCULATE (
    [Sales Amount],
    KEEPFILTERS ( DimCustomer[Country] IN { "Germany", "Italy", "France" } )
)
```

- การเขียน `DimCustomer[Country] IN { ... }` เป็นเงื่อนไขแบบ Boolean ที่เอนจิน VertiPaq สามารถแปลงเป็นคำสั่งบิตแมปและประมวลผลได้อย่างรวดเร็วในระดับเสี้ยววินาที
- **ทำไมต้องมี `KEEPFILTERS`?:** โดยปกติถ้าเราไม่ใส่ `KEEPFILTERS` ตัวกรองใหม่ในสูตรจะเข้าไป **แทนที่ (Overwrite)** ตัวกรองเดิมของคอลัมน์นั้นอย่างไร้ความปรานี แต่การครอบด้วย `KEEPFILTERS` จะเป็นการสั่งว่า **"ให้นำเงื่อนไขนี้ไปตัดกัน (Intersect / AND) กับตัวกรองที่ผู้ใช้เลือกไว้หน้ารายงานด้วย"** เช่น ถ้าผู้ใช้เลือกดูเฉพาะ Italy ตัวเลขจะแสดงเฉพาะ Italy ไม่ใช่เด้งกลับไปรวม France และ Germany ขึ้นมา

> **Best Practice:** เลี่ยงการใช้ `FILTER ( ตารางทั้งก้อน, เงื่อนไข )` ภายใน `CALCULATE` เมื่อสามารถเขียนด้วย Boolean Filter ได้ เพราะการใช้ `FILTER ( ตาราง )` จะบังคับให้เครื่องเดินสแกนทีละแถวอย่างไม่จำเป็น  
> *อ้างอิง:* [Microsoft Learn: Avoid FILTER as a filter argument](https://learn.microsoft.com/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument)

---

## `USERELATIONSHIP`: การเปิดใช้งานสะพานสำรองชั่วคราว

จากบทที่ 07 เราทราบว่าเส้นเชื่อมระหว่าง `FactSales` ไปยัง `DimDate` มีเส้น Active เพียงเส้นเดียวคือ `OrderDateKey` (วันที่สั่งซื้อ)  
ถ้าผู้บริหารตั้งคำถามว่า: **"ในเดือนพฤษภาคม เราจัดส่งสินค้าจริงออกไปเป็นมูลค่าเท่าไหร่ (ตาม Shipped Date)?"**

เราไม่ต้องสร้างตารางปฏิทินเพิ่มอีกใบให้เปลืองแรม แต่เราใช้ `CALCULATE` ควบคู่กับ `USERELATIONSHIP`:

```dax
Sales Amount (Shipped Date) =
CALCULATE (
    [Sales Amount],
    USERELATIONSHIP ( FactSales[ShippedDateKey], DimDate[DateKey] )
)

Profit (Shipped Date) =
CALCULATE (
    [Profit],
    USERELATIONSHIP ( FactSales[ShippedDateKey], DimDate[DateKey] )
)
```

> 💡 **คิดภาพตามง่ายๆ (Mental Model): การเปิดสวิตช์ไฟเขียวให้สะพานพับ**  
> คำสั่ง `USERELATIONSHIP` ทำหน้าที่เสมือนการ **"กดสวิตช์ไฟเขียวลดสะพานพับสำรองลงมา"** เป็นการสั่งว่า ในระหว่างที่กำลังคำนวณสูตรนี้ ขอให้สลับไปส่งแรงกรองผ่านเส้น `ShippedDateKey` แทนเส้นหลักชั่วคราว พอคิดเสร็จสะพานจะถูกยกเก็บกลับไปเป็นเหมือนเดิม

---

## การใช้ตัวแปร `VAR` เพื่อเพิ่มความเร็วและความสะอาดของโค้ด

```dax
Sales Amount EU Share =
VAR EuSales = [Sales Amount EU]
VAR AllSales = CALCULATE ( [Sales Amount], REMOVEFILTERS ( DimCustomer[Country] ) )
RETURN
    DIVIDE ( EuSales, AllSales )
```
การเก็บค่าใส่ `VAR` ช่วยให้คอมพิวเตอร์คำนวณตัวเลขนั้นเพียง **ครั้งเดียว** แล้วจำไว้ในหน่วยความจำชั่วคราว ไม่ต้องเหนื่อยคิดซ้ำเมื่อถูกเรียกใช้หลายครั้งในสูตรเดียวกัน

---

## Lab 09 — ฝึกใช้งาน CALCULATE ในสถานการณ์จริง (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. สร้าง Measure `[Sales Amount EU]` โดยใช้ `CALCULATE` ร่วมกับ `KEEPFILTERS` สำหรับประเทศ Germany, Italy, France
2. สร้าง Measure `[Sales Amount (Shipped Date)]` โดยใช้ `USERELATIONSHIP` เพื่อคำนวณยอดขายตามวันส่งของจริง
3. สร้าง Measure `[Profit (Shipped Date)]` เพื่อคำนวณกำไรตามวันส่งของจริง
4. นำ Measure ทั้งหมดไปวางในตาราง Matrix โดยนำ `DimDate[MonthName]` มาวางที่ Rows และเปรียบเทียบดูความแตกต่างระหว่างยอดตามวันสั่งซื้อ (`[Sales Amount]`) กับยอดตามวันส่งสินค้า (`[Sales Amount (Shipped Date)]`)

### เฉลยสูตร
```dax
Sales Amount EU =
CALCULATE (
    [Sales Amount],
    KEEPFILTERS ( DimCustomer[Country] IN { "Germany", "Italy", "France" } )
)

Sales Amount (Shipped Date) =
CALCULATE (
    [Sales Amount],
    USERELATIONSHIP ( FactSales[ShippedDateKey], DimDate[DateKey] )
)

Profit (Shipped Date) =
CALCULATE (
    [Profit],
    USERELATIONSHIP ( FactSales[ShippedDateKey], DimDate[DateKey] )
)
```

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- ในบางเดือน ตัวเลขยอดสั่งซื้อ (`[Sales Amount]`) กับยอดส่งของจริง (`[Sales Amount (Shipped Date)]`) จะต้องมีค่าไม่เท่ากัน ซึ่งสะท้อนความจริงทางธุรกิจว่า สินค้าที่สั่งซื้อในเดือนนี้อาจจะถูกจัดส่งในเดือนถัดไป

---

**บทเรียนถัดไป:** [16 — Filter modifiers และ Context transition](16-filter-modifiers-and-context-transition.md) *(แนะนำให้เรียนต่อจากบทที่ 09 ทันที)*
