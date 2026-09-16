# Archive — แหล่งอ้างอิงโครงเรื่อง (ไม่ใช่ไฟล์สอนหลัก)

## ไฟล์ที่เอาออกจาก repo แล้ว

| รายการ | เหตุผล |
| --- | --- |
| `9EXPERT-Case Study-Power BI DAX-V22/` | ไม่ใช่โมเดลสอน — เคยใช้ครั้งเดียวตอนขยายคอลัมน์เข้า Northwind |
| `Northwind_DW_DimFact.xlsx` ที่ root | ซ้ำกับ [`data/Northwind_DW_DimFact.xlsx`](../data/Northwind_DW_DimFact.xlsx) |

**ต้นทางเดียวของคอร์ส:** [`data/Northwind_DW_DimFact.xlsx`](../data/Northwind_DW_DimFact.xlsx)

## PowerPoint

ไฟล์ `.pptx` ขนาดใหญ่ (~200MB) **ไม่ commit ขึ้น GitHub** (ดู `.gitignore`)

- ใช้ในห้องเป็นโครงเล่าเรื่อง / screenshot UI ได้ — **ไม่จำเป็นต่อการเรียน**
- สูตรและ Lab ครบใน [`docs/lessons/`](../docs/lessons/) (โจทย์รวมเฉลยท้ายแต่ละบท)
- สูตรในสไลด์หลายจุดยังอ้าง `Orders`, `CUSTOMERS`, `PRODUCTS` — **อย่าก๊อป**

## ทำไมไม่ใช้ 9EXPERT เป็นโมเดลหลัก

สรุปสั้น: snowflake + คีย์ข้อความบน fact + datetime หลายคอลัมน์ + float cost high-cardinality — เหมาะเป็น “ยิม DAX” แต่ไม่เหมาะเป็นนิสัย production

ดู [บท 15](../docs/lessons/15-vertipaq-and-performance.md) และ [best practices](../docs/best-practices/README.md)
