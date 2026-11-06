#!/usr/bin/env python3
"""Build playbooks/lead-tracker.xlsx (opens in Excel, Google Sheets, Numbers). Standard library only.

  python3 scripts/build-lead-tracker.py

Sheet 1 "Leads": one row per business, dropdowns for signal / channel / status, follow-up dates filled in from the
first touch (day 3 and day 11), overdue follow-ups turn orange. Sheet 2 "20 in 20": the daily routine log with totals.
Sheet 3 "How to use".
"""
import datetime as dt
import os
import zipfile
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "playbooks", "lead-tracker.xlsx")


def col(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def serial(d):
    return (d - dt.date(1899, 12, 30)).days


def cell(ref, v, style=0):
    if v is None or v == "":
        return f'<c r="{ref}" s="{style}"/>' if style else ""
    if isinstance(v, tuple) and v[0] == "f":
        return f'<c r="{ref}" s="{style}"><f>{escape(v[1])}</f></c>'
    if isinstance(v, (int, float)):
        return f'<c r="{ref}" s="{style}"><v>{v}</v></c>'
    return f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{escape(str(v))}</t></is></c>'


def sheet(rows, widths, styles=None, freeze=True, extra=""):
    """rows: list of lists; styles: function(row_idx, col_idx) -> style id."""
    cols = "".join(f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths, 1))
    data = []
    for r, row in enumerate(rows, 1):
        cells = "".join(cell(f"{col(c)}{r}", v, styles(r, c) if styles else 0) for c, v in enumerate(row, 1))
        data.append(f'<row r="{r}">{cells}</row>')
    pane = ('<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" '
            'state="frozen"/></sheetView></sheetViews>') if freeze else '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f'{pane}<sheetFormatPr defaultRowHeight="18"/><cols>{cols}</cols><sheetData>{"".join(data)}</sheetData>'
            f'{extra}</worksheet>')


# ---------- Sheet 1: Leads ----------
LEAD_HEAD = ["Business", "Trade", "Town", "Signal", "Proof (the true first line)", "Phone", "Email (only if they publish it)",
             "Maps / website link", "Score 1–5", "Channel", "First touch", "Follow-up 1 (day 3)", "Follow-up 2 (day 11)",
             "Status", "Next step", "Notes"]
LEAD_W = [26, 16, 14, 16, 40, 15, 24, 30, 9, 11, 13, 16, 16, 18, 26, 30]
SIGNALS = "No website,Broken site,Just opened,Review complaint,Asking online,Partner,Warm intro,Other"
CHANNELS = "Walk-in,Call,DM,Email"
STATUSES = "New,Contacted,Replied,Call booked,Proposal sent,Won,Not now,Asked to stop"
today = dt.date.today()
examples = [
    ["EXAMPLE Pressure Washing (delete me)", "Pressure washing", "Tulsa", "No website",
     "4.8★ from 63 reviews, no website on the listing", "", "", "", 5, "Call", serial(today - dt.timedelta(days=4)),
     None, None, "Contacted", "Follow up with the preview link", ""],
    ["EXAMPLE Deck Builders (delete me)", "Decks", "Broken Arrow", "Broken site",
     "Site shows a 'Not secure' warning and a © 2019 footer", "", "", "", 4, "Walk-in", serial(today - dt.timedelta(days=1)),
     None, None, "Replied", "15-min call Thursday", "Owner wants more repair jobs"],
    ["EXAMPLE Cafe (delete me)", "Cafe", "Chicago", "Just opened", "License issued last week, not on Google Maps yet", "",
     "", "", 3, "", "", None, None, "New", "Walk in mid-afternoon", ""],
]
lead_rows = [LEAD_HEAD]
for i in range(2, 502):
    ex = examples[i - 2] if i - 2 < len(examples) else [""] * 16
    row = list(ex)
    row[11] = ("f", f'IF(K{i}="","",K{i}+3)')
    row[12] = ("f", f'IF(K{i}="","",K{i}+11)')
    lead_rows.append(row)


def lead_style(r, c):
    if r == 1:
        return 1
    if c in (11, 12, 13):
        return 2
    if c in (5, 15, 16):
        return 3
    return 0


lead_extra = (
    '<autoFilter ref="A1:P501"/>'
    '<conditionalFormatting sqref="L2:M501"><cfRule type="expression" dxfId="0" priority="1">'
    '<formula>AND($N2="Contacted",L2&lt;&gt;"",L2&lt;=TODAY())</formula></cfRule></conditionalFormatting>'
    '<conditionalFormatting sqref="A2:P501"><cfRule type="expression" dxfId="1" priority="2">'
    '<formula>$N2="Asked to stop"</formula></cfRule></conditionalFormatting>'
    '<dataValidations count="4">'
    f'<dataValidation type="list" allowBlank="1" sqref="D2:D501"><formula1>"{SIGNALS}"</formula1></dataValidation>'
    f'<dataValidation type="list" allowBlank="1" sqref="J2:J501"><formula1>"{CHANNELS}"</formula1></dataValidation>'
    f'<dataValidation type="list" allowBlank="1" sqref="N2:N501"><formula1>"{STATUSES}"</formula1></dataValidation>'
    '<dataValidation type="whole" allowBlank="1" sqref="I2:I501"><formula1>1</formula1><formula2>5</formula2></dataValidation>'
    '</dataValidations>')

