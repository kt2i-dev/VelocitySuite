"""Builds docs/manufacturing/quality/data-model.html from the entity list below.

Edit MODEL (and RELATIONSHIPS) here, then run:  python3 tools/build_data_model.py
Each attribute is "Name: Type", with a trailing * when mandatory. A line starting with "# "
is a group heading inside the entity's table. Every entity also has an Id (Long Integer,
except the static entities, whose Id is shown).
"""
from html import escape
from pathlib import Path

STANDARD_STATIC = "Id: Text*\nLabel: Text*\nOrder: Integer*\nIs_Active: Boolean*\nColor: Text"

MODEL = [
    ("Core quality records", "core", [
        ("QualityEvent", "The issue as it was found. Every other quality record starts from or links to one.", """
# Identity and detection
EventType: Text*
EventTitle: Text
ProblemTitle: Text*
ProblemDescription: Text
EventSourceId: EventSource*
DateTimeDetected: DateTime*
DetectedById: User*
AssignedOwnerId: User
QualityEventStatusId: QualityEventStatus*
SeverityId: Severity
DueDate: Date
LastUpdatedDate: DateTime
# Location
Plant: Text
Site: Text
Department: Text
ProductionArea: Text
WorkCenter: Text
ProductionLine: Text
# Traceability
ProductId: Product
MaterialId: Material
LotId: Lot
SerialNumberId: SerialNumber
SupplierId: Supplier
PurchaseOrderId: PurchaseOrder
ReceiptId: Receipt
WorkOrderId: WorkOrder
ProductionOperationId: ProductionOperation
# Defect details
DefectCategory: Text
DefectCodeId: DefectCode
FailureMode: Text
SpecificationRequirement: Text
ActualMeasurement: Text
ExpectedMeasurement: Text
UnitOfMeasure: Text
DetectionMethod: Text
# Quantities
QuantityProduced: Decimal
QuantityInspected: Decimal
QuantityAffected: Decimal
QuantitySuspect: Decimal
QuantityFailed: Decimal
# Risk and impact
Probability: Integer
Detectability: Integer
RiskScore: Integer
CustomerImpact: Text
CustomerImpactKnown: Text
SafetyImpact: Text
SafetyImpacted: Boolean
# Immediate actions
ImmediateActionNotes: Text
ProductionStopRequired: Boolean
StopProduction: Boolean
QuarantineMaterial: Boolean
Perform100PercentInspection: Boolean
BlockShipment: Boolean
NotifyQualityManager: Boolean
NotifySupplier: Boolean"""),
        ("NCR", "Nonconformance Report.", """
# Identity
NCRNumber: Text*
QualityEventId: QualityEvent*
DateCreated: DateTime*
CreatedById: User*
OwnerId: User
NCRStatusId: NCRStatus*
ResponsibleDepartment: Text
# Traceability
ProductId: Product
MaterialId: Material
LotId: Lot
SerialNumberId: SerialNumber
WorkOrderId: WorkOrder
SupplierId: Supplier
PurchaseOrderId: PurchaseOrder
ReceiptId: Receipt
InventoryLocationId: InventoryLocation
DefectCodeId: DefectCode
SupplierLot: Text
# Problem description
ProblemTitle: Text
ProblemDescription: Text
Requirement: Text
ObservedCondition: Text
ActualCondition: Text
DefectType: Text
# Quantities
QuantityAffected: Decimal
QuantitySuspect: Decimal
# Containment and risk
ImmediateAction: Text
ContainmentStatus: Text
ProposedDisposition: Text
RiskClassificationId: RiskClassification
# Flags
MRBRequired: Boolean
CAPARequired: Boolean
SCARRequired: Boolean
CustomerImpact: Boolean
RegulatoryImpact: Boolean"""),
        ("MRBReview", "A Material Review Board review of an NCR's material.", """
# Identity
NCRId: NCR*
ReviewDate: DateTime*
ReviewedById: User*
OwnerId: User
MRBStatusId: MRBStatus
QualityEventId: QualityEvent
# Material
LotId: Lot
InventoryLocationId: InventoryLocation
QuantityAffected: Decimal
# Review content
DefectDescription: Text
CustomerExposure: Text
Specification: Text
EngineeringInformation: Text
# Disposition
ProposedDispositionId: DispositionType
EstimatedDispositionCost: Currency
ApprovalHistoryId: Approval"""),
        ("MRBDisposition", "The board's decision on a review.", """
MRBReviewId: MRBReview*
DispositionTypeId: MRBDispositionType*
DispositionDate: DateTime*
DispositionById: User*
Comments: Text"""),
        ("CAPA", "Corrective and Preventive Action.", """
# Identity
CAPANumber: Text
Title: Text
Description: Text
CategoryId: CAPACategory*
CAPAStatusId: CAPAStatus*
SeverityId: Severity
SourceId: CAPASource
DateCreated: DateTime*
CreatedById: User*
OwnerId: User
DueDate: Date
# Links
QualityEventId: QualityEvent
NCRId: NCR
SCARId: SCAR
# Investigation
ProblemStatement: Text
BusinessImpact: Text
Scope: Text
InvestigationSummary: Text
ConfirmedRootCause: Text
EscapePoint: Text
# Effectiveness and closure
EffectivenessResult: Text
ReviewPeriodDays: Integer
VerifiedById: User
VerificationDate: DateTime
ClosedOn: DateTime
ClosedById: User
ReopenReason: Text
ReopenedById: User"""),
        ("SCAR", "Supplier Corrective Action Request.", """
# Identity
SCARNumber: Text*
SupplierId: Supplier*
SupplierSite: Text
SupplierContactId: SupplierContact
SCARStatusId: SCARStatus*
SeverityId: Severity
# Links
QualityEventId: QualityEvent
NCRId: NCR
ProductId: Product
MaterialId: Material
PurchaseOrderId: PurchaseOrder
ReceiptId: Receipt
# Part and lot
SupplierPartNumber: Text
InternalPartNumber: Text
SupplierLot: Text
QuantityAffected: Decimal
# Content
ProblemStatement: Text
EvidenceSummary: Text
ManufacturerVerificationNote: Text
EvidenceId: File
# Dates
IssueDate: Date
ResponseDueDate: Date
SupplierAcknowledgementDate: Date"""),
        ("SCAR8DResponse", "One step of the supplier's 8D answer to a SCAR.", """
SCARId: SCAR*
StepCode: Text*
StepTitle: Text
ResponseText: Text
ManufacturerComment: Text
ReviewStatus: Text
SubmittedDate: DateTime
AttachmentFileId: File"""),
        ("RootCause", "A root cause found for a Quality Event, NCR, CAPA or SCAR.", """
RootCauseCategoryId: RootCauseCategory*
QualityEventId: QualityEvent
NCRId: NCR
CAPAId: CAPA
SCARId: SCAR
EvidenceId: File
InvestigativeSummary: Text
RootCause: Text
ConfirmedRootCause: Text
EscapePointText: Text"""),
        ("RootCauseAnalysis", "The “Why” rows of a root cause (5 Whys).", """
RootCauseId: RootCause
Question: Text
Answer: Text
Order: Integer"""),
        ("Action", "A task assigned to someone, from a Quality Event or CAPA.", """
ActionDescription: Text*
ActionType: Text
OwnerId: User*
Department: Text
DueDate: Date
Priority: Integer
ActionStatusId: ActionStatus*
CompletionDate: Date
EvidenceId: File
ApprovalRequired: Boolean
VerifiedById: User
VerificationDate: DateTime
SourceEntityType: Text
CAPAId: CAPA
QualityEventId: QualityEvent
ImplementationNotes: Text"""),
        ("ContainmentAction", "A containment step on an NCR, with its inspection counts.", """
NCRId: NCR*
ActionId: Action*
OwnerId: User*
DueDate: Date
StatusId: ActionStatus*
CompletionDate: Date
EvidenceId: File
QuantityInspected: Decimal
QuantityAccepted: Decimal
QuantityRejected: Decimal"""),
        ("EffectivenessCheck", "Whether a CAPA's fix worked.", """
CAPAId: CAPA*
ActionId: Action
CheckDate: DateTime
CheckedById: User*
Result: Text
Comments: Text
Criteria: Text
MeasurementMethod: Text"""),
        ("QualityHold", "A hold on material until it's released.", """
HoldNumber: Text*
QualityEventId: QualityEvent
NCRId: NCR
LotId: Lot
MaterialId: Material
InventoryLocationId: InventoryLocation
Quantity: Decimal
Reason: Text
DatePlaced: DateTime
PlacedById: User
QualityHoldStatus: Text
ReleaseAuthorizationId: User
ReleaseDate: DateTime"""),
    ]),
    ("Cross-cutting records", "cross", [
        ("File", "An attachment on any record.", """
FileName: Text*
AttachmentCategoryId: AttachmentCategory*
Description: Text
UploadedById: User*
UploadDate: DateTime*
RelatedEntityType: Text
FileUrl: Text
FileSize: Long Integer
FileContent: Binary Data
ContentType: Text
QualityEventId: QualityEvent
CAPAId: CAPA
NCRId: NCR
EffectivenessCheckId: EffectivenessCheck"""),
        ("Approval", "", """
EntityType: Text*
ApproverId: User*
ApprovalDate: DateTime*
ApprovalStatus: Text*
Comments: Text"""),
        ("AuditLog", "", """
EntityType: Text*
ActionType: Text*
PerformedById: User*
PerformedDate: DateTime*
Details: Text
QualityEventId: QualityEvent"""),
        ("Comment", "", """
EntityType: Text*
CommentText: Text*
CreatedById: User*
CreatedDate: DateTime*"""),
    ]),
    ("Master and traceability data", "master", [
        ("Customer", "", "CustomerName: Text*\nContactName: Text\nPhoneNumber: Phone\nEmail: Email"),
        ("DefectCode", "", "Code: Text*\nDescription: Text"),
        ("InventoryLocation", "", "LocationName: Text*\nDescription: Text"),
        ("Lot", "", "LotNumber: Text*\nProductId: Product\nMaterialId: Material\nBatchNumber: Text\nSupplierLotNumber: Text\nProductionDate: Date\nWorkOrderId: WorkOrder"),
        ("LotGenealogy", "Parent/child links between lots: splits, merges, rework and multi-level BOMs.", "ParentLotId: Lot*\nChildLotId: Lot*"),
        ("Material", "", "MaterialNumber: Text*\nDescription: Text\nRevision: Text\nSupplierId: Supplier"),
        ("Product", "", "ProductNumber: Text*\nDescription: Text\nRevision: Text\nMaterialId: Material"),
        ("ProductionOperation", "", "OperationName: Text*\nWorkOrderId: WorkOrder\nMachine: Text\nTool: Text\nShift: Text\nOperatorId: User"),
        ("PurchaseOrder", "", "PurchaseOrderNumber: Text*\nSupplierId: Supplier\nOrderDate: Date\nTotalAmount: Currency"),
        ("Receipt", "", "ReceiptNumber: Text*\nPurchaseOrderId: PurchaseOrder\nSupplierId: Supplier\nReceiptDate: Date\nQuantityReceived: Decimal"),
        ("SerialNumber", "", "SerialNumberValue: Text*\nLotId: Lot\nProductId: Product"),
        ("Shipment", "", "ShipmentNumber: Text*\nCustomerId: Customer\nShipmentDate: Date\nLotId: Lot\nQuantityShipped: Decimal"),
        ("Supplier", "", "SupplierName: Text*\nSupplierSite: Text\nContactId: SupplierContact"),
        ("SupplierContact", "", "SupplierId: Supplier*\nContactName: Text*\nPhoneNumber: Phone\nEmail: Email"),
        ("WorkOrder", "", "WorkOrderNumber: Text*\nProductId: Product\nQuantity: Decimal\nStartDate: Date\nEndDate: Date"),
    ]),
    ("Static entities (lookups)", "static", [
        ("Standard lookups", "AttachmentCategory, CAPACategory, CAPASource, CAPAStatus, DispositionType, EventSource, MRBDispositionType, NCRStatus, RiskClassification, RootCauseCategory, SCARStatus, Severity. Their values are still to be listed here.", STANDARD_STATIC),
        ("ActionStatus, QualityEventStatus", "The standard set plus IsFinal.", STANDARD_STATIC + "\nIsFinal: Boolean"),
        ("MRBStatus", "", "Id: Integer*\nLabel: Text"),
        ("DateRangeOption", "", "Id: Integer*\nIs_Active: Boolean\nOrder: Integer\nLabel: Text*\nDays: Integer*"),
    ]),
]

