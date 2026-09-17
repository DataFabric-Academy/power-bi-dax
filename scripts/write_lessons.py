# -*- coding: utf-8 -*-
"""Generate standalone lesson markdown (lab = exercise + solution combined).

Enhanced with intuitive mental models and real-world analogies suitable for
learners at a high-school comprehension level, while strictly preserving all
professional technical keyphrases and best practices for Data Analysts,
Business Analysts, and BI Developers.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "docs" / "lessons"


def w(name: str, body: str) -> None:
    path = LESSONS / name
    path.write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def get_readme() -> str:
    return """
# บทเรียน (แหล่งความจริงของคอร์ส — Source of Truth)

เอกสารชุดนี้ออกแบบมาเพื่อสร้างความเข้าใจใน **Power BI Semantic Model & DAX** ตั้งแต่พื้นฐานไปจนถึงระดับสถาปัตยกรรมขั้นสูง โดยใช้ชุดข้อมูลจำลองมาตรฐาน **Northwind DW**

> 💡 **แนวคิดในการเรียนรู้ (Mental Model):**  
> การเรียน DAX ไม่ใช่แค่การจำสูตรคณิตศาสตร์ แต่คือการทำความเข้าใจ **"กลไกการคิดของระบบ" (Evaluation Context)** ถ้าเราเข้าใจว่าคอมพิวเตอร์กำลัง "สวมแว่นกรองข้อมูลแบบไหน" (Filter Context) หรือ "กำลังเอานิ้วชี้อยู่ที่บรรทัดใด" (Row Context) เราจะสามารถเขียนสูตรที่ทำงานได้อย่างถูกต้อง รวดเร็ว และตอบโจทย์ธุรกิจได้อย่างมั่นใจ

เอกสารชุดนี้สอนครบจบในตัว — **ไม่ต้องพึ่งสไลด์** สำหรับสูตรหรือขั้นตอนปฏิบัติ  
สไลด์ (ถ้ามี) ใช้เพื่อดูภาพรวมและโครงสร้างการเล่าเรื่องเท่านั้น

| # | บทเรียน | แนวคิดสำคัญ (Keyphrases & Concepts) | Lab รวมเฉลย |
| ---: | :--- | :--- | :---: |
| 01 | [Star schema และ Get Data](01-star-schema-and-get-data.md) | Star Schema, Fact vs Dim, Grain, Surrogate Key, Explicit Measure | ท้ายบท |
| 02 | [DAX syntax และ Context](02-dax-syntax-and-context.md) | Filter Context, Row Context, Table[Column] vs [Measure] | ท้ายบท |
| 03 | [Calculated Column](03-calculated-column.md) | Row Context, VertiPaq Storage, RAM Footprint, Sort by Column | ท้ายบท |
| 04 | [Measures](04-measures.md) | Dynamic Calculation, Query Time, DIVIDE (Safe Division) | ท้ายบท |
| 05 | [Aggregation และ Iterators](05-aggregation-and-iterators.md) | Aggregators (SUM), Iterators (SUMX), Storage vs Formula Engine | ท้ายบท |
| 06 | [Logical / Text / Date](06-logical-text-date.md) | IF, SWITCH ( TRUE () ), FORMAT, BLANK Handling | ท้ายบท |
| 07 | [RELATED และ Relationships](07-related-and-relationships.md) | Many-to-One, Cross-Filter Direction, Lookup via Relationship | ท้ายบท |
| 08 | [Date Table](08-date-table.md) | Contiguous Dates, Mark as Date Table, Fiscal Calendar | ท้ายบท |
| 09 | [CALCULATE](09-calculate.md) | Context Modification, Boolean Filter, KEEPFILTERS, USERELATIONSHIP | ท้ายบท |
| 10 | [Time Intelligence](10-time-intelligence.md) | TOTALYTD, SAMEPERIODLASTYEAR, Measure Explosion Problem | ท้ายบท |
| 11 | [Calculation Groups](11-calculation-groups.md) | Calculation Items, SELECTEDMEASURE(), Format Strings | ท้ายบท |
| 12 | [Field Parameters](12-field-parameters.md) | Dynamic Dimensions/Measures, Reporting UX, NAMEOF() | ท้ายบท |
| 13 | [What-if](13-what-if.md) | GENERATESERIES, Disconnected Table, Scenario Simulation | ท้ายบท |
| 14 | [Visual Calculations](14-visual-calculations.md) | Visual Matrix Axis, RUNNINGSUM, EXPAND / COLLAPSE | ท้ายบท |
| 15 | [VertiPaq checklist](15-vertipaq-and-performance.md) | Columnar Engine, Dictionary Encoding, Run-Length Encoding, Cardinality | ท้ายบท |
| 16 | [Filter modifiers และ Context transition](16-filter-modifiers-and-context-transition.md) | REMOVEFILTERS, ALLSELECTED, Context Transition in Row Context | ท้ายบท |

- **แคตตาล็อกสูตรทางการ:** [`dax/measures.dax`](../../dax/measures.dax) · [`dax/calculation-groups.tmdl`](../../dax/calculation-groups.tmdl)  
- **ดัชนีแนวทางปฏิบัติที่ดีที่สุด (Best Practices):** [../best-practices/README.md](../best-practices/README.md)
"""


def get_lesson_01() -> str:
    return """
# 01 — Star schema และ Get Data

**เป้าหมาย:** สร้าง Semantic Model ตั้งต้นที่ได้มาตรฐานระดับองค์กร — ทำความเข้าใจโครงสร้างแบบ Star Schema, คีย์ตัวเลข (Integer Surrogate Keys), ตารางปฏิทินวันที่ (Date Table), และการสร้าง Explicit Measure ตัวแรก  
**ไฟล์ข้อมูล:** [`data/Northwind_DW_DimFact.xlsx`](../../data/Northwind_DW_DimFact.xlsx)  
**ผลลัพธ์ตอนจบบท:** มีโมเดลความสัมพันธ์ 6 ตารางที่ถูกต้อง + Relationships + `[Sales Amount]` พร้อม Slicer ปีกรองยอดขายได้สมบูรณ์

---

## ทำไมต้องเริ่มที่โมเดล ไม่ใช่เริ่มที่การเขียนสูตร?

ในการทำงานจริงของ Data Analyst และ BI Developer ข้อผิดพลาดอันดับหนึ่งไม่ได้เกิดจากการเขียนสูตร DAX ไม่เป็น แต่เกิดจาก **"การจัดวางโครงสร้างตารางข้อมูลผิดตั้งแต่ต้น"**

DAX ทำงานโดยอาศัยกลไกการกรองข้อมูลที่เรียกว่า **Filter Context** ซึ่งส่งผ่านตามเส้นเชื่อมโยงความสัมพันธ์ (**Relationship**)  
ถ้าเราเอาข้อมูลทุกอย่างมารวมเป็นตารางแบนๆ ผืนเดียว (Flat Table) หรือต่อตารางซ้อนกันหลายชั้นเป็นเกล็ดหิมะ (Snowflake Schema) หรือใช้ข้อความยาวๆ เป็นตัวเชื่อมโยงตาราง แทนที่จะเป็นตัวเลข — โมเดลจะทำงานช้า กินแรมมหาศาล และสูตรวิเคราะห์วันเวลา (Time Intelligence) จะคำนวณผิดพลาดทันที

หลักสูตรนี้จึงใช้ **Northwind Data Warehouse (Star Schema)** ที่ออกแบบมาถูกต้องตามมาตรฐานสากลเป็นโมเดลหลักตลอดทั้งคอร์ส

> 💡 **คิดภาพตามง่ายๆ (Mental Model): Star Schema คือระบบสุริยะจักรวาล**  
> - **Fact Table (ตารางข้อเท็จจริง):** เปรียบเหมือน **"ดวงอาทิตย์"** ที่อยู่ตรงกลาง บันทึกเหตุการณ์หรือธุรกรรมที่เกิดขึ้นซ้ำๆ ในชีวิตประจำวัน เช่น ใบเสร็จขายสินค้า ซึ่งมีปริมาณแถวเยอะมากๆ ในตารางนี้จะมีตัวเลขยอดเงิน ปริมาณ และตัวเลขรหัสเชื่อมโยง  
> - **Dimension Tables (ตารางมิติ/ตารางอ้างอิง):** เปรียบเหมือน **"ดาวเคราะห์บริวาร"** ที่โคจรรอบดวงอาทิตย์ เป็นเสมือนสมุดทะเบียนประวัติ เช่น ทะเบียนรายชื่อลูกค้า แคตตาล็อกสินค้า รายชื่อพนักงาน และปฏิทินวันที่ ซึ่งทำหน้าที่ให้คำอธิบายว่า "ใคร (Who), ทำอะไร (What), ที่ไหน (Where), เมื่อไร (When)"

---

## โครงสร้างข้อมูล (อ่านก่อน Import)

| ตาราง | บทบาท | Grain (ระดับความละเอียดของข้อมูล) / คำอธิบาย |
| :--- | :--- | :--- |
| `FactSales` | **Fact** | **1 แถว = 1 order line (แถวสินค้าในบิล)** มีตัวเลขวัดผล `SalesAmount`, `Profit`, `LineCost` (ชนิด Fixed Decimal) |
| `DimDate` | **Date Dim** | วันที่ต่อเนื่องกันครบทุกวัน (**Contiguous Dates**); มีทั้งปฏิทินสากล และปีงบประมาณ (Fiscal Year เริ่ม 1 ต.ค.) |
| `DimCustomer` | **Dim** | ข้อมูลลูกค้า: ประเทศ (`Country`), กลุ่มลูกค้า (`Segment`), ชื่อบริษัทลูกค้า (`Customer`) |
| `DimEmployee` | **Dim** | ข้อมูลพนักงานขาย: ชื่อ-นามสกุล, วันเกิด, วันเริ่มงาน, แผนก, ตำแหน่ง |
| `DimProduct` | **Dim** | ข้อมูลสินค้า: หมวดหมู่ (`Category`), ชื่อผู้ผลิต (`Supplier`), ราคาป้าย (`ListPrice`), สถานะสินค้า |
| `DimShipper` | **Dim** | ข้อมูลบริษัทขนส่ง: รหัสและชื่อบริษัทขนส่งสินค้า |

> 💡 **คิดภาพตามง่ายๆ (Mental Model): "Grain" คือความละเอียดของกล้องจุลทรรศน์**  
> คำว่า **Grain (ระดับเกรนของข้อมูล)** หมายถึง "1 แถวในตารางแทนสิ่งใดในโลกความจริง?"  
> ใน `FactSales` เม็ดข้อมูลอยู่ที่ระดับ **Order Line (รายการสินค้าแต่ละชิ้นในบิล)** ไม่ใช่ทั้งใบเสร็จ (Order Header)  
> เช่น ถ้าลูกค้า 1 คนเดินเข้าซูเปอร์มาร์เก็ต ซื้อนม 1 กล่อง และขนมปัง 1 ชิ้น ใบเสร็จ 1 ใบนี้จะกลายเป็น **2 แถว** ใน `FactSales` ทันที การรู้ Grain ชัดเจนจะช่วยป้องกันไม่ให้เราคำนวณตัวเลขซ้ำซ้อน

> ⚠️ **ข้อควรระวัง:** ชีตในไฟล์ Excel ที่ขึ้นต้นด้วยขีดล่าง `_` (เช่น `_Columns`, `_Measures`, `_Relationships`, `_QA`) เป็น **เอกสารกำกับสำหรับมนุษย์และชุดทดสอบอัตโนมัติ (pytest)** — **ห้าม Import เข้าโมเดลเด็ดขาด**