# ---------- Sheet 2: 20 in 20 ----------
D_HEAD = ["Date", "Google Maps (10)", "Broken sites (5)", "New licenses (5)", "Found", "Contacted (best 5)", "Replies",
          "Calls booked", "Notes"]
D_W = [13, 16, 15, 16, 9, 18, 9, 13, 36]
d_rows = [D_HEAD]
for i in range(2, 32):
    d_rows.append(["", "", "", "", ("f", f'IF(A{i}="","",SUM(B{i}:D{i}))'), "", "", "", ""])
d_rows.append(["Total", ("f", "SUM(B2:B31)"), ("f", "SUM(C2:C31)"), ("f", "SUM(D2:D31)"), ("f", "SUM(E2:E31)"),
               ("f", "SUM(F2:F31)"), ("f", "SUM(G2:G31)"), ("f", "SUM(H2:H31)"), ""])
d_rows.append(["Reply rate", "", "", "", "", ("f", 'IF(F32=0,"",G32/F32)'), "", "", "replies ÷ contacted"])


def d_style(r, c):
    if r == 1 or r >= 32 and c == 1:
        return 1
    if c == 1:
        return 2
    if r == 33 and c == 6:
        return 4
    return 0


# ---------- Sheet 3: How to use ----------
HOW = [
    ["How to use this tracker"],
    ["1. Leads: one row per business. Delete the 3 EXAMPLE rows first."],
    ["2. Signal = why they need you now (no website, broken site, just opened, a review that complains, asking online)."],
    ["3. Proof = the one true thing you'll open with. If you can't write it, the lead isn't ready."],
    ["4. Email: only an address the business publishes (and in Canada, only about their business). Never scrape personal emails."],
    ["5. Type the date of your first touch: both follow-up dates fill in (day 3 and day 11). They turn orange when due."],
    ["6. Two follow-ups, then stop. 'Asked to stop' greys the row out: never contact them again."],
    ["7. 20 in 20: 20 minutes a day, 20 leads (10 Maps, 5 broken sites, 5 new licenses), contact the best 5 the same day."],
    [""],
    ["Free skills that fill this in for you: github.com/WordRocket/local-client-finder (find-clients, find-broken-sites,"],
    ["find-new-businesses, client-agents). Check every lead before you contact it. Results vary."],
]

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<numFmts count="1"><numFmt numFmtId="164" formatCode="yyyy-mm-dd"/></numFmts>
<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font></fonts>
<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FF0E2A47"/><bgColor indexed="64"/></patternFill></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="5">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
<xf numFmtId="9" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
<dxfs count="2">
<dxf><font><b/><color rgb="FF9A3412"/></font><fill><patternFill patternType="solid"><bgColor rgb="FFFED7AA"/></patternFill></fill></dxf>
<dxf><font><color rgb="FF9CA3AF"/><strike/></font></dxf>
</dxfs>
</styleSheet>"""

WORKBOOK = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="Leads" sheetId="1" r:id="rId1"/><sheet name="20 in 20" sheetId="2" r:id="rId2"/><sheet name="How to use" sheetId="3" r:id="rId3"/></sheets>
<definedNames><definedName name="_xlnm._FilterDatabase" localSheetId="0" hidden="1">Leads!$A$1:$P$501</definedName></definedNames>
<calcPr calcId="0" fullCalcOnLoad="1"/>
</workbook>"""

WB_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", TYPES)
    z.writestr("_rels/.rels", ROOT_RELS)
    z.writestr("xl/workbook.xml", WORKBOOK)
    z.writestr("xl/_rels/workbook.xml.rels", WB_RELS)
    z.writestr("xl/styles.xml", STYLES)
    z.writestr("xl/worksheets/sheet1.xml", sheet(lead_rows, LEAD_W, lead_style, extra=lead_extra))
    z.writestr("xl/worksheets/sheet2.xml", sheet(d_rows, D_W, d_style))
    z.writestr("xl/worksheets/sheet3.xml", sheet(HOW, [120], lambda r, c: 1 if r == 1 else 0, freeze=False))
print(f"{os.path.abspath(OUT)} ({os.path.getsize(OUT) / 1024:.0f} KB)")
