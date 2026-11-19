"""Builds the screen mockups for Quality Event & Corrective Action Management, in
docs/quality-engineering/quality-event-capa/:

  sign-in.html, home.html                     sign-in and the home dashboard
  qe-workspace.html                           Quality Event workspace (View and Edit)
  ncr-list.html, ncr-workspace.html           NCR list and workspace (View and Edit)
  mrb-workspace.html                          MRB review and disposition (View and Edit)
  capa-workspace.html                         CAPA workspace (View and Edit)

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


# ---------- status -> pill variant (what the StatusBadge block does) ----------
# grey: draft · blue: in progress · amber: waiting on someone · green: done · red: rejected or held
VARIANT = {
    # NCR: the NCRStatus values in the app's database
    "Draft": "", "Submitted": "info", "QA Triage": "warning", "Containment": "info", "Investigation": "info",
    "Disposition": "warning", "Root Cause": "info", "CAPA Actions": "info", "Effectiveness": "info",
    "QA Approval": "warning", "Closed": "success",
    # Quality Event, MRB, CAPA: UI/UX spec until the database values are listed
    "Under Review": "warning", "Contained": "info", "Action Required": "warning", "Verification": "info",
    "Approved": "info", "Completed": "success", "Information Requested": "warning", "Rejected": "danger",
    "Root Cause Identified": "info", "Action Plan": "info", "Implementation": "info", "Effectiveness Review": "info",
    # SCAR, holds, actions, approvals
    "Supplier Response": "warning", "Active": "danger", "Released": "success",
    "Not Started": "", "In Progress": "info", "Verified": "success", "Pending": "", "Overdue": "danger",
}
NCR_STATUSES = ["Draft", "Submitted", "QA Triage", "Containment", "Investigation", "Disposition",
                "Root Cause", "CAPA Actions", "Effectiveness", "QA Approval", "Closed"]
QE_STATUSES = ["Draft", "Submitted", "Under Review", "Contained", "Investigation", "Action Required", "Verification", "Closed"]
MRB_STATUSES = ["Draft", "Under Review", "Approved", "Completed"]
CAPA_STATUSES = ["Draft", "Investigation", "Root Cause Identified", "Action Plan", "Implementation", "Effectiveness Review", "Closed"]


def pill(label, variant=""):
    cls = "app-pill" + (f" app-pill-{variant}" if variant else "")
    return f'<span class="{cls}">{escape(label)}</span>'


def status(label):
    return pill(label, VARIANT[label])


def severity(label):
    # Low and Medium read as text; only High and Critical get color
    return {"High": pill("High", "warning"), "Critical": pill("Critical", "danger")}.get(label, f"<span>{label}</span>")


HOLD = pill("HOLD", "danger")


def link(text, href="#"):  # record numbers never wrap
    return f'<a class="app-link app-num" href="{href}">{text}</a>'


def num(text):
    return f'<span class="app-num">{text}</span>'


# ---------- shell: LayoutSideMenu stand-in ----------
MENU = [
    ("house", "Home", "home.html"), ("warning", "Quality Events", "qe-workspace.html"), ("file-x", "NCRs", "ncr-list.html"),
    ("users-three", "MRB", "mrb-workspace.html"), ("shield-check", "CAPA", "capa-workspace.html"), ("arrows-clockwise", "SCAR", None),
    ("tree-structure", "Lot Trace", None), ("list-checks", "My Actions", None),
    ("-", "Insights", None), ("chart-bar", "Reports", None), ("gear", "Administration", None),
]

TOGGLE = ('<span class="mock-toggle" role="group" aria-label="Mode"><button data-mode="view" class="on">View</button>'
          '<button data-mode="edit">Edit</button></span>')

SCRIPT = """<script>
(function(){
  function setMode(m){
    document.body.classList.toggle('is-edit', m==='edit');
    document.querySelectorAll('.mock-toggle button').forEach(function(b){b.classList.toggle('on', b.dataset.mode===m)});
    if(m==='edit') showTab(document.querySelector('[data-tab]').dataset.tab);
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


def page(title, body, mockbar="", script=""):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Mockup</title>
<link rel="stylesheet" href="{ROOT}assets/app.css"></head>
<body>
<div class="mock-bar"><strong>Mockup</strong><span>{title}</span>{mockbar}<span class="mock-sp"></span><a href="index.html">Quality Event &amp; CAPA</a><a href="{ROOT}template.html">Screen template notes</a><a href="{ROOT}index.html">Mockups home</a></div>
{body}
{script}
</body></html>
"""


def shell(title, active, body, mockbar="", script=""):
    items = []
    for icon, label, href in MENU:
        if icon == "-":
            items.append(f'<div class="mock-group">{label}</div>')
            continue
        cls = ' class="active"' if label == active else ""
        items.append(f'<a{cls} href="{href or "#"}">{ic(icon)}{label}</a>')
    inner = f"""<div class="mock-shell">
<nav class="mock-menu" aria-label="Main menu">
<div class="mock-brand"><span class="mock-logo">KT2i</span><span><b>Velocity Suite</b><small>Quality &amp; CAPA</small></span></div>
{''.join(items)}
</nav>
<div class="mock-body">
<header class="mock-top"><span class="mock-search">{ic("magnifying-glass")}Search events, NCRs, lots, suppliers…</span>
<div class="mock-user">{ic("bell")}<span class="mock-avatar">ML</span><span>Maria Lopez<small>Quality Engineer</small></span></div></header>
{body}
</div></div>"""
    return page(title, inner, mockbar, script)


# ---------- building blocks ----------
def inp(v):
    return f'<input class="mock-input" value="{escape(v)}">'


def sel(v, opts):
    return '<select class="mock-input">' + "".join(
        f'<option{" selected" if o == v else ""}>{escape(o)}</option>' for o in opts) + "</select>"


def ta(v):
    return f'<textarea class="mock-input" rows="3">{escape(v)}</textarea>'


def field(label, value, edit=None, req=False, span=1):
    """A label and value. edit=None: set by the system, stays text in Edit mode.
    value=None: only shown in Edit mode (it's already in the key fields at the top)."""
    star = ' <span class="req edit-only">*</span>' if req and edit else ""
    style = f' style="grid-column:span {span}"' if span > 1 else ""
    if value is None:
        return f'<div class="app-field app-field-stack edit-only"{style}><span class="app-label">{label}{star}</span>{edit}</div>'
    if edit is None:
        return f'<div class="app-field app-field-stack"{style}><span class="app-label">{label}</span><span class="app-value">{value}</span></div>'
    return (f'<div class="app-field app-field-stack"{style}><span class="app-label">{label}{star}</span>'
            f'<span class="app-value view-only">{value}</span><span class="edit-only">{edit}</span></div>')


def text_field(label, value, req=False):
    """A long text: paragraph in View, text area in Edit."""
    return field(label, f'<span class="app-text">{escape(value)}</span>', ta(value), req=req)


def grid(n, *items, cls=""):
    return f'<div class="app-grid app-cols-{n}{" " + cls if cls else ""}">' + "".join(items) + "</div>"


def card(title, inner, extra=""):
    return f'<section class="app-card app-card-sm app-stack"><div class="app-row"><h3 class="app-card-title">{title}</h3>{extra}</div>{inner}</section>'


def card_btn(label, icon, primary=False):
    return f'<span class="app-actions"><button class="btn{" btn-primary" if primary else ""}">{ic(icon)}{label}</button></span>'


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


def readiness(title, rows, footer):
    return card(title, '<div class="app-list-stack">' + "".join(ready(*r) for r in rows)
                + f'</div><p class="app-label" style="margin:0">{footer}</p>')


def related(rows):
    """rows: (record, kind, status label or pill html or '')"""
    out = []
    for rec, kind, st in rows:
        badge = status(st) if st in VARIANT else st
        out.append(f'<div class="app-list-row"><span style="flex:1">{link(rec)}<br><span class="app-label">{kind}</span></span>{badge}</div>')
    return card("Related records", '<div class="app-list-stack">' + "".join(out) + "</div>")


def assistant(summary, suggestion):
    return card(ic("sparkle") + " Quality Assistant", f"""<p class="app-text" style="margin:0"><strong>Summary.</strong> {summary}</p>
<div class="app-panel app-stack" style="gap:8px"><span>{suggestion}</span>
<span class="app-row"><button class="btn">{ic("check")}Accept</button><button class="btn">{ic("x")}Dismiss</button></span></div>""")


def table(headers, rows):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div style="overflow-x:auto"><table class="app-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def more_link():
    return f'<a class="app-icon-link" href="#" aria-label="More">{ic("dots-three")}</a>'


def activity(events):
    return card("Activity", '<div class="app-list-stack">' + "".join(
        f'<div class="app-list-row"><span class="app-label app-num" style="min-width:118px">{t}</span><span><strong>{w}</strong> {e}</span></div>'
        for t, w, e in reversed(events)) + "</div>", card_btn("Add Comment", "chat-text"))


def attachments(files):
    return card("Attachments", '<table class="app-attach-table"><tbody>' + "".join(
        f'<tr><td>{ic("paperclip")} {link(n)}</td><td class="app-label">{c}</td><td class="app-label">{u}</td>'
        f'<td style="text-align:right"><a class="app-icon-link app-icon-link-danger" href="#" aria-label="Remove">{ic("trash")}</a></td></tr>'
        for n, c, u in files)
        + f'</tbody></table><div class="app-dropzone">{ic("upload-simple")}Drop files here or <a href="#">browse</a> · JPG, PNG, PDF, XLSX, DOCX</div>')


def workspace(*, title, active, back, number, pills, subtitle, primary, actions, more, key_fields, lifecycle,
              current, alert, tabs, side, kind):
    """The Details/Edit Screen Template. primary = (label, icon, disabled reason or None)."""
    p_label, p_icon, p_reason = primary
    p_attr = f' disabled title="{escape(p_reason)}"' if p_reason else ""
    view_btns = f'<button class="btn btn-primary"{p_attr}>{ic(p_icon)}{p_label}</button>' + "".join(
        f'<button class="btn"{" data-mode=" + chr(34) + "edit" + chr(34) if lbl == "Edit" else ""}>{ic(i)}{lbl}</button>' for lbl, i in actions)
    view_btns += f'<button class="btn" title="More: {escape(more)}" aria-label="More actions">{ic("dots-three")}</button>'
    reason = f'<span class="app-label view-only" style="width:100%;text-align:right">{ic("lock")} {p_reason}</span>' if p_reason else ""
    alert_html = f'<div class="app-alert-warning">{ic("warning")}<span>{alert}</span></div>' if alert else ""
    on = ' class="on"'
    tab_html = '<div class="mock-tabs" role="tablist">' + "".join(
        f'<button role="tab" data-tab="{k}"{on if i == 0 else ""}>{lbl}' + (f'<span class="count">{c}</span>' if c else "") + "</button>"
        for i, (k, lbl, c, _) in enumerate(tabs)) + "</div>"
    panels = "".join(
        f'<div data-panel="{k}" class="app-stack"{"" if i == 0 else " hidden"}>{html}</div>' for i, (k, _, _, html) in enumerate(tabs))
    body = f"""<main class="app-page-wide">
<div class="app-page-header">
<a class="app-back" href="{back[1]}">{ic("caret-left")}{back[0]}</a>
<div class="app-row" style="align-items:flex-start">
<div class="app-stack" style="gap:4px">
<div class="app-row"><h1 style="margin:0;font-size:24px">{number}</h1>{pills}</div>
<div style="font-size:16px">{subtitle}</div>
</div>
<div class="app-actions view-only">{view_btns}{reason}</div>
<div class="app-actions edit-only">
<span class="mock-note">Delete shows only while the {kind} is a Draft</span>
<button class="btn" data-mode="view">{ic("x")}Cancel</button>
<button class="btn btn-primary" data-mode="view">{ic("floppy-disk")}Save</button>
</div>
</div>
<div class="app-card app-card-sm">{grid(4, *[field(l, v) for l, v in key_fields])}</div>
<div class="app-card app-card-sm">{steps(lifecycle, current)}</div>
{alert_html}
</div>
<div class="app-split">
<div class="app-split-main">
{tab_html}
<p class="mock-note edit-only" style="align-self:flex-start">Edit mode: the {tabs[0][1]} cards switch to inputs in place. Fields set by the system stay as text.</p>
{panels}
</div>
<aside class="app-split-side">{side}</aside>
</div>
</main>"""
    return shell(title, active, body, TOGGLE, SCRIPT)


# ======================================================================
# NCR list
# ======================================================================
ROWS = [
    ("NCR-2026-00143", "Shaft diameter out of tolerance", "RM-1042", "Containment", "High", "RM48-9817", True, "ABC Precision Components", "Maria Lopez", "08/25/2026", False),
    ("NCR-2026-00142", "Porosity in housing casting", "CS-2210", "Disposition", "Medium", "CS22-4410", True, "Northline Castings", "Kevin Jones", "08/22/2026", False),
    ("NCR-2026-00141", "Label misprint on carton", "PK-0311", "Submitted", "Low", "PK03-1187", False, "Internal (Packaging)", "Sarah Mitchell", "08/21/2026", False),
    ("NCR-2026-00140", "Thread pitch gauge failure", "FS-0880", "CAPA Actions", "Medium", "FS08-2291", False, "Summit Fasteners", "Maria Lopez", "08/18/2026", False),
    ("NCR-2026-00139", "Seal hardness below specification", "PL-5520", "QA Triage", "High", "PL55-0712", True, "Delta Polymer Supply", "David Kim", "08/15/2026", True),
    ("NCR-2026-00138", "Weld spatter on mounting bracket", "FG-31007", "Effectiveness", "Low", "WIP-31007-B", False, "Internal (Line 3)", "Kevin Jones", "08/12/2026", False),
    ("NCR-2026-00137", "Heat-treat certificate missing", "RM-2040", "Investigation", "Critical", "RM20-5530", True, "Keystone Alloys", "Maria Lopez", "08/11/2026", True),
    ("NCR-2026-00136", "Surface scratches on cover", "FG-20415", "Draft", "Low", "FG20-0098", False, "Internal (Paint)", "Sarah Mitchell", "08/10/2026", False),
    ("NCR-2026-00135", "Bore runout out of tolerance", "MC-7781", "QA Approval", "Medium", "MC77-3302", False, "Internal (Machining)", "David Kim", "08/07/2026", False),
    ("NCR-2026-00131", "Wrong resin grade received", "PL-5521", "Closed", "Medium", "PL55-0650", False, "Delta Polymer Supply", "Kevin Jones", "07/29/2026", False),
]


def ncr_list():
    rows = []
    for n, title, mat, st, sev, lot, held, sup, owner, opened, overdue in ROWS:
        href = "ncr-workspace.html" if n == "NCR-2026-00143" else "#"
        warn = f' <span class="app-icon-warn" title="Has overdue actions">{ic("clock")}</span>' if overdue else ""
        rows.append(f"""<tr>
<td class="app-num">{link(n, href)}{warn}</td>
<td>{escape(title)}<br><span class="app-label">{mat}</span></td>
<td>{status(st)}</td><td>{severity(sev)}</td>
<td class="app-num">{lot}{' ' + HOLD if held else ''}</td>
<td>{escape(sup)}</td><td>{owner}</td><td class="app-num">{opened}</td>
<td style="white-space:nowrap"><a class="app-icon-link" href="{href}" title="Open" aria-label="Open {n}">{ic("eye")}</a>{more_link()}</td>
</tr>""")
    kpis = [("Open NCRs", "14", "4 opened this week", False), ("In containment", "5", "2 with held material", False),
            ("Waiting on QA", "4", "QA Triage and QA Approval", False), ("Overdue actions", "3", "On 2 NCRs", True)]
    kpi_html = "".join(
        f'<a class="app-kpi" href="#"><span class="app-kpi-label">{l}</span><span class="app-kpi-value app-num">{v}</span>'
        f'<span class="app-kpi-note">{(ic("clock") + " ") if w else ""}{n}</span></a>' for l, v, n, w in kpis)
    options = "".join(f"<option>{s}</option>" for s in NCR_STATUSES)
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
<select class="mock-input" style="width:auto"><option>All open statuses</option>{options}</select>
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
    return shell("NCR list", "NCRs", body)


# ======================================================================
# NCR workspace (08/25/2026, day one)
# ======================================================================
def ncr_workspace():
    yes_no = ["Yes", "No"]
    overview = "".join([
        card("Nonconformance",
             grid(2, '<div class="app-panel app-panel-info"><div class="app-label">Requirement</div><div class="app-value-lg app-num">Ø 10.00 mm ± 0.20</div><div class="app-label">Drawing RM-1042 rev C</div></div>',
                  '<div class="app-panel app-panel-danger"><div class="app-label">Actual</div><div class="app-value-lg app-num">Ø 10.48 mm</div><div class="app-label">0.28 mm over the upper limit</div></div>', cls="view-only")
             + grid(2, field("Requirement", "", inp("Ø 10.00 mm ± 0.20 (drawing RM-1042 rev C)"), req=True),
                    field("Actual condition", "", inp("Ø 10.48 mm measured on 25 of 25 samples"), req=True), cls="edit-only")
             + grid(3, field("Defect category", "Dimensional", sel("Dimensional", ["Dimensional", "Material", "Surface", "Documentation", "Process"]), req=True),
                    field("Defect code", "DIM-02 · Outside diameter high", sel("DIM-02 · Outside diameter high", ["DIM-01 · Outside diameter low", "DIM-02 · Outside diameter high", "DIM-05 · Runout"])),
                    field("Detected by", "Sarah Mitchell, 08/25/2026 09:05"))
             + text_field("Problem description", "Incoming inspection of receipt RCPT-39471 measured the shaft outside diameter at 10.48 mm against 10.00 ± 0.20 mm. All 25 sampled units failed, so the whole supplier lot SUP-84721 (200 units) is suspect.", req=True)),
        card("Product and source",
             grid(4, field("Material", None, sel("RM-1042", ["RM-1042", "RM-1043", "RM-2040"]), req=True),
                  field("Internal lot", None, sel("RM48-9817", ["RM48-9817", "RM48-9818"]), req=True),
                  field("Supplier lot", None, inp("SUP-84721")),
                  field("Receipt", "RCPT-39471", inp("RCPT-39471")),
                  field("Purchase order", "PO-448712", inp("PO-448712")),
                  field("Work order", "WO-875443 · consumed 80", inp("WO-875443")),
                  field("Location", "Receiving quarantine QA-01", sel("Receiving quarantine QA-01", ["Receiving quarantine QA-01", "Main stores", "FG-WH-A12"])))
             + '<p class="app-label" style="margin:0"><span class="view-only">Material, lot and supplier are in the key fields at the top.</span><span class="edit-only">Supplier comes from the lot and can’t be edited here.</span></p>'),
        card("Quantity and risk",
             grid(4, field("Failed", '<span class="app-value-lg app-num">25</span>', inp("25"), req=True),
                  field("Suspect", '<span class="app-value-lg app-num">200</span>', inp("200"), req=True),
                  field("Consumed", '<span class="app-value-lg app-num">80</span>'),
                  field("On hold", '<span class="app-value-lg app-num">160</span>'))
             + '<hr class="app-rule">'
             + grid(3, field("Risk", severity("High"), sel("High", ["Low", "Medium", "High", "Critical"]), req=True),
                    field("Customer impact", "Yes · 40 units shipped", sel("Yes", yes_no)),
                    field("Regulatory impact", "No", sel("No", yes_no)))
             + '<p class="app-label view-only" style="margin:0">Consumed and on-hold quantities come from Lot Trace and the holds.</p>'),
        card("Follow-up required",
             grid(3, field("MRB", pill("Required", "warning")), field("SCAR", pill("Required", "warning")), field("CAPA", "To be decided"), cls="view-only")
             + grid(3, '<label class="app-check"><input type="checkbox" checked> MRB required</label>',
                    '<label class="app-check"><input type="checkbox" checked> SCAR required</label>',
                    '<label class="app-check"><input type="checkbox"> CAPA required</label>', cls="edit-only")),
    ])
    actions = [("Quarantine 120 units of RM48-9817 in QA-01", "Sarah Mitchell", "08/25/2026", "Verified", "120 / 0 / 0"),
               ("Hold FG-50022 (40 units) in FG-WH-A12", "Robert Chen", "08/25/2026", "Verified", "40 / 0 / 0"),
               ("Notify Apex Industrial Systems about FG-50021", "Maria Lopez", "08/27/2026", "In Progress", "–"),
               ("100% inspect the remaining 120 units", "Kevin Jones", "08/29/2026", "Not Started", "–")]
    containment = card("Containment actions", table(
        ["Action", "Owner", "Due", "Status", "Inspected / accepted / rejected", ""],
        [(a, o, num(d), status(s), num(q), more_link()) for a, o, d, s, q in actions]), card_btn("Add Containment", "plus"))
    holds = card("Quality holds", table(
        ["Hold", "Material", "Quantity", "Status", "Placed"],
        [(link("HOLD-2026-00057"), "RM48-9817 · RM-1042", num("120"), status("Active"), num("08/25/2026")),
         (link("HOLD-2026-00058"), "FG-50022 · finished goods", num("40"), status("Active"), num("08/25/2026"))]),
        card_btn("Place Hold", "pause-circle"))
    disposition = card("Disposition", f"""<p class="app-text" style="margin:0">Not recorded yet. The MRB decides the disposition (use as is, rework, sort / 100% inspect, return to supplier or scrap); it shows here once the MRB is approved.</p>
<div><button class="btn">{ic("users-three")}Request MRB</button></div>""")
    events = [("08/25/2026 09:05", "Sarah Mitchell", "created Quality Event QE-2026-00187 from incoming inspection"),
              ("08/25/2026 09:21", "Sarah Mitchell", "placed lot RM48-9817 on hold (HOLD-2026-00057)"),
              ("08/25/2026 09:40", "Sarah Mitchell", "created this NCR from QE-2026-00187"),
              ("08/25/2026 09:55", "Kevin Jones", "triaged the NCR as High risk and assigned Maria Lopez"),
              ("08/25/2026 10:02", "Maria Lopez", "moved the NCR to Containment"),
              ("08/25/2026 11:15", "Robert Chen", "held FG-50022 in FG-WH-A12 (HOLD-2026-00058)")]
    files = [("Inspection report RCPT-39471.pdf", "Inspection", "Sarah Mitchell"),
             ("Shaft measurements.xlsx", "Measurement data", "Sarah Mitchell"),
             ("Photo – gauge reading.jpg", "Photo", "Sarah Mitchell")]
    side = "".join([
        readiness("Closure readiness", [(True, "Problem described and risk set"), (False, "Containment actions open", "2 of 4 still open"),
                                        (False, "MRB required, not requested"), (False, "Disposition not recorded"), (False, "SCAR required, not created")],
                  "Close NCR becomes available when every item is met."),
        related([("QE-2026-00187", "Quality Event", "Contained"), ("HOLD-2026-00057", "Hold · RM48-9817", "Active"),
                 ("HOLD-2026-00058", "Hold · FG-50022", "Active"), ("Lot RM48-9817", "Open in Lot Trace", "")]),
        assistant("Supplier lot SUP-84721 of RM-1042 is 0.28 mm oversize. 120 units are held, 40 finished units are held, and 40 have shipped to one customer.",
                  f'<strong>Likely repeat.</strong> {link("NCR-2025-00412")} (03/14/2025) had the same defect on RM-1042 from ABC Precision Components. Consider a CAPA.'),
    ])
    return workspace(
        title="NCR &amp; Containment Workspace", active="NCRs", back=("NCRs", "ncr-list.html"), kind="NCR",
        number="NCR-2026-00143", pills=status("Containment") + severity("High") + HOLD, subtitle="Shaft diameter out of tolerance",
        primary=("Move to Investigation", "arrow-right", None),
        actions=[("Edit", "pencil-simple"), ("Request MRB", "users-three"), ("Trace Lot", "arrow-right")],
        more="Add Containment, Place Hold, Create SCAR, Create CAPA, Assign, Export PDF, Copy Link",
        key_fields=[("Quality Event", link("QE-2026-00187", "qe-workspace.html")), ("Material", "RM-1042 · Stainless steel shaft"),
                    ("Lot", "RM48-9817 " + HOLD + " · supplier lot SUP-84721"), ("Supplier", "ABC Precision Components"), ("Owner", "Maria Lopez"),
                    ("Opened", num("08/25/2026")), ("Source", "Incoming inspection"), ("Containment due", num("08/29/2026"))],
        lifecycle=NCR_STATUSES, current=3,
        alert="<strong>40 units from this lot have shipped.</strong> FG-50021 went to Apex Industrial Systems on SH-48127. Customer notification is in progress.",
        tabs=[("overview", "Overview", "", overview), ("containment", "Containment", "4", containment), ("holds", "Holds", "2", holds),
              ("disposition", "Disposition", "", disposition), ("activity", "Activity", "6", activity(events)),
              ("attachments", "Attachments", "3", attachments(files))],
        side=side)


# ======================================================================
# Quality Event workspace (09/15/2026, the whole chain open)
# ======================================================================
def qe_workspace():
    overview = "".join([
        card("What happened",
             grid(3, field("Event type", "Nonconforming material", sel("Nonconforming material", ["Nonconforming material", "Process deviation", "Customer complaint", "Equipment issue"]), req=True),
                  field("Defect category", "Dimensional", sel("Dimensional", ["Dimensional", "Material", "Surface", "Documentation"])),
                  field("Source", None, sel("Incoming inspection", ["Incoming inspection", "In-process inspection", "Final inspection", "Customer complaint", "Supplier"]), req=True)) +
             text_field("Problem description", "Shaft outside diameter measured at 10.48 mm against 10.00 ± 0.20 mm on 25 of 25 samples from supplier lot SUP-84721.", req=True)),
        card("Where and when",
             grid(4, field("Detected at", "08/25/2026 09:05"), field("Detected by", "Sarah Mitchell"),
                  field("Plant", "Plant B", sel("Plant B", ["Plant A", "Plant B"]), req=True),
                  field("Location", "Receiving dock 2", sel("Receiving dock 2", ["Receiving dock 1", "Receiving dock 2", "Line 3"])))),
        '<div class="edit-only">' + card("Product and material",
             grid(3, field("Material", None, sel("RM-1042", ["RM-1042", "RM-1043"]), req=True),
                  field("Internal lot", None, sel("RM48-9817", ["RM48-9817", "RM48-9818"]), req=True),
                  field("Supplier lot", None, inp("SUP-84721")))) + "</div>",
        card("Immediate actions",
             text_field("What was done at the time", "Lot RM48-9817 tagged and moved to quarantine QA-01. Line 3 told not to issue RM-1042 from this lot.")),
    ])
    impact = card("Impact", grid(4, *[f'<div class="app-kpi"><span class="app-kpi-label">{l}</span><span class="app-kpi-value app-num">{v}</span><span class="app-kpi-note">{n}</span></div>'
                                       for l, v, n in [("Suspect", "200", "Whole supplier lot"), ("Known defective", "25", "Failed inspection"),
                                                       ("On hold", "120", "After the MRB sort released 40"), ("Customers exposed", "1", "40 units shipped")]])
                  + table(["Where the material is", "Quantity", "Status"],
                          [("RM48-9817 · receiving quarantine QA-01", num("120"), HOLD),
                           ("FG-50022 · FG-WH-A12 (sorted, released)", num("40"), status("Released")),
                           ("FG-50021 · shipped on SH-48127 to Apex Industrial Systems", num("40"), pill("CUSTOMER", "warning"))]),
                  card_btn("Open Lot Trace", "tree-structure"))
    acts = [("Notify Apex Industrial Systems about FG-50021", "NCR-2026-00143", "Maria Lopez", "08/27/2026", "Verified"),
            ("Sort RM48-9817 with go / no-go gauge", "MRB-2026-00081", "Kevin Jones", "09/05/2026", "Verified"),
            ("Return 25 rejected units to supplier", "MRB-2026-00081", "Robert Chen", "09/12/2026", "Overdue"),
            ("Supplier 8D response", "SCAR-2026-00024", "Mark Stevens", "09/18/2026", "In Progress"),
            ("Install tool-life counter on lathe L-4", "CAPA-2026-00031", "Mark Stevens", "09/30/2026", "In Progress")]
    actions_html = card("Actions across this event", table(["Action", "Record", "Owner", "Due", "Status"],
                        [(a, link(r), o, num(d), status(s)) for a, r, o, d, s in acts]), card_btn("Add Action", "plus"))
    events = [("08/25/2026 09:05", "Sarah Mitchell", "created this event from incoming inspection"),
              ("08/25/2026 09:21", "Sarah Mitchell", "placed RM48-9817 on hold"),
              ("08/25/2026 09:40", "Sarah Mitchell", "created NCR-2026-00143"),
              ("08/27/2026 14:10", "Maria Lopez", "requested MRB-2026-00081"),
              ("09/01/2026 10:30", "Maria Lopez", "issued SCAR-2026-00024 to ABC Precision Components"),
              ("09/02/2026 08:45", "Maria Lopez", "created CAPA-2026-00031 on the assistant’s suggestion")]
    side = "".join([
        readiness("Closure readiness", [(True, "Contained: material held and customer notified"), (True, "MRB-2026-00081 completed"),
                                        (False, "SCAR-2026-00024 waiting on supplier", "Response due 09/18/2026"),
                                        (False, "CAPA-2026-00031 in Implementation"), (False, "1 overdue action")],
                  "Move to Verification becomes available when every linked record is done."),
        related([("NCR-2026-00143", "NCR", "CAPA Actions"), ("MRB-2026-00081", "MRB · Sort / 100% inspect", "Completed"),
                 ("SCAR-2026-00024", "SCAR · ABC Precision Components", "Supplier Response"), ("CAPA-2026-00031", "CAPA", "Implementation"),
                 ("HOLD-2026-00057", "Hold · RM48-9817", "Active")]),
        assistant("RM-1042 shafts from ABC Precision were 0.28 mm oversize. 25 units rejected, 40 shipped to one customer, root cause traced to tool wear at the supplier.",
                  "<strong>Next step.</strong> Send a reminder to Mark Stevens: the SCAR response is due in 3 days."),
    ])
    return workspace(
        title="Quality Event Workspace", active="Quality Events", back=("Quality Events", "#"), kind="Quality Event",
        number="QE-2026-00187", pills=status("Investigation") + severity("High") + HOLD, subtitle="RM-1042 shafts oversize at incoming inspection",
        primary=("Move to Verification", "check", "Available when the SCAR and CAPA are done"),
        actions=[("Edit", "pencil-simple"), ("Trace Lot", "arrow-right"), ("Add Action", "plus")],
        more="Create NCR, Request MRB, Create SCAR, Create CAPA, Place Hold, Assign, Export PDF, Copy Link",
        key_fields=[("Material", "RM-1042 · Stainless steel shaft"), ("Lot", "RM48-9817 " + HOLD + " · supplier lot SUP-84721"),
                    ("Supplier", "ABC Precision Components"), ("Owner", "Maria Lopez"), ("Detected", num("08/25/2026")),
                    ("Source", "Incoming inspection"), ("Customer", "Apex Industrial Systems"), ("Age", "21 days")],
        lifecycle=QE_STATUSES, current=4,
        alert="<strong>1 action is overdue.</strong> Return 25 rejected units to supplier (MRB-2026-00081) was due 09/12/2026.",
        tabs=[("overview", "Overview", "", overview), ("impact", "Impact", "", impact), ("actions", "Actions", "5", actions_html),
              ("activity", "Activity", "6", activity(events)),
              ("attachments", "Attachments", "3", attachments([("Inspection report RCPT-39471.pdf", "Inspection", "Sarah Mitchell"),
                                                                ("Photo – gauge reading.jpg", "Photo", "Sarah Mitchell"),
                                                                ("Customer notice Apex.pdf", "Customer", "Maria Lopez")]))],
        side=side)


# ======================================================================
# MRB workspace (08/28/2026, under review)
# ======================================================================
def mrb_workspace():
    lines = card("Material under review", table(
        ["Lot", "Location", "Quantity", "Disposition", "Rejects go to"],
        [("RM48-9817 " + HOLD, "Receiving quarantine QA-01", num("120"),
          f'<span class="view-only">Sort / 100% Inspect</span><span class="edit-only">{sel("Sort / 100% Inspect", ["Use As Is", "Rework", "Repair", "Sort / 100% Inspect", "Scrap", "Return to Vendor"])}</span>',
          "Return to Vendor"),
         ("FG-50022 " + HOLD, "FG-WH-A12", num("40"),
          f'<span class="view-only">Sort / 100% Inspect</span><span class="edit-only">{sel("Sort / 100% Inspect", ["Use As Is", "Rework", "Sort / 100% Inspect", "Scrap"])}</span>',
          "Scrap")]))
    proposal = card("Instructions and cost",
                    grid(3, field("Estimated cost", num("$1,840"), inp("1840")), field("Sort hours", num("12"), inp("12")),
                         field("Proposed by", "Maria Lopez, 08/27/2026"))
                    + text_field("Instructions", "Check every unit with the 10.00 ± 0.20 mm go / no-go gauge. Release units in tolerance; tag rejects red and return them to ABC Precision Components against PO-448712.", req=True)
                    + text_field("Justification", "Oversize units can’t be reworked to size. Sorting saves the in-tolerance units and keeps Line 3 supplied."))
    approvers = [("Maria Lopez", "Quality Engineer", "Pending", "", "You"),
                 ("David Kim", "Engineering", "Approved", "08/28/2026 10:12", "Fit is unaffected inside tolerance; sort is fine."),
                 ("Robert Chen", "Operations", "Information Requested", "08/28/2026 11:40", "How many sort hours do we need on second shift?"),
                 ("Kevin Jones", "Quality Manager", "Pending", "", "")]
    rows = []
    for who, role, st, when, note in approvers:
        rows.append(f'<div class="app-list-row"><span style="flex:1"><strong>{who}</strong> · <span class="app-label">{role}</span>'
                    + (f'<br><span class="app-label">{note}</span>' if note else "") + "</span>"
                    + (f'<span class="app-label app-num">{when}</span>' if when else "") + status(st) + "</div>")
    approvals = card("Approvals", '<div class="app-list-stack">' + "".join(rows) + "</div>"
                     + f"""<div class="app-panel app-stack view-only" style="gap:8px"><strong>Your decision</strong>
<textarea class="mock-input" rows="2" placeholder="Comment (required to reject or request information)"></textarea>
<span class="app-row"><button class="btn btn-primary">{ic("check")}Approve</button><button class="btn">{ic("x")}Reject</button><button class="btn">{ic("chat-text")}Request Information</button></span></div>""")
    overview = lines + proposal + approvals
    events = [("08/27/2026 14:10", "Maria Lopez", "requested this MRB from NCR-2026-00143"),
              ("08/27/2026 14:22", "Maria Lopez", "proposed Sort / 100% Inspect for 160 units"),
              ("08/28/2026 10:12", "David Kim", "approved"),
              ("08/28/2026 11:40", "Robert Chen", "requested information: sort hours on second shift")]
    side = "".join([
        readiness("Completion readiness", [(True, "Disposition and instructions recorded"), (True, "Quantities match the NCR (160 held)"),
                                           (False, "Approvals", "1 of 4 in"), (False, "Information requested by Robert Chen")],
                  "Complete MRB becomes available when every required approver has responded (BR-007)."),
        related([("NCR-2026-00143", "NCR", "Containment"), ("QE-2026-00187", "Quality Event", "Contained"),
                 ("HOLD-2026-00057", "Hold · RM48-9817", "Active"), ("HOLD-2026-00058", "Hold · FG-50022", "Active")]),
        assistant("160 held shafts are 0.28 mm oversize at worst. The proposal sorts them all and returns rejects to the supplier.",
                  "<strong>Past decisions.</strong> 2 earlier MRBs on RM-1042 chose Sort / 100% Inspect; rejects averaged 14%."),
    ])
    return workspace(
        title="MRB Review &amp; Disposition", active="MRB", back=("MRB", "#"), kind="MRB",
        number="MRB-2026-00081", pills=status("Under Review") + severity("High"), subtitle="Disposition for 160 held RM-1042 shafts",
        primary=("Complete MRB", "check", "Waiting on 3 of 4 approvers"),
        actions=[("Edit", "pencil-simple"), ("Trace Lot", "arrow-right"), ("Send Reminder", "bell")],
        more="Add Approver, Add Action, Cancel MRB, Export PDF, Copy Link",
        key_fields=[("NCR", link("NCR-2026-00143", "ncr-workspace.html")), ("Quality Event", link("QE-2026-00187", "qe-workspace.html")),
                    ("Material", "RM-1042 · Stainless steel shaft"), ("Quantity", num("160")), ("Requested by", "Maria Lopez"),
                    ("Requested", num("08/27/2026")), ("Decision due", num("08/29/2026")), ("Risk", severity("High"))],
        lifecycle=MRB_STATUSES, current=1, alert="",
        tabs=[("overview", "Disposition", "", overview), ("activity", "Activity", "4", activity(events)),
              ("attachments", "Attachments", "2", attachments([("Sort plan.pdf", "Instructions", "Maria Lopez"),
                                                                ("Shaft measurements.xlsx", "Measurement data", "Sarah Mitchell")]))],
        side=side)


# ======================================================================
# CAPA workspace (09/15/2026, implementation)
# ======================================================================
def capa_workspace():
    overview = "".join([
        card("Problem",
             text_field("Problem statement", "RM-1042 shafts from ABC Precision Components arrived 0.28 mm oversize (lot SUP-84721). A similar NCR on the same part in 03/2025 makes this a repeat.", req=True)
             + grid(2, text_field("Scope", "RM-1042 and the other turned parts ABC Precision makes on lathe L-4 (RM-1043, RM-1050)."),
                    text_field("Business impact", "40 units shipped to a customer, 25 rejected, 6 hours of line downtime on Line 3."))),
        card("Root cause",
             grid(2, field("Category", "Supplier · Method", sel("Supplier", ["People", "Machine", "Method", "Material", "Measurement", "Supplier"]), req=True),
                  field("Confirmed by", "Maria Lopez, 09/09/2026"))
             + text_field("Confirmed root cause", "The supplier tracked cutting-tool life by hand, so tool wear on lathe L-4 went unnoticed and the diameter drifted oversize.", req=True)
             + text_field("Escape point", "Final inspection at the supplier sampled 1 part in 50, too few to catch the drift.", req=True)),
        card("Corrective action progress",
             grid(4, *[field(l, f'<span class="app-value-lg app-num">{v}</span>') for l, v in
                       [("Actions", "4"), ("Verified", "2"), ("Awaiting verification", "1"), ("In progress", "1")]])),
    ])
    whys = ["Why were the shafts oversize? The cutting tool on lathe L-4 was worn.",
            "Why was the tool worn? It wasn’t changed at its rated life of 400 parts.",
            "Why wasn’t it changed? Tool life was tracked by hand on a paper log.",
            "Why by hand? Lathe L-4 has no tool-life counter.",
            "Why no counter? The supplier’s control plan doesn’t require one for turned parts."]
    root = card("5 Whys", '<div class="app-list-stack">' + "".join(
        f'<div class="app-list-row"><span class="app-pill app-pill-info">{i}</span><span class="app-text" style="flex:1">{escape(w)}</span></div>'
        for i, w in enumerate(whys, 1)) + "</div>", card_btn("Add Why", "plus"))
    acts = [("Install tool-life counter on lathe L-4", "Mark Stevens (supplier)", "09/10/2026", "Verified"),
            ("Update control plan: change tool every 400 parts", "Mark Stevens (supplier)", "09/10/2026", "Verified"),
            ("Raise final inspection sampling to 1 in 10 for OD", "Mark Stevens (supplier)", "09/14/2026", "Completed"),
            ("Exclude RM-1042 from skip-lot for the next 3 lots", "Sarah Mitchell", "09/20/2026", "In Progress")]
    actions_html = card("Corrective actions", table(["Action", "Owner", "Due", "Status", ""],
                        [(a, o, num(d), status(s), more_link()) for a, o, d, s in acts]), card_btn("Add Action", "plus"))
    effect = card("Effectiveness check",
                  text_field("Success criteria", "No dimensional NCRs on RM-1042 across the next three supplier lots, over at least 60 days.", req=True)
                  + grid(3, field("Review period", "60 days", inp("60")), field("Starts", "When every action is verified"),
                         field("Result", "Not started", sel("Not started", ["Not started", "Effective", "Not Effective"]))))
    events = [("09/02/2026 08:45", "Maria Lopez", "created this CAPA from NCR-2026-00143 on the assistant’s suggestion"),
              ("09/09/2026 16:20", "Maria Lopez", "confirmed the root cause and escape point"),
              ("09/09/2026 16:25", "Maria Lopez", "moved the CAPA to Action Plan"),
              ("09/10/2026 09:00", "Kevin Jones", "approved the action plan; moved to Implementation"),
              ("09/12/2026 15:30", "Sarah Mitchell", "verified 2 supplier actions with photos from ABC Precision")]
    side = "".join([
        readiness("Closure readiness", [(True, "Root cause and escape point confirmed"), (False, "Corrective actions verified", "2 of 4"),
                                        (False, "Effectiveness check not started"), (False, "Effectiveness result recorded")],
                  "Close CAPA needs every action verified and an Effective result (BR-008, BR-009)."),
        related([("QE-2026-00187", "Quality Event", "Investigation"), ("NCR-2026-00143", "NCR", "CAPA Actions"),
                 ("SCAR-2026-00024", "SCAR · ABC Precision Components", "Supplier Response"), ("NCR-2025-00412", "Similar NCR, 03/14/2025", "Closed")]),
        assistant("Repeat oversize defect on RM-1042, traced to manual tool-life tracking at the supplier. Two of four actions are verified.",
                  "<strong>Check the scope.</strong> RM-1043 and RM-1050 run on the same lathe; consider adding their next lots to the effectiveness check."),
    ])
    return workspace(
        title="CAPA Workspace", active="CAPA", back=("CAPA", "#"), kind="CAPA",
        number="CAPA-2026-00031", pills=status("Implementation") + severity("High"), subtitle="Stop tool-wear drift on RM-1042 at ABC Precision Components",
        primary=("Move to Effectiveness Review", "arrow-right", "Available when all 4 actions are verified"),
        actions=[("Edit", "pencil-simple"), ("Add Action", "plus"), ("Send Reminder", "bell")],
        more="Find Similar Events, Assign, Export PDF, Copy Link",
        key_fields=[("Quality Event", link("QE-2026-00187", "qe-workspace.html")), ("NCR", link("NCR-2026-00143", "ncr-workspace.html")),
                    ("SCAR", link("SCAR-2026-00024")), ("Supplier", "ABC Precision Components"), ("Owner", "Maria Lopez"),
                    ("Opened", num("09/02/2026")), ("Due", num("10/30/2026")), ("Source", "NCR and SCAR")],
        lifecycle=CAPA_STATUSES, current=4, alert="",
        tabs=[("overview", "Overview", "", overview), ("root", "Root cause", "", root), ("actions", "Actions", "4", actions_html),
              ("effectiveness", "Effectiveness", "", effect), ("activity", "Activity", "5", activity(events)),
              ("attachments", "Attachments", "2", attachments([("Tool-life counter photo.jpg", "Evidence", "Mark Stevens"),
                                                                ("Control plan rev F.pdf", "Evidence", "Mark Stevens")]))],
        side=side)


# ======================================================================
# Home dashboard and sign-in
# ======================================================================
MODULES = [("warning", "Quality Events", "Record an issue in about a minute and follow it to closure.", "12 open", "qe-workspace.html"),
           ("file-x", "NCR &amp; MRB", "Document nonconformances, contain them and decide the disposition.", "14 NCRs · 3 MRBs", "ncr-list.html"),
           ("shield-check", "CAPA &amp; SCAR", "Find root causes, fix them with suppliers and check the fix worked.", "6 CAPAs · 4 SCARs", "capa-workspace.html"),
           ("tree-structure", "Lot Trace", "See where a lot came from, where it went and who received it.", "2 lots on hold", "#")]


def module_cards():
    return "".join(f"""<a class="app-card app-card-sm app-stack" href="{href}"><span class="app-icon-badge">{ic(icon)}</span>
<span class="app-card-title">{title}</span><span class="app-label" style="font-size:13px">{desc}</span><span class="app-label app-num">{count}</span></a>"""
                   for icon, title, desc, count, href in MODULES)


def home():
    counts = [("Open events", "12"), ("Contained", "4"), ("Awaiting approval", "3"), ("Overdue actions", "2")]
    count_html = "".join(f'<div class="app-kpi"><span class="app-kpi-label">{l}</span><span class="app-kpi-value app-num">{v}</span></div>' for l, v in counts)
    mine = [("Approve", link("MRB-2026-00084"), "Disposition for CS22-4410 castings", "Today", "Pending"),
            ("Review", link("SCAR-2026-00024"), "8D response from ABC Precision Components", "09/18/2026", "Supplier Response"),
            ("Verify", link("CAPA-2026-00031", "capa-workspace.html"), "Raise final inspection sampling to 1 in 10", "09/16/2026", "Completed"),
            ("Follow up", link("MRB-2026-00081", "mrb-workspace.html"), "Return 25 rejected units to supplier", "09/12/2026", "Overdue")]
    mine_html = card("My work", table(["", "Record", "What", "Due", "Status"],
                     [(f"<strong>{v}</strong>", r, w, num(d), status(s)) for v, r, w, d, s in mine]), card_btn("All my actions", "list-checks"))
    recent = [("QE-2026-00192", "Cracked bracket weld on Line 3", "Submitted", "Medium", "Kevin Jones", "09/15/2026"),
              ("QE-2026-00191", "Customer complaint: loose fasteners", "Under Review", "High", "Maria Lopez", "09/14/2026"),
              ("QE-2026-00190", "Resin moisture above limit", "Contained", "Medium", "David Kim", "09/12/2026"),
              (link("QE-2026-00187", "qe-workspace.html"), "RM-1042 shafts oversize", "Investigation", "High", "Maria Lopez", "08/25/2026")]
    recent_html = card("Recent quality events", table(["Event", "Title", "Status", "Severity", "Owner", "Detected"],
                       [(e if e.startswith("<") else link(e), t, status(s), severity(v), o, num(d)) for e, t, s, v, o, d in recent]))
    attention = card("Needs attention", '<div class="app-list-stack">' + "".join([
        f'<div class="app-list-row"><span class="app-icon-warn">{ic("clock")}</span><span>2 actions overdue<br><span class="app-label">Oldest 3 days, on MRB-2026-00081</span></span></div>',
        f'<div class="app-list-row">{HOLD}<span>2 lots on hold<br><span class="app-label">RM48-9817, CS22-4410</span></span></div>',
        f'<div class="app-list-row">{pill("Critical", "danger")}<span>1 critical NCR<br><span class="app-label">NCR-2026-00137 · heat-treat certificate missing</span></span></div>',
        f'<div class="app-list-row">{pill("CUSTOMER", "warning")}<span>1 customer exposed<br><span class="app-label">Apex Industrial Systems · FG-50021</span></span></div>',
    ]) + "</div>")
    body = f"""<main class="app-page-wide app-stack" style="gap:16px">
<section class="app-hero">
<div class="app-stack" style="gap:6px;max-width:560px">
<span class="app-label">Tuesday, 09/15/2026</span>
<h1 class="app-hero-title">Good morning, Maria. <span class="app-hero-accent">4 things need you today.</span></h1>
<span class="app-text">Contain quality issues fast, trace affected material and fix root causes, from one place.</span>
<span class="app-row" style="margin-top:6px"><button class="btn btn-primary">{ic("plus")}New Quality Event</button><button class="btn">{ic("tree-structure")}Open Lot Trace</button></span>
</div>
<div class="app-grid app-cols-2" style="min-width:300px">{count_html}</div>
</section>
<div class="app-grid app-cols-4">{module_cards()}</div>
<div class="app-split"><div class="app-split-main">{mine_html}{recent_html}</div><aside class="app-split-side">{attention}</aside></div>
</main>"""
    return shell("Home dashboard", "Home", body)


def sign_in():
    body = f"""<main class="app-grid app-cols-2" style="min-height:calc(100vh - 41px);gap:0">
<section class="app-hero" style="border-radius:0;align-content:center">
<div class="app-stack" style="gap:16px;max-width:520px;margin:0 auto">
<div class="app-row"><span class="mock-logo">KT2i</span><span class="app-label">Velocity Suite for Manufacturing</span></div>
<h1 class="app-hero-title" style="font-size:32px">Quality Event &amp; Corrective Action Management<br><span class="app-hero-accent">CAPA · SCAR · MRB · NCR · Lot Trace</span></h1>
<span class="app-text">Contain quality issues faster, trace affected material across lots and shipments, and fix root causes with your suppliers.</span>
<div class="app-grid app-cols-2">{''.join(f'<span class="app-row">{ic(i)}<span>{t}</span></span>' for i, t, _, _, _ in MODULES)}</div>
</div>
</section>
<section class="app-stack" style="justify-content:center;padding:32px">
<div class="app-card app-card-lg app-stack" style="max-width:400px;width:100%;margin:0 auto">
<h2 class="app-card-title" style="font-size:20px">Sign in</h2>
<span class="app-label" style="font-size:13px">Use your company account.</span>
<button class="btn btn-primary" style="justify-content:center">{ic("lock")}Continue with company sign-in</button>
<hr class="app-rule">
<div class="app-field app-field-stack"><span class="app-field-label">Email</span><input class="mock-input" placeholder="name@company.com"></div>
<div class="app-field app-field-stack"><span class="app-field-label">Password</span><input class="mock-input" type="password"></div>
<button class="btn" style="justify-content:center">Sign in with email</button>
<a class="app-link" href="home.html" style="font-size:13px">Mockup: go to the home dashboard</a>
</div>
</section>
</main>"""
    return page("Sign-in", body)


def build():
    out = DOCS / APP
    for name, fn in [("sign-in.html", sign_in), ("home.html", home), ("qe-workspace.html", qe_workspace),
                     ("ncr-list.html", ncr_list), ("ncr-workspace.html", ncr_workspace),
                     ("mrb-workspace.html", mrb_workspace), ("capa-workspace.html", capa_workspace)]:
        (out / name).write_text(fn(), encoding="utf-8")
        print(f"Wrote {out / name}")


if __name__ == "__main__":
    build()
