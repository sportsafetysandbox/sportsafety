"""Build docs/downloads/risk-assessment-template.xlsx (portal-original design).

Method follows the Code of Practice on WSH Risk Management (2021): 5x5 matrix,
RPN = Severity x Likelihood, hierarchy of control. Bands: Low 1-3, Medium 4-12, High 15-25.
Run: python tools/make_risk_template.py
"""
import os

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "downloads", "risk-assessment-template.xlsx")

F = "Arial"
RED, CRIMSON, GREY = "E31E2D", "A6192E", "F4F4F4"
INPUT = PatternFill("solid", fgColor="FFF9DB")
HEAD = PatternFill("solid", fgColor=CRIMSON)
SUB = PatternFill("solid", fgColor=GREY)
LOW = PatternFill("solid", fgColor="DFF3E4")
MED = PatternFill("solid", fgColor="FFF0D6")
HIGH = PatternFill("solid", fgColor="FCE0E2")
thin = Side(style="thin", color="BBBBBB")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def font(**kw):
    return Font(name=F, **kw)


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = font(size=14, bold=True, color=CRIMSON)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = font(size=9, italic=True, color="555555")


wb = Workbook()

# ---------------- How to use ----------------
ws = wb.active
ws.title = "How to use"
title(ws, "Risk Assessment Template for Sport Activities",
      "Sport Safety Portal · based on the Code of Practice on WSH Risk Management (2021) and SS 681:2022, clause 4")
rows = [
    ("Step", "What to do"),
    ("1. Prepare", "Form a small team who know the activity. List each part of the activity on the 'Activity Inventory' sheet."),
    ("2. Identify", "On 'Risk Assessment', give each hazard its own row: what could go wrong, who could be harmed, and the possible injury."),
    ("3. Evaluate", "Rate Severity (S) and Likelihood (L) from 1 to 5 with existing controls in place. See 'Matrix & Guide'. RPN and Risk level calculate automatically."),
    ("4. Control", "Add controls starting from the top of the hierarchy: eliminate, substitute, engineering, administrative, then PPE. Re-rate S and L. The new RPN must not be higher, and High risks must reach at least Medium before the activity starts."),
    ("5. Implement", "Name an owner and due date for each additional control. Get the assessment approved and brief everyone affected."),
    ("6. Record", "Keep the assessment for at least 3 years. List it on the 'Risk Register' sheet."),
    ("7. Review", "Review at least every 3 years (preferably yearly), after any injury, after significant change, before each event edition, and dynamically on the day."),
    ("", ""),
    ("Legend", ""),
    ("Yellow cells", "Fill these in."),
    ("White cells with formulas", "Calculate automatically. Do not overwrite."),
    ("Example rows", "Rows marked EXAMPLE on 'Risk Assessment' show the expected format. Replace or delete them."),
    ("Risk bands", "Low 1–3 · Medium 4–12 · High 15–25. The WSH Code lets each organisation set its bands with management agreement; change the formulas consistently if yours differ."),
    ("", ""),
    ("Disclaimer", "A starting point only. Adapt it to your activity, venue and people. It does not replace the full standards or legal advice."),
]
for i, (a, b) in enumerate(rows, start=4):
    ws.cell(i, 1, a).font = font(bold=True)
    ws.cell(i, 2, b).font = font()
    ws.cell(i, 2).alignment = WRAP
ws["A4"].fill = ws["B4"].fill = HEAD
ws["A4"].font = ws["B4"].font = font(bold=True, color="FFFFFF")
ws["A14"].fill = INPUT
ws.column_dimensions["A"].width = 26
ws.column_dimensions["B"].width = 110

# ---------------- Activity Inventory ----------------
ws = wb.create_sheet("Activity Inventory")
title(ws, "Inventory of Activities", "List every part of the activity before assessing it.")
labels = [("Activity / event assessed", "B4"), ("Location", "B5"), ("Date assessed", "B6")]
for (lab, ref) in labels:
    r = int(ref[1:])
    ws.cell(r, 1, lab).font = font(bold=True)
    ws[ref].fill = INPUT
    ws[ref].border = BOX
hdr = ["S/No", "Phase", "Work activity / sub-activity", "Location / area", "Remarks"]
for c, h in enumerate(hdr, 1):
    cell = ws.cell(8, c, h)
    cell.font = font(bold=True, color="FFFFFF")
    cell.fill = HEAD
    cell.alignment = CENTER
