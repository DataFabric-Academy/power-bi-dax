# 11 — Calculation Groups

**เป้าหมาย:** กำจัดปัญหา Measure Explosion จากบทที่ 10 โดยสิ้นเชิงด้วยการสร้าง **Calculation Groups**, เข้าใจการทำงานของฟังก์ชันอเนกประสงค์ `SELECTEDMEASURE()`, และกำหนดรูปแบบการแสดงผลแบบไดนามิกด้วย Format String Expressions  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 10 เรียบร้อยแล้ว และใน Model view ได้เปิดตัวเลือก **Discourage implicit measures** เป็น On แล้ว

---

## Calculation Groups คืออะไร?

Calculation Groups คือฟีเจอร์ระดับสูงของ Semantic Model ที่ช่วยเปลี่ยนวิธีคิดและวิธีเขียน DAX ของเราไปตลอดกาล  
มันทำหน้าที่เป็น **"แม่พิมพ์ตรรกะอเนกประสงค์"** ที่สามารถนำไปสวมทับ Measure ใดๆ ในโมเดลก็ได้!

> 💡 **คิดภาพตามง่ายๆ (Mental Model): แผ่นฟิลเตอร์สีสวมทับหน้าเลนส์กล้อง**  
> ลองนึกภาพตากล้องที่มีเลนส์กล้องหลายตัว: เลนส์ยอดขาย, เลนส์ต้นทุน, เลนส์กำไร  
> แทนที่ตากล้องจะต้องไปสั่งทำ "เลนส์ยอดขายแบบติดฟิลเตอร์ขาวดำ", "เลนส์ต้นทุนแบบติดฟิลเตอร์ขาวดำ" แยกเป็นชิ้นๆ  
> ตากล้องคนนี้แค่ซื้อ **"แผ่นฟิลเตอร์ขาวดำ" (Calculation Item)** มาแผ่นเดียว  
> เมื่อต้องการดูภาพขาวดำ ก็นำแผ่นฟิลเตอร์นี้ไป **สวมทับหน้าเลนส์ตัวไหนก็ได้ทันที!**  
> ฟังก์ชัน **`SELECTEDMEASURE()`** ก็คือคำสั่งที่แปลว่า *"ไม่ว่าตอนนี้ผู้ใช้จะหยิบเลนส์ Measure อะไรมาส่อง ให้เอาสูตรคำนวณนี้ไปครอบทับเลนส์นั้นทันที!"*

---

## โครงสร้างของ Time Intelligence Calculation Group

เราสร้าง Calculation Group ขึ้นมา 1 กลุ่ม (เช่น ตั้งชื่อว่า `Time Intelligence`) ภายในจะมีตารางเสมือนที่มีคอลัมน์ชื่อ `CalculationItem` ซึ่งประกอบด้วยรายการทางเลือกดังนี้:

| Calculation Item (แผ่นฟิลเตอร์) | นิพจน์ DAX Expression (สิ่งที่ทำกับ Measure) | Format String Expression (รูปแบบตัวเลข) |
| :--- | :--- | :--- |
| **Current** | `SELECTEDMEASURE()` | `SELECTEDMEASUREFORMATSTRING()` |
| **YTD** | `TOTALYTD ( SELECTEDMEASURE(), DimDate[Date] )` | `SELECTEDMEASUREFORMATSTRING()` |
| **PY** | `CALCULATE ( SELECTEDMEASURE(), SAMEPERIODLASTYEAR ( DimDate[Date] ) )` | `SELECTEDMEASUREFORMATSTRING()` |
| **YoY** | `SELECTEDMEASURE() - CALCULATE ( SELECTEDMEASURE(), SAMEPERIODLASTYEAR ( DimDate[Date] ) )` | `SELECTEDMEASUREFORMATSTRING()` |
| **YoY %** | `DIVIDE ( ...คำนวณส่วนต่าง..., ...คำนวณ PY... )` | `"0.0%"` *(บังคับแปลงเป็นเปอร์เซ็นต์อัตโนมัติ)* |

---

## ข้อกำหนดทางสถาปัตยกรรม: ทำไมต้องเปิด Discourage Implicit Measures?

