# Semantic Model — ขอบเขตคอร์สและเครื่องมือ

คอร์สนี้โฟกัส **Import semantic model ใน Power BI Desktop** บน Northwind star schema  
ไม่ครอบคลุมรายงาน PBIR เป็นหลัก — แต่ทักษะโมเดลนี้ใช้ต่อกับ **Fabric semantic model** ได้

---

## ชั้นที่สอน vs ไม่สอน

| ชั้น | สอนใน repo | หมายเหตุ |
| --- | --- | --- |
| Tables, relationships, measures, calc columns | ✅ บท 01–16 | แหล่งความจริง: lessons + `dax/` |
| Calculation groups, field parameters | ✅ บท 11–12 | TMDL ตัวอย่างใน `dax/calculation-groups.tmdl` |
| Report pages / visuals | ⚠️ เฉพาะที่ lab อ้าง | Skills PBIR อยู่ `.cursor/skills/powerbi-report-*` |
| DirectQuery / Direct Lake | 📎 อ้าง Learn | แนวคิด materialize ยังใช้กับ Import |
| RLS, object-level security | 📎 ไม่มี lab | ดู [RLS](https://learn.microsoft.com/power-bi/admin/service-admin-rls) |
| Prep for AI / Copilot | 📎 บท 15 + [Semantic model best practices](https://learn.microsoft.com/fabric/data-science/semantic-model-best-practices) | หลังโมเดล stable |

---

## Workflow แนะนำ (นักเรียน)

1. Get Data จาก Excel ตาม [บท 01](../lessons/01-star-schema-and-get-data.md)
2. สร้าง measures ตาม [`dax/measures.dax`](../../dax/measures.dax) ทีละบท
3. เปิด **DAX query view** ทดสอบ:

```dax
EVALUATE
ROW (
    "Sales", [Sales Amount],
    "YTD", CALCULATE ( [Sales Amount], DATESYTD ( DimDate[Date] ) )
)
```

4. ก่อนบท 11: **Discourage implicit measures** + Mark date table
5. สร้าง calculation group จาก [`dax/calculation-groups.tmdl`](../../dax/calculation-groups.tmdl) (Model view หรือ TMDL)

---

## Workflow maintainer (Cursor + MCP)

1. เปิด workspace นี้ใน Cursor — MCP: [`powerbi-modeling-mcp`](../../.cursor/mcp.json)
2. เชื่อมต่อเป้าหมาย: Desktop `.pbix` / Fabric workspace / PBIP `definition`
3. หลัง MCP แก้โมเดล: sync กลับ `dax/measures.dax` และบทเรียนที่เกี่ยวข้อง
4. Rule: [`.cursor/rules/powerbi-modeling-mcp.mdc`](../../.cursor/rules/powerbi-modeling-mcp.mdc)

Skill ลึก: `.cursor/skills/semantic-model-authoring/` (Microsoft skills-for-fabric)

---

## PBIP / Git (ภาคผนวก)

ถ้าต้องการ version โมเดลเป็นโฟลเดอร์:

- [Power BI Project (.pbip)](https://learn.microsoft.com/power-bi/developer/projects/projects-overview)
- TMDL guidelines ใน skill `references/tmdl-guidelines.md`

คอร์สไม่บังคับ PBIP — นักเรียนใช้ `.pbix` เดียวได้ครบ

---

## คุณภาพข้อมูลและ measure catalog

| ตรวจ | วิธี |
| --- | --- |
| FK, Date contiguous, teaching columns | `pytest -q` → `tests/test_northwind_dw.py` |
| `_Measures` ตรง `measures.dax` | `tests/test_measures_catalog.py` |
| Regenerate metadata ชีต `_` | `python scripts/extend_northwind_dw.py` |

---

## อ่านต่อ

- [CURRICULUM.md](../CURRICULUM.md)
- [Best practices index](../best-practices/README.md)
- [Instructor guide](../instructor/README.md)