example = [1, "Set-up", "Erecting start/finish gantry and tents (EXAMPLE)", "Start/finish area", "Contractor"]
for r in range(9, 39):
    ws.cell(r, 1, r - 8)
    for c in range(1, 6):
        cell = ws.cell(r, c)
        cell.border = BOX
        cell.font = font(italic=(r == 9))
        if c > 1:
            cell.fill = INPUT
for c, v in enumerate(example[1:], 2):
    ws.cell(9, c, v)
for col, w in zip("ABCDE", [7, 16, 50, 26, 30]):
    ws.column_dimensions[col].width = w

# ---------------- Risk Assessment ----------------
ws = wb.create_sheet("Risk Assessment")
title(ws, "Risk Assessment Form", "RPN = Severity x Likelihood · Low 1–3 · Medium 4–12 · High 15–25")
meta = [("Activity / event", "B3"), ("Location", "B4"), ("RA leader", "B5"), ("Team members", "B6"),
        ("Original RA date", "H3"), ("Approved by (name, designation)", "H4"), ("Approval date", "H5"),
        ("Next review date", "H6")]
for lab, ref in meta:
    col, r = ref[0], int(ref[1:])
    lc = chr(ord(col) - 1)
    ws[f"{lc}{r}"] = lab
    ws[f"{lc}{r}"].font = font(bold=True)
    ws[ref].fill = INPUT
    ws[ref].border = BOX
ws.merge_cells("B3:E3"); ws.merge_cells("B4:E4"); ws.merge_cells("B5:E5"); ws.merge_cells("B6:E6")
ws.merge_cells("H3:J3"); ws.merge_cells("H4:J4"); ws.merge_cells("H5:J5"); ws.merge_cells("H6:J6")

# group header row 8, column header row 9
groups = [("A8:F8", "HAZARD IDENTIFICATION"), ("G8:J8", "RISK EVALUATION"), ("K8:R8", "RISK CONTROL")]
for rng, text in groups:
    ws.merge_cells(rng)
    c = ws[rng.split(":")[0]]
    c.value = text
    c.font = font(bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=RED)
    c.alignment = CENTER
cols = ["S/No", "Work activity / sub-activity", "Hazard", "Who could be harmed", "Possible injury / ill-health",
        "Existing controls", "S", "L", "RPN", "Risk level",
        "Additional controls (consider eliminating the hazard first)", "S", "L", "RPN", "Risk level",
        "Owner", "Due date", "Remarks"]
for i, h in enumerate(cols, 1):
    c = ws.cell(9, i, h)
    c.font = font(bold=True, color="FFFFFF")
    c.fill = HEAD
    c.alignment = CENTER
ws.row_dimensions[9].height = 42

FIRST, LAST = 10, 49
ex = [
    ["Running the 10 km route (EXAMPLE)", "Heat and humidity", "Participants", "Exertional heatstroke",
     "Early start; water at 5 km", 4, 3, None, None,
     "Check WBGT from 6 am with cancel/shorten rule; water every 2.5 km; ice-water immersion tub and medic at finish; heat briefing",
     4, 2, None, None, "Race director", "", ""],
    ["Running the 10 km route (EXAMPLE)", "Sudden cardiac arrest", "Participants", "Death",
     "First-aider at finish", 5, 2, None, None,
     "AEDs at start/finish and mid-route; cycling first-aider with AED; pre-participation questionnaire at registration",
     5, 1, None, None, "Medical lead", "", ""],
]
for r in range(FIRST, LAST + 1):
    ws.cell(r, 1, r - FIRST + 1)
    for c in range(1, 19):
        cell = ws.cell(r, c)
        cell.border = BOX
        cell.alignment = WRAP if c not in (1, 7, 8, 9, 10, 12, 13, 14, 15) else CENTER
        cell.font = font(italic=(r - FIRST) < len(ex))
        if c not in (1, 9, 10, 14, 15):
            cell.fill = INPUT
    ws.cell(r, 9, f'=IF(OR(G{r}="",H{r}=""),"",G{r}*H{r})')
    ws.cell(r, 10, f'=IF(I{r}="","",IF(I{r}<=3,"Low",IF(I{r}<=12,"Medium","High")))')
    ws.cell(r, 14, f'=IF(OR(L{r}="",M{r}=""),"",L{r}*M{r})')
    ws.cell(r, 15, f'=IF(N{r}="","",IF(N{r}<=3,"Low",IF(N{r}<=12,"Medium","High")))')
