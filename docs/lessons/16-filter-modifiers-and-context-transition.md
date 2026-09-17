# 16 — Filter modifiers และ Context transition

**เป้าหมาย:** เข้าใจการทำงานของตัวดัดแปลงตัวกรอง (**Filter Modifiers**) เช่น `REMOVEFILTERS`, `ALL`, `ALLSELECTED`, และเข้าใจปรากฏการณ์สำคัญระดับหัวใจขั้นสูงของ DAX: **Context Transition** (การแปลง Row Context ให้กลายเป็น Filter Context)  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 09 (`CALCULATE`, `KEEPFILTERS`) มาสดๆ ร้อนๆ

---

## Filter Modifiers: เครื่องมือปรับแต่งแว่นกรองสี

นอกจากเงื่อนไขตัวกรองทั่วไปแล้ว ภายใน `CALCULATE` เราสามารถใส่ฟังก์ชันพิเศษที่ทำหน้าที่ **"ดัดแปลงหรือถอดถอน"** ตัวกรองเดิมที่กำลังทำงานอยู่ได้:

| ฟังก์ชัน Modifier | หน้าที่และการทำงาน |
| :--- | :--- |
| `REMOVEFILTERS` | **ถอดตัวกรองทิ้ง:** สั่งลบตัวกรองออกจากคอลัมน์หรือตารางที่ระบุอย่างสมบูรณ์ (เป็นคำสั่งสมัยใหม่ที่แนะนำให้ใช้แทน `ALL`) |
| `ALL` / `ALLEXCEPT` | ลบตัวกรอง (ฟังก์ชันรุ่นดั้งเดิม นิยมใช้ในสูตรยุคเก่า) |
| `ALLSELECTED` | **คืนค่ายอดรวมที่ปรากฏบนหน้าจอ (Visual Total):** ถอดตัวกรองประจำแถวในตารางออก แต่ยังคงตัวกรองของ Slicer ภายนอกไว้ |
| `KEEPFILTERS` | **รักษาตัวกรองเดิมไว้:** นำตัวกรองใหม่ไปตัดร่วม (Intersect) กับตัวกรองเดิม ไม่ลบล้างทิ้ง (เรียนในบทที่ 09) |

---

## การคำนวณสัดส่วน % ยอดขายด้วย `REMOVEFILTERS` vs `ALLSELECTED`

### 1. ใช้ `REMOVEFILTERS` เพื่อหาสัดส่วนต่อยอดรวมทั้งโลก
เมื่อต้องการรู้ว่ายอดขายของแถวนี้ คิดเป็นกี่เปอร์เซ็นต์ของยอดขายทั้งหมดโดยไม่สนใจการแบ่งกลุ่มในตาราง:

```dax
Sales Amount EU Share =
VAR EuSales = [Sales Amount EU]
VAR AllSales =
    CALCULATE ( [Sales Amount], REMOVEFILTERS ( DimCustomer[Country] ) )
RETURN
    DIVIDE ( EuSales, AllSales )
```
`REMOVEFILTERS(DimCustomer[Country])` จะทำหน้าที่ **"ถอดแว่นกรองประเทศออก"** ทำให้ตัวหาร (`AllSales`) ได้ยอดรวมของทุกประเทศเสมอ นำไปเป็นตัวหารหาค่า % สัดส่วนได้อย่างแม่นยำ

### 2. ใช้ `ALLSELECTED` เพื่อหาสัดส่วนต่อยอดรวมที่มองเห็นบน Visual
เมื่อผู้ใช้สร้างตาราง Matrix แล้วอยากให้ยอดรวมของทุกแถวในตารางนั้นบวกกันได้ **100% พอดี**:

```dax
Sales Amount % of Visual =
VAR Numerator = [Sales Amount]
VAR Denominator =
    CALCULATE ( [Sales Amount], ALLSELECTED ( DimProduct[Category] ) )
RETURN
    DIVIDE ( Numerator, Denominator )
```

> 💡 **คิดภาพตามง่ายๆ (Mental Model): ถอดแว่นใหญ่ vs ถอดแว่นเล็ก**  
> - `REMOVEFILTERS` เหมือนการ **"ถอดแว่นตาทุกอันออกจนหมด"** มองเห็นภาพรวมทั้งโลก ทั้งโมเดล เหมาะสำหรับการเทียบสัดส่วนต่อเป้าหมายภาพรวมของบริษัท  
> - `ALLSELECTED` เหมือนการ **"ถอดแว่นเฉพาะบรรทัดในตาราง แต่ยังคงสวมแว่นตัวกรองภายนอกที่ผู้ใช้คลิกเลือกไว้"** ทำให้หายอดรวมของสิ่งที่ผู้ใช้กำลังจ้องมองอยู่บนหน้าจอได้อย่างพอดีเป๊ะ

