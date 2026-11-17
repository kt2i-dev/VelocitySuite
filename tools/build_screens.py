"""Builds the screen mockups for Quality Event & Corrective Action Management:

  docs/quality-engineering/quality-event-capa/ncr-list.html
  docs/quality-engineering/quality-event-capa/ncr-workspace.html   (View and Edit)

They use docs/assets/app.css (the app-* classes and tokens) and docs/assets/icons.svg
(Phosphor names). All data is the fictional demo scenario. Edit this script, then run:
  python3 tools/build_screens.py
"""
from html import escape
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
APP = "quality-engineering/quality-event-capa"
ROOT = "../../"  # from the app folder back to docs/


def ic(name, cls="i"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="{ROOT}assets/icons.svg#{name}"/></svg>'


# ---------- status and severity -> pill variant (what the StatusBadge block does) ----------
STATUS = {
    "Draft": "", "Open": "info", "Containment": "info", "Awaiting MRB": "warning",
    "Disposition Approved": "info", "Verification": "info", "Closed": "success", "Cancelled": "",
}


def pill(label, variant=""):
    cls = "app-pill" + (f" app-pill-{variant}" if variant else "")
    return f'<span class="{cls}">{escape(label)}</span>'


def status(label):
    return pill(label, STATUS[label])


def severity(label):
    # Low and Medium read as text; only High and Critical get color
    return {"High": pill("High", "warning"), "Critical": pill("Critical", "danger")}.get(label, f'<span>{label}</span>')


HOLD = pill("HOLD", "danger")


# ---------- shell: LayoutSideMenu stand-in ----------
MENU = [
    ("house", "Home", None), ("warning", "Quality Events", None), ("file-x", "NCRs", "ncr-list.html"),
    ("users-three", "MRB", None), ("shield-check", "CAPA", None), ("arrows-clockwise", "SCAR", None),
    ("tree-structure", "Lot Trace", None), ("list-checks", "My Actions", None),
    ("-", "Insights", None), ("chart-bar", "Reports", None), ("gear", "Administration", None),
]


def shell(title, active, mockbar, body, script=""):
    items = []
    for icon, label, href in MENU:
        if icon == "-":
            items.append(f'<div class="mock-group">{label}</div>')
            continue
        cls = ' class="active"' if label == active else ""
        items.append(f'<a{cls} href="{href or "#"}">{ic(icon)}{label}</a>')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Mockup</title>
<link rel="stylesheet" href="{ROOT}assets/app.css"></head>
<body>
<div class="mock-bar"><strong>Mockup</strong><span>{title}</span>{mockbar}<span class="mock-sp"></span><a href="index.html">Quality Event &amp; CAPA</a><a href="{ROOT}template.html">Screen template notes</a><a href="{ROOT}index.html">Mockups home</a></div>
<div class="mock-shell">
<nav class="mock-menu" aria-label="Main menu">
<div class="mock-brand"><span class="mock-logo">KT2i</span><span><b>Velocity Suite</b><small>Quality &amp; CAPA</small></span></div>
{''.join(items)}
</nav>
<div class="mock-body">
<header class="mock-top"><span class="mock-search">{ic("magnifying-glass")}Search events, NCRs, lots, suppliers…</span>
<div class="mock-user">{ic("bell")}<span class="mock-avatar">ML</span><span>Maria Lopez<small>Quality Engineer</small></span></div></header>
{body}
</div></div>
{script}
</body></html>
"""


# ---------- NCR list ----------
ROWS = [
    ("NCR-2026-00143", "Shaft diameter out of tolerance", "RM-1042", "Containment", "High", "RM48-9817", True, "ABC Precision Components", "Maria Lopez", "08/25/2026", False),
    ("NCR-2026-00142", "Porosity in housing casting", "CS-2210", "Awaiting MRB", "Medium", "CS22-4410", True, "Northline Castings", "Kevin Jones", "08/22/2026", False),
    ("NCR-2026-00141", "Label misprint on carton", "PK-0311", "Open", "Low", "PK03-1187", False, "Internal (Packaging)", "Sarah Mitchell", "08/21/2026", False),
    ("NCR-2026-00140", "Thread pitch gauge failure", "FS-0880", "Disposition Approved", "Medium", "FS08-2291", False, "Summit Fasteners", "Maria Lopez", "08/18/2026", False),
    ("NCR-2026-00139", "Seal hardness below specification", "PL-5520", "Awaiting MRB", "High", "PL55-0712", True, "Delta Polymer Supply", "David Kim", "08/15/2026", True),
    ("NCR-2026-00138", "Weld spatter on mounting bracket", "FG-31007", "Verification", "Low", "WIP-31007-B", False, "Internal (Line 3)", "Kevin Jones", "08/12/2026", False),
    ("NCR-2026-00137", "Heat-treat certificate missing", "RM-2040", "Containment", "Critical", "RM20-5530", True, "Keystone Alloys", "Maria Lopez", "08/11/2026", True),
    ("NCR-2026-00136", "Surface scratches on cover", "FG-20415", "Draft", "Low", "FG20-0098", False, "Internal (Paint)", "Sarah Mitchell", "08/10/2026", False),
    ("NCR-2026-00135", "Bore runout out of tolerance", "MC-7781", "Open", "Medium", "MC77-3302", False, "Internal (Machining)", "David Kim", "08/07/2026", False),
    ("NCR-2026-00131", "Wrong resin grade received", "PL-5521", "Closed", "Medium", "PL55-0650", False, "Delta Polymer Supply", "Kevin Jones", "07/29/2026", False),
]


def ncr_list():
    rows = []
    for num, title, mat, st, sev, lot, held, sup, owner, opened, overdue in ROWS:
        href = "ncr-workspace.html" if num == "NCR-2026-00143" else "#"
        warn = f' <span class="app-icon-warn" title="Has overdue actions">{ic("clock")}</span>' if overdue else ""
        rows.append(f"""<tr>
<td class="app-num"><a class="app-link" href="{href}">{num}</a>{warn}</td>
<td>{escape(title)}<br><span class="app-label">{mat}</span></td>
<td>{status(st)}</td><td>{severity(sev)}</td>
<td class="app-num">{lot}{' ' + HOLD if held else ''}</td>
<td>{escape(sup)}</td><td>{owner}</td><td class="app-num">{opened}</td>
<td style="white-space:nowrap"><a class="app-icon-link" href="{href}" title="Open" aria-label="Open {num}">{ic("eye")}</a><a class="app-icon-link" href="#" title="More" aria-label="More actions">{ic("dots-three")}</a></td>
</tr>""")
    kpis = [("Open NCRs", "14", "4 opened this week", False), ("In containment", "5", "2 with held material", False),
            ("Awaiting MRB", "6", "Oldest: 9 days", False), ("Overdue actions", "3", "On 2 NCRs", True)]
    kpi_html = "".join(
        f'<a class="app-kpi" href="#"><span class="app-kpi-label">{l}</span><span class="app-kpi-value app-num">{v}</span>'
        f'<span class="app-kpi-note">{(ic("clock") + " ") if w else ""}{n}</span></a>' for l, v, n, w in kpis)
    body = f"""<main class="app-page-wide">
<div class="app-page-header">
<div class="app-row"><div><h1 style="margin:0;font-size:24px">Nonconformances</h1>
<div class="app-label" style="font-size:13px">Material, product and process conditions that don’t meet requirements</div></div>
<div class="app-actions"><button class="btn">{ic("download-simple")}Export</button><button class="btn btn-primary">{ic("plus")}New NCR</button></div></div>
</div>
<div class="app-stack">
<div class="app-grid app-cols-4">{kpi_html}</div>
<div class="app-card app-card-sm app-stack">
<div class="app-row">
<input class="mock-input" style="flex:1 1 260px;width:auto" placeholder="Search NCR number, title, material, lot or supplier">
<select class="mock-input" style="width:auto"><option>All open statuses</option><option>Draft</option><option>Open</option><option>Containment</option><option>Awaiting MRB</option><option>Disposition Approved</option><option>Verification</option><option>Closed</option></select>
<select class="mock-input" style="width:auto"><option>Any severity</option><option>Low</option><option>Medium</option><option>High</option><option>Critical</option></select>
<select class="mock-input" style="width:auto"><option>Any owner</option><option>Me</option></select>
<button class="btn">{ic("funnel")}More filters</button>
</div>
<div style="overflow-x:auto"><table class="app-table">
<thead><tr><th>NCR</th><th>Title · material</th><th>Status</th><th>Severity</th><th>Lot</th><th>Supplier / source</th><th>Owner</th><th>Opened</th><th><span class="app-label">Actions</span></th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<div class="app-row"><span class="app-label">Showing 1–10 of 14 open NCRs</span><span class="app-actions"><button class="btn" disabled>Previous</button><button class="btn">Next</button></span></div>
</div>
</div>
</main>"""
    return shell("NCR list", "NCRs", "", body)


# ---------- NCR workspace ----------
def inp(v):
    return f'<input class="mock-input" value="{escape(v)}">'


def sel(v, opts):
    return '<select class="mock-input">' + "".join(
        f'<option{" selected" if o == v else ""}>{escape(o)}</option>' for o in opts) + "</select>"


def ta(v):
    return f'<textarea class="mock-input" rows="3">{escape(v)}</textarea>'


def field(label, value, edit=None, req=False, span=1):
    """A label and value. edit=None: set by the system, stays text in Edit mode."""
    star = ' <span class="req edit-only">*</span>' if req and edit else ""
    style = f' style="grid-column:span {span}"' if span > 1 else ""
    if edit is None:
        return f'<div class="app-field app-field-stack"{style}><span class="app-label">{label}</span><span class="app-value">{value}</span></div>'
    return (f'<div class="app-field app-field-stack"{style}><span class="app-label">{label}{star}</span>'
            f'<span class="app-value view-only">{value}</span><span class="edit-only">{edit}</span></div>')


def card(title, inner, extra=""):
    return f'<section class="app-card app-card-sm app-stack"><div class="app-row"><h3 class="app-card-title">{title}</h3>{extra}</div>{inner}</section>'


def steps(names, current):
    out = []
    for i, n in enumerate(names):
        state = "done" if i < current else "current" if i == current else "pending"
        dot = ic("check") if state == "done" else ""
        out.append(f'<div class="app-step-{state}"><span class="app-step-dot">{dot}</span><span class="app-step-name">{n}</span></div>')
    return '<div class="app-steps">' + "".join(out) + "</div>"


def ready(ok, text, note=""):
    icon = (f'<span style="color:var(--app-success)">{ic("check-circle")}</span>' if ok
            else f'<span class="app-icon-warn">{ic("x-circle")}</span>')
    n = f'<br><span class="app-label">{note}</span>' if note else ""
    return f'<div class="app-list-row">{icon}<span>{text}{n}</span></div>'


def ncr_workspace():
    yes_no = ["Yes", "No"]
    header = f"""<div class="app-page-header">
<a class="app-back" href="ncr-list.html">{ic("caret-left")}NCRs</a>
<div class="app-row" style="align-items:flex-start">
<div class="app-stack" style="gap:4px">
<div class="app-row"><h1 style="margin:0;font-size:24px">NCR-2026-00143</h1>{status("Containment")}{severity("High")}{HOLD}</div>
<div style="font-size:16px">Shaft diameter out of tolerance</div>
</div>
<div class="app-actions view-only">
<button class="btn btn-primary">{ic("users-three")}Request MRB</button>
<button class="btn" data-mode="edit">{ic("pencil-simple")}Edit</button>
<button class="btn">{ic("plus")}Add Containment</button>
<button class="btn">{ic("arrow-right")}Trace Lot</button>
<button class="btn" title="More: Place Hold, Create SCAR, Create CAPA, Assign, Export PDF, Copy Link" aria-label="More actions">{ic("dots-three")}</button>
</div>
<div class="app-actions edit-only">
<span class="mock-note">Delete shows only while the NCR is a Draft</span>
<button class="btn" data-mode="view">{ic("x")}Cancel</button>
<button class="btn btn-primary" data-mode="view">{ic("floppy-disk")}Save</button>
</div>
</div>
<div class="app-card app-card-sm"><div class="app-grid app-cols-4">
{field("Quality Event", '<a class="app-link" href="#">QE-2026-00187</a>')}
{field("Material", "RM-1042 · Stainless steel shaft")}
{field("Lot", "RM48-9817 · supplier lot SUP-84721")}
{field("Supplier", "ABC Precision Components")}
{field("Owner", "Maria Lopez")}
{field("Opened", '<span class="app-num">08/25/2026</span>')}
{field("Source", "Incoming inspection")}
{field("Containment due", '<span class="app-num">08/29/2026</span>')}
</div></div>
<div class="app-card app-card-sm">{steps(["Draft", "Open", "Containment", "Awaiting MRB", "Disposition Approved", "Closed"], 2)}</div>
<div class="app-alert-warning">{ic("warning")}<span><strong>40 units from this lot have shipped.</strong> FG-50021 went to Apex Industrial Systems on SH-48127. Customer notification is in progress.</span></div>
</div>"""

    overview = f"""<div class="app-stack" data-panel="overview">
{card("Nonconformance", f'''<div class="app-grid app-cols-2 view-only">
<div class="app-panel app-panel-info"><div class="app-label">Requirement</div><div class="app-value-lg app-num">Ø 10.00 mm ± 0.20</div><div class="app-label">Drawing RM-1042 rev C</div></div>
<div class="app-panel app-panel-danger"><div class="app-label">Actual</div><div class="app-value-lg app-num">Ø 10.48 mm</div><div class="app-label">0.28 mm over the upper limit</div></div>
</div>
<div class="app-grid app-cols-2 edit-only">
{field("Requirement", "", inp("Ø 10.00 mm ± 0.20 (drawing RM-1042 rev C)"), req=True)}
{field("Actual condition", "", inp("Ø 10.48 mm measured on 25 of 25 samples"), req=True)}
</div>
<div class="app-grid app-cols-3">
{field("Defect category", "Dimensional", sel("Dimensional", ["Dimensional", "Material", "Surface", "Documentation", "Process"]), req=True)}
{field("Defect code", "DIM-02 · Outside diameter high", sel("DIM-02 · Outside diameter high", ["DIM-01 · Outside diameter low", "DIM-02 · Outside diameter high", "DIM-05 · Runout"]))}
{field("Detected by", "Sarah Mitchell, 08/25/2026 09:05")}
</div>
{field("Problem description", '<span class="app-text">Incoming inspection of receipt RCPT-39471 measured the shaft outside diameter at 10.48 mm against 10.00 ± 0.20 mm. All 25 sampled units failed, so the whole supplier lot SUP-84721 (200 units) is suspect.</span>', ta("Incoming inspection of receipt RCPT-39471 measured the shaft outside diameter at 10.48 mm against 10.00 ± 0.20 mm. All 25 sampled units failed, so the whole supplier lot SUP-84721 (200 units) is suspect."), req=True)}''')}
{card("Product and source", f'''<div class="app-grid app-cols-4">
{field("Material", "RM-1042", sel("RM-1042", ["RM-1042", "RM-1043", "RM-2040"]), req=True)}
{field("Internal lot", "RM48-9817 " + HOLD, sel("RM48-9817", ["RM48-9817", "RM48-9818"]), req=True)}
{field("Supplier lot", "SUP-84721", inp("SUP-84721"))}
{field("Supplier", "ABC Precision Components")}
{field("Receipt", "RCPT-39471", inp("RCPT-39471"))}
{field("Purchase order", "PO-448712", inp("PO-448712"))}
{field("Work order", "WO-875443 · consumed 80", inp("WO-875443"))}
{field("Location", "Receiving quarantine QA-01", sel("Receiving quarantine QA-01", ["Receiving quarantine QA-01", "Main stores", "FG-WH-A12"]))}
</div><p class="app-label edit-only" style="margin:0">Supplier comes from the lot and can’t be edited here.</p>''')}
{card("Quantity and risk", f'''<div class="app-grid app-cols-4">
{field("Failed", '<span class="app-value-lg app-num">25</span>', inp("25"), req=True)}
{field("Suspect", '<span class="app-value-lg app-num">200</span>', inp("200"), req=True)}
{field("Consumed", '<span class="app-value-lg app-num">80</span>')}
{field("On hold", '<span class="app-value-lg app-num">160</span>')}
</div>
<hr class="app-rule">
<div class="app-grid app-cols-3">
{field("Risk", severity("High"), sel("High", ["Low", "Medium", "High", "Critical"]), req=True)}
{field("Customer impact", "Yes · 40 units shipped", sel("Yes", yes_no))}
{field("Regulatory impact", "No", sel("No", yes_no))}
</div>
<p class="app-label view-only" style="margin:0">Consumed and on-hold quantities come from Lot Trace and the holds.</p>''')}
{card("Follow-up required", f'''<div class="app-grid app-cols-3 view-only">
{field("MRB", pill("Required", "warning"))}
{field("SCAR", pill("Required", "warning"))}
{field("CAPA", "To be decided")}
</div>
<div class="app-grid app-cols-3 edit-only">
<label class="app-check"><input type="checkbox" checked> MRB required</label>
<label class="app-check"><input type="checkbox" checked> SCAR required</label>
<label class="app-check"><input type="checkbox"> CAPA required</label>
</div>''')}
</div>"""

    actions = [("Quarantine 120 units of RM48-9817 in QA-01", "Sarah Mitchell", "08/25/2026", "Done", "120 / 0 / 0"),
               ("Hold FG-50022 (40 units) in FG-WH-A12", "Robert Chen", "08/25/2026", "Done", "40 / 0 / 0"),
               ("Notify Apex Industrial Systems about FG-50021", "Maria Lopez", "08/27/2026", "In progress", "–"),
               ("100% inspect the remaining 120 units", "Kevin Jones", "08/29/2026", "Open", "–")]
    act_variant = {"Done": "success", "In progress": "info", "Open": ""}
    containment = f"""<div data-panel="containment" class="mock-panel" hidden>{card("Containment actions", '''<div style="overflow-x:auto"><table class="app-table">
<thead><tr><th>Action</th><th>Owner</th><th>Due</th><th>Status</th><th>Inspected / accepted / rejected</th><th></th></tr></thead><tbody>''' + "".join(
        f'<tr><td>{a}</td><td>{o}</td><td class="app-num">{d}</td><td>{pill(s, act_variant[s])}</td><td class="app-num">{q}</td>'
        f'<td><a class="app-icon-link" href="#" aria-label="More">{ic("dots-three")}</a></td></tr>' for a, o, d, s, q in actions)
        + '</tbody></table></div>', f'<span class="app-actions"><button class="btn">{ic("plus")}Add Containment</button></span>')}</div>"""

    holds = f"""<div data-panel="holds" class="mock-panel" hidden>{card("Quality holds", f'''<table class="app-table"><thead><tr><th>Hold</th><th>Material</th><th>Quantity</th><th>Status</th><th>Placed</th></tr></thead><tbody>
<tr><td><a class="app-link" href="#">HOLD-2026-00057</a></td><td>RM48-9817 · RM-1042</td><td class="app-num">120</td><td>{pill("Active", "danger")}</td><td class="app-num">08/25/2026</td></tr>
<tr><td><a class="app-link" href="#">HOLD-2026-00058</a></td><td>FG-50022 · finished goods</td><td class="app-num">40</td><td>{pill("Active", "danger")}</td><td class="app-num">08/25/2026</td></tr>
</tbody></table>''', f'<span class="app-actions"><button class="btn">{ic("pause-circle")}Place Hold</button></span>')}</div>"""

    disposition = f"""<div data-panel="disposition" class="mock-panel" hidden>{card("Disposition", f'''<p class="app-text" style="margin:0">Not recorded yet. The MRB decides the disposition (use as is, rework, sort / 100% inspect, return to supplier or scrap); it shows here once MRB-2026-00081 is approved.</p>
<div><button class="btn btn-primary">{ic("users-three")}Request MRB</button></div>''')}</div>"""

    events = [("08/25/2026 09:05", "Sarah Mitchell", "created Quality Event QE-2026-00187 from incoming inspection"),
              ("08/25/2026 09:21", "Sarah Mitchell", "placed lot RM48-9817 on hold (HOLD-2026-00057)"),
              ("08/25/2026 09:40", "Sarah Mitchell", "created this NCR from QE-2026-00187"),
              ("08/25/2026 10:02", "Maria Lopez", "took ownership and moved the NCR to Containment"),
              ("08/25/2026 11:15", "Robert Chen", "held FG-50022 in FG-WH-A12 (HOLD-2026-00058)"),
              ("08/25/2026 11:30", "Quality Assistant", "found a similar NCR on RM-1042 from the same supplier")]
    activity = f"""<div data-panel="activity" class="mock-panel" hidden>{card("Activity", '<div class="app-list-stack">' + "".join(
        f'<div class="app-list-row"><span class="app-label app-num" style="min-width:118px">{t}</span><span><strong>{w}</strong> {e}</span></div>'
        for t, w, e in reversed(events)) + '</div>', f'<span class="app-actions"><button class="btn">{ic("chat-text")}Add Comment</button></span>')}</div>"""

    files = [("Inspection report RCPT-39471.pdf", "Inspection", "Sarah Mitchell"),
             ("Shaft measurements.xlsx", "Measurement data", "Sarah Mitchell"),
             ("Photo – gauge reading.jpg", "Photo", "Sarah Mitchell")]
    attachments = f"""<div data-panel="attachments" class="mock-panel" hidden>{card("Attachments", '<table class="app-attach-table"><tbody>' + "".join(
        f'<tr><td>{ic("paperclip")} <a class="app-link" href="#">{n}</a></td><td class="app-label">{c}</td><td class="app-label">{u}</td>'
        f'<td style="text-align:right"><a class="app-icon-link app-icon-link-danger" href="#" aria-label="Remove">{ic("trash")}</a></td></tr>' for n, c, u in files)
        + f'</tbody></table><div class="app-dropzone">{ic("upload-simple")}Drop files here or <a href="#">browse</a> · JPG, PNG, PDF, XLSX, DOCX</div>')}</div>"""

    tabs = [("overview", "Overview", ""), ("containment", "Containment", "4"), ("holds", "Holds", "2"),
            ("disposition", "Disposition", ""), ("activity", "Activity", "6"), ("attachments", "Attachments", "3")]
    on_cls = ' class="on"'
    tab_html = '<div class="mock-tabs" role="tablist">' + "".join(
        f'<button role="tab" data-tab="{k}"{on_cls if k == "overview" else ""}>{l}'
        + (f'<span class="count">{c}</span>' if c else "") + "</button>"
        for k, l, c in tabs) + "</div>"

    side = f"""<aside class="app-split-side">
{card("Closure readiness", '<div class="app-list-stack">' + ready(True, "Problem described and risk set")
      + ready(False, "Containment actions open", "2 of 4 still open")
      + ready(False, "MRB required, not requested")
      + ready(False, "Disposition not recorded")
      + ready(False, "SCAR required, not created") + '</div><p class="app-label" style="margin:0">Close NCR becomes available when every item is met.</p>')}
{card("Related records", f'''<div class="app-list-stack">
<div class="app-list-row"><span style="flex:1"><a class="app-link" href="#">QE-2026-00187</a><br><span class="app-label">Quality Event</span></span>{status("Containment").replace("Containment", "Contained")}</div>
<div class="app-list-row"><span style="flex:1"><a class="app-link" href="#">HOLD-2026-00057</a><br><span class="app-label">Hold · RM48-9817</span></span>{pill("Active", "danger")}</div>
<div class="app-list-row"><span style="flex:1"><a class="app-link" href="#">HOLD-2026-00058</a><br><span class="app-label">Hold · FG-50022</span></span>{pill("Active", "danger")}</div>
<div class="app-list-row"><span style="flex:1"><a class="app-link" href="#">Lot RM48-9817</a><br><span class="app-label">Open in Lot Trace</span></span></div>
</div>''')}
{card(ic("sparkle") + " Quality Assistant", f'''<p class="app-text" style="margin:0"><strong>Summary.</strong> Supplier lot SUP-84721 of RM-1042 is 0.28 mm oversize. 120 units are held, 40 finished units are held, and 40 have shipped to one customer.</p>
<div class="app-panel app-stack" style="gap:8px"><span><strong>Likely repeat.</strong> <a class="app-link" href="#">NCR-2025-00412</a> (03/14/2025) had the same defect on RM-1042 from ABC Precision Components. Consider a CAPA.</span>
<span class="app-row"><button class="btn">{ic("check")}Accept</button><button class="btn">{ic("x")}Dismiss</button></span></div>
<div class="app-label">Agent activity <span class="mock-note">Later phase</span></div>''')}
</aside>"""

    body = f"""<main class="app-page-wide">
{header}
<div class="app-split">
<div class="app-split-main">
{tab_html}
<p class="mock-note edit-only" style="align-self:flex-start">Edit mode: the Overview cards switch to inputs in place. Fields set by the system stay as text.</p>
{overview}{containment}{holds}{disposition}{activity}{attachments}
</div>
{side}
</div>
</main>"""

    mockbar = ('<span class="mock-toggle" role="group" aria-label="Mode"><button data-mode="view" class="on">View</button>'
               '<button data-mode="edit">Edit</button></span>')
    script = """<script>
(function(){
  function setMode(m){
    document.body.classList.toggle('is-edit', m==='edit');
    document.querySelectorAll('.mock-toggle button').forEach(function(b){b.classList.toggle('on', b.dataset.mode===m)});
    if(m==='edit') showTab('overview');
  }
  function showTab(t){
    document.querySelectorAll('[data-tab]').forEach(function(b){b.classList.toggle('on', b.dataset.tab===t)});
    document.querySelectorAll('[data-panel]').forEach(function(p){p.hidden = p.dataset.panel!==t});
  }
  document.querySelectorAll('[data-mode]').forEach(function(b){b.addEventListener('click', function(){setMode(b.dataset.mode)})});
  document.querySelectorAll('[data-tab]').forEach(function(b){b.addEventListener('click', function(){showTab(b.dataset.tab)})});
  if(/mode=edit/.test(location.search)) setMode('edit');
})();
</script>"""
    return shell("NCR &amp; Containment Workspace", "NCRs", mockbar, body, script)


def build():
    out = DOCS / APP
    for name, html in [("ncr-list.html", ncr_list()), ("ncr-workspace.html", ncr_workspace())]:
        (out / name).write_text(html, encoding="utf-8")
        print(f"Wrote {out / name}")


if __name__ == "__main__":
    build()