for i, row in enumerate(ex):
    r = FIRST + i
    for c, v in enumerate(row, 2):
        if c in (9, 10, 14, 15) or v is None:
            continue
        ws.cell(r, c, v)

dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True,
                    showErrorMessage=True, errorTitle="Rating 1 to 5", error="Enter a whole number from 1 to 5.")
ws.add_data_validation(dv)
for col in "GHLM":
    dv.add(f"{col}{FIRST}:{col}{LAST}")
for col in ("I", "N"):
    rng = f"{col}{FIRST}:{col}{LAST}"
    ws.conditional_formatting.add(rng, CellIsRule(operator="between", formula=["1", "3"], fill=LOW))
    ws.conditional_formatting.add(rng, CellIsRule(operator="between", formula=["4", "12"], fill=MED))
    ws.conditional_formatting.add(rng, CellIsRule(operator="between", formula=["13", "25"], fill=HIGH))
for col in ("J", "O"):
    rng = f"{col}{FIRST}:{col}{LAST}"
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Low"'], fill=LOW))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Medium"'], fill=MED))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"High"'], fill=HIGH))
widths = [6, 28, 22, 16, 22, 30, 5, 5, 6, 10, 42, 5, 5, 6, 10, 16, 12, 18]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[chr(64 + i)].width = w
ws.freeze_panes = "C10"
ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.page_setup.fitToHeight = 0
ws.print_title_rows = "8:9"

# ---------------- Matrix & Guide ----------------
ws = wb.create_sheet("Matrix & Guide")
title(ws, "5x5 Risk Matrix and Rating Guide", "From the Code of Practice on WSH Risk Management (2021); sport examples added by the portal")
ws["A4"] = "Severity \\ Likelihood"
like = ["Rare (1)", "Remote (2)", "Occasional (3)", "Frequent (4)", "Almost certain (5)"]
sev = ["Catastrophic (5)", "Major (4)", "Moderate (3)", "Minor (2)", "Negligible (1)"]
for j, l in enumerate(like):
    c = ws.cell(4, 2 + j, l)
    c.font = font(bold=True, color="FFFFFF"); c.fill = HEAD; c.alignment = CENTER
ws["A4"].font = font(bold=True, color="FFFFFF"); ws["A4"].fill = HEAD
for i, s in enumerate(sev):
    r = 5 + i
    ws.cell(r, 1, s).font = font(bold=True)
    sval = 5 - i
    for j in range(5):
        lval = j + 1
        cell = ws.cell(r, 2 + j, f"=$Z${r}*{chr(66 + j)}$11")
        cell.alignment = CENTER
        cell.font = font(bold=True)
        cell.border = BOX
        rpn = sval * lval
        cell.fill = LOW if rpn <= 3 else MED if rpn <= 12 else HIGH
    ws.cell(r, 26, sval)  # helper: severity value
for j in range(5):
    ws.cell(11, 2 + j, j + 1)  # helper: likelihood values
    ws.cell(11, 2 + j).font = font(size=8, color="999999")
ws.cell(11, 1, "Likelihood value").font = font(size=8, color="999999")
ws.column_dimensions["Z"].hidden = True

r = 13
ws.cell(r, 1, "Severity guide").font = font(bold=True, size=12, color=CRIMSON)
sg = [("Level", "Severity", "Meaning (WSH Code)", "Sport example (portal)"),
      (5, "Catastrophic", "Death, fatal disease or exposure, or multiple major injuries", "Cardiac arrest with no AED on site; drowning"),
      (4, "Major", "Serious injury or illness, e.g. major fractures, disability, serious head injury", "Exertional heatstroke; spinal injury from a fall"),
      (3, "Moderate", "Injury or ill-health requiring medical treatment", "Laceration needing stitches; minor fracture; concussion"),
      (2, "Minor", "Injury or ill-health requiring first aid only", "Grazes, bruises, mild cramp"),
      (1, "Negligible", "Negligible injury", "Brief discomfort")]
for i, row in enumerate(sg):
    for j, v in enumerate(row):
        c = ws.cell(r + 1 + i, 1 + j, v)
        c.font = font(bold=(i == 0), color=("FFFFFF" if i == 0 else "000000"))
        c.border = BOX; c.alignment = WRAP
        if i == 0:
            c.fill = HEAD