> **Best Practice:** ใช้โครงสร้างแบบ **Star schema** ร่วมกับรหัสตัวเลขแทนข้อมูล (**Integer Surrogate Keys** เช่น `*Key`) เสมอ แล้วทำการซ่อนคอลัมน์คีย์เหล่านี้จากหน้า Report View  
> *อ้างอิง:* [Microsoft Learn: Understand star schema and the importance for Power BI](https://learn.microsoft.com/power-bi/guidance/star-schema)

---

## ขั้นตอนปฏิบัติทีละคลิก (Step-by-Step)

### 1) การนำเข้าข้อมูล (Get Data)
1. เปิดโปรแกรม Power BI Desktop → คลิกที่ **Get Data → Excel workbook**
2. เลือกไฟล์ `data/Northwind_DW_DimFact.xlsx`
3. ในหน้าต่าง Navigator ให้ติ๊กเลือกเฉพาะ **Tables** (สังเกตไอคอนรูปตารางสีฟ้า):  
   `DimDate`, `DimCustomer`, `DimEmployee`, `DimProduct`, `DimShipper`, `FactSales`
4. คลิก **Load** (หรือคลิก Transform Data เพื่อเข้า Power Query ไปตรวจสอบชนิดข้อมูล แล้วคลิก Close & Apply)

### 2) ปิดระบบ Auto date/time (กฎเหล็กของโมเดลระดับมืออาชีพ)
1. ไปที่เมนู **File → Options and settings → Options**
2. ภายใต้หัวข้อ **Current File → Data Load → Time intelligence**
3. เอาเครื่องหมายถูกออกจากช่อง **Auto date/time**  
   *(คำแนะนำ: แนะนำให้ปิดที่หัวข้อ Global → Data Load ด้วย เพื่อไม่ให้เปิดขึ้นมาเองในไฟล์ใหม่อื่นๆ)*

> 💡 **คิดภาพตามง่ายๆ (Mental Model): ทำไมต้องปิด Auto date/time?**  
> ถ้าเราไม่ปิด Power BI จะแอบสร้างตารางปฏิทินซ่อนไว้ข้างหลังให้กับ "ทุกคอลัมน์ที่มีชนิดเป็นวันที่" ในไฟล์ เปรียบเหมือนทุกคนในห้องเรียนต่างคนต่างพกปฏิทินคนละเล่ม ซึ่งนอกจากจะเปลืองหน่วยความจำ (RAM) อย่างมากแล้ว ยังทำให้สูตรคำนวณวันเวลาสับสน  
> การปิด Auto date/time แล้วใช้ตาราง `DimDate` เพียงตารางเดียว เปรียบเสมือนการติดตั้ง **"นาฬิกากลางประจำห้องเรียน"** ที่ทุกคนใช้อ้างอิงเวลาตรงกันอย่างแม่นยำ

### 3) ตรวจสอบและสร้างความสัมพันธ์ (Relationships)
สลับไปที่มุมมอง **Model view** ตรวจสอบหรือลากเส้นความสัมพันธ์ตามตารางด้านล่างนี้ (อ้างอิงตามชีต `_Relationships`):

| จากตาราง (From: Many ฝั่งลูกศร) | ไปยังตาราง (To: One ฝั่งเลข 1) | สถานะ Active? | ความหมายทางธุรกิจ |
| :--- | :--- | :---: | :--- |
| `FactSales[ProductKey]` | `DimProduct[ProductKey]` | **Yes** | สินค้าที่ขาย |
| `FactSales[CustomerKey]` | `DimCustomer[CustomerKey]` | **Yes** | ลูกค้าผู้ซื้อ |
| `FactSales[EmployeeKey]` | `DimEmployee[EmployeeKey]` | **Yes** | พนักงานผู้ปิดการขาย |
| `FactSales[ShipperKey]` | `DimShipper[ShipperKey]` | **Yes** | บริษัทที่ใช้จัดส่ง |
| `FactSales[OrderDateKey]` | `DimDate[DateKey]` | **Yes (Active)** | วันที่สั่งซื้อสินค้า (เส้นหลักของระบบ) |
| `FactSales[RequiredDateKey]` | `DimDate[DateKey]` | **No (Inactive)** | วันที่นัดส่งสินค้าตามกำหนด |
| `FactSales[ShippedDateKey]` | `DimDate[DateKey]` | **No (Inactive)** | วันที่ส่งสินค้าออกจริง |

- **Cardinality (ความสัมพันธ์):** Many-to-one (`* : 1`)
- **Cross-filter direction:** **Single** (ทิศทางลูกศรชี้จาก Dim ไหลไปกรอง Fact เสมอ)

> 💡 **คิดภาพตามง่ายๆ (Mental Model): ทิศทางลูกศร Single Cross-Filter**  
> เปรียบเสมือน **"ทางน้ำไหลจากภูเขาสู่ đồng bằng"** กฎพื้นฐานคือ เมื่อผู้ใช้เลือกตัวกรองที่ตารางข้อมูลอ้างอิง (Dim) เช่น เลือก "ประเทศเยอรมนี" แรงกรองจะไหลตามลูกศรไปบีบตารางยอดขาย (Fact) ให้เหลือเฉพาะยอดของเยอรมนีทันที

### 4) กำหนดให้เป็น Date Table ทางการ (Mark as Date Table)
1. ในหน้า Model view หรือ Data view ให้คลิกขวาที่ชื่อตาราง `DimDate`
2. เลือก **Mark as date table → Mark as date table**
3. ในช่อง Date column ให้เลือกคอลัมน์ `Date` แล้วกด OK
4. *เงื่อนไขสำคัญ:* คอลัมน์นี้ต้องเป็นชนิดข้อมูลแบบ Date แท้, ไม่มีค่าว่าง, และต้องมีวันที่เรียงต่อเนื่องกันไม่ขาดตอน

### 5) ซ่อนคอลัมน์คีย์เชื่อมโยง (Hide Keys / Foreign Keys)
1. คลิกขวาที่คอลัมน์ที่ลงท้ายด้วย `*Key` ทั้งหมดในตาราง `FactSales` และตาราง `Dim*` ต่างๆ
2. เลือก **Hide in report view**  
*(เพราะผู้บริหารและผู้ใช้รายงานต้องการเลือกดู "ชื่อลูกค้า" หรือ "ชื่อสินค้า" ไม่ได้ต้องการดูตัวเลขรหัสระบบ)*

### 6) สร้าง Explicit Measure ตัวแรก + เปิดโหมด Discourage Implicit Measures
1. สลับไปที่ **Report view** คลิกขวาที่ตาราง `FactSales` → เลือก **New measure**
2. พิมพ์สูตร DAX ดังนี้:

```dax
Sales Amount = SUM ( FactSales[SalesAmount] )
```

3. สลับไปที่ **Model view** → คลิกที่พื้นที่ว่างของโมเดลในหน้าต่าง Properties ทางขวา → เลื่อนลงมาเปิดสวิตช์ **Discourage implicit measures** ให้เป็น **On**  
*(คำสั่งนี้จะปิดการลากคอลัมน์ตัวเลขไปหยอดลงกราฟแล้วให้โปรแกรมเดาใจหาผลรวมอัตโนมัติ บังคับให้ทุกคนต้องใช้ Measure ที่ประกาศสูตรไว้อย่างเป็นทางการเท่านั้น ซึ่งจำเป็นมากสำหรับโมเดลระดับองค์กร)*

> 💡 **คิดภาพตามง่ายๆ (Mental Model): Implicit vs. Explicit Measure**  
> - **Implicit Measure (การเดาใจ):** เหมือนการสั่งอาหารว่า "เอาข้าวมาจานนึง" แล้วให้พ่อครัวเดาเอาเองว่าเราอยากกินอะไร เสี่ยงต่อความผิดพลาดและควบคุมมาตรฐานไม่ได้  
> - **Explicit Measure (การประกาศทางการ):** เหมือนการเขียนระบุชื่อเมนูและสูตรอย่างชัดเจนลงในสมุดเมนู เช่น `[Sales Amount] = SUM(FactSales[SalesAmount])` ทุกคนหยิบไปใช้จะได้ผลลัพธ์ที่ถูกต้อง โปร่งใส และนำไปต่อยอดในสูตรชั้นสูงได้

---

## สิ่งที่ต้องจดจำขึ้นใจสำหรับ Data / Business Analyst
1. **Grain ของ Fact:** 1 แถวคือ Order Line (รายการสินค้าแต่ละชิ้นในบิล)
2. **Denormalization ใน Star Schema:** ข้อมูลผู้ผลิต (Supplier) ถูกรวบรวมเข้ามาไว้ใน `DimProduct` เรียบร้อยแล้ว จึงไม่มีตาราง `Suppliers` แยกอีก ช่วยลดขั้นตอนการเชื่อมโยงตารางหลายชั้น
3. **LineCost ไม่เท่ากับ StandardCost × Quantity:** ใน `FactSales` เราได้บันทึกต้นทุนจริงหน้างานไว้ในคอลัมน์ `LineCost` แล้ว เพื่อใช้เปรียบเทียบประสิทธิภาพกับการคำนวณแบบวนลูปในบทที่ 05

---

## Lab 01 — ติดตั้งโมเดลและทดสอบการทำงาน (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. นำเข้าตารางทั้ง 6 ตารางจากไฟล์ Excel `data/Northwind_DW_DimFact.xlsx`
2. ปิดตัวเลือก Auto date/time ของไฟล์นี้
3. กำหนด `DimDate[Date]` ให้เป็น Date Table ทางการ
4. เชื่อมโยง Relationships ไปยัง `DimDate` จำนวน 3 เส้น (Active 1 เส้นคือ OrderDateKey, Inactive 2 เส้น)
5. เขียนสูตร Measure `[Sales Amount]`
6. สร้างการ์ด (Card Visual) แสดง `[Sales Amount]` และสร้างตัวเลือก (Slicer) ด้วย `DimDate[Year]` เพื่อทดสอบว่าเมื่อคลิกเปลี่ยนปี ตัวเลขยอดขายเปลี่ยนตามถูกต้องหรือไม่

### แนวทางการตรวจและเฉลย
- สูตร Measure ที่ถูกต้อง:
```dax
Sales Amount = SUM ( FactSales[SalesAmount] )
```
- **จุดสังเกต:** ถ้าคลิกเลือกปีบน Slicer แล้วตัวเลขบน Card ไม่ยอมเปลี่ยน ให้ตรวจสอบว่าเส้นเชื่อมโยงระหว่าง `FactSales[OrderDateKey]` กับ `DimDate[DateKey]` มีสถานะเป็นเส้นทึบ (**Active**) หรือไม่ และบน Card ได้หยิบ `[Sales Amount]` ไปวางจริงหรือไม่

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- ใน Model view มีตาราง 6 ตารางที่มีเส้นเชื่อมโยงแบบ Many-to-One ถูกต้องครบทุกเส้น
- `DimDate` มีสัญลักษณ์รูปปฏิทินกำกับ (Mark as date table แล้ว)
- มี Explicit Measure `[Sales Amount]` แสดงผลลัพธ์ได้ถูกต้องตามตัวกรองปี

---

**บทเรียนถัดไป:** [02 — DAX syntax และ Context](02-dax-syntax-and-context.md)
"""


def get_lesson_02() -> str:
    return """
# 02 — DAX syntax และ Context

**เป้าหมาย:** ทำความเข้าใจไวยากรณ์ DAX มาตรฐานระดับสากล (`Table[Column]` vs `[Measure]`) และเข้าใจกลไกหัวใจสำคัญที่สุดของ DAX: **Row Context** และ **Filter Context**  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 01 เรียบร้อยแล้ว และมี Measure `[Sales Amount]` อยู่ในโมเดล

---

## ไวยากรณ์พื้นฐานของภาษา DAX (Syntax Rules)

ในภาษา DAX มีกฎเหล็กที่ได้รับการยอมรับเป็นมาตรฐานสากล (Best Practice) ดังนี้:

| องค์ประกอบ | รูปแบบตัวอย่าง | กฎระเบียบที่ต้องปฏิบัติ |
| :--- | :--- | :--- |
| **การอ้างอิงคอลัมน์ (Column)** | `FactSales[SalesAmount]` | **ต้อง (MUST)** ระบุชื่อตารางนำหน้าเสมอ (Fully Qualified) |
| **การอ้างอิงสูตรวัด (Measure)** | `[Sales Amount]` | **ห้าม (NEVER)** ใส่ชื่อตารางนำหน้าเด็ดขาด |
| **Comment บรรทัดเดียว** | `// ข้อความอธิบาย` หรือ `-- ข้อความอธิบาย` | ใช้สำหรับจดบันทึกสั้นๆ |
| **Comment หลายบรรทัด** | `/* ข้อความอธิบายหลายบรรทัด */` | ใช้สำหรับอธิบายที่มาของสูตรยาวๆ |

```dax
// ตัวอย่างสูตรที่เขียนได้ถูกต้องตามมาตรฐานสากล
Sales Amount = SUM ( FactSales[SalesAmount] )

// ตัวอย่างที่ผิดและพบบ่อยมาก — ผู้อ่านและตัวระบบจะแยกไม่ออกทันทีว่าเป็นคอลัมน์หรือสูตรวัด
// Sales Amount = SUM ( [SalesAmount] )
```

> 💡 **คิดภาพตามง่ายๆ (Mental Model): ทำไมต้องมีชื่อตารางนำหน้าคอลัมน์ แต่ห้ามนำหน้า Measure?**  
> - **คอลัมน์เปรียบเหมือน "คนที่มีสังกัดชัดเจน":** คอลัมน์ถูกเก็บอยู่ในตารางใดตารางหนึ่งทางกายภาพ การเขียน `FactSales[SalesAmount]` เปรียบเหมือนการเรียก "นายสมชาย แผนกขาย" ทำให้ทุกคนรู้ทันทีว่าเป็นข้อมูลดิบจากตาราง  
> - **Measure เปรียบเหมือน "สูตรคิดเลขกลางของบริษัท":** Measure เป็นตรรกะการคำนวณที่ลอยอยู่เหนือโมเดล มันสามารถถูกย้ายไปเก็บไว้ที่ตารางใดก็ได้โดยไม่เปลี่ยนผลลัพธ์ การเขียน `[Sales Amount]` เปล่าๆ โดยไม่มีชื่อตารางนำหน้า ช่วยให้ทั้งมนุษย์และโปรแกรมรู้ทันทีตั้งแต่แวบแรกว่า **"นี่คือสูตรคำนวณ ไม่ใช่คอลัมน์ข้อมูลดิบ"**

> **Best Practice:** Always fully qualify **columns**. Never fully qualify **measures**.  
> *อ้างอิง:* [Microsoft Learn: DAX column and measure references](https://learn.microsoft.com/dax/best-practices/dax-column-measure-references)

---

## บริบททั้งสองชนิด (Context: สองขั้วหัวใจของ DAX)

คำว่า **Context (บริบท)** คือสภาพแวดล้อมที่สูตร DAX กำลังทำงานอยู่ แบ่งออกเป็น 2 ชนิด:

### 1. Filter Context (บริบทการกรองข้อมูล)
คือชุดของตัวกรองที่เกิดขึ้น **ก่อนที่สูตรจะเริ่มคำนวณ** โดยมาจาก:
- หัวแถวและหัวคอลัมน์ของ Visual (เช่น แกนของกราฟ หรือ แถวของตาราง Matrix)
- ตัวเลือกบน Slicer หรือแผง Filters ด้านขวา
- ฟังก์ชัน `CALCULATE` ที่สั่งเปลี่ยนตัวกรองชั่วคราว (จะเรียนลึกในบทที่ 09)

> 💡 **คิดภาพตามง่ายๆ (Mental Model): Filter Context คือ "แว่นตากรองแสงสี"**  
> ลองนึกภาพว่าคุณมีกองกระดาษใบเสร็จนับล้านใบวางอยู่บนโต๊ะ  
> เมื่อผู้บริหารคลิก Slicer เลือก `Country = "Germany"` และเลือก `Year = 2024`  
> สภาพแวดล้อมนี้เหมือนกับการสวม **"แว่นตากรองสี"** ที่ทำให้คุณมองเห็นเฉพาะใบเสร็จของเยอรมนีในปี 2024 เท่านั้น ใบเสร็จอื่นๆ ทั้งหมดจะล่องหนหายไปชั่วคราว  
> จากนั้นเมื่อสูตร `SUM ( FactSales[SalesAmount] )` ทำงาน มันจะรวมเงินเฉพาะใบเสร็จที่มองเห็นผ่านแว่นตานี้เท่านั้น!

### 2. Row Context (บริบทของแถวปัจจุบัน)
เกิดขึ้นเมื่อสูตร DAX กำลังทำงานโดย **"เดินทีละแถว"** ภายในตาราง:
- ในการสร้าง **Calculated Column** (ระบบจะคำนวณทีละแถวตั้งแต่บรรทัดแรกจนถึงบรรทัดสุดท้ายของตาราง)
- ในฟังก์ชันประเภท **Iterator** (ฟังก์ชันที่ลงท้ายด้วย X เช่น `SUMX`, `AVERAGEX`, `FILTER`)

> 💡 **คิดภาพตามง่ายๆ (Mental Model): Row Context คือ "นิ้วชี้ที่ไล่ตรวจทีละบรรทัด"**  
> นึกภาพสมุดบัญชีรายรับรายจ่าย เมื่อเราสั่งคำนวณทีละแถว ระบบจะเอานิ้วชี้ไปที่แถวที่ 1 แล้วอ่านค่าเฉพาะแถวนั้น เช่น เอา `จำนวนชิ้น × ราคาต่อหน่วย` เมื่อคิดเสร็จก็นำนิ้วเลื่อนลงไปชี้ที่แถวที่ 2 แล้วทำซ้ำไปเรื่อยๆ จนสุดสมุด  
> **ข้อจำกัดสำคัญ:** นิ้วที่ชี้อยู่ในแถวปัจจุบันจะมองเห็นเฉพาะคอลัมน์ในแถวของตัวเองเท่านั้น มันไม่ได้กรองตารางอื่น และไม่ได้รับรู้ถึง Filter Context โดยอัตโนมัติ

---

## กฎทองของ Context (Golden Rule)
> ⚠️ **คำเตือนที่ต้องจำ:** **Row Context ไม่ได้กรองตารางอื่น และไม่แปลงร่างเป็น Filter Context โดยอัตโนมัติ!**  
> หากต้องการดึงข้อมูลจากตารางอื่นในขณะที่นิ้วกำลังชี้อยู่ทีละแถว เราต้องใช้คำสั่งเชื่อมโยง เช่น `RELATED` (บทที่ 07) หรือต้องใช้การเปลี่ยนผ่านบริบท (**Context Transition**) ผ่านฟังก์ชัน `CALCULATE` (บทที่ 16)

---

## ตัวอย่างการสังเกต Context ในหน้าจอจริง

1. **ไม่มี Filter Context:** ลาก Card Visual มาวาง แล้วใส่ `[Sales Amount]` ลงไป → ได้ตัวเลขยอดขายรวมทั้งบริษัท เพราะยังไม่มีตัวกรองใดๆ มาจำกัดข้อมูล
2. **มี Filter Context:** วาง Slicer เลือก `DimCustomer[Country]` แล้วกดเลือก "Germany" → ตัวเลขบน Card ปรับลดลงเหลือเฉพาะยอดของเยอรมนีทันที
3. **มี Row Context:** สร้าง Calculated Column ใหม่บนตาราง `DimEmployee` โดยเขียนสูตรคำนวณอายุพนักงาน → ระบบจะเอานิ้วชี้ไล่คำนวณทีละแถวของพนักงานแต่ละคนจนครบทุกคน

---

## Lab 02 — ทดสอบความเข้าใจเรื่อง Syntax และ Context (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. สร้าง Measure ใหม่ชื่อ `[Orders]` เพื่อคำนวณจำนวนใบสั่งซื้อที่ไม่ซ้ำกัน (ใช้คำสั่ง `DISTINCTCOUNT` และเขียนอ้างอิงชื่อคอลัมน์ให้ถูกต้องตามกฎ Syntax)
2. นำ Card Visual มาวาง 2 ใบ: ใบแรกใส่ `[Sales Amount]` และใบที่สองใส่ `[Orders]` พร้อมวาง Slicer เลือกประเทศ (`DimCustomer[Country]`)
3. สังเกตการทำงาน และบันทึกคำอธิบายสั้นๆ ว่าเมื่อเราคลิกเลือกประเทศบน Slicer เกิดอะไรขึ้นกับ Measure ทั้งสองตัวในมุมมองของ Filter Context

### เฉลยสูตรและการวิเคราะห์
```dax
Orders = DISTINCTCOUNT ( FactSales[OrderID] )
```

**การวิเคราะห์ผลลัพธ์:**
- **ความถูกต้องตาม Syntax:** คอลัมน์ `OrderID` อ้างอิงแบบระบุชื่อตารางชัดเจน `FactSales[OrderID]`
- **การทำงานของ Filter Context:** เมื่อเลือกประเทศ เช่น "France" บน Slicer สภาพ Filter Context จะส่งแรงกรองข้ามจากตาราง `DimCustomer` วิ่งตามลูกศร Relationship ไปบีบตาราง `FactSales` ให้เหลือเฉพาะรายการสั่งซื้อของลูกค้าชาวฝรั่งเศส ส่งผลให้ทั้ง `[Sales Amount]` และ `[Orders]` คำนวณยอดเฉพาะกลุ่มข้อมูลที่ถูกกรองพร้อมกันอย่างถูกต้อง

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- สูตร Measure ใช้ `FactSales[OrderID]` ครบถ้วน
- ไม่มีชื่อตารางนำหน้าชื่อ Measure เมื่อนำไปเรียกใช้ในสูตรอื่น
- เข้าใจและอธิบายความแตกต่างระหว่าง Filter Context (แว่นกรองข้อมูล) และ Row Context (นิ้วชี้ทีละบรรทัด) ได้อย่างชัดเจน

---

**บทเรียนถัดไป:** [03 — Calculated Column](03-calculated-column.md)
"""


def get_lesson_03() -> str:
    return """
# 03 — Calculated Column

**เป้าหมาย:** เข้าใจกระบวนการทำงานของ Calculated Column ภายใต้ Row Context, รู้จักผลกระทบต่อหน่วยความจำ (RAM Footprint) ในเอนจิน VertiPaq, และรู้วิธีตั้งค่า Sort by Column อย่างถูกต้อง  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 02 เรียบร้อยแล้ว

---

## Calculated Column ทำงานอย่างไร?

Calculated Column คือคอลัมน์ที่ถูกสร้างขึ้นใหม่ในตารางข้อมูล โดยใช้สูตร DAX คำนวณหาผลลัพธ์ทีละแถว

> 💡 **คิดภาพตามง่ายๆ (Mental Model): การเขียนหมึกถาวรลงในสมุดบัญชี**  
> การสร้าง Calculated Column เปรียบเสมือนการ **"หยิบปากกาหมึกซึมมาตีเส้นเพิ่มช่องคอลัมน์ใหม่ลงในสมุดบัญชี แล้วนั่งคำนวณทีละบรรทัดจนครบทุกหน้า"**  
> - การคำนวณนี้จะเกิดขึ้น **ครั้งเดียวตอนที่เรากด Refresh ข้อมูล** (หรือตอนพิมพ์สูตรเสร็จ)  
> - ผลลัพธ์ตัวเลขหรือข้อความจะถูกบันทึกลงในหน่วยความจำ RAM ของคอมพิวเตอร์อย่างถาวร (เรียกว่าการ **Materialize**)  
> - เมื่อมีคนเปิดดูรายงาน ค่าเหล่านี้มีอยู่แล้วในตาราง จึงไม่ต้องเสียเวลาคำนวณใหม่อีก

---

## เมื่อไหร่ควรใช้ และเมื่อไหร่ที่ "ห้ามใช้"?

นี่คือข้อแตกต่างสำคัญระหว่างผู้ใช้ทั่วไป กับ Data Analyst / BI Developer มืออาชีพ:

| สถานการณ์ที่ **ควรใช้** Calculated Column | สถานการณ์ที่ **ห้ามใช้** (ให้ใช้ Measure แทน) |
| :--- | :--- |
| 1. ต้องการนำผลลัพธ์ไปใส่เป็น **แกนกราฟ (Axis)** เช่น ช่วงอายุ, กลุ่มราคา | 1. ต้องการหา **ผลรวม ยอดเงิน หรือค่าเฉลี่ย** เพื่อเอาไปโชว์บนการ์ดสรุปหรือในตาราง |
| 2. ต้องการนำผลลัพธ์ไปเป็น **ตัวกรอง (Slicer)** เช่น สถานะสินค้า (Active/Discontinued) | 2. สูตรนั้นต้องเปลี่ยนค่าไปตามการคลิกเลือก Slicer ของผู้ใช้รายงาน |
| 3. ต้องการใช้คอลัมน์นี้เป็น **คีย์ในการเชื่อมความสัมพันธ์ (Relationship Key)** | 3. ตารางมีข้อมูลนับสิบล้านแถว และการคำนวณกินเนื้อที่แรมโดยไม่จำเป็น |

> ⚠️ **คำเตือนระดับองค์กร (Best Practice):**  
> อย่าสร้าง Calculated Column เพื่อหายอดเงินรวม เช่น สร้างคอลัมน์กำไรแล้วลากไป SUM บนกราฟ เพราะจะเปลืองเนื้อที่ RAM มหาศาล ให้สร้างเป็น **Explicit Measure** แทนเสมอ!

---

## ตัวอย่างการใช้งานจริงใน Northwind DW

### ตัวอย่างที่ 1: การรวมข้อความบนตาราง Dimension (Row Context)
การนำชื่อและนามสกุลของพนักงานมารวมกันบนตาราง `DimEmployee`:
```dax
FullName = DimEmployee[FirstName] & " " & DimEmployee[LastName]
```
*(ระบบใช้นิ้วชี้ทีละแถวใน `DimEmployee` หยิบชื่อและนามสกุลมาต่อกัน ได้คอลัมน์ใหม่เอาไปใช้ใส่ใน Slicer หรือแกนกราฟได้อย่างสวยงาม)*

### ตัวอย่างที่ 2: การแปลงรหัสตัวเลขเป็นข้อความที่มนุษย์เข้าใจง่าย
ในตาราง `DimProduct` คอลัมน์ `Discontinued` เก็บค่าเป็นเลข 1 (เลิกผลิต) หรือ 0 (ยังผลิตอยู่) เราสามารถสร้างคอลัมน์คำอธิบายได้ดังนี้:
```dax
IsDiscontinuedText = 
IF ( 
    DimProduct[Discontinued] = 1, 
    "Discontinued", 
    "Active" 
)
```

### ตัวอย่างที่ 3: การคำนวณส่วนต่างในระดับแถวของตาราง Fact
ในตาราง `FactSales` เราต้องการหา Margin (กำไรส่วนเพิ่มต่อชิ้นงาน) ในระดับแต่ละแถว:
```dax
Margin = FactSales[SalesAmount] - FactSales[LineCost]
```
และคำนวณสัดส่วน Margin Rate:
```dax
MarginRate = DIVIDE ( FactSales[Margin], FactSales[SalesAmount] )
```
*(ข้อสังเกต: ในระบบงานจริงขนาดใหญ่ หากคอลัมน์ตัวเลขเหล่านี้สามารถคำนวณและเตรียมไว้ได้ตั้งแต่ในฐานข้อมูล SQL หรือขั้นตอน Data Pipeline (ELT) จะช่วยประหยัดทรัพยากรของ Power BI ได้ดียิ่งขึ้น)*

---

## เทคนิคสำคัญ: Sort by Column (การแก้ปัญหาเรียงลำดับผิดธรรมชาติ)

ลองนึกภาพว่าคุณนำชื่อเดือน (เช่น "มกราคม", "กุมภาพันธ์", "มีนาคม" หรือ "January", "February") ไปวางบนแกนกราฟ  
คอมพิวเตอร์เป็นระบบที่อ่านตัวอักษร มันจะไม่รู้ว่าเดือนไหนมาก่อนมาหลังตามธรรมชาติ แต่มันจะเรียงตาม **ตัวอักษร ก-ฮ หรือ A-Z** (เช่น "April" จะขึ้นมาก่อน "January" หรือ "กุมภาพันธ์" จะขึ้นก่อน "มกราคม")

> 💡 **คิดภาพตามง่ายๆ (Mental Model): การติดป้ายหมายเลขคิว**  
> เพื่อให้คอมพิวเตอร์เรียงลำดับได้ถูกต้อง เราต้องบอกมันว่า **"เวลาเรียงชื่อเดือนนี้ ให้แอบดูหมายเลขคิวในอีกคอลัมน์หนึ่งนะ"**

### วิธีตั้งค่า Sort by Column:
1. ไปที่มุมมอง **Data view** หรือ **Model view**
2. คลิกเลือกคอลัมน์ชื่อเดือน เช่น `DimDate[MonthName]`
3. ที่แถบเครื่องมือด้านบน เลือกเมนู **Column tools → Sort by column**
4. เลือกคอลัมน์ที่เป็นตัวเลขลำดับ เช่น `DimDate[MonthKey]` หรือ `DimDate[MonthNumberOfYear]`
5. ผลลัพธ์: กราฟและตารางจะเรียงลำดับเดือน มกราคม → กุมภาพันธ์ → มีนาคม อย่างถูกต้องสมบูรณ์ทันที

---

## Lab 03 — สร้าง Calculated Column และจัดลำดับ (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. ในตาราง `DimProduct` สร้าง Calculated Column ชื่อ `IsDiscontinuedText` โดยถ้า `Discontinued = 1` ให้แสดงคำว่า `"Discontinued"` ถ้าไม่ใช่ให้แสดงคำว่า `"Active"`
2. ในตาราง `DimEmployee` สร้าง Calculated Column ชื่อ `FullName` โดยนำ `FirstName` เว้นวรรค แล้วตามด้วย `LastName`
3. ในตาราง `DimDate` ตรวจสอบคอลัมน์ `MonthName` และตั้งค่า **Sort by column** ให้เรียงตาม `MonthKey`
4. สร้างกราฟคอลัมน์ แสดงยอดขายตาม `MonthName` เพื่อตรวจดูว่าเดือนเรียงลำดับตามปฏิทินถูกต้องหรือไม่

### เฉลยสูตร
```dax
// 1. ตาราง DimProduct
IsDiscontinuedText = IF ( DimProduct[Discontinued] = 1, "Discontinued", "Active" )

// 2. ตาราง DimEmployee
FullName = DimEmployee[FirstName] & " " & DimEmployee[LastName]
```

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- คอลัมน์ `FullName` แสดงชื่อและนามสกุลมีเว้นวรรคถูกต้องทุกแถว
- เมื่อนำ `MonthName` ไปใส่ในแกนกราฟ แสดงลำดับเรียงจากเดือนมกราคมไปจนถึงธันวาคม ไม่ได้เรียงตามตัวอักษร A-Z

---

**บทเรียนถัดไป:** [04 — Measures](04-measures.md)
"""


def get_lesson_04() -> str:
    return """
# 04 — Measures

**เป้าหมาย:** เข้าใจธรรมชาติของ Measure ซึ่งคำนวณแบบพลวัต ณ เวลาที่เรียกดูข้อมูล (Dynamic Calculation at Query Time), ฝึกเขียน Base Measures พื้นฐานของธุรกิจ, และใช้ฟังก์ชัน `DIVIDE` เพื่อป้องกันปัญหาการหารด้วยศูนย์ได้อย่างปลอดภัย  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 03 เรียบร้อยแล้ว

---

## Measure คืออะไร และทำงานอย่างไร?

ถ้า Calculated Column คือการเขียนหมึกลงบนกระดาษอย่างถาวร...  
**Measure คือ "สมองกลหรือสูตรในเครื่องคิดเลข"** ที่ไม่มีการจดบันทึกตัวเลขค้างไว้ในตารางเลยแม้แต่ไบต์เดียว!

> 💡 **คิดภาพตามง่ายๆ (Mental Model): Measure คือเครื่องคิดเลขสดตามคำสั่ง**  
> ลองนึกภาพว่าคุณเป็นผู้บริหารเดินเข้าไปในห้องทำงาน แล้วถามว่า **"ปีนี้เราขายได้เท่าไหร่?"**  
> Measure จะเริ่มทำงานทันที ณ วินาทีนั้น (Query Time):  
> 1. มันจะก้มดูว่าตอนนี้คุณสวมแว่นกรองข้อมูลอะไรอยู่ (**Filter Context**) เช่น คุณกำลังชี้ที่ปี 2024 และสินค้าหมวด Beverages  
> 2. มันจะร่อนข้อมูลเฉพาะส่วนนั้นขึ้นมา  
> 3. จากนั้นจึงกดเครื่องคิดเลขคำนวณตัวเลขผลลัพธ์ออกมาให้คุณเห็นบนหน้าจอ  
> 4. เมื่อคุณเปลี่ยนใจไปคลิกดูปี 2025 ตัวเลขเดิมจะหายไป และเครื่องคิดเลขจะคิดยอดใหม่ของปี 2025 ให้ทันที  
> **ข้อดีมหาศาล:** ไม่กินเนื้อที่เก็บข้อมูล (RAM Footprint ต่ำมาก) และปรับเปลี่ยนผลลัพธ์ตามผู้ใช้งานได้อย่างยืดหยุ่น 100%

---

## กฎความปลอดภัยทางคณิตศาสตร์: ทำไมต้องใช้ `DIVIDE()` แทนเครื่องหมาย `/`?

ในวิชาคณิตศาสตร์พื้นฐาน การหารตัวเลขด้วยศูนย์ เช่น $\\frac{100}{0}$ เป็นสิ่งที่ **"ไม่นิยามทางคณิตศาสตร์" (Undefined)**  
ในระบบคอมพิวเตอร์ ถ้าเราเขียนสูตรแบบดั้งเดิม:
```dax
// ห้ามเขียนแบบนี้ในระดับมืออาชีพ
Margin % = [Profit] / [Sales Amount]
```
ถ้าวันใดวันหนึ่งมียอดขายเป็นศูนย์ หรือไม่มีข้อมูล (BLANK) ผลลัพธ์ที่ได้อาจกลายเป็นข้อผิดพลาด (Error) หรือแสดงคำว่า `Infinity` ซึ่งทำให้กราฟและหน้าปัดรายงานของผู้บริหารพังเสียหายทั้งหน้าจอ

> **Best Practice:** ให้ใช้ฟังก์ชัน `DIVIDE ( Numerator, Denominator, [AlternateResult] )` เสมอ  
> ฟังก์ชัน `DIVIDE` มีระบบความปลอดภัยในตัว (Safe Division) หากตัวหารเป็น 0 หรือเป็นค่าว่าง มันจะคืนค่าว่าง (**BLANK**) ออกมาให้อย่างนุ่มนวลโดยไม่ทำให้รายงาน Error

```dax
// ถูกต้อง ปลอดภัย และได้มาตรฐานสากล
Profit Margin = DIVIDE ( [Profit], [Sales Amount] )
```

---

## ชุด Base Measures มาตรฐานของ Northwind DW

ในฐานะ Data Analyst หรือ BI Developer เมื่อเริ่มสร้างโปรเจกต์ใหม่ เราควรสร้างชุดสูตรวัดพื้นฐาน (**Base Measures**) ประจำโมเดลเตรียมไว้เสมอ เพื่อนำไปต่อยอดในสูตรที่ซับซ้อนขึ้น:

```dax
// 1. ยอดขายรวม
Sales Amount = SUM ( FactSales[SalesAmount] )

// 2. ต้นทุนรวม
Total Cost = SUM ( FactSales[LineCost] )

// 3. กำไรขั้นต้น (นำ Measure ลบ Measure)
Profit = [Sales Amount] - [Total Cost]

// 4. อัตราส่วนกำไรขั้นต้น (Safe Division)
Profit Margin = DIVIDE ( [Profit], [Sales Amount] )

// 5. จำนวนออเดอร์ที่ไม่ซ้ำกัน
Orders = DISTINCTCOUNT ( FactSales[OrderID] )

// 6. ปริมาณสินค้าที่ขายได้ทั้งหมด
Quantity = SUM ( FactSales[Quantity] )

// 7. มูลค่าเฉลี่ยต่อหนึ่งออเดอร์ (Average Order Value - AOV)
Average Order Value = DIVIDE ( [Sales Amount], [Orders] )
```

> 💡 **คิดภาพตามง่ายๆ (Mental Model): การต่อตัวต่อเลโก้ (Measure Reusability)**  
> สังเกตสูตร `[Profit] = [Sales Amount] - [Total Cost]`  
> เราไม่ได้เขียนว่า `SUM(SalesAmount) - SUM(LineCost)` ซ้ำอีกรอบ แต่เราหยิบ "ก้อนเลโก้" Measure เดิมที่เราเคยสร้างไว้มาประกอบเข้าด้วยกัน  
> ประโยชน์คือ หากวันหน้าสูตรยอดขายมีการปรับเปลี่ยนเงื่อนไขทางธุรกิจ เราแก้ที่ `[Sales Amount]` จุดเดียว ทุกสูตรที่นำมันไปใช้จะได้รับผลการอัปเดตที่ถูกต้องทันที!

---

## Lab 04 — สร้างชุด Base Measures ประจำโมเดล (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. สร้าง Measure ตามรายการด้านบนให้ครบถ้วนในตาราง `FactSales`:  
   - `[Total Cost]`  
   - `[Profit]`  
   - `[Profit Margin]` (กำหนดรูปแบบการแสดงผลเป็น Percentage `0.0%`)  
   - `[Quantity]`  
   - `[Average Order Value]` (กำหนดรูปแบบเป็นสกุลเงิน Currency)
2. สร้างตารางแบบ Matrix Visual:  
   - นำ `DimProduct[Category]` มาวางที่ Rows  
   - นำ `[Sales Amount]`, `[Total Cost]`, `[Profit]`, และ `[Profit Margin]` มาวางที่ Values
3. นำ Slicer เลือกปี `DimDate[Year]` มาทดสอบคลิกเลือกปีต่างๆ

### เฉลยสูตร
ตรวจสอบสูตรและรูปแบบตัวเลขให้ตรงกับไฟล์ [`dax/measures.dax`](../../dax/measures.dax)

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- เมื่อ `[Sales Amount]` และ `[Total Cost]` แสดงผลใน Matrix ยอด `[Profit]` ต้องเท่ากับผลต่างของสองช่องนั้นพอดีในทุกแถว
- ในแถวรวมท้ายตาราง (Total Row) ช่อง `[Profit Margin]` ต้องคำนวณจาก $\\frac{\\text{Total Profit}}{\\text{Total Sales}}$ อย่างถูกต้อง ไม่ใช่การนำเปอร์เซ็นต์ของแต่ละแถวมาบวกกันเฉยๆ

---

**บทเรียนถัดไป:** [05 — Aggregation และ Iterators](05-aggregation-and-iterators.md)
"""


def get_lesson_05() -> str:
    return """
# 05 — Aggregation และ Iterators

**เป้าหมาย:** แยกความแตกต่างระหว่าง Aggregation ทั่วไป (`SUM`) กับฟังก์ชันวนลูป Iterator (`SUMX`), เข้าใจการทำงานของ Storage Engine เทียบกับ Formula Engine, และเข้าใจเหตุผลทางสถาปัตยกรรมว่าทำไมระบบขนาดใหญ่จึงควรทำ Materialize ตัวเลขเตรียมไว้  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 04 เรียบร้อยแล้ว

---

## สองแนวทางในการคิดเลข: Aggregators vs Iterators

ในภาษา DAX เมื่อเราต้องการรวมผลลัพธ์ของตัวเลข เรามีเครื่องมือ 2 รูปแบบหลัก:

### 1. Standard Aggregators (`SUM`, `AVERAGE`, `MIN`, `MAX`)
ทำงานโดยตรงกับ **คอลัมน์เดี่ยวๆ ที่มีอยู่แล้วในตาราง**  
ประมวลผลด้วย **Storage Engine (VertiPaq)** โดยตรง ซึ่งเป็นระดับเครื่องจักรที่เร็วที่สุด สามารถสแกนและรวมผลข้อมูลหลายสิบล้านแถวได้ภายในเสี้ยววินาที

```dax
Sales Amount = SUM ( FactSales[SalesAmount] )
```

### 2. Iterators (ฟังก์ชันที่ลงท้ายด้วย X เช่น `SUMX`, `AVERAGEX`, `MINX`)
ทำงานโดยการสร้าง **Row Context ชั่วคราวขึ้นมา แล้วเดินชี้คำนวณทีละแถว** ตามสูตรที่เราระบุไว้ จากนั้นจึงนำผลลัพธ์ที่ได้ของแต่ละแถวมารวมกันในขั้นตอนสุดท้าย

```dax
Sales Amount (Iterated) = 
SUMX ( 
    FactSales, 
    FactSales[Quantity] * FactSales[UnitPrice] * ( 1 - FactSales[Discount] ) 
)
```

> 💡 **คิดภาพตามง่ายๆ (Mental Model): เครื่องคัดแยกเหรียญอัตโนมัติ vs พนักงานพร้อมกระดาษทด**  
> - **`SUM` เปรียบเสมือน "เครื่องนับเหรียญอัตโนมัติ":** เมื่อคุณมีช่องใส่เหรียญ (คอลัมน์ `SalesAmount`) ที่เทเงินลงไป เครื่องจะหมุนนับยอดรวมทั้งหมดออกมาได้ทันที รวดเร็ว เงียบ และไม่เปลืองแรง  
> - **`SUMX` เปรียบเสมือน "พนักงานคิดเลขที่ถือกระดาษทด":** พนักงานต้องเดินไปที่โต๊ะทีละแถว (สร้าง Row Context) หยิบจำนวนชิ้นมาคูณกับราคา ลบส่วนลด ได้ตัวเลขเท่าไหร่ก็จดใส่กระดาษทดไว้ในใจ พอเดินครบทุกแถวจนครบทั้งตาราง จึงค่อยเอายอดในกระดาษทดทั้งหมดมารวมเป็นก้อนสุดท้าย  
> แน่นอนว่าถ้าตารางมีเพียง 1,000 แถว พนักงานอาจใช้เวลาเสี้ยววินาที แต่ถ้าตารางมี **10,000,000 แถว** พนักงานคนนี้จะต้องทดเลขสิบล้านครั้งทุกครั้งที่ผู้ใช้คลิกหน้าจอ!

---

## เบื้องหลังการประมวลผล: Formula Engine vs. Storage Engine

- **Storage Engine (VertiPaq):** ทำงานแบบ Multithread ขนานกัน บีบอัดข้อมูลสูง และทำงานกับคอลัมน์ตรงๆ ได้เร็วระดับฟ้าผ่า
- **Formula Engine:** เป็นสมองกลส่วนกลางที่คอยประมวลผลตรรกะที่ซับซ้อน การวนลูป (Iterate) มักจะดึงการประมวลผลมาทำงานที่ Formula Engine ซึ่งทำงานแบบ Single-thread เป็นหลัก ทำให้ใช้เวลานานกว่า

> **Best Practice ระดับองค์กร (Enterprise Architecture):**  
> สำหรับตัวเลขธุรกรรมหลักที่ต้องเรียกดูบ่อยๆ (เช่น มูลค่ายอดขายสุทธิ หรือต้นทุนสินค้า) ควรทำการคำนวณและเก็บเป็นคอลัมน์จริง (**Materialize**) มาให้เสร็จสิ้นตั้งแต่กระบวนการเตรียมข้อมูล (SQL / Data Warehouse / Power Query) เช่น คอลัมน์ `FactSales[SalesAmount]` และ `FactSales[LineCost]` เพื่อให้ใน Power BI เราสามารถใช้ฟังก์ชัน `SUM` ได้โดยตรง ช่วยให้แดชบอร์ดโหลดเร็ว ลื่นไหล แม้ข้อมูลจะมีขนาดมหาศาล

---

## เมื่อไหร่ที่จำเป็นต้องใช้ `SUMX`?

แม้ `SUM` จะเร็วกว่า แต่มีหลายสถานการณ์ทางธุรกิจที่ `SUM` ธรรมดาทำไม่ได้ และจำเป็นต้องพึ่งพา `SUMX`:
1. **เมื่อต้องคำนวณตัวเลขข้ามตารางตามเงื่อนไข:** เช่น การนำจำนวนสินค้าในตาราง Fact ไปคูณกับราคามาตรฐานในตารางสินค้าผ่านฟังก์ชัน `RELATED`:
```dax
Line Cost (Iterated) = 
SUMX ( 
    FactSales, 
    FactSales[Quantity] * RELATED ( DimProduct[StandardCost] ) 
)
```
2. **เมื่อต้องคำนวณบนตารางที่ถูกกรองชั่วคราว:** เช่น การใช้ `SUMX` ร่วมกับฟังก์ชัน `FILTER` หรือการหาผลรวมของตารางสรุปย่อย

---

## Lab 05 — เปรียบเทียบผลลัพธ์ระหว่าง SUM และ SUMX (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. สร้าง Measure `[Sales Amount (Iterated)]` ด้วย `SUMX` โดยคำนวณจาก:  
   `FactSales[Quantity] * FactSales[UnitPrice] * ( 1 - FactSales[Discount] )`
2. สร้าง Measure `[Line Cost (Iterated)]` ด้วย `SUMX` โดยนำ `FactSales[Quantity]` คูณกับ `RELATED(DimProduct[StandardCost])`
3. นำ Measure ทั้งสองไปวางเปรียบเทียบกับ `[Sales Amount]` และ `[Total Cost]` เดิมใน Matrix เพื่อตรวจสอบความแตกต่างของตัวเลข

### เฉลยสูตร
```dax
Sales Amount (Iterated) =
SUMX (
    FactSales,
    FactSales[Quantity] * FactSales[UnitPrice] * ( 1 - FactSales[Discount] )
)

Line Cost (Iterated) =
SUMX (
    FactSales,
    FactSales[Quantity] * RELATED ( DimProduct[StandardCost] )
)
```

### การสังเกตและเกณฑ์การผ่าน
- ตัวเลข `[Sales Amount]` และ `[Sales Amount (Iterated)]` จะมีค่าเท่ากันอย่างสมบูรณ์ (เพราะคอลัมน์ `SalesAmount` ถูกคำนวณด้วยสูตรเดียวกันไว้ล่วงหน้าแล้ว)
- ตัวเลข `[Line Cost (Iterated)]` จะมีความแตกต่างจาก `[Total Cost]` เล็กน้อยในบางรายการ เนื่องจากในโมเดล Northwind DW นี้ ต้นทุนจริงหน้างาน (`LineCost`) สะท้อนราคาต้นทุน ณ วันที่เกิดรายการจริง ซึ่งอาจมีการเปลี่ยนแปลงไปจากราคามาตรฐานปัจจุบัน (`StandardCost`) ในตารางสินค้า

---

**บทเรียนถัดไป:** [06 — Logical, Text, Date](06-logical-text-date.md)
"""


def get_lesson_06() -> str:
    return """
# 06 — Logical, Text, Date

**เป้าหมาย:** ใช้ฟังก์ชันตรรกะแบบหลายเงื่อนไขด้วย `SWITCH ( TRUE () )` เพื่อทดแทน Nested IF ที่ซับซ้อน, ใช้งานฟังก์ชันข้อความและการจัดรูปแบบด้วย `FORMAT`, และเข้าใจการทำงานกับค่าว่าง (`BLANK`) ใน DAX  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 05 เรียบร้อยแล้ว

---

## เลิกใช้ Nested IF แล้วเปลี่ยนมาใช้ `SWITCH ( TRUE () )`

เมื่อเราต้องเขียนเงื่อนไขทางธุรกิจที่มีการตัดเกรดหรือแบ่งช่วงตัวเลขหลายระดับ เช่น การแบ่งกลุ่มราคาสินค้า:
- ถ้าน้อยกว่า 20 ให้เป็น "Budget"
- ถ้าน้อยกว่า 50 ให้เป็น "Standard"
- ถ้ามากกว่านั้นให้เป็น "Premium"

หากเขียนด้วยฟังก์ชัน `IF` ซ้อนกันหลายชั้น (Nested IF):
```dax
// อ่านยาก แก้ไขยาก วงเล็บซ้อนกันจนตาลาย
PriceTier = IF ( DimProduct[ListPrice] < 20, "Budget", IF ( DimProduct[ListPrice] < 50, "Standard", "Premium" ) )
```

> 💡 **คิดภาพตามง่ายๆ (Mental Model): บันไดตรวจสอบความจริงทีละขั้น**  
> รูปแบบ `SWITCH ( TRUE (), ... )` เปรียบเสมือนการเดินลงบันไดตรวจสอบเงื่อนไขทีละขั้นอย่างเป็นระเบียบ  
> คำว่า `TRUE()` ที่ใส่ไว้ตัวแรก บอกระบบว่า **"ให้เริ่มเดินเช็คเงื่อนไขตั้งแต่บรรทัดแรก บรรทัดไหนที่ให้ผลลัพธ์เป็นจริง (TRUE) เป็นข้อแรก ให้หยิบคำตอบนั้นไปใช้ทันที แล้วหยุดเดินทันที!"**

```dax
// อ่านง่าย สบายตา จัดระเบียบง่าย และเป็นมาตรฐานระดับมืออาชีพ
PriceTier = 
SWITCH ( 
    TRUE (), 
    DimProduct[ListPrice] < 20, "Budget", 
    DimProduct[ListPrice] < 50, "Standard", 
    "Premium" 
)
```

---

## การจัดการกับข้อความและวันที่ด้วย `FORMAT()`

ฟังก์ชัน `FORMAT` ใช้สำหรับแปลงค่าตัวเลขหรือวันที่ให้ออกมาเป็นข้อความตามรูปแบบที่เราต้องการ:
```dax
// แปลงวันที่ให้อยู่ในรูป ปี-เดือน เช่น "1997-05"
YearMonth = FORMAT ( DimDate[Date], "YYYY-MM" )
```

> ⚠️ **ข้อควรระวังสำคัญสำหรับ BI Developer:**  
> ผลลัพธ์ที่ได้จากฟังก์ชัน `FORMAT()` จะกลายเป็น **ข้อความ (Text)** เสมอ!  
> ถ้าคุณนำคอลัมน์ที่ได้จาก `FORMAT(Date, "YYYY-MM")` ไปใส่ในกราฟ คอมพิวเตอร์จะมองเป็นข้อความธรรมดา ทำให้ไม่สามารถใช้คุณสมบัติของระบบวิเคราะห์วันเวลา (Time Intelligence) ได้อย่างสมบูรณ์ และการเรียงลำดับอาจผิดเพี้ยนหากไม่ตั้งค่า Sort by Column ควบคู่ไปด้วย

---

## ทำความเข้าใจค่า `BLANK()` ใน DAX

ในภาษา DAX ค่าว่างหรือ **`BLANK()`** มีพฤติกรรมพิเศษที่แตกต่างจากภาษาอื่น:
- `BLANK()` ไม่ใช่เลขศูนย์ `0`
- `BLANK()` ไม่ใช่ข้อความว่าง `""`
- แต่มันเปรียบเหมือน **"กล่องเปล่าที่ยังไม่ได้ใส่ข้อมูล"**

**พฤติกรรมทางคณิตศาสตร์ของ BLANK:**
- ในการคำนวณบวกลบคูณหาร: `BLANK() + 10` จะได้ผลลัพธ์เป็น `10` (ประพฤติตัวเสมือน 0 ชั่วคราว)
- ในการต่อข้อความ: `BLANK() & "Text"` จะได้ผลลัพธ์เป็น `"Text"`
- ในการแสดงผลบน Visual: แถวที่มีค่าเป็น `BLANK()` จะถูกซ่อนออกจากตารางโดยอัตโนมัติ ช่วยให้รายงานดูสะอาดตา ไม่แสดงแถวที่ไม่มีข้อมูลให้รกสายตา

---

## Lab 06 — สร้างคอลัมน์ตัดเกรดและจัดรูปแบบ (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. ในตาราง `DimProduct` สร้าง Calculated Column ชื่อ `PriceTier` เพื่อแบ่งกลุ่มสินค้าระดับราคา:
   - ต่ำกว่า 20: `"Budget"`
   - ต่ำกว่า 50: `"Standard"`
   - ตั้งแต่ 50 ขึ้นไป: `"Premium"`
2. ในตาราง `DimDate` สร้าง Calculated Column ชื่อ `YearMonth` โดยใช้ฟังก์ชัน `FORMAT` ในรูปแบบ `"YYYY-MM"`
3. นำ `PriceTier` ไปสร้างเป็น Slicer และทดสอบกรองยอดขาย `[Sales Amount]`

### เฉลยสูตร
```dax
// 1. ตาราง DimProduct
PriceTier =
SWITCH (
    TRUE (),
    DimProduct[ListPrice] < 20, "Budget",
    DimProduct[ListPrice] < 50, "Standard",
    "Premium"
)

// 2. ตาราง DimDate
YearMonth = FORMAT ( DimDate[Date], "YYYY-MM" )
```

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- คอลัมน์ `PriceTier` ให้ผลลัพธ์ตรงตามเงื่อนไขราคาของสินค้าทุกชิ้น
- สามารถใช้ Slicer `PriceTier` กรองยอดขายในตารางได้อย่างสมบูรณ์

---

**บทเรียนถัดไป:** [07 — RELATED และ Relationships](07-related-and-relationships.md)
"""


def get_lesson_07() -> str:
    return """
# 07 — RELATED และ Relationships

**เป้าหมาย:** ใช้งานฟังก์ชัน `RELATED` และ `RELATEDTABLE` เพื่อดึงข้อมูลข้ามตารางได้อย่างถูกต้องตามทิศทางความสัมพันธ์, เข้าใจความแตกต่างระหว่าง Active และ Inactive Relationships, และรู้วิธีรับมือกับสถานการณ์ Role-Playing Dimensions  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 06 เรียบร้อยแล้ว

---

## การเดินทางข้ามตาราง: `RELATED` vs `RELATEDTABLE`

เมื่อเรากำลังทำงานอยู่ในแถวใดแถวหนึ่ง (Row Context) แล้วต้องการหยิบข้อมูลจากอีกตารางหนึ่งมาใช้ เราไม่สามารถพิมพ์ชื่อคอลัมน์ของตารางอื่นตรงๆ ได้ แต่ต้องใช้สะพานเชื่อมโยงตามทิศทางความสัมพันธ์:

```
[ตารางข้อมูลอ้างอิง Dim] (ฝั่ง One: เลข 1)
         ▲
         │   RELATED (เดินขึ้นไปหาฝั่ง One ได้ค่าเดี่ยวเสมอ)
         │   ─────────────────────────────────────────────
         │   RELATEDTABLE (เดินลงมาหาฝั่ง Many ได้ตารางหลายแถว)
         ▼
  [ตารางรายการ Fact] (ฝั่ง Many: เครื่องหมายดอกจัน *)
```

### 1. ฟังก์ชัน `RELATED` (เดินจากฝั่ง Many ไปหาฝั่ง One)
ใช้เมื่อเราอยู่ที่ตารางฝั่ง Many (เช่น `FactSales`) แล้วต้องการขอดูข้อมูลจากฝั่ง One (เช่น `DimProduct`)

> 💡 **คิดภาพตามง่ายๆ (Mental Model): การเปิดสมุดทะเบียนประวัติ**  
> นึกภาพว่าคุณกำลังถือ **ใบเสร็จขายสินค้า (Fact)** อยู่ในมือ ในใบเสร็จมีรหัสสินค้า `ProductKey = 14`  
> คุณอยากรู้ว่า "สินค้าชิ้นนี้มีต้นทุนมาตรฐานเท่าไหร่?"  
> คุณจึงเงยหน้าขึ้นแล้วเดินไป **เปิดสมุดแคตตาล็อกสินค้า (Dimension)** เพื่อเปิดดูหน้าที่ 14  
> เนื่องจากสินค้า 1 รหัส มีคุณลักษณะได้เพียงแบบเดียวเสมอ (**Many-to-One**) คุณจึงได้คำตอบกลับมาเป็น **ค่าเดี่ยวๆ (Single Value)** อย่างแน่นอนเสมอ จึงใช้คำสั่ง `RELATED ( DimProduct[StandardCost] )` ได้ทันที

### 2. ฟังก์ชัน `RELATEDTABLE` (เดินจากฝั่ง One ไปหาฝั่ง Many)
ใช้เมื่อเราอยู่ที่ตารางฝั่ง One (เช่น `DimCustomer`) แล้วต้องการดูว่ามีรายการในฝั่ง Many เกี่ยวข้องกับแถวนี้กี่รายการ

> 💡 **คิดภาพตามง่ายๆ (Mental Model): การค้นประวัติการซื้อของลูกค้า**  
> ผู้จัดการกำลังเปิดดูหน้าของ "ลูกค้าบริษัท ก" ในสมุดทะเบียนลูกค้า แล้วถามว่า "ลูกค้าคนนี้เคยซื้อของกับเราไปกี่ครั้ง?"  
> เนื่องจากลูกค้า 1 คน สามารถซื้อของได้หลายครั้ง (**One-to-Many**) คำตอบที่ได้กลับมาจึงไม่ใช่ตัวเลขตัวเดียว แต่ได้กลับมาเป็น **"ตารางทั้งก้อน" (Table of rows)** ที่รวบรวมใบเสร็จทั้งหมดของลูกค้ารายนี้เอาไว้ เราจึงต้องนำไปครอบด้วยฟังก์ชันนับ เช่น `COUNTROWS ( RELATEDTABLE ( FactSales ) )`

---

## เส้นเชื่อมโยงแบบ Active vs. Inactive (สะพานหลัก vs. สะพานสำรอง)

ในชีวิตจริงของการวิเคราะห์ข้อมูล ธุรกิจมักมีมิติเวลาที่เกี่ยวข้องกับธุรกรรมมากกว่า 1 วันที่ (เรียกว่า **Role-Playing Dimensions**) เช่น ในตาราง `FactSales`:
1. `OrderDateKey` = วันที่ลูกค้ากดสั่งซื้อ
2. `RequiredDateKey` = วันที่ลูกค้าต้องการให้ส่งถึงมือ
3. `ShippedDateKey` = วันที่บริษัทจัดส่งสินค้าออกจากคลังจริง

**กฎเหล็กของ Power BI:**  
ระหว่างตารางสองตารางเดียวกัน สามารถมีเส้นเชื่อมโยงที่เปิดใช้งาน (**Active Relationship**) ได้เพียง **1 เส้นเท่านั้น** (แสดงด้วยเส้นทึบ) ส่วนเส้นอื่นๆ จะต้องเป็นเส้นสำรองที่ปิดอยู่ (**Inactive Relationship** แสดงด้วยเส้นประ) ทั้งนี้เพื่อป้องกันไม่ให้เกิดความกำกวมในการไหลของฟิลเตอร์

> 💡 **คิดภาพตามง่ายๆ (Mental Model): สะพานข้ามแม่น้ำแบบพับเก็บได้**  
> - **Active Relationship (เส้นทึบ):** คือ **"สะพานหลักข้ามแม่น้ำ"** ที่เปิดให้รถสัญจรตามปกติ ตัวกรองจาก `DimDate` จะวิ่งข้ามสะพานนี้ไปยัง `OrderDateKey` เสมอ  
> - **Inactive Relationship (เส้นประ):** คือ **"สะพานพับฉุกเฉิน"** ที่ปกติจะยกค้างไว้ ไม่เปิดให้รถทั่วไปวิ่งผ่าน  
> - เมื่อไหร่ก็ตามที่ผู้บริหารต้องการดู "ยอดขายตามวันที่ส่งของจริง (Shipped Date)" BI Developer จะกดปุ่มสั่งการพิเศษผ่านคำสั่ง `USERELATIONSHIP` ในฟังก์ชัน `CALCULATE` เพื่อลดสะพานพับนี้ลงมาใช้งานเฉพาะกิจในสูตรนั้น! (จะได้ลงมือทำในบทที่ 09)

---

## Lab 07 — ทดลองดึงข้อมูลข้ามตารางและนับแถว (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. ในตาราง `DimCustomer` สร้าง Calculated Column ชื่อ `LifetimeOrderLines` เพื่อนับจำนวนรายการสินค้าที่ลูกค้ารายนั้นเคยซื้อ โดยใช้ `COUNTROWS` ร่วมกับ `RELATEDTABLE`
2. ตรวจสอบหน้า Model view เพื่อยืนยันว่าเส้นเชื่อมระหว่าง `FactSales` ไปยัง `DimDate` มีเส้นทึบ 1 เส้น (`OrderDateKey`) และเส้นประ 2 เส้น (`RequiredDateKey`, `ShippedDateKey`)

### เฉลยสูตร
```dax
LifetimeOrderLines = COUNTROWS ( RELATEDTABLE ( FactSales ) )
```

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- คอลัมน์ `LifetimeOrderLines` บน `DimCustomer` แสดงตัวเลขจำนวนแถวของลูกค้าแต่ละรายได้ถูกต้อง (ลูกค้าที่ซื้อบ่อยจะมีตัวเลขสูง ลูกค้าที่ไม่เคยซื้อจะมีค่าเป็น BLANK)

---

**บทเรียนถัดไป:** [08 — Date Table](08-date-table.md)
"""


def get_lesson_08() -> str:
    return """
# 08 — Date Table

**เป้าหมาย:** เข้าใจความสำคัญของตารางวันที่ (Date Table) ต่อการวิเคราะห์ข้อมูล, ปฏิบัติตามกฎเหล็ก 4 ประการของ Date Table เพื่อให้สูตร Time Intelligence ทำงานได้อย่างแม่นยำ, และเข้าใจบทบาทของปีงบประมาณ (Fiscal Calendar)  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 07 เรียบร้อยแล้ว

---

## ทำไมตารางวันที่ (Date Table) จึงเป็นหัวใจของระบบ BI?

ในการวิเคราะห์ข้อมูลธุรกิจ คำถามส่วนใหญ่ของผู้บริหารมักผูกติดกับกาลเวลาเสมอ เช่น:
- "ยอดขายเดือนนี้เทียบกับเดือนเดียวกันของปีที่แล้ว (**Same Period Last Year**) เป็นอย่างไร?"
- "ยอดขายสะสมตั้งแต่ต้นปีจนถึงปัจจุบัน (**Year-To-Date : YTD**) โตขึ้นกี่เปอร์เซ็นต์?"

สูตรคำนวณวันเวลาเหล่านี้ใน DAX จะทำงานได้อย่างถูกต้อง **ก็ต่อเมื่อมีตารางปฏิทินที่สมบูรณ์แบบ 100% ให้อ้างอิงเท่านั้น**  
ถ้าเราใช้วันที่จากตารางยอดขาย (`FactSales[OrderDate]`) ตรงๆ วันที่บางวันอาจจะแหว่งไป (เช่น วันหยุดเสาร์-อาทิตย์ หรือวันที่ไม่มีการขาย) ซึ่งจะทำให้ฟังก์ชันคำนวณเวลาของ DAX ทำงานล้มเหลวทันที!

---

## กฎเหล็ก 4 ประการของ Date Table มาตรฐานสากล

ตารางที่จะนำมาใช้เป็น Date Table ใน Power BI ต้องมีคุณสมบัติครบทั้ง 4 ข้อดังนี้:

1. **ต้องมีคอลัมน์ที่เป็นชนิดข้อมูล Date แท้:** (DataType = Date หรือ DateTime)
2. **วันที่ต้องเรียงต่อเนื่องกันไม่ขาดตอน (Contiguous Dates):** ต้องมีวันครบทุกวันตั้งแต่วันเริ่มต้นจนถึงวันสิ้นสุด ห้ามมีวันใดตกหล่นแม้แต่วันเดียว
3. **ห้ามมีวันที่ซ้ำกัน (Unique Dates):** แต่ละวันต้องปรากฏเพียงแถวเดียวในตาราง
4. **ต้องประกาศเป็นทางการ (Mark as Date Table):** ต้องคลิกขวาที่ตารางแล้วเลือกคำสั่ง "Mark as date table" ใน Power BI Desktop

> 💡 **คิดภาพตามง่ายๆ (Mental Model): ปฏิทินติดผนังที่ห้ามฉีกหน้าทิ้ง**  
> ลองนึกถึงปฏิทินติดผนังบ้านของคุณ แม้ว่าวันเสาร์-อาทิตย์คุณจะนอนอยู่บ้านโดยไม่ได้ออกไปซื้อของ คุณก็ **ห้ามฉีกช่องวันเสาร์-อาทิตย์ทิ้งเด็ดขาด**  
> ปฏิทินต้องมีวันที่ 1, 2, 3... ครบทั้ง 365 วันอย่างเป็นระเบียบ เพื่อให้เวลาที่เรานับย้อนหลังว่า "30 วันที่แล้วคือวันไหน" เราจะได้คำตอบที่ถูกต้องตรงกับความเป็นจริงเสมอ

---

## ปฏิทินสากล (Calendar) เทียบกับ ปีงบประมาณ (Fiscal Calendar)

ในหลายองค์กรและหน่วยงาน รอบระยะเวลาบัญชีไม่ได้เริ่มต้นวันที่ 1 มกราคมเหมือนปฏิทินทั่วไป  
ในชุดข้อมูล **Northwind DW** ของเรา ได้ออกแบบให้มีคอลัมน์รองรับ **ปีงบประมาณ (Fiscal Year)** ไว้ล่วงหน้า:
- **เริ่มต้นปีงบประมาณ:** วันที่ **1 ตุลาคม** ของทุกปี
- ในตาราง `DimDate` จึงมีคอลัมน์คู่ขนานกัน:
  - `Year` (ปีปฏิทินปกติ) vs `FiscalYear` (ปีงบประมาณ เช่น FY1997)
  - `Quarter` (ไตรมาสปกติ Q1-Q4) vs `FiscalQuarter` (ไตรมาสงบประมาณ)

ความพร้อมของตาราง `DimDate` นี้ ทำให้เราสามารถสลับมุมมองรายงานของผู้บริหารระหว่าง "ปีปฏิทิน" และ "ปีงบประมาณ" ได้ทันทีเพียงแค่เปลี่ยนฟิลด์ใน Slicer

---

## Lab 08 — ตรวจสอบความสมบูรณ์ของ Date Table (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. ไปที่ตาราง `DimDate` ในมุมมอง Data view เพื่อตรวจดูคอลัมน์ `Date`, `Year`, `MonthName`, `FiscalYear`, `FiscalQuarter`
2. ตรวจสอบว่าคอลัมน์ `MonthName` ได้รับการตั้งค่า **Sort by column** ด้วย `MonthKey` แล้วหรือไม่
3. ตรวจสอบสถานะการเป็น Date Table อย่างเป็นทางการของตาราง `DimDate`

### แนวทางการตรวจสอบ
- คลิกขวาที่ตาราง `DimDate` ในรายการตารางด้านขวา → เมนูย่อยจะต้องปรากฏข้อความว่า **"Mark as date table"** และเมื่อกดเข้าไปจะเห็นว่าถูกผูกไว้กับคอลัมน์ `Date` เรียบร้อยแล้ว
- เมื่อนำ `FiscalYear` และ `FiscalQuarter` ไปวางใน Matrix คู่กับ `[Sales Amount]` ตัวเลขยอดขายจะต้องถูกแบ่งกลุ่มตามรอบปีงบประมาณอย่างถูกต้อง

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- ตาราง `DimDate` ผ่านคุณสมบัติ Date Table ครบทั้ง 4 ประการ
- การแสดงผลชื่อเดือนในทุก Visual เรียงตามลำดับเวลาถูกต้องเสมอ

---

**บทเรียนถัดไป:** [09 — CALCULATE](09-calculate.md)
"""


def get_lesson_09() -> str:
    return """
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
"""


def get_lesson_16() -> str:
    return """
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
"""


def get_lesson_10() -> str:
    return """
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
"""


def get_lesson_11() -> str:
    return """
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
"""


def get_lesson_12() -> str:
    return """
# 12 — Field Parameters

**เป้าหมาย:** สร้างความยืดหยุ่นระดับสูงสุดให้กับประสบการณ์ผู้ใช้งานรายงาน (Reporting UX) ด้วย **Field Parameters**, รู้วิธีเปิดโอกาสให้ผู้บริหารกดสลับแกนกราฟหรือสลับตัวชี้วัดได้เองอย่างอิสระ, และเข้าใจความแตกต่างระหว่าง Field Parameters กับ Calculation Groups  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 11 เรียบร้อยแล้ว

---

## Field Parameters คืออะไร?

ในอดีต หากผู้บริหารอยากดูกราฟยอดขายแบ่งตาม "หมวดหมู่สินค้า" (Category) แต่ผู้จัดการฝ่ายบุคคลอยากดูกราฟยอดขายเดียวกันนั้นแบ่งตาม "ชื่อพนักงานขาย" (Employee) และผู้จัดการฝ่ายขายอยากดูตาม "ประเทศลูกค้า" (Country)  
BI Developer จะต้องสร้างกราฟหน้าตาเหมือนกันเป๊ะซ้ำๆ กันถึง 3 กราฟ แล้วใช้ปุ่ม Bookmark ซ่อนเปิด-ปิดอย่างยากลำบาก

**Field Parameters** เข้ามาแก้ปัญหานี้อย่างสง่างาม โดยเปิดโอกาสให้เราสร้าง **"สวิตช์ปุ่มกด"** ให้ผู้ใช้เลือกได้เองบนหน้าจอว่าอยากให้แกนของกราฟ หรือตัวชี้วัดในตาราง เปลี่ยนไปแสดงข้อมูลคอลัมน์ใด!

> 💡 **คิดภาพตามง่ายๆ (Mental Model): สวิตช์เลือกช่องบนหน้าปัดรถยนต์**  
> Field Parameter เปรียบเหมือน **"ปุ่มหมุนเปลี่ยนโหมดบนหน้าปัดรถยนต์"**  
> หน้าจอด้านหน้ามีจอเดียว แต่คุณสามารถกดเลือกว่าจะให้โชว์ "ความเร็วรถ", "อัตราสิ้นเปลืองน้ำมัน", หรือ "แผนที่นำทาง" ได้ตามใจชอบ โดยไม่ต้องติดตั้งหน้าจอเพิ่ม 3 อันให้เกะกะรถ

---

## เบื้องหลังการทำงาน: ฟังก์ชัน `NAMEOF()`

เมื่อเราสร้าง Field Parameter ผ่านเมนู Modeling ใน Power BI Desktop โปรแกรมจะสร้างตารางพิเศษขึ้นมา ซึ่งใช้ฟังก์ชัน `NAMEOF()` ในการชี้พิกัดไปยังคอลัมน์หรือ Measure:

```dax
Selectable Dimensions = {
    ( "Product Category", NAMEOF ( DimProduct[Category] ), 0 ),
    ( "Customer Country", NAMEOF ( DimCustomer[Country] ), 1 ),
    ( "Sales Employee", NAMEOF ( DimEmployee[FullName] ), 2 )
}
```

- **ชื่อที่แสดง:** `"Product Category"` คือข้อความสวยงามที่จะปรากฏบนปุ่ม Slicer
- **พิกัดคอลัมน์:** `NAMEOF(...)` เป็นตัวบอกระบบอย่างชัดเจนว่ากำลังอ้างถึงฟิลด์ใดในโมเดล
- **ลำดับ:** ตัวเลข `0, 1, 2` ใช้สำหรับควบคุมการเรียงลำดับปุ่มบนหน้าจอ

---

## ตารางเปรียบเทียบ: Field Parameters vs Calculation Groups

สองฟีเจอร์นี้เป็นเครื่องมือระดับโปรทั้งคู่ แต่มีหน้าที่และจุดประสงค์ทางสถาปัตยกรรมต่างกันอย่างชัดเจน:

| คุณสมบัติ | Field Parameters | Calculation Groups |
| :--- | :--- | :--- |
| **หน้าที่หลัก** | สลับ **Field / Column** หรือสลับแกนกราฟ | สลับและแปลง **ตรรกะการคำนวณ (Calculation Logic)** ของ Measure |
| **สิ่งที่กระทำ** | นำคอลัมน์มาสลับวางบน Visual Axis หรือ Legend | นำสูตรคณิตศาสตร์ (เช่น YTD, YoY) ไปสวมทับ Measure |
| **การสร้าง** | สร้างได้ง่ายจากเมนู **Modeling → New parameter → Fields** ใน Desktop | สร้างในหน้า Model view (ต้องการการควบคุม Format String และความเข้าใจ DAX) |

---

## Lab 12 — สร้าง Dynamic Axis ด้วย Field Parameters (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. ไปที่เมนู **Modeling → New parameter → Fields**
2. ตั้งชื่อ Parameter ว่า `Dimension Selector`
3. ลากฟิลด์ต่อไปนี้เข้ามาร่วมในรายการ:  
   - `DimProduct[Category]`  
   - `DimCustomer[Country]`  
   - `DimEmployee[FullName]`
4. นำ Slicer ที่ได้ไปวางบนหน้ารายงาน
5. สร้างกราฟแท่ง (Bar Chart): นำ `Dimension Selector` ไปวางที่แกน X-Axis และนำ `[Sales Amount]` ไปวางที่ Y-Axis
6. ทดสอบคลิกปุ่มบน Slicer สลับไปมาระหว่าง Category, Country, และ FullName

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- เมื่อคลิกเปลี่ยนปุ่มบน Slicer แกนกราฟจะเปลี่ยนการจัดกลุ่มข้อมูลทันทีโดยที่กราฟยังแสดงตัวเลขยอดขายรวมได้อย่างถูกต้อง

---

**บทเรียนถัดไป:** [13 — What-if](13-what-if.md)
"""


def get_lesson_13() -> str:
    return """
# 13 — What-if Parameters

**เป้าหมาย:** สร้างแบบจำลองสถานการณ์ทางธุรกิจ (Scenario Analysis / Sensitivity Testing) ด้วย **What-if Parameters**, เข้าใจบทบาทของตารางลอยแบบตัดขาดความสัมพันธ์ (**Disconnected Table**), และนำค่าพารามิเตอร์ไปจำลองผลกระทบต่อยอดขายและกำไรของบริษัท  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 12 เรียบร้อยแล้ว

---

## การวิเคราะห์สถานการณ์จำลอง (What-if Analysis) คืออะไร?

ในงานของ Business Analyst และ Data Analyst งานที่สร้างมูลค่าสูงสุดให้กับฝ่ายบริหารคือการตอบคำถามประเภท:
- *"ถ้าปีหน้าเราขึ้นราคาสินค้า 5% ยอดขายและกำไรของเราจะเปลี่ยนไปเป็นเท่าไหร่?"*
- *"ถ้าต้นทุนการผลิตเพิ่มขึ้น 10% เราจะยังเหลือกำไรอยู่กี่บาท?"*

คำถามเหล่านี้ไม่สามารถตอบได้ด้วยข้อมูลยอดขายในอดีตเพียงอย่างเดียว แต่ต้องการ **"ตัวแปรจำลอง"** ที่ผู้บริหารสามารถปรับหมุนตัวเลขขึ้นลงเพื่อดูผลลัพธ์ได้แบบ Real-time

> 💡 **คิดภาพตามง่ายๆ (Mental Model): ลูกบิดปรับระดับเสียง**  
> What-if Parameter เปรียบเสมือน **"ลูกบิดหมุนปรับเสียงบนแอมพลิฟายเออร์"**  
> คุณสามารถเลื่อนสไลเดอร์เพื่อหมุนปรับตัวเลขจำลอง เช่น ปรับส่วนลด 0%, 5%, 10%, 15% แล้วระบบจะคำนวณผลกระทบทางธุรกิจออกมาให้เห็นทันที

---

## Disconnected Table: ตารางลอยที่ต้องไม่มีเส้นเชื่อมโยง

เบื้องหลังของ What-if Parameter คือการสร้างตารางจำลองตัวเลขขึ้นมา 1 ตาราง ด้วยฟังก์ชัน `GENERATESERIES`:

```dax
Price Adjustment = GENERATESERIES ( -0.20, 0.20, 0.05 )
```
สูตรนี้จะสร้างรายการตัวเลขตั้งแต่ -20% ถึง +20% โดยขยับทีละ 5%

> ⚠️ **กฎเหล็กทางสถาปัตยกรรม (Architecture Rule):**  
> ตาราง What-if Parameter จะต้องเป็น **Disconnected Table (ตารางอิสระที่ห้ามลากเส้นเชื่อมโยง Relationship กับตารางใดๆ ในโมเดลเด็ดขาด)**  
> เพราะถ้าเราเผลอไปเชื่อมความสัมพันธ์ ตัวเลขจำลองจะวิ่งไปกรองข้อมูลจริงในอดีตจนเสียหาย การปล่อยให้มันลอยอยู่อย่างอิสระ จะทำให้เราสามารถนำค่าที่ผู้ใช้เลือกไปคำนวณจำลองสถานการณ์ได้อย่างปลอดภัย 100%

---

## การดึงค่าพารามิเตอร์มาใช้ใน Measure ด้วย `SELECTEDVALUE()`

เมื่อผู้ใช้เลื่อนสไลเดอร์บนหน้าจอ เราจะอ่านค่าที่ผู้ใช้เลือกด้วยคำสั่ง `SELECTEDVALUE`:

```dax
// 1. อ่านค่าที่ผู้บริหารกำลังเลือกบน Slider (ถ้าไม่เลือกให้ถือเป็น 0)
Price Adjustment Value = SELECTEDVALUE ( 'Price Adjustment'[Price Adjustment], 0 )

// 2. นำไปจำลองยอดขายใหม่
Sales Amount (What-if) = 
[Sales Amount] * ( 1 + [Price Adjustment Value] )

// 3. นำไปจำลองกำไรใหม่ (สมมติให้ต้นทุนจริงคงที่)
Profit (What-if) = 
[Sales Amount (What-if)] - [Total Cost]
```

---

## Lab 13 — สร้างระบบจำลองการปรับราคาสินค้า (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. ไปที่เมนู **Modeling → New parameter → Numeric range**
2. ตั้งค่าพารามิเตอร์:
   - ชื่อ: `Price Adjustment`
   - Data type: `Decimal number`
   - Minimum: `-0.20`
   - Maximum: `0.20`
   - Increment: `0.05`
   - Default: `0.00`
3. ตรวจสอบว่ามี Slicer แบบ Slider ปรากฏขึ้นบนหน้ารายงาน
4. สร้าง Measure `[Sales Amount (What-if)]` และ `[Profit (What-if)]` ตามสูตรด้านบน
5. นำ Card Visual แสดง `[Sales Amount]` เทียบกับ `[Sales Amount (What-if)]` และทดสอบเลื่อนสไลเดอร์ไปที่ `+10%`

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- เมื่อเลื่อนสไลเดอร์ไปที่ `+10%` (0.10) ตัวเลขบน Card `[Sales Amount (What-if)]` จะต้องมีค่าเพิ่มขึ้นจากยอดขายเดิม 10% อย่างถูกต้อง

---

**บทเรียนถัดไป:** [14 — Visual Calculations](14-visual-calculations.md)
"""


def get_lesson_14() -> str:
    return """
# 14 — Visual Calculations (ภาคผนวก)

**เป้าหมาย:** ทำความเข้าใจนวัตกรรมใหม่ของ Power BI: **Visual Calculations**, รู้วิธีคำนวณหายอดสะสมหรือผลต่างแถวต่อแถวบนตารางโดยตรงด้วย `RUNNINGSUM`, และรู้ข้อจำกัดในการเลือกใช้งานเมื่อเทียบกับโมเดล DAX ปกติ  
**ข้อกำหนดเบื้องต้น:** จบบทเรียนที่ 13 เรียบร้อยแล้ว

---

## Visual Calculations คืออะไร?

ตลอดทั้งหลักสูตรนี้ เราเรียนรู้การเขียน DAX บน Semantic Model (Calculated Column, Measure, Calculation Groups) ซึ่งเป็นการคำนวณที่อิงกับฐานข้อมูลส่วนกลาง  
แต่นวัตกรรมล่าสุดของ Power BI ได้เพิ่มความสามารถที่เรียกว่า **Visual Calculations (การคำนวณระดับภาพ)** เข้ามา

> 💡 **คิดภาพตามง่ายๆ (Mental Model): การทดเลขบนกระดานไวท์บอร์ด**  
> - **DAX ปกติ (Model Level):** เหมือนการเดินเข้าไปค้นข้อมูลในคลังเอกสารใหญ่หลังบ้าน แล้วนั่งกดเครื่องคิดเลขคำนวณออกมาใหม่ทั้งหมด  
> - **Visual Calculations:** เหมือนการ **"หยิบปากกาไวท์บอร์ดมาทดเลขบวก-ลบต่อยอดจากตัวเลขที่โชว์อยู่บนกระดานตรงหน้าทันที"**  
> เช่น ตาราง Matrix มีตัวเลขยอดขายของ 12 เดือนโชว์อยู่แล้ว เราแค่อยากหายอดรวมสะสมไล่ลงมาทีละเดือน การคำนวณบนตัวเลขที่เห็นอยู่ตรงหน้าเลยจะทำได้ง่ายและรวดเร็วมาก โดยไม่ต้องเขียนสูตร DAX โมเดลที่ซับซ้อน

---

## ตัวอย่างไวยากรณ์ Visual Calculations

Visual Calculations จะทำงานกับแกนพิกัดของตารางโดยตรง โดยมีฟังก์ชันเฉพาะทาง เช่น:

```dax
// หายอดรวมสะสมตามแถวที่ปรากฏในตาราง
Running Total = RUNNINGSUM ( [Sales Amount] )

// เลื่อนขยับไปดูค่าของแถวก่อนหน้า (คล้าย LAG ใน SQL)
Previous Month Sales = PREVIOUS ( [Sales Amount] )

// คำนวณผลต่างเทียบกับแถวก่อนหน้า
MoM Change = [Sales Amount] - PREVIOUS ( [Sales Amount] )
```

---

## ข้อดีและข้อจำกัดที่ BI Developer ต้องระวัง

| ข้อดีของ Visual Calculations | ข้อจำกัดสำคัญ |
| :--- | :--- |
| 1. เขียนง่าย ไม่ต้องปวดหัวเรื่อง Filter Context ที่ซับซ้อน | 1. **ไม่สามารถนำไปใช้ซ้ำใน Visual อื่นได้** (สูตรติดอยู่เฉพาะในตารางนั้น) |
| 2. ประมวลผลได้เร็วมาก เพราะคิดบนข้อมูลที่ถูกสรุปมาแล้ว | 2. ไม่สามารถนำไปใส่ใน Slicer หรือส่งออกไปเป็น Semantic Model กลางได้ |
| 3. เหมาะมากสำหรับโจทย์ Running Total, Moving Average, หรือ % of Parent | 3. ไม่เหมาะกับตรรกะธุรกิจหลักที่ต้องใช้อ้างอิงร่วมกันทั่วทั้งองค์กร |

---

## Lab 14 — ทดลองสร้าง Visual Calculation (โจทย์ + เฉลย)

### โจทย์ปฏิบัติ
1. สร้างตาราง Matrix: นำ `DimDate[Year]` และ `DimDate[MonthName]` มาวางที่ Rows และนำ `[Sales Amount]` ไปวางที่ Values
2. คลิกที่ตาราง Matrix นั้น → บนแถบเครื่องมือด้านบน เลือก **New visual calculation**
3. พิมพ์สูตร:
```dax
Sales Running Total = RUNNINGSUM ( [Sales Amount] )
```
4. สังเกตคอลัมน์ใหม่ที่ปรากฏใน Matrix

### เกณฑ์การผ่านประเมิน (Pass Criteria)
- คอลัมน์ `Sales Running Total` แสดงตัวเลขยอดขายสะสมทบยอดเพิ่มขึ้นเรื่อยๆ ทีละเดือนได้อย่างถูกต้อง

---

**บทเรียนถัดไป:** [15 — VertiPaq checklist](15-vertipaq-and-performance.md)
"""


def get_lesson_15() -> str:
    return """
# 15 — VertiPaq checklist และการปรับแต่งประสิทธิภาพ

**เป้าหมาย:** เข้าใจสถาปัตยกรรมการจัดเก็บข้อมูลของเอนจิน **VertiPaq** ในหน่วยความจำ, ทำความเข้าใจกลไกการบีบอัดข้อมูลด้วย **Dictionary Encoding** และ **Run-Length Encoding (RLE)**, เข้าใจผลกระทบของ **Cardinality**, และใช้เช็คลิสต์ตรวจเช็คโมเดลก่อนนำขึ้นใช้งานจริงบน Production  
**ข้อกำหนดเบื้องต้น:** ศึกษาเนื้อหาบทเรียนที่ 01 ถึง 14 หรือ 16 ครบถ้วนแล้ว

---

## เบื้องหลังความเร็วระดับเสี้ยววินาที: VertiPaq Engine ทำงานอย่างไร?

เคยสงสัยไหมครับว่า ทำไม Power BI ถึงสามารถสแกน ค้นหา และคำนวณข้อมูลหลายสิบล้านแถวบนแล็ปท็อปธรรมดาๆ ได้อย่างรวดเร็ว?  
คำตอบอยู่ที่เอนจินฐานข้อมูลในแรมที่มีชื่อว่า **VertiPaq** ซึ่งใช้สถาปัตยกรรมแบบ **Columnar In-Memory Database**

### 1. การจัดเก็บข้อมูลแยกตามคอลัมน์ (Columnar Storage)
ฐานข้อมูลแบบเดิม (เช่น SQL ทั่วไป) จะเก็บข้อมูลเรียงทีละแถว (Row-oriented) ทำให้เวลาต้องการหายอดรวมของคอลัมน์เดียว เครื่องต้องอ่านข้อมูลทั้งแถวขึ้นมาทั้งหมด  
แต่ VertiPaq จะ **หั่นเก็บแยกทีละคอลัมน์** ทำให้เวลาสั่ง `SUM ( FactSales[SalesAmount] )` เครื่องจะพุ่งตรงไปอ่านเฉพาะช่องตัวเลขนั้นได้ทันทีโดยไม่ต้องแตะคอลัมน์อื่นเลย

### 2. พจนานุกรมรหัสย่อ (Dictionary Encoding)
ถ้าคอลัมน์ชื่อประเทศมีคำว่า `"Germany"` ซ้ำกัน 1,000,000 แถว...  
VertiPaq จะไม่บันทึกคำว่า `"Germany"` หนึ่งล้านครั้งลงในแรม แต่จะสร้างตารางพจนานุกรมรหัสย่อ:
- `1 = France`
- `2 = Germany`
- `3 = Italy`  
แล้วในตารางข้อมูลจริง จะเก็บเพียงตัวเลขรหัส `2` ซึ่งเป็นตัวเลขขนาดจิ๋ว ช่วยลดขนาดข้อมูลลงได้นับสิบเท่า!

### 3. การบีบอัดแถวที่ซ้ำซ้อน (Run-Length Encoding : RLE)
ถ้ามีรหัส `2` เรียงติดกัน 100,000 แถว ระบบจะไม่บันทึกเลข `2` หนึ่งแสนตัว แต่จะบันทึกข้อความสั้นๆ ว่า: **"มีเลข 2 ซ้ำกันตั้งแต่แถวที่ 1 ถึงแถวที่ 100,000"** ข้อมูลขนาดใหญ่จึงถูกย่อเหลือเพียงไม่กี่ไบต์!

> 💡 **คิดภาพตามง่ายๆ (Mental Model): ตู้เสื้อผ้าที่คัดแยกสีเรียบร้อย**  
> เปรียบเหมือนการจัดตู้เสื้อผ้า ถ้าคุณโยนเสื้อผ้าทุกชนิดคละกันลงในตะกร้า (Row store) เวลาจะหาถุงเท้าสีดำคู่เดียวคุณต้องรื้อผ้าทั้งตะกร้า  
> แต่ถ้าคุณแยกตู้: ตู้ถุงเท้า, ตู้เสื้อยืด, ตู้กางเกง (Columnar store) และพับเรียงตามสี (RLE Compression) คุณจะสามารถหยิบถุงเท้าที่ต้องการได้ทันทีภายใน 1 วินาที!

---

## ศัตรูตัวร้ายอันดับหนึ่งของประสิทธิภาพ: Cardinality

คำว่า **Cardinality** หมายถึง **"จำนวนค่าที่ไม่ซ้ำกัน (Distinct Values) ในคอลัมน์นั้นๆ"**
- **Low Cardinality (ดีเยี่ยม):** เช่น เพศ (มี 2 ค่า), สถานะสินค้า (มี 2 ค่า), วันในสัปดาห์ (มี 7 ค่า) → บีบอัดได้มหาศาล แรมใช้น้อย โมเดลเร็วมาก
- **High Cardinality (อันตราย):** เช่น รหัสธุรกรรมที่ไม่ซ้ำกันเลย (Transaction ID), หรือคอลัมน์วันที่ที่ติดเวลาเป็นระดับวินาที (`2024-05-12 14:23:59`) ซึ่งมีค่าแทบไม่ซ้ำกันเลย ทำให้ VertiPaq ไม่สามารถบีบอัดได้ ต้องสร้างพจนานุกรมขนาดยักษ์ ส่งผลให้ไฟล์ `.pbix` มีขนาดบวมโตและรายงานโหลดช้าลงอย่างเห็นได้ชัด

---

## Production Readiness Checklist (เช็คลิสต์ตรวจความพร้อมของโมเดล)

ก่อนที่คุณจะส่งมอบงานหรือ Publish โมเดลขึ้น Power BI Service ให้ตรวจเช็คตามรายการนี้เสมอ:

- [ ] **1. Star Schema:** โครงสร้างหลักต้องเป็น Fact ล้อมรอบด้วย Dim ไม่เป็น Snowflake หลายชั้น
- [ ] **2. Auto date/time ปิดสนิท:** ตรวจสอบว่าได้ปิด Auto date/time แล้ว และมีตาราง `DimDate` ที่ Mark as Date Table เรียบร้อย
- [ ] **3. ซ่อนคอลัมน์รหัส:** คอลัมน์ `*Key` หรือ Foreign Keys ทั้งหมดต้องถูก Hide ไว้ ไม่ปล่อยให้ผู้ใช้เห็น
- [ ] **4. เปิด Discourage Implicit Measures:** บังคับให้รายงานใช้เฉพาะ Explicit Measure เท่านั้น
- [ ] **5. กำจัดคอลัมน์ High Cardinality ที่ไม่จำเป็น:** ลบคอลัมน์วันที่ที่มีเวลาติดมา หรือแยกชั่วโมง/นาทีออกจากวันที่
- [ ] **6. ใช้ `DIVIDE()` เสมอ:** ตรวจสอบว่าไม่มีสูตรไหนที่ใช้เครื่องหมาย `/` สดๆ เพื่อป้องกัน Error
- [ ] **7. ใช้ Calculation Groups สำหรับ Time Intelligence:** เพื่อลดจำนวน Measure ในโมเดลและทำให้รายงานเป็นระเบียบ

---

## เครื่องมือประจำตัวของ BI Developer ระดับมืออาชีพ

1. **DAX Query View:** หน้าต่างใหม่ใน Power BI Desktop สำหรับทดสอบเขียนคำสั่ง DAX Query (`EVALUATE`) โดยตรง สะดวกรวดเร็วโดยไม่ต้องสร้าง Visual ชั่วคราว
2. **Performance Analyzer:** เมนูในหน้า View เพื่อจับเวลาดูว่า Visual แต่ละชิ้นใช้เวลาประมวลผลกี่มิลลิวินาที (แยกเป็นเวลาของ DAX Query, Visual Display, และเวลาอื่นๆ)
3. **DAX Studio & Tabular Editor:** เครื่องมือภายนอกระดับสากลสำหรับส่องดูขนาดคอลัมน์ในแรม (VertiPaq Analyzer) และบริหารจัดการโมเดลอย่างมืออาชีพ

---

## Lab 15 — ตรวจสอบคุณภาพโมเดลผ่านการทดสอบอัตโนมัติ (โจทย์ + เฉลย)

ในโปรเจกต์นี้ เรามีชุดทดสอบอัตโนมัติด้วย `pytest` เพื่อตรวจเช็คความสอดคล้องของโมเดล Northwind DW และแคตตาล็อกสูตรใน `dax/measures.dax`:

```bash
# รันคำสั่งทดสอบใน Terminal
pytest -q
```

### ผลลัพธ์ที่ต้องการ
- การทดสอบทั้ง 24 รายการต้องผ่านสมบูรณ์ (`24 passed`) ยืนยันว่าโมเดล Star Schema และชุดสูตร DAX ทั้งหมดตรงตามข้อกำหนดและพร้อมใช้งานจริงระดับ Production!

---

**ยินดีด้วย! คุณได้สำเร็จหลักสูตร Power BI DAX & Semantic Model ครบถ้วนทุกบทเรียนอย่างสมบูรณ์**
"""


def main() -> None:
    LESSONS.mkdir(parents=True, exist_ok=True)

    w("README.md", get_readme())
    w("01-star-schema-and-get-data.md", get_lesson_01())
    w("02-dax-syntax-and-context.md", get_lesson_02())
    w("03-calculated-column.md", get_lesson_03())
    w("04-measures.md", get_lesson_04())
    w("05-aggregation-and-iterators.md", get_lesson_05())
    w("06-logical-text-date.md", get_lesson_06())
    w("07-related-and-relationships.md", get_lesson_07())
    w("08-date-table.md", get_lesson_08())
    w("09-calculate.md", get_lesson_09())
    w("16-filter-modifiers-and-context-transition.md", get_lesson_16())
    w("10-time-intelligence.md", get_lesson_10())
    w("11-calculation-groups.md", get_lesson_11())
    w("12-field-parameters.md", get_lesson_12())
    w("13-what-if.md", get_lesson_13())
    w("14-visual-calculations.md", get_lesson_14())
    w("15-vertipaq-and-performance.md", get_lesson_15())


if __name__ == "__main__":
    main()
