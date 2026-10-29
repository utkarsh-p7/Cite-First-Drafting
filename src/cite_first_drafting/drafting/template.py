"""Shared report template — identical for baseline and evidence-linked drafters.
Section order derived from /profiles/initial_report.md rows (fair RQ1 comparison:
same model, same context, same template; only the evidence-linking instruction differs).
"""

# (section_id, heading, profile_rows_covered)
SECTIONS = [
    ("advice_given", "The advice we are giving you", [2]),
    ("your_circumstances", "Your objectives, circumstances, knowledge and experience", [6]),
    ("why_suitable", "Why this recommendation is suitable for you", [3, 4]),
    ("risks_disadvantages", "Risks and possible disadvantages", [11]),
    ("costs_charges", "Costs and charges", [10]),
    ("ongoing_review", "Ongoing review of your arrangements", [5]),
    ("delivery_note", "About this report", [1]),
]

TEMPLATE_INSTRUCTION = (
    "Draft an INITIAL SUITABILITY REPORT for a retail client, addressed to the client, "
    "in plain English, using EXACTLY these sections in this order as '## ' headings:\n"
    + "\n".join(f"{i}. {h}" for i, (_, h, _r) in enumerate(SECTIONS, 1))
    + "\n\nRules:\n"
    "- Use ONLY information present in the SOURCE EVIDENCE provided. Never invent client "
    "facts, figures, product features, or tax limits.\n"
    "- The adviser's recommendation is given in the fact-find (recommendation_context). "
    "You are drafting the report OF that recommendation. You must NOT form, alter, or "
    "score the suitability judgment yourself.\n"
    "- 'About this report' must state the report is provided before the transaction is "
    "concluded, in a durable medium.\n"
    "- 'Ongoing review' must state whether periodic review of the arrangements is likely "
    "to be needed.\n"
)

# ---- Task 3 additions (evidence-linked drafter ONLY; baseline never sees these) ----

# Row 14: appended as section 8 on top of the SAME section list.
TOOL_EXTRA_SECTION = ("missing_information", "Missing information we still need from you", [14])

EVIDENCE_INSTRUCTION = (
    "\nEVIDENCE-LINKING RULES (mandatory):\n"
    "- Every material statement (any sentence stating a client fact, figure, product "
    "feature, risk, cost, or regulatory point) MUST end with >=1 span citation in square "
    "brackets, exactly as shown in the SOURCE EVIDENCE, e.g. [FF:C001:objectives.horizon_years] "
    "or [KB:COBS_9A_3:02_what_the_report_must_contain_do_paraphra]. Multiple: [FF:...][TR:...].\n"
    "- Use plain ASCII square brackets [ ] for citations. Never fullwidth brackets.\n"
    "- Cite ONLY span IDs that appear verbatim in the SOURCE EVIDENCE. Never invent IDs.\n"
    "- If a material statement is required by the template but the evidence is absent or "
    "insufficient, write the statement position as: [INSUFFICIENT EVIDENCE: <what is missing>].\n"
    f"- Add a final section '## {TOOL_EXTRA_SECTION[1]}' listing required-but-absent "
    "client facts as bullet points (the row-14 checklist). If none, state 'None identified.'\n"
    "- CONFLICT FLAGS (mandatory, machine-checked): if any two evidence spans conflict — "
    "including (a) the client's attitude to risk vs their capacity for loss, and (b) any "
    "fact-find value vs any transcript statement — you MUST output a line that begins "
    "exactly with 'ADVISER FLAG:' — this exact prefix at the start of the line, not a "
    "heading, not bold — describing the conflict and citing BOTH conflicting span IDs on "
    "that same line. One such line per conflict, placed at the end of the most relevant "
    "section. Mentioning a conflict in prose or a risk bullet does NOT replace the "
    "'ADVISER FLAG:' line. Flag only — do NOT resolve the conflict or pick a side.\n"
    "- 'Risks and possible disadvantages' must be evidenced like every other section.\n"
)