r = 21
ws.cell(r, 1, "Likelihood guide").font = font(bold=True, size=12, color=CRIMSON)
lg = [("Level", "Likelihood", "Meaning (WSH Code)"),
      (1, "Rare", "Not expected to occur but still possible"),
      (2, "Remote", "Not likely to occur under normal circumstances"),
      (3, "Occasional", "Possible or known to occur"),
      (4, "Frequent", "Common occurrence"),
      (5, "Almost certain", "Continual or repeating experience")]
for i, row in enumerate(lg):
    for j, v in enumerate(row):
        c = ws.cell(r + 1 + i, 1 + j, v)
        c.font = font(bold=(i == 0), color=("FFFFFF" if i == 0 else "000000"))
        c.border = BOX; c.alignment = WRAP
        if i == 0:
            c.fill = HEAD
r = 29
ws.cell(r, 1, "Action by risk level").font = font(bold=True, size=12, color=CRIMSON)
ag = [("Risk level", "RPN", "Acceptability", "What to do"),
      ("Low", "1–3", "Acceptable", "No additional controls may be needed. Monitor so the risk does not increase."),
      ("Medium", "4–12", "Tolerable", "Reduce as low as reasonably practicable within a set time. Interim controls allowed. Management attention needed."),
      ("High", "15–25", "Not acceptable", "Do not start until reduced to at least Medium. Eliminate if practicable. Do not rely mainly on PPE. Management review required.")]
for i, row in enumerate(ag):
    for j, v in enumerate(row):
        c = ws.cell(r + 1 + i, 1 + j, v)
        c.font = font(bold=(i == 0), color=("FFFFFF" if i == 0 else "000000"))
        c.border = BOX; c.alignment = WRAP
        if i == 0:
            c.fill = HEAD
        elif j == 0:
            c.fill = [LOW, MED, HIGH][i - 1]
r = 35
ws.cell(r, 1, "Hierarchy of control (most to least effective)").font = font(bold=True, size=12, color=CRIMSON)
hc = [("Elimination", "Remove a dangerous route section; cancel the open-water leg in unsafe conditions"),
      ("Substitution", "Replace a swim leg with a run; move training indoors"),
      ("Engineering controls", "Anchor goalposts; barriers between runners and traffic; shade and cooling stations"),
      ("Administrative controls", "Schedule outside hottest hours; rest breaks; screening questionnaire; briefings; marshals"),
      ("Personal protective equipment", "Helmets, mouthguards, buoyancy aids, high-visibility vests (last resort)")]
for i, (a, b) in enumerate(hc):
    ws.cell(r + 1 + i, 1, a).font = font(bold=True)
    ws.cell(r + 1 + i, 2, b).font = font()
    ws.cell(r + 1 + i, 2).alignment = WRAP
    ws.merge_cells(start_row=r + 1 + i, start_column=2, end_row=r + 1 + i, end_column=6)
ws.column_dimensions["A"].width = 24
for col in "BCDEF":
    ws.column_dimensions[col].width = 22
ws.column_dimensions["C"].width = 40
ws.column_dimensions["D"].width = 40

# ---------------- Risk Register ----------------
ws = wb.create_sheet("Risk Register")
title(ws, "Risk Register Cover Sheet", "List every risk assessment in force. Keep records for at least 3 years.")
hdr = ["RA ref no.", "Activity / event assessed", "Location", "RA leader", "Approval date",
       "Next review date", "Remarks"]
for c, h in enumerate(hdr, 1):
    cell = ws.cell(4, c, h)
    cell.font = font(bold=True, color="FFFFFF"); cell.fill = HEAD; cell.alignment = CENTER
for r in range(5, 35):
    for c in range(1, 8):
        cell = ws.cell(r, c)
        cell.border = BOX; cell.fill = INPUT; cell.font = font()
for col, w in zip("ABCDEFG", [12, 40, 24, 20, 14, 16, 30]):
    ws.column_dimensions[col].width = w

for sheet in wb.worksheets:
    for row in sheet.iter_rows():
        for cell in row:
            if cell.font and cell.font.name != F:
                cell.font = Font(name=F, bold=cell.font.bold, italic=cell.font.italic,
                                 size=cell.font.size, color=cell.font.color)

wb.active = wb.sheetnames.index("Risk Assessment")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("saved", OUT)
