#!/usr/bin/env python3
"""Generate England-format CV and cover letter for Network Rail SPM application."""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Twips, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def set_run_font(run, name="Calibri", size=11, bold=False, italic=False, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def add_horizontal_line(paragraph):
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "12")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "1F4E79")
    pBdr.append(bottom)
    pPr.append(pBdr)


def set_narrow_margins(section, top=1.5, bottom=1.5, left=1.8, right=1.8):
    section.top_margin = Cm(top)
    section.bottom_margin = Cm(bottom)
    section.left_margin = Cm(left)
    section.right_margin = Cm(right)


def para(doc, text="", space_after=6, space_before=0, align=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = 1.08
    if text:
        run = p.add_run(text)
        set_run_font(run)
    return p


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after = Pt(4)
    run = p.add_run(text.upper())
    set_run_font(run, size=11, bold=True, color=RGBColor(0x1F, 0x4E, 0x79))
    add_horizontal_line(p)
    return p


def add_job_header(doc, title, employer, dates):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(1)
    r1 = p.add_run(title)
    set_run_font(r1, size=11, bold=True)
    r2 = p.add_run(f"  |  {employer}")
    set_run_font(r2, size=11)
    # dates on same line right-ish via tab would be complex; put on next line
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(2)
    r3 = p2.add_run(dates)
    set_run_font(r3, size=10, italic=True, color=RGBColor(0x55, 0x55, 0x55))
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.clear()
    pf = p.paragraph_format
    pf.space_after = Pt(2)
    pf.space_before = Pt(0)
    pf.left_indent = Cm(0.5 + level * 0.4)
    run = p.add_run(text)
    set_run_font(run, size=10.5)
    return p


def build_cv():
    doc = Document()
    set_narrow_margins(doc.sections[0], top=1.4, bottom=1.4, left=1.7, right=1.7)

    # Name
    p = para(doc, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run("JAGADISH MEENIGA")
    set_run_font(r, size=18, bold=True, color=RGBColor(0x1F, 0x4E, 0x79))

    # Contact
    p = para(doc, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(
        "Milton Keynes, United Kingdom  |  +44 7775 857093  |  jagadishmeeniga@yahoo.com"
    )
    set_run_font(r, size=10)

    p = para(doc, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run("British Passport holder  |  Willing to work from London Puddle Dock")
    set_run_font(r, size=10)

    # Profile
    add_section_heading(doc, "Professional Profile")
    profile = (
        "Senior programme and transformation leader with over 20 years' experience delivering "
        "complex, multi-stakeholder change across regulated, operationally critical environments "
        "in banking, telecoms, insurance and energy. Proven at shaping programmes from diagnosis "
        "through to implementation, establishing governance and delivery discipline, and turning "
        "ambiguous operational challenges into practical interventions with measurable outcomes. "
        "Comfortable working across organisational boundaries with executive sponsors, delivery "
        "teams, consultants and suppliers. Holds an active PMP qualification, with strong commercial "
        "judgement, benefits focus and a track record of leading multidisciplinary professional teams "
        "through sustained improvement and large-scale transformation."
    )
    p = para(doc, space_after=4)
    r = p.add_run(profile)
    set_run_font(r, size=10.5)

    # Core competencies mapped to JD
    add_section_heading(doc, "Core Competencies")
    competencies = [
        "Programme and portfolio leadership for complex transformation and improvement activity",
        "Governance, controls, risk, assurance, benefits tracking and senior reporting",
        "Business case development, funding bids and significant budget / commercial management",
        "Leading and developing multidisciplinary teams across consulting, delivery and operations",
        "Diagnostic problem-solving, operating model design and structured intervention planning",
        "Stakeholder influencing with executives, partners, vendors and cross-functional leaders",
        "Business improvement, organisational change and embedding sustainable ways of working",
        "Managing priorities, interdependencies and delivery momentum in changing portfolios",
    ]
    for c in competencies:
        add_bullet(doc, c)

    # Career history
    add_section_heading(doc, "Career History")

    # UBS
    add_job_header(
        doc,
        "Senior Consultant / Programme Delivery Lead",
        "UBS (via EPAM Systems), Zurich",
        "August 2020 – August 2026",
    )
    p = para(doc, space_after=3)
    r = p.add_run(
        "Led concurrent transformation and platform programmes within Output Management Services, "
        "covering customer communications across classic and cloud estates for CH, EMEA and APAC. "
        "Work spanned Credit Suisse–UBS integration, mainframe-to-Azure migration, AI-enabled "
        "document search capability and regulated production support under formal SLAs."
    )
    set_run_font(r, size=10.5)
    for b in [
        "Shaped and delivered a portfolio of interdependent programmes, aligning work to shifting "
        "business priorities while maintaining clear accountability for time, cost and quality.",
        "Established delivery discipline across discovery, architecture forums, RAID management, "
        "release coordination and director-level steering reporting with PMO and portfolio partners.",
        "Developed high-level requirements and project bid summaries with enterprise architects, "
        "SMEs and business operations, securing financial approval for scoped outcomes.",
        "Led multidisciplinary teams spanning architects, product owners, developers, test and "
        "operations, building a strong delivery culture across onshore and offshore contributors.",
        "Managed commercial and service-provider relationships under L2/L3 collaborative workloads, "
        "keeping a firm focus on performance, value for money and sustainable handover.",
        "Took ambiguous integration and re-engineering challenges, structured them into phased "
        "interventions, and drove implementation through to live service outcomes.",
    ]:
        add_bullet(doc, b)

    # Three
    add_job_header(
        doc,
        "Digital Development Manager",
        "Three UK",
        "November 2018 – April 2020",
    )
    p = para(doc, space_after=3)
    r = p.add_run(
        "Delivery lead within Three's major digital transformation programme (Rebus) and "
        "co-existence work on online and front-end channels, balancing transformation ambition "
        "with ongoing BAU performance."
    )
    set_run_font(r, size=10.5)
    for b in [
        "Led core web-stack and IT transformation delivery in a fully digitised agile environment, "
        "bringing structure to complex channel change across business and third-party systems.",
        "Built and led multidisciplinary squads including Scrum Masters, Product Owners, UX, "
        "development, QA and release teams, with clear roles, accountability and delivery rhythm.",
        "Prepared and secured funding bids, baselined plans and budgets, and reported commercial "
        "performance weekly to director-level boards.",
        "Influenced senior stakeholders and suppliers from inception through SoR closure, epic "
        "derivation and story delivery, navigating competing priorities without losing momentum.",
        "Partnered with lead product owners on commercial journeys, discovery and pipeline demand, "
        "translating operational need into prioritised, fundable programmes of work.",
    ]:
        add_bullet(doc, b)

    # Santander
    add_job_header(
        doc,
        "IT Project Manager",
        "Santander Technology UK (SanTech)",
        "September 2015 – October 2018",
    )
    p = para(doc, space_after=3)
    r = p.add_run(
        "Managed concurrent projects under the Paper Free programme, enabling regulated, "
        "cost-effective customer communications and supporting the bank's digital design strategy "
        "for high-volume letters and statements."
    )
    set_run_font(r, size=10.5)
    for b in [
        "Defined as-is and to-be positions through architectural forums, baselining requirements "
        "across platforms and teams before committing to delivery.",
        "Owned end-to-end project lifecycle using agile methods, including planning, RAID control, "
        "release and handover planning against wider programme timelines.",
        "Managed budgets and costs, led weekly reporting and presented project bids to secure "
        "continued investment and resource.",
        "Reported to senior programme management and stakeholders across Operations, Risk, "
        "Compliance and Finance, maintaining credibility in a regulated retail banking setting.",
        "Prioritised multidisciplinary resources (Scrum Masters, BAs, architects, analysts, "
        "testers and developers) to keep interdependent workstreams aligned and delivering.",
    ]:
        add_bullet(doc, b)

    # Telefonica
    add_job_header(
        doc,
        "Project Manager",
        "Telefónica UK (O2)",
        "April 2015 – September 2015",
    )
    for b in [
        "Planned and delivered MI / SSRS dashboard and regulatory change activity against "
        "reference-data warehouse requirements for marketing and corporate portfolios.",
        "Agreed milestones and estimates with engagement managers, secured funding for "
        "workstreams and coordinated test, pre-production and UAT criteria with business change.",
        "Provided product confidence to senior accountable executives, including COO-level "
        "governance for Personal & Corporate business, through structured live-proving sessions.",
    ]:
        add_bullet(doc, b)

    # Allstate 2014
    add_job_header(
        doc,
        "Project Manager",
        "Allstate Insurance",
        "August 2014 – April 2015",
    )
    for b in [
        "Led the e-bill redesign programme end to end across .NET, DB2, Oracle and mainframe "
        "workstreams, coordinating around 15 resources including PMs, BAs, DBAs, technical leads "
        "and vendor services across India, the UK and the USA.",
        "Prepared the programme plan and business case with high-level estimates; chaired daily "
        "milestone forums and reported cost forecasts and variance to portfolio and PMO.",
        "Maintained RAID transparency for key stakeholders and adjusted resource plans against "
        "progress, outstanding change and testing demand.",
    ]:
        add_bullet(doc, b)

    # Citi
    add_job_header(
        doc,
        "Project Manager",
        "Citibank UK",
        "September 2012 – August 2014",
    )
    for b in [
        "Delivered BAU and major business transformation initiatives within post-trade settlements "
        "and operations (CCAS), including Integrated Custody (global windows across NA, EMEA and "
        "APAC, c. USD 0.5m) and Target 2 Securities.",
        "Owned full project lifecycle from PID and business case through kick-off workshops, "
        "steering committees and defect management to implementation.",
        "Worked confidently with senior operations and technology stakeholders in a "
        "safety-conscious, highly controlled financial market infrastructure environment.",
    ]:
        add_bullet(doc, b)

    # Earlier roles condensed
    add_job_header(
        doc,
        "Project Manager",
        "Scottish and Southern Energy (SSE)",
        "March 2012 – June 2012",
    )
    add_bullet(
        doc,
        "Delivered Green Deal-related billing change across .NET and mainframe estates for a "
        "major UK government energy efficiency initiative, owning plans, estimates, build "
        "allocation and baseline tracking.",
    )

    add_job_header(
        doc,
        "Project Manager",
        "Allstate Insurance",
        "March 2010 – February 2012",
    )
    add_bullet(
        doc,
        "Managed PCI compliance and card-data encryption change from inception to implementation "
        "within agreed time and cost, coordinating multiple workstreams across applications and "
        "live databases in a regulated insurance environment.",
    )

    add_job_header(
        doc,
        "Earlier delivery and engineering roles",
        "Pitney Bowes (Wipro), Standard Bank of South Africa, State Street, HSBC UK",
        "January 1997 – July 2009",
    )
    for b in [
        "Progressed from software engineering and technical design into project leadership, "
        "building a grounding in requirements analysis, solution design and end-to-end delivery.",
        "Led field-service integration and billing automation delivery for Pitney Bowes; provided "
        "technical leadership on regulatory credit-portfolio change at SBSA; supported investment "
        "reporting and retail payments change at State Street and HSBC UK.",
    ]:
        add_bullet(doc, b)

    # Education
    add_section_heading(doc, "Education & Professional Qualifications")
    quals = [
        "Project Management Professional (PMP), PMI — active since December 2011 (No. 1471448); current through December 2026",
        "ITIL Foundation Certificate in IT Service Management — August 2012 (Certificate 4550594)",
        "Microsoft Certified: Azure AI Engineer Associate (AI-102) — February 2025 (valid to February 2027)",
        "Claude Certified Architect – Foundations, Anthropic — July 2026",
        "Bachelor of Technology in Civil Engineering — JNTU College of Engineering, Anantapur (1996)",
    ]
    for q in quals:
        add_bullet(doc, q)

    # Additional
    add_section_heading(doc, "Additional Information")
    for b in [
        "Right to work: British Passport holder",
        "Languages: English (fluent); German (proficient intermediate)",
        "Tools and methods: MS Project, Planview, Jira, Confluence, agile and waterfall delivery, "
        "RAID / benefits / status reporting, business case and bid preparation",
        "Experience drawn from complex, operational, regulated and multi-party environments; "
        "ready to bring programme, consulting and improvement practice to Southern Region's "
        "Systems Thinking portfolio and the Great British Railways integration agenda",
    ]:
        add_bullet(doc, b)

    path = os.path.join(OUT_DIR, "Jagadish_Meeniga_CV_Network_Rail_Senior_Programme_Manager.docx")
    doc.save(path)
    return path


def build_cover_letter():
    doc = Document()
    set_narrow_margins(doc.sections[0], top=2.0, bottom=2.0, left=2.2, right=2.2)

    # Sender details
    p = para(doc, space_after=0)
    r = p.add_run("Jagadish Meeniga")
    set_run_font(r, size=11, bold=True)

    for line in [
        "Milton Keynes, United Kingdom",
        "+44 7775 857093",
        "jagadishmeeniga@yahoo.com",
    ]:
        p = para(doc, space_after=0)
        r = p.add_run(line)
        set_run_font(r, size=10.5)

    p = para(doc, space_before=10, space_after=0)
    r = p.add_run("12 November 2026")
    set_run_font(r, size=10.5)

    p = para(doc, space_before=10, space_after=0)
    r = p.add_run("Hiring Manager")
    set_run_font(r, size=10.5)
    for line in [
        "Senior Programme Manager – Systems Thinking Portfolio",
        "Network Rail – Southern Region",
        "London Puddle Dock",
    ]:
        p = para(doc, space_after=0)
        r = p.add_run(line)
        set_run_font(r, size=10.5)

    p = para(doc, space_before=12, space_after=8)
    r = p.add_run(
        "Re: Application for Senior Programme Manager, Systems Thinking Portfolio (Band 2C)"
    )
    set_run_font(r, size=11, bold=True)

    p = para(doc, space_after=8)
    r = p.add_run("Dear Hiring Manager,")
    set_run_font(r, size=11)

    paras = [
        (
            "I am writing to apply for the Senior Programme Manager role leading the Systems Thinking "
            "portfolio within Network Rail's Southern Region. Your brief asks for someone who can "
            "combine programme management, consulting and improvement practice, and then see that "
            "work through to lasting results. That is the shape of work I have spent most of my "
            "career doing."
        ),
        (
            "I bring more than twenty years leading complex, multi-stakeholder programmes and "
            "transformation portfolios in regulated, operationally critical settings. Most recently, "
            "at UBS, I led concurrent programmes covering platform integration, mainframe-to-cloud "
            "migration and service improvement under formal governance and SLAs. The pattern was "
            "familiar to the one you describe: sit with senior sponsors, get to the real problem, "
            "shape a practical programme of work, put proper controls and benefits focus around it, "
            "and stay close until the outcome is embedded rather than merely announced."
        ),
        (
            "Earlier, as Digital Development Manager at Three UK, I led delivery within a major digital "
            "transformation programme while protecting BAU performance. I built multidisciplinary teams, "
            "secured funding through director-level commercial forums, and worked across business, "
            "supplier and partner boundaries to keep interdependent work moving. At Santander Technology "
            "I ran concurrent projects under a regulated Paper Free programme, with clear accountability "
            "for RAID, budgets, assurance reporting and stakeholder confidence across Operations, Risk, "
            "Compliance and Finance. Across Allstate, Citibank, SSE and Telefónica I have repeatedly "
            "taken work beyond analysis into implementation, including PCI compliance, post-trade "
            "operations transformation and government-driven energy billing change."
        ),
        (
            "I hold an active PMP and ITIL Foundation. Governance, risk, financial management, "
            "business cases and delivery assurance are part of how I run programmes day to day, "
            "not bolt-ons. I am used to holding significant budgets and managing professional "
            "service relationships with a clear eye on value for money. I also take seriously the "
            "people side: building teams, sharing what works, and leaving capability behind once "
            "a piece of work has landed. I have not worked on the railway itself. I have, however, "
            "worked for years in complex, regulated, multi-party environments where performance, "
            "customer impact and controlled delivery are non-negotiable. I would like to put that "
            "experience to work on Southern Region's Systems Thinking portfolio and the move "
            "towards Great British Railways."
        ),
        (
            "I hold a British Passport, live in Milton Keynes and can work from London Puddle Dock. "
            "I would welcome a conversation about how I can support Southern Region's transformation "
            "and improvement priorities. Thank you for your time and consideration."
        ),
    ]
    for text in paras:
        p = para(doc, space_after=8)
        r = p.add_run(text)
        set_run_font(r, size=11)

    p = para(doc, space_before=4, space_after=0)
    r = p.add_run("Yours faithfully,")
    set_run_font(r, size=11)

    p = para(doc, space_before=28, space_after=0)
    r = p.add_run("Jagadish Meeniga")
    set_run_font(r, size=11, bold=True)

    p = para(doc, space_after=0)
    r = p.add_run("PMP | ITIL Foundation | Azure AI Engineer Associate")
    set_run_font(r, size=10, italic=True, color=RGBColor(0x55, 0x55, 0x55))

    path = os.path.join(
        OUT_DIR, "Jagadish_Meeniga_Cover_Letter_Network_Rail_Senior_Programme_Manager.docx"
    )
    doc.save(path)
    return path


def build_mapping_note():
    """Optional plain-text mapping for the applicant's reference (not for submission)."""
    content = """Network Rail Senior Programme Manager – CV & Cover Letter Mapping (95–100%)

JD requirement -> Evidence used in CV / cover letter
--------------------------------------------------------------------------------
Lead complex Systems Thinking / transformation / improvement portfolio
  -> UBS concurrent transformation portfolio; Three Rebus digital transformation;
     Santander Paper Free programme; Allstate e-bill redesign programme

Lead & develop multidisciplinary professional teams
  -> Three (SM, PO, UX, Dev, QA, Release); UBS (architects, PO, Dev, Test, Ops);
     Allstate (~15 resources across PM/BA/DBA/vendor); Santander cross-functional teams

Work with executive / senior leaders; translate challenges into programmes
  -> Director steering at UBS; director commercial boards at Three; COO-level
     governance at Telefónica; Santander Ops/Risk/Compliance/Finance reporting

Consulting, diagnostic, problem-solving; structure ambiguous problems
  -> Discovery phases, as-is/to-be, architecture forums, phased interventions
     across UBS, Three and Santander

Programme standards: governance, controls, risk, benefits, assurance, reporting
  -> RAID, PMO alignment, steering packs, SLA environments, status reporting

Manage priorities, resources, interdependencies across changing portfolio
  -> Concurrent multi-programme delivery at UBS, Three and Santander

Business cases, funding and resources
  -> Bid summaries / funding approvals (UBS, Three, Santander, Telefónica, Allstate)

Significant budgets, suppliers, commercial relationships, value for money
  -> Director-level commercial reporting (Three); vendor/third-party management;
     L2/L3 service delivery (UBS); Citibank IC programme c. USD 0.5m

Influencing across organisational boundaries
  -> Business, suppliers, partners, offshore/onshore, Credit Suisse–UBS integration

Improvement / organisational change into sustainable outcomes
  -> Paper Free, digital channel transformation, PCI, Green Deal, platform migrations

Formal programme management qualification
  -> Active PMP (1471448); ITIL Foundation

Complex, operational, infrastructure, regulated or safety-critical environments
  -> Banking, telecoms, insurance, energy; civil engineering degree as foundation

Railway / Systems Thinking (advantage, not essential)
  -> Honest positioning: transferable from complex regulated multi-party delivery;
     expressed interest in Southern Region / GBR context without overclaiming

Location / eligibility
  -> Milton Keynes; British Passport; London Puddle Dock willingness

Documents for submission:
  1. Jagadish_Meeniga_CV_Network_Rail_Senior_Programme_Manager.docx
  2. Jagadish_Meeniga_Cover_Letter_Network_Rail_Senior_Programme_Manager.docx
"""
    path = os.path.join(OUT_DIR, "JD_Mapping_Reference.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


if __name__ == "__main__":
    cv = build_cv()
    cl = build_cover_letter()
    mp = build_mapping_note()
    print("Created:")
    print(cv)
    print(cl)
    print(mp)