RELATIONSHIPS = [
    "A <strong>QualityEvent</strong> has NCRs, CAPAs, SCARs, quality holds, files, actions and audit entries.",
    "An <strong>NCR</strong> has MRB reviews, containment actions, root causes and files.",
    "An <strong>MRBReview</strong> has MRB dispositions.",
    "A <strong>CAPA</strong> has actions, effectiveness checks, root causes and files.",
    "A <strong>SCAR</strong> has 8D responses.",
    "A <strong>RootCause</strong> has root cause analysis (“Why”) rows.",
    "A <strong>Lot</strong> links to its genealogy (parents and children), serial numbers and shipments, and is referenced by NCRs, Quality Events and quality holds.",
    "A <strong>Supplier</strong> links to materials, purchase orders, receipts and contacts.",
    "A <strong>Product</strong> links to Material, WorkOrder and Lot.",
    "The system <strong>User</strong> and <strong>Role</strong> entities are referenced read-only.",
]

ENTITY_NAMES = {name for _, _, ents in MODEL for name, _, _ in ents}


def anchor(name):
    return "e-" + name.split(",")[0].strip().lower()


def type_cell(t):
    t = t.strip()
    return f'<a class="inl" href="#{anchor(t)}">{escape(t)}</a>' if t in ENTITY_NAMES else escape(t)


