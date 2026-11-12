#!/usr/bin/env python3
"""Generate England-format CV and cover letter for Network Rail SPM application.

Aligned to the official Network Rail Job Description:
Senior Programme Manager [Systems Thinking] (issued / last saved 2025–2026),
reporting to People & Transformation Director, Regions/Functions.
"""

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
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

    p = para(doc, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run("JAGADISH MEENIGA")
    set_run_font(r, size=18, bold=True, color=RGBColor(0x1F, 0x4E, 0x79))

    p = para(doc, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(
        "Milton Keynes, United Kingdom  |  +44 7775 857093  |  jagadishmeeniga@yahoo.com"
    )
    set_run_font(r, size=10)

    p = para(doc, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(
        "British Passport holder  |  Willing to work from London Puddle Dock  |  "
        "Happy to obtain required Track Safety competence"
    )
    set_run_font(r, size=10)

    add_section_heading(doc, "Professional Profile")
    profile = (
        "Senior programme manager with over 20 years' experience designing and delivering "
        "large-scale, multi-stakeholder transformation and improvement programmes in regulated, "
        "operationally critical environments across banking, telecoms, insurance and energy. "
        "Used to taking an end-to-end systems view of complex change: mapping interdependencies, "
        "aligning partners and suppliers, and turning cross-cutting problems into programmes that "
        "land to time, cost and quality under formal governance. Strong commercial and investment "
        "judgement, including business cases, funding authorisation, procurement of service "
        "providers and significant budget control. Active PMP, degree-educated, with a proven "
        "record of leading multidisciplinary teams, strengthening capability, driving behavioural "
        "change and reporting with assurance to executive and director-level sponsors."
    )
    p = para(doc, space_after=4)
    r = p.add_run(profile)
    set_run_font(r, size=10.5)

    add_section_heading(doc, "Core Competencies")
    competencies = [
        "Designing and delivering multi-programme portfolios with governance, risk management and benefits realisation",
        "End-to-end systems perspective on complex change: interdependencies, integration and cross-industry partnering",
        "Programme standards, processes, controls, audit sponsorship and delivery assurance to time, budget and success criteria",
        "Business case development, investment-framework discipline, funding authorisation and value for money",
        "Procurement and commercial management of consultants, vendors and professional service providers",
        "Leading and developing multidisciplinary programme teams; building flexible, skilled capability",
        "Influencing executive directors and senior third-party stakeholders; negotiation and relationship building",
        "Data-led decision support from executive steering through to local delivery leadership",
        "Organisational development, continuous improvement and sustained behavioural change in large organisations",
        "Safe, controlled delivery in regulated and operationally critical settings; security-aware working practice",
    ]
    for c in competencies:
        add_bullet(doc, c)

    add_section_heading(doc, "Career History")

    add_job_header(
        doc,
        "Senior Consultant / Programme Delivery Lead",
        "UBS (via EPAM Systems), Zurich",
        "August 2020 – August 2026",
    )
    p = para(doc, space_after=3)
    r = p.add_run(
        "Led concurrent transformation and platform programmes within Output Management Services "
        "for customer communications across classic and cloud estates (CH, EMEA, APAC). Portfolio "
        "covered Credit Suisse–UBS integration, mainframe-to-Azure migration, AI-enabled document "
        "search and regulated production support under formal SLAs — treating interdependent "
        "platforms, suppliers and operations as one delivery system rather than isolated projects."
    )
    set_run_font(r, size=10.5)
    for b in [
        "Developed and tailored the programme of work as company priorities and industry "
        "integration pressures shifted, keeping strategic and tactical alignment across related "
        "workstreams and partner organisations.",
        "Established and monitored programme standards, processes and governance; maintained RAID, "
        "release coordination and director-level steering packs with PMO and portfolio partners to "
        "provide assurance of delivery to time, budget and agreed success criteria.",
        "Led discovery and architecture forums, analysed complex operational and technical data, "
        "and used that evidence to shape interventions and support decisions from executive "
        "sponsors through to local delivery leads.",
        "Prepared high-level requirements and bid summaries with enterprise architects, SMEs and "
        "business operations, securing financial authorisation and managing spend within agreed "
        "limits with a clear value-for-money focus.",
        "Managed service-provider and vendor relationships under L2/L3 collaborative workloads; "
        "set resource requirements and performance controls across onshore and offshore contributors.",
        "Led and developed a multidisciplinary team of specialists and delivery professionals, "
        "building capability and keeping the workforce flexible enough to absorb changing demand.",
        "Sponsored and supported reviews of programme documentation, processes and handover "
        "quality; communicated key issues early to sponsors and control functions.",
        "Delivered within tightly controlled, audit-ready environments where security, data "
        "handling and production safety were non-negotiable.",
    ]:
        add_bullet(doc, b)

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
        "with ongoing operational performance across business, supplier and partner boundaries."
    )
    set_run_font(r, size=10.5)
    for b in [
        "Led core web-stack and IT transformation delivery, identifying priority opportunities "
        "and keeping interdependent channel programmes aligned rather than competing for resource.",
        "Built and led multidisciplinary squads — Scrum Masters, Product Owners, UX, development, "
        "QA and release — creating clear accountability and a delivery culture that could flex "
        "as demand moved.",
        "Prepared and secured funding bids, baselined plans and budgets, and reported commercial "
        "performance weekly to director-level boards; strong commercial focus throughout.",
        "Influenced senior business stakeholders, third-party systems owners, suppliers and "
        "vendors from inception through SoR closure and story delivery.",
        "Promoted consistent ways of working across squads, sharing what worked so improvements "
        "stuck beyond individual releases.",
        "Partnered with lead product owners on discovery and pipeline demand, translating "
        "ambiguous commercial need into prioritised, fundable programmes of work.",
    ]:
        add_bullet(doc, b)

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
        "across platforms before committing investment — a systems view of how change landed "
        "across operations, technology and compliance.",
        "Owned end-to-end delivery including planning, RAID control, release and handover against "
        "wider programme timelines, in line with internal governance frameworks.",
        "Managed budgets and costs, led weekly reporting and presented project bids to secure "
        "authorisation and ongoing funding.",
        "Reported to senior programme management and stakeholders across Operations, Risk, "
        "Compliance and Finance, maintaining credibility in a regulated retail banking setting.",
        "Prioritised multidisciplinary resources and monitored interdependencies so concurrent "
        "workstreams stayed aligned and deliverable.",
    ]:
        add_bullet(doc, b)

    add_job_header(
        doc,
        "Project Manager",
        "Telefónica UK (O2)",
        "April 2015 – September 2015",
    )
    for b in [
        "Planned and delivered MI / SSRS dashboard and regulatory change against reference-data "
        "warehouse requirements; used complex data outputs to support operational decision-making.",
        "Agreed milestones and estimates with engagement managers, secured funding, and "
        "coordinated test, pre-production and UAT criteria with business change.",
        "Provided product confidence through structured live-proving sessions up to COO-level "
        "governance for Personal & Corporate business.",
    ]:
        add_bullet(doc, b)

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
        "Maintained RAID transparency and adjusted resource plans against progress, outstanding "
        "change and testing demand to protect benefits realisation.",
    ]:
        add_bullet(doc, b)

    add_job_header(
        doc,
        "Project Manager",
        "Citibank UK",
        "September 2012 – August 2014",
    )
    for b in [
        "Delivered BAU and major transformation initiatives within post-trade settlements and "
        "operations (CCAS), including Integrated Custody (global windows across NA, EMEA and "
        "APAC, c. USD 0.5m) and Target 2 Securities — complex, multi-party operational change "
        "in a tightly controlled market-infrastructure environment.",
        "Owned full lifecycle from PID and business case through kick-off workshops, steering "
        "committees and defect management to implementation, under formal investment and "
        "governance expectations.",
        "Worked with senior operations and technology stakeholders where control, auditability "
        "and operational continuity were essential.",
    ]:
        add_bullet(doc, b)

    add_job_header(
        doc,
        "Project Manager",
        "Scottish and Southern Energy (SSE)",
        "March 2012 – June 2012",
    )
    add_bullet(
        doc,
        "Delivered Green Deal-related billing change across .NET and mainframe estates for a "
        "major UK government energy-efficiency initiative, owning plans, estimates, build "
        "allocation and baseline tracking in a regulated utility setting.",
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
        "live databases — behavioural and process change as much as technical delivery.",
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
        "Led field-service integration and billing automation for Pitney Bowes; provided technical "
        "leadership on regulatory credit-portfolio change at SBSA; supported investment reporting "
        "and retail payments change at State Street and HSBC UK.",
    ]:
        add_bullet(doc, b)

    add_section_heading(doc, "Education & Professional Qualifications")
    quals = [
        "Bachelor of Technology in Civil Engineering — JNTU College of Engineering, Anantapur (1996)",
        "Project Management Professional (PMP), PMI — active since December 2011 (No. 1471448); current through December 2026",
        "ITIL Foundation Certificate in IT Service Management — August 2012 (Certificate 4550594)",
        "Microsoft Certified: Azure AI Engineer Associate (AI-102) — February 2025 (valid to February 2027)",
        "Claude Certified Architect – Foundations, Anthropic — July 2026",
    ]
    for q in quals:
        add_bullet(doc, q)

    add_section_heading(doc, "Additional Information")
    for b in [
        "Right to work: British Passport holder; based in Milton Keynes; able to work from London Puddle Dock",
        "Safety and clearance: experienced in regulated, audit-ready and security-sensitive delivery; "
        "willing to complete Network Rail Track Safety competence and any required security clearance "
        "for a Key Safety Post",
        "Languages: English (fluent); German (proficient intermediate)",
        "Methods and tools: MS Project, Planview, Jira, Confluence, agile and waterfall delivery, "
        "RAID / benefits / status reporting, business case and bid preparation, vendor and "
        "procurement coordination",
        "Industry context: no direct UK railway employment to date; substantial transferable "
        "experience leading multidisciplinary teams through complex outcomes in operational, "
        "regulated and multi-party environments, with a Civil Engineering foundation and a strong "
        "interest in integrated railways, Systems Thinking practice and Great British Railways "
        "integration",
    ]:
        add_bullet(doc, b)

    path = os.path.join(
        OUT_DIR, "Jagadish_Meeniga_CV_Network_Rail_Senior_Programme_Manager.docx"
    )
    doc.save(path)
    return path