ในการใช้งาน Calculation Groups ระบบ Power BI มีข้อกำหนดเข้มงวดว่า **โมเดลนั้นต้องเปิดโหมด "Discourage implicit measures" (ไม่อนุญาตให้ใช้ Implicit Measure)**  
เพราะถ้าผู้ใช้ลากคอลัมน์ตัวเลขดิบไปวางบน Visual แล้วให้โปรแกรมเดาใจหาผลรวม แผ่นฟิลเตอร์ของ Calculation Group จะไม่สามารถทำงานได้อย่างถูกต้องสมบูรณ์ มันต้องการทำงานร่วมกับ **Explicit Measure ที่ประกาศสูตรไว้อย่างเป็นทางการเท่านั้น**

---

## ตัวอย่างโค้ดในรูปแบบ TMDL (Tabular Model Definition Language)

ใน Power BI ยุคปัจจุบันและ Fabric เราสามารถประกาศ Calculation Group ผ่านไฟล์สคริปต์ TMDL ได้ดังนี้ (ดูไฟล์ต้นฉบับเต็มได้ที่ [`dax/calculation-groups.tmdl`](../../dax/calculation-groups.tmdl)):

```tmdl
table 'Time Intelligence'
	calculationGroup
		precedence: 0

		calculationItem Current = SELECTEDMEASURE()

		calculationItem YTD = TOTALYTD ( SELECTEDMEASURE(), DimDate[Date] )

		calculationItem PY =
				CALCULATE (
				    SELECTEDMEASURE(),
				    SAMEPERIODLASTYEAR ( DimDate[Date] )
				)

		calculationItem YoY =
				VAR PriorYear =
				    CALCULATE (
				        SELECTEDMEASURE(),
				        SAMEPERIODLASTYEAR ( DimDate[Date] )
				    )
				RETURN
				    SELECTEDMEASURE() - PriorYear

		calculationItem 'YoY %' =
				VAR CurrentValue = SELECTEDMEASURE()
				VAR PriorYear =
				    CALCULATE (
				        SELECTEDMEASURE(),
				        SAMEPERIODLASTYEAR ( DimDate[Date] )
				    )
				VAR Diff = CurrentValue - PriorYear
				RETURN
				    DIVIDE ( Diff, PriorYear )
			formatStringDefinition = "0.0%"
```

---

## Lab 11 — สร้างและทดสอบ Calculation Group (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. ในหน้า Model view ของ Power BI Desktop คลิกสร้าง **Calculation group** ใหม่ (ตั้งชื่อกลุ่มว่า `Time Intelligence` และตั้งชื่อคอลัมน์ว่า `Time Calculation`)
2. สร้าง Calculation Items ให้ครบ 5 ตัว: `Current`, `YTD`, `PY`, `YoY`, และ `YoY %` ตามนิพจน์ด้านบน
3. ที่ไอเทม `YoY %` ให้คลิกตั้งค่า **Format string expression** ระบุเป็น `"0.0%"`
4. สร้างตาราง Matrix:
   - นำ `DimDate[MonthName]` มาวางที่ Rows
   - นำ `Time Calculation` (จาก Calculation Group) มาวางที่ Columns
   - นำ Measure `[Sales Amount]` ตัวเดียวไปวางที่ Values
5. จากนั้นลองลาก Measure `[Profit]` และ `[Orders]` สลับลงไปวางแทนที่ แล้วสังเกตความมหัศจรรย์ของผลลัพธ์!

### การสังเกตและผลลัพธ์
- โดยที่คุณไม่ต้องเขียนสูตร `[Profit YTD]` หรือ `[Orders PY]` เพิ่มแม้แต่สูตรเดียว ตาราง Matrix จะสามารถแตกผลลัพธ์ YTD, PY, YoY และ YoY % ของทั้งกำไรและจำนวนออเดอร์ออกมาได้อย่างถูกต้องสมบูรณ์ทันที
- ช่องที่เป็น `YoY %` จะแสดงเครื่องหมาย `%` อัตโนมัติ ในขณะที่ช่องอื่นๆ ยังคงแสดงเป็นตัวเลขจำนวนเงินตามฟอร์แมตเดิมของตัวมันเอง

---

**บทเรียนถัดไป:** [12 — Field Parameters](12-field-parameters.md)