def table(spec):
    rows = []
    for line in spec.strip().splitlines():
        line = line.strip()
        if line.startswith("# "):
            rows.append(f'<tr><td class="grp" colspan="2">{escape(line[2:])}</td></tr>')
            continue
        name, typ = (s.strip() for s in line.split(":", 1))
        req = typ.endswith("*")
        typ = typ.rstrip("*")
        mark = ' <span class="req" title="Mandatory">*</span>' if req else ""
        rows.append(f"<tr><td><code>{escape(name)}</code>{mark}</td><td>{type_cell(typ)}</td></tr>")
    return '<table class="dm"><thead><tr><th>Attribute</th><th>Type</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>"


def build():
    home = '<nav class="mock-home" aria-label="Mockup navigation"><a href="../../index.html"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/></svg>Mockups home</a></nav>'
    out = [
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>QA Data Model</title>",
        '<link rel="stylesheet" href="../../assets/site.css"></head>',
        f"<body><main>{home}",
        '<p class="crumbs"><a href="../index.html">Manufacturing</a> › <a href="index.html">Quality Assurance</a> ›</p><h1>Data model</h1>',
        "<p>The entities in the OutSystems module <code>VS_MFG_QualityAssurance</code>. "
        '<span class="req">*</span> marks a mandatory attribute. Every entity also has an <code>Id</code> '
        "(a Long Integer, except the static entities). Generated by <code>tools/build_data_model.py</code>: edit that, not this page.</p>",
        '<div class="toc">' + "".join(f'<a href="#{gid}">{escape(g)}</a>' for g, gid, _ in MODEL) + '<a href="#relationships">Relationships</a></div>',
        '<h2 id="relationships">Relationships</h2><div class="card"><ul>' + "".join(f"<li>{r}</li>" for r in RELATIONSHIPS) + "</ul></div>",
    ]
    for group, gid, ents in MODEL:
        out.append(f'<h2 id="{gid}">{escape(group)}</h2>')
        for name, desc, spec in ents:
            d = f'<p class="muted">{escape(desc)}</p>' if desc else ""
            out.append(f'<div class="card" id="{anchor(name)}"><h3>{escape(name)}</h3>{d}{table(spec)}</div>')
    out.append("</main></body></html>\n")
    path = Path(__file__).resolve().parent.parent / "docs/manufacturing/quality/data-model.html"
    path.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    build()
