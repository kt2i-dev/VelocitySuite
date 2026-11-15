"""Builds docs/buttons.html (the Button standard) from the lists below.

Edit BUTTONS / PLACEMENT here, then run:  python3 tools/build_buttons.py
Icons are drawn inline for the mockups; the second value is the Phosphor 2.0 icon name to pick in
ODC Studio (the app's icon library).
"""
from pathlib import Path

# 24x24 stroke icons for the samples, and the Phosphor 2.0 name to use in OutSystems
ICONS = {
    "plus": ("M12 5v14M5 12h14", "plus"),
    "pencil": ("M4 20h4L19 9l-4-4L4 16v4z", "pencil-simple"),
    "save": ("M5 3h11l3 3v15H5zM8 3v5h7V3M8 21v-7h8v7", "floppy-disk"),
    "send": ("M22 2 11 13M22 2l-7 20-4-9-9-4z", "paper-plane-tilt"),
    "x": ("M6 6l12 12M18 6 6 18", "x"),
    "trash": ("M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14", "trash"),
    "user": ("M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21c0-4 4-6 8-6s8 2 8 6", "user"),
    "trace": ("M5 12h14M13 6l6 6-6 6", "arrow-right"),
    "hold": ("M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM10 9v6M14 9v6", "pause-circle"),
    "file": ("M6 2h9l5 5v15H6zM14 2v6h6", "file-text"),
    "users": ("M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM3 20c0-3 3-5 6-5s6 2 6 5M16 5a3 3 0 0 1 0 6M21 20c0-3-2-5-4-5", "users-three"),
    "shield": ("M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6z", "shield-check"),
    "refresh": ("M20 12a8 8 0 1 1-3-6.3M20 4v5h-5", "arrows-clockwise"),
    "check": ("M5 12l5 5 9-10", "check"),
    "flag": ("M5 21V4M5 4h12l-2 4 2 4H5", "flag"),
    "undo": ("M4 12a8 8 0 1 0 3-6.3M4 4v5h5", "arrow-counter-clockwise"),
    "download": ("M12 3v12M7 10l5 5 5-5M5 21h14", "download-simple"),
    "search": ("M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM21 21l-5-5", "magnifying-glass"),
    "more": ("M6 12h.01M12 12h.01M18 12h.01", "dots-three"),
    "camera": ("M4 7h4l2-3h4l2 3h4v12H4zM12 17a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z", "camera"),
    "clip": ("M21 12l-8 8a5 5 0 0 1-7-7l9-9a3 3 0 0 1 4 4l-9 9a1 1 0 0 1-2-2l8-8", "paperclip"),
    "comment": ("M4 4h16v12H8l-4 4z", "chat-text"),
    "bell": ("M6 16v-5a6 6 0 0 1 12 0v5l2 2H4zM10 21h4", "bell"),
    "eye": ("M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12zM12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z", "eye"),
    "back": ("M19 12H5M11 6l-6 6 6 6", "arrow-left"),
    "spark": ("M12 3l2 6 6 2-6 2-2 6-2-6-6-2 6-2z", "sparkle"),
    "power": ("M12 3v9M6.3 6.3a8 8 0 1 0 11.4 0", "power"),
}


