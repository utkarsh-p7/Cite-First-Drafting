"""System prompts, identical to the dissertation artefact.

The baseline sees the SAME template and context; the ONLY difference is the
evidence-linking instruction block and the row-14 missing-information section.
"""

from cite_first_drafting.drafting.template import EVIDENCE_INSTRUCTION, TEMPLATE_INSTRUCTION

MAX_TOKENS = 3000

_PREAMBLE = (
    "You are a drafting assistant for a UK independent financial adviser. "
    "All data is FICTITIOUS synthetic research data. "
)

SYSTEM_TOOL = (
    _PREAMBLE
    + TEMPLATE_INSTRUCTION
    + EVIDENCE_INSTRUCTION
    + "- Write the report only. No preamble, no commentary outside the report.\n"
)

SYSTEM_BASELINE = (
    _PREAMBLE
    + TEMPLATE_INSTRUCTION
    + "- Write the report only. No preamble, no commentary, no citations of any kind.\n"
)

SYSTEM_BY_PIPELINE = {"tool": SYSTEM_TOOL, "baseline": SYSTEM_BASELINE}
