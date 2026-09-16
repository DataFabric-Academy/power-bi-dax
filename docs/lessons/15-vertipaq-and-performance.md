# 15 — VertiPaq checklist และเครื่องมือตรวจ

**เป้าหมาย:** ทบทวนนิสัยโมเดลทั้งคอร์สเป็น checklist ที่ตรวจกับไฟล์ `.pbix` ของตัวเองได้  
**ข้อกำหนด:** ทำ lab หลักบท 01–13 แล้ว

---

## Checklist โมเดล (ติ๊กทีละข้อ)

### Modeling

- [ ] Star schema — Fact กลาง, Dim รอบ; ไม่มี snowflake ที่ไม่จำเป็น
- [ ] Integer surrogate keys; ซ่อน `*Key` / FK จาก Report view
- [ ] ปิด Auto date/time
- [ ] Mark `DimDate[Date]` as Date Table; contiguous dates
- [ ] Relationship single-direction เป็นค่าเริ่มต้น; role-playing date = inactive + `USERELATIONSHIP`
- [ ] เงินเป็น Fixed Decimal; ยอด materialize → `SUM`
- [ ] Explicit measures + **Discourage implicit measures**
- [ ] ลบคอลัมน์ที่ไม่ใช้ (ลด cardinality / ขนาดโมเดล)

### DAX authoring

- [ ] คอลัมน์เป็น `Table[Column]`; measure เป็น `[Measure]`
- [ ] `DIVIDE` แทน `/` เมื่อหาร
- [ ] `CALCULATE` ใช้ Boolean filter; `KEEPFILTERS` เมื่อต้องการ intersection
- [ ] เลี่ยง `FILTER ( ทั้งตาราง )` เมื่อไม่จำเป็น
- [ ] `VAR` เมื่อใช้ผลซ้ำ
- [ ] Calculated column เฉพาะ Slicer/กลุ่ม; ไม่พึ่ง `TODAY()` ใน production

### Dynamics

- [ ] Time patterns ซ้ำ → **Calculation groups** ไม่ใช่ YTD คนละตัวต่อ measure
- [ ] สลับ field บน visual → **Field parameters**
- [ ] What-if เป็น disconnected numeric parameter

---

## เครื่องมือ

| เครื่องมือ | ใช้ทำ |
| --- | --- |
| **Performance Analyzer** | จับเวลา visual / DAX query บนหน้ารายงาน |
| **DAX query view** | ทดสอบ measure และ calc items แบบ `EVALUATE` |
| ชีต `_QA` ใน Excel + `pytest` | ยืนยันคุณภาพไฟล์ข้อมูลต้นทาง |

รันใน repo:

```bash
pip install -r requirements.txt
pytest -q
```

คาดหวัง: tests ผ่านครบ (ปัจจุบัน 21 passed)

> อ้าง: [Import data reduction](https://learn.microsoft.com/power-bi/guidance/import-modeling-data-reduction) · [Star schema](https://learn.microsoft.com/power-bi/guidance/star-schema) · [Best practices index](../best-practices/README.md)

---

## Lab 15 — Checklist (โจทย์ + เฉลย)

### โจทย์

1. เปิด `.pbix` ของคุณ ติ๊ก checklist ด้านบนทุกข้อที่เกี่ยวข้อง
2. รัน `pytest -q` ใน repo เพื่อยืนยัน Excel
3. (แนะนำ) Performance Analyzer บน Matrix ที่มี calc group — บันทึกว่า query กลับมา

### เฉลย

ผ่านเมื่อ:

- Checklist โมเดล/DAX/Dynamics ติ๊กครบตามที่สร้างจริง
- `pytest -q` ผ่าน
- มี calc group Time Intelligence ใช้งานกับอย่างน้อย `[Sales Amount]` และ `[Sales Quantity]`

### เกณฑ์ผ่าน

- ไม่มี lab ที่บังคับ snowflake หรือ hash key บน fact
- Discourage implicit measures เปิดอยู่
- จบคอร์สโดยไม่ต้องพึ่งสูตรจากสไลด์

---

**จบชุดบทเรียน** — ดัชนี: [README](README.md) · BP: [../best-practices/README.md](../best-practices/README.md)