def svg(name):
    d = ICONS[name][0]
    w = "3" if name == "more" else "2"
    return (f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg>')


def btn(label, icon, style="", small=False, disabled=False):
    cls = "btn" + (f" {style}" if style else "") + (" btn-sm" if small else "") + (" btn-icon" if not label else "")
    dis = " disabled" if disabled else ""
    aria = f' aria-label="{ICONS[icon][1]}"' if not label else ""
    return f'<span class="{cls}"{dis}{aria}>{svg(icon)}{label}</span>'


# (group, [(label, icon, style, block_or_form, where)])
B, P, D = "", "btn-primary", "btn-delete"
BUTTONS = [
    ("Record actions", [
        ("New Quality Event", "plus", P, "ButtonNew block (Label input)", "Top right of a list and the dashboard. Hidden for roles that can’t create. “New NCR”, “New CAPA” and so on on their lists."),
        ("Edit", "pencil", B, "ButtonEdit block", "Record header, View mode. Hidden once the record is Closed (BR-011)."),
        ("Save", "save", P, "In the form", "Edit mode, rightmost. Runs the form’s validation."),
        ("Save Draft", "save", B, "In the form", "Create form, left of Submit. Leaves the record in Draft."),
        ("Submit Quality Event", "send", P, "In the form", "Create form, rightmost. Draft → Submitted."),
        ("Cancel", "x", B, "ButtonCancel block", "Left of Save / Submit on every form and dialog. Leaves edit mode without saving."),
        ("Delete", "trash", D, "ButtonDelete block", "Draft records only (submitted quality records are never deleted), left of Cancel with a divider. Always confirms, naming the record: “Delete draft QE-2026-00187?”"),
    ]),
    ("Workflow actions", [
        ("Assign", "user", B, "ButtonAssign block", "Record header. Opens a user picker."),
        ("Trace Lot", "trace", B, "ButtonTraceLot block", "Record header of a Quality Event, NCR or MRB. Opens Lot Trace for the record’s lot."),
        ("Place Hold", "hold", B, "ButtonPlaceHold block", "Quality Event, NCR and Lot Trace. Not offered for a lot that has shipped."),
        ("Add Action", "plus", B, "ButtonAddAction block (Label input)", "Any record with actions. “Add Containment” on an NCR."),
        ("Create NCR", "file", B, "Workflow button", "Quality Event header."),
        ("Request MRB", "users", B, "Workflow button", "Quality Event and NCR header."),
        ("Create CAPA", "shield", B, "Workflow button", "Quality Event, NCR and SCAR header. Shown as primary when the assistant or a rule recommends a CAPA."),
        ("Create SCAR", "refresh", B, "Workflow button", "Quality Event and NCR header when a supplier is involved."),
        ("Issue SCAR", "send", P, "Workflow button", "SCAR header in Draft."),
        ("Close Event", "flag", B, "Workflow button", "Record header. “Close CAPA”, “Close SCAR”, “Submit for Closure” on an NCR. Disabled with the reason shown until the closure rules pass."),
        ("Reopen", "undo", B, "Workflow button", "In the More menu of a Closed record, Quality Manager only. Asks for a reason (BR-012)."),
    ]),
    ("Approvals", [
        ("Approve", "check", P, "ButtonApprove block", "MRB decisions, CAPA action plan, hold release, closures. A user can’t approve twice."),
        ("Reject", "x", B, "ButtonReject block", "Next to Approve. Requires a comment."),
        ("Request Information", "comment", B, "ButtonRequestInfo block", "MRB and SCAR review. Requires a comment."),
    ]),
    ("Lists and filters", [
        ("Apply", "search", P, "ButtonApply block", "Bottom of the filter panel. Runs the filter and returns the list to page 1."),
        ("Clear", "x", B, "ButtonClear block", "Right of Apply. Clears the filters and reloads the list."),
        ("Save View", "save", B, "ButtonSaveView block", "Under Apply / Clear. Saves the filters as a named view."),
        ("Export", "download", B, "ButtonExport block", "List header, right of New."),
        ("Open", "eye", B, "ButtonOpen block (small)", "Row Actions column, first. Opens the record’s workspace. The record number is also a link."),
        ("", "more", B, "ButtonMore block (small)", "Row Actions column, last; record header, last. Opens a menu of the row’s or record’s other actions."),
    ]),
    ("Evidence and communication", [
        ("Add Photo", "camera", B, "ButtonAddPhoto block", "Create Quality Event and actions. Opens the camera on a phone or tablet."),
        ("Add Attachment", "clip", B, "ButtonAddAttachment block", "Attachments tab and evidence sections."),
        ("Add Comment", "comment", B, "ButtonAddComment block", "Activity tab, SCAR communication."),
        ("Send Reminder", "bell", B, "Workflow button", "SCAR header while waiting on the supplier."),
    ]),
    ("Administration", [
        ("Deactivate", "power", B, "ButtonDeactivate block", "Reference data already in use, which can’t be deleted. “Activate” to bring it back."),
    ]),
    ("AI assistant", [
        ("Summarize", "spark", B, "Inside the AI Assistant Panel", "Every suggestion the assistant makes needs a person to accept it: suggestions carry Accept and Dismiss (small)."),
    ]),
]


def build():
    home = ('<nav class="mock-home" aria-label="Mockup navigation"><a href="index.html"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/></svg>Mockups home</a></nav>')
    rows = []
    for group, items in BUTTONS:
        rows.append(f'<tr><td class="grp" colspan="4">{group}</td></tr>')
        for label, icon, style, built, where in items:
            sample = btn(label, icon, style, small=(not label or "small" in built))
            rows.append(f"<tr><td>{sample}</td><td><code>{style or 'btn'}</code></td><td><code>{ICONS[icon][1]}</code></td>"
                        f"<td>{where}<br><span class=\"muted\">{built}</span></td></tr>")
    out = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Button Standard</title>
<link rel="stylesheet" href="assets/site.css"></head>
<body><main>{home}<h1>Button standard</h1>
<p>One icon and a label for every action, the same style and place on every screen of every Velocity Suite application. Generated by <code>tools/build_buttons.py</code>: edit that, not this page.</p>

<h2>Three styles</h2>
<div class="card">
<div class="btn-row">{btn("Submit", "send", P)}{btn("Edit", "pencil")}{btn("Delete", "trash", D)}{btn("Trace Lot", "trace", disabled=True)}</div>
<ul>
<li><code>btn</code>: outlined, the default for every action.</li>
<li><code>btn-primary</code>: filled. <strong>One per screen or section</strong>: the step that moves the record forward (Submit, Save, Issue SCAR, Approve, Apply). <span class="ours">Our standard</span></li>
<li><code>btn-delete</code>: red outline, for Delete only. A custom class we add to the theme. Cancel and Reject stay <code>btn</code>: red means data is about to be lost. <span class="ours">Our standard</span></li>
<li>A button that can’t be used yet stays visible but disabled, with the reason as its tooltip (“Available after submission”, “MRB-2026-00081 is still awaiting approval”). A button the user’s role can never use is hidden.</li>
</ul>
<p class="muted">Theme CSS for the new class, using OutSystems UI’s own error color:</p>
<pre class="card" style="margin:0;font-size:12.5px;overflow:auto">.btn.btn-delete {{ border-color: var(--color-error); color: var(--color-error); }}
.btn.btn-delete:hover {{ background-color: var(--color-error); color: var(--color-neutral-0); }}</pre>
</div>

<h2>Every button</h2>
<div class="card" style="overflow-x:auto">
<table class="dm"><thead><tr><th>Button</th><th>Class</th><th>Icon</th><th>Where it goes · how it’s built</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table>
<p class="muted">Icon names are <strong>Phosphor 2.0</strong>, the app’s icon library: pick them by these names in ODC Studio’s icon picker. Use the regular weight everywhere. The AI mentor review found about 120 icon references that don’t resolve in the app; replace each with the name from this table.</p>
</div>

<h2>The button blocks</h2>
<div class="card">
<ul>
<li><strong>One block per common button</strong> (ButtonEdit, ButtonCancel, ButtonDelete, ButtonAssign, ButtonApprove…), each with the icon, label and class built in, so the same action looks the same everywhere.</li>
<li><strong>Inputs:</strong> <code>IsEnabled</code> (Boolean, mandatory) and <code>ExtendedClass</code> (Text, optional). ButtonNew and ButtonAddAction also take <code>Label</code>.</li>
<li><strong>Event:</strong> <code>Clicked</code>, no parameters. What happens goes in the parent’s handler.</li>
<li><strong>Not blocks:</strong> Save, Save Draft and Submit stay plain buttons inside the form, because they have to run the form’s validation. They use OutSystems UI’s Button Loading (“Saving…”) and are disabled until the call finishes.</li>
<li><strong>Workflow buttons</strong> (Create NCR, Request MRB, Close Event…) are plain buttons with the icon and class above. Each calls one server action that checks the rule and moves the status, so status only changes through these actions.</li>
</ul>
<p class="muted">Same pattern as the LifeView button blocks.</p>
</div>

<h2>Placement</h2>
<div class="card">
<table class="dm"><thead><tr><th>Where</th><th>What goes there</th></tr></thead><tbody>
<tr><td>Record header, View</td><td>
<div class="btn-row">{btn("Create NCR", "file", P)}{btn("Edit", "pencil")}{btn("Trace Lot", "trace")}{btn("Add Action", "plus")}{btn("", "more", small=False)}</div>
The <strong>next workflow step</strong> for this record’s status and the user’s role as the one primary button, then up to three everyday actions, then More (⋯) for the rest (Assign, Request MRB, Create CAPA / SCAR, Reopen, Print, Export, Copy Link). Only actions valid for the current status show. <span class="ours">Our standard</span></td></tr>
<tr><td>Record header, Edit</td><td>
<div class="btn-row">{btn("Delete", "trash", D)}<span class="sep"></span>{btn("Cancel", "x")}{btn("Save", "save", P)}</div>
Delete (Draft only) on the left behind a divider; Cancel, then Save rightmost.</td></tr>
<tr><td>Create form</td><td>
<div class="btn-row">{btn("Cancel", "x")}{btn("Add Photo", "camera")}{btn("Save Draft", "save")}{btn("Submit Quality Event", "send", P)}</div>
At the bottom of the form, Submit rightmost. The follow-up actions (Create NCR, Place Hold, Trace Lot) appear in the record header once the event is submitted, not as disabled buttons under the form. <span class="ours">Our standard</span></td></tr>
<tr><td>List header</td><td>
<div class="btn-row">{btn("Export", "download")}{btn("New Quality Event", "plus", P)}</div>
Title left; Export and New right, New rightmost.</td></tr>
<tr><td>List rows</td><td>
<div class="btn-row">{btn("Open", "eye", small=True)}{btn("", "more", small=True)}</div>
Actions is the last column: Open, then More for the row’s other actions.</td></tr>
<tr><td>Filter panel</td><td>
<div class="btn-row">{btn("Clear", "x")}{btn("Apply", "search", P)}{btn("Save View", "save")}</div>
At the bottom of the panel. Filters don’t run until Apply.</td></tr>
<tr><td>Back</td><td>A text link with {svg("back").replace("<svg", '<svg width="14" height="14" style="vertical-align:-2px"')} Back above the record header, returning to the list or record the user came from. Not a button.</td></tr>
</tbody></table>
</div>

<h2>How this differs from the mockups</h2>
<div class="card">
<ul>
<li><strong>Fewer header buttons.</strong> The mockups put seven to ten outlined buttons in a row on every workspace, sometimes with two primaries (Save and Submit for Closure). Here: one primary, up to three others, then More.</li>
<li><strong>Red only for Delete.</strong> The Administration mockup draws Cancel in red; here Cancel is a plain <code>btn</code>.</li>
<li><strong>No disabled “after submission” row.</strong> The Create Quality Event mockup shows Create NCR, Place Hold and Trace Lot greyed out under the form; here they appear in the header once they can be used.</li>
<li>The icons follow the mockups’ choices where they had one.</li>
</ul>
</div>
</main></body></html>
"""
    path = Path(__file__).resolve().parent.parent / "docs/buttons.html"
    path.write_text(out, encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    build()