---

## ปรากฏการณ์ Context Transition (หัวใจขั้นสูงสุดของ DAX)

นี่คือหนึ่งในแนวคิดที่ทำให้ผู้เริ่มต้นเรียน DAX มักจะสับสนมากที่สุด แต่ถ้าเข้าใจแล้วจะเขียน DAX ได้อย่างทะลุปรุโปร่ง:

> 💡 **คิดภาพตามง่ายๆ (Mental Model): นิ้วชี้ที่หยิบโทรโข่งขึ้นมาประกาศ**  
> จำภาพ **Row Context (นิ้วชี้ทีละบรรทัด)** จากบทที่ 02 ได้ไหมครับ?  
> ปกติแล้ว นิ้วที่ชี้อยู่ที่แถวใดแถวหนึ่ง มันมองเห็นเฉพาะค่าในแถวของตัวเองเท่านั้น มันไม่ได้กรองตารางอื่น  
> แต่เมื่อไหร่ก็ตามที่ในแถวนั้นมีการเรียกใช้คำสั่ง **`CALCULATE`** (หรือมีการเรียกใช้ Measure)  
> สิ่งที่เกิดขึ้นคือ: **นิ้วชี้จะหยิบโทรโข่งขึ้นมาตะโกนทันที!**  
> มันจะนำค่าทุกคอลัมน์ของแถวที่นิ้วกำลังชี้อยู่ ส่งเสียงสั่งให้ทั้งโมเดล **"เปลี่ยนเป็น Filter Context ครอบคลุมทั้งตารางเดี๋ยวนี้!"**  
> ปรากฏการณ์นี้เรียกว่า **Context Transition (การเปลี่ยนผ่านจาก Row Context กลายเป็น Filter Context)**

### ตัวอย่างการประยุกต์ใช้ Context Transition ใน Calculated Column
ลองดูการสร้าง Calculated Column บนตาราง `DimCustomer` เพื่อแบ่งกลุ่มลูกค้าตามยอดซื้อสะสม:

```dax
Customer Revenue Band =
VAR CustomerSales =
    CALCULATE (
        [Sales Amount],
        ALLEXCEPT ( DimCustomer, DimCustomer[CustomerKey] )
    )
RETURN
    IF ( CustomerSales < 2500, "Low", "High" )
```

**สิ่งที่เกิดขึ้นเบื้องหลัง:**  
แม้สูตรนี้จะถูกเขียนใน Calculated Column (ซึ่งมี Row Context เดินทีละแถวของลูกค้า) แต่เพราะมีฟังก์ชัน `CALCULATE` ครอบอยู่ มันจึงทำ **Context Transition** แปลงแถวลูกค้านั้นให้กลายเป็นตัวกรอง ส่งแรงกรองข้ามไปที่ตาราง `FactSales` ทำให้ `[Sales Amount]` คำนวณยอดขายรวมของลูกค้ารายนั้นๆ ออกมาได้สำเร็จ!

---

## Lab 16 — ฝึกใช้งาน Modifiers และ Context Transition (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. สร้าง Measure `[Sales Amount EU Share]` โดยใช้ `REMOVEFILTERS`
2. สร้าง Measure `[Sales Amount % of Visual]` โดยใช้ `ALLSELECTED` บนคอลัมน์ `DimProduct[Category]`
3. นำ `DimProduct[Category]` ไปสร้าง Matrix ร่วมกับ `[Sales Amount]` และ `[Sales Amount % of Visual]` พร้อมวาง Slicer เลือกปี ตรวจสอบดูว่ายอดรวมในคอลัมน์ % รวมกันได้ 100% หรือไม่

### เฉลยสูตร
```dax
Sales Amount EU Share =
VAR EuSales = [Sales Amount EU]
VAR AllSales =
    CALCULATE ( [Sales Amount], REMOVEFILTERS ( DimCustomer[Country] ) )
RETURN
    DIVIDE ( EuSales, AllSales )

Sales Amount % of Visual =
VAR Numerator = [Sales Amount]
VAR Denominator =
    CALCULATE ( [Sales Amount], ALLSELECTED ( DimProduct[Category] ) )
RETURN
    DIVIDE ( Numerator, Denominator )
```

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- ในตาราง Matrix แถว Total ของ `[Sales Amount % of Visual]` จะต้องมีค่าเท่ากับ 1.0 (หรือ 100.0%) เสมอ ไม่ว่าจะคลิกเลือกตัวกรองปีใดๆ ก็ตาม

---

**บทเรียนถัดไป:** [10 — Time Intelligence](10-time-intelligence.md)