def build_cover_letter():
    doc = Document()
    set_narrow_margins(doc.sections[0], top=2.0, bottom=2.0, left=2.2, right=2.2)

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
    r = p.add_run("People & Transformation Director / Hiring Manager")
    set_run_font(r, size=10.5)
    for line in [
        "Senior Programme Manager [Systems Thinking]",
        "Network Rail",
        "London Puddle Dock",
    ]:
        p = para(doc, space_after=0)
        r = p.add_run(line)
        set_run_font(r, size=10.5)

    p = para(doc, space_before=12, space_after=8)
    r = p.add_run(
        "Re: Senior Programme Manager [Systems Thinking] — application"
    )
    set_run_font(r, size=11, bold=True)

    p = para(doc, space_after=8)
    r = p.add_run("Dear Hiring Manager,")
    set_run_font(r, size=11)

    paras = [
        (
            "I am writing to apply for the Senior Programme Manager [Systems Thinking] post. "
            "Having read the formal job description, the purpose of the role is clear: develop "
            "and deliver programmes of work for integrated railways — including track and train "
            "trials — safely, to cost, time and quality, under company standards and corporate "
            "governance. That combination of programme leadership, systems-level thinking and "
            "disciplined delivery is the work I want to do next."
        ),
        (
            "I have spent more than twenty years designing and delivering large-scale, "
            "multi-stakeholder programmes in regulated, operationally critical environments. "
            "At UBS I led concurrent programmes covering platform integration, mainframe-to-cloud "
            "migration and service improvement. The practical habit was the same one your "
            "accountabilities describe: treat interdependent platforms, suppliers and operations "
            "as one system; set standards and governance; monitor delivery to time and budget; "
            "and keep assurance visible to directors and control functions. I prepared bid "
            "summaries for financial authorisation, managed significant spend within agreed "
            "limits, and held service-provider relationships to performance and value for money."
        ),
        (
            "At Three UK I led delivery inside a major digital transformation programme while "
            "protecting day-to-day operational performance. I built multidisciplinary teams, "
            "secured funding through director-level commercial forums, and worked across "
            "business, supplier and partner boundaries. At Santander Technology I ran concurrent "
            "projects under a regulated Paper Free programme, with clear ownership of RAID, "
            "budgets, governance reporting and stakeholder confidence across Operations, Risk, "
            "Compliance and Finance. Across Citibank, Allstate, SSE and Telefónica I have taken "
            "work from diagnosis and business case through implementation, including "
            "post-trade operations change, PCI compliance and government-driven energy billing "
            "change — environments where behavioural change, auditability and controlled "
            "delivery mattered as much as the technical solution."
        ),
        (
            "I hold an active PMP and a Civil Engineering degree, and I am used to investment-"
            "framework discipline, procurement of professional services, and sponsoring reviews "
            "of programme documentation and process quality. I lead by building capability in "
            "the team, sharing what works between workstreams, and leaving better ways of "
            "working behind once a programme has landed. I do not yet have UK railway employment "
            "or a formal Systems Thinking accreditation. I do bring a strong end-to-end systems "
            "practice from complex multi-party delivery, and I am ready to deepen that in your "
            "methodology, obtain the required Track Safety competence, and work within the "
            "expectations of a Key Safety Post."
        ),
        (
            "I hold a British Passport, live in Milton Keynes and can work from London Puddle "
            "Dock. I would welcome the chance to discuss how I can support the Systems Thinking "
            "programme, industry integration and Great British Railways alignment. Thank you "
            "for your time and consideration."
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
    r = p.add_run("PMP | ITIL Foundation | BTech Civil Engineering")
    set_run_font(r, size=10, italic=True, color=RGBColor(0x55, 0x55, 0x55))

    path = os.path.join(
        OUT_DIR,
        "Jagadish_Meeniga_Cover_Letter_Network_Rail_Senior_Programme_Manager.docx",
    )
    doc.save(path)
    return path


def build_mapping_note():
    content = """Network Rail – Senior Programme Manager [Systems Thinking]
Official JD vs earlier advert: delta + CV/cover-letter mapping
================================================================================

SOURCE DOCUMENTS
- Official NR Job Description (.doc): Senior Programme Manager [Systems Thinking]
  Reports to: People & Transformation Director, Regions/Functions
  (attached as Senior Programme Manager [Systems Thinking] July 25)
- Earlier public advert: Southern Region / Band 2C / London Puddle Dock narrative

MATERIAL DIFFERENCES (official JD is stricter / more specific)
--------------------------------------------------------------------------------
1. SYSTEMS THINKING
   Advert: advantage, not essential
   Official: core job title, job purpose and required skill ("in-depth understanding
   of systems thinking methodologies, tools and frameworks")
   Response: framed as end-to-end systems practice on complex multi-party change;
   honest that no formal ST accreditation / railway ST role yet; ready to adopt NR methods

2. SAFETY
   Advert: limited mention
   Official: KEY SAFETY POST; manages employees; Track Safety competence required;
   security clearance may apply; safe & environmentally responsible delivery
   Response: CV header + Additional Information + cover letter readiness for Track Safety
   and Key Safety Post; emphasised regulated/audit-ready/security-sensitive delivery

3. RAILWAY OPERATIONS
   Advert: railway experience advantageous, not essential; other complex environments welcome
   Official: "Significant experience of leading multi discipline teams delivering complex
   outcomes in an operational railway environment" listed under skills
   Response: honest no UK railway employment; mapped transferable operational/regulated/
   multi-party leadership; Civil Engineering degree noted; GBR/integration interest stated

4. JOB PURPOSE
   Official: programmes for integrated railways (track and train trials); cost/time/quality;
   company standards; corporate governance
   Response: cover letter opens on this purpose explicitly

5. ACCOUNTABILITIES ADDED / STRENGTHENED vs advert
   - Develop/tailor the systems thinking programme to evolving strategy & industry integration
   - Lead system thinking specialists AND programme managers
   - Programme AND systems-thinking standards; assurance of delivery
   - Service-provider resource controls and performance
   - Best-practice sharing between programmes; interdependencies with integration & GBR
   - Business cases + investment frameworks + significant budgets + value for money
   - Procurement of service providers for transformation programmes
   - Build team capability / flexible skilled workforce
   - Sponsor audits of documentation, activities, processes and systems
   - Comply with PM governance including procurement & investment frameworks
   Response: UBS/Three/Santander/Citi bullets rewritten for these themes

6. SKILLS ADDED vs advert
   - Complex data analysis for executive-to-local decision making
   - How ST integrates with OD / transformation / continuous improvement
   - Strong commercial focus; investment process knowledge
   - Behavioural change in a large organisation
   - Chartered membership and/or degree level education
   - Industry collaboration models, integration strategies, regulatory environments
   Response: degree elevated; data/commercial/behavioural/investment language added

JD REQUIREMENT -> EVIDENCE
--------------------------------------------------------------------------------
Develop ST programme / tailor to evolving strategy & industry integration
  -> UBS portfolio tailored as priorities shifted; Three Rebus + BAU coexistence;
     cover letter purpose paragraph

Lead ST specialists & programme managers / build capability
  -> Multidisciplinary team leadership (Three, UBS, Allstate); capability & flexibility language

Standards, processes, governance; deliver to time/budget/success criteria; assurance
  -> RAID, PMO, steering, SLAs across UBS/Santander/Citi

Service providers: resource requirements, controls, performance, procurement
  -> Vendor/L2/L3 management (UBS); supplier/vendor influence (Three); commercial boards

Business cases, investment frameworks, funding authorisation, significant budgets, VfM
  -> Bid summaries, funding approvals, cost variance reporting (UBS, Three, Santander, Allstate, Citi)

Interdependencies; best practice sharing; GBR / industry integration alignment
  -> Concurrent programme alignment; ways-of-working promotion; GBR interest stated honestly

Stakeholder / consultant / supplier influencing; executive directors
  -> Director steering; COO governance (Telefónica); Ops/Risk/Compliance/Finance (Santander)

Sponsor audits; communicate key programme issues
  -> Audit-ready regulated delivery; documentation/handover reviews (UBS)

Complex data -> decision making
  -> Telefónica MI/SSRS; UBS discovery/architecture evidence-based interventions

Behavioural / OD / continuous improvement
  -> Paper Free, PCI, digital channel change; team capability building

Formal PM qualification + degree
  -> Active PMP; BTech Civil Engineering

Safe / Key Safety Post / Track Safety
  -> Willingness stated; regulated/security-sensitive experience cited

UK railway knowledge/experience
  -> Honest gap; transferable operational/regulated multi-party delivery + civil engineering

SUBMIT
  1. Jagadish_Meeniga_CV_Network_Rail_Senior_Programme_Manager.docx
  2. Jagadish_Meeniga_Cover_Letter_Network_Rail_Senior_Programme_Manager.docx
Do NOT submit JD_Mapping_Reference.txt
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
