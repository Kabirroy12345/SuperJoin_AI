"""
Pydantic models for the Fact Knowledge Layer.

The Fact schema uses a generic subject/predicate/object_value shape that handles
financial figures, director status changes, addresses, and any other fact type
equally well. An open `attributes` dict allows the LLM to populate additional
structured fields per fact type without schema changes.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RelationshipType(str, Enum):
    CORROBORATION = "corroboration"
    CONTRADICTION = "contradiction"
    CONTEXTUAL_RECONCILIATION = "contextual_reconciliation"
    UNRELATED = "unrelated"


class ChunkType(str, Enum):
    TEXT = "text"
    TABLE = "table"


# ---------------------------------------------------------------------------
# Document & Chunk
# ---------------------------------------------------------------------------

class Document(BaseModel):
    """Metadata for an uploaded PDF."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    filename: str
    upload_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    page_count: int = 0


class Chunk(BaseModel):
    """A text or table segment extracted from a single page of a document."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    doc_id: str
    doc_filename: str = ""
    page_number: int
    text: str
    chunk_type: ChunkType = ChunkType.TEXT
    token_estimate: int = 0  # rough token count for LLM budgeting


# ---------------------------------------------------------------------------
# Fact — the core data model
# ---------------------------------------------------------------------------

class Fact(BaseModel):
    """
    Generic fact extracted from a document.

    Uses subject/predicate/object_value instead of rigid value/unit fields,
    so it handles financial metrics, personnel changes, geographic data,
    and any other fact type equally well.

    The `attributes` dict is an open schema the LLM can populate with
    whatever structured fields the fact type needs (value, unit, period,
    role, status, address components, etc.).
    """

    id: str = Field(default_factory=lambda: uuid.uuid4().hex)

    # --- Core fact triple ---
    claim: str              # Human-readable: "Delhivery revenue in FY24 was ₹8,142 crore"
    subject: str            # Main entity: "Delhivery"
    predicate: str          # Attribute/relation: "annual revenue"
    object_value: str       # Stated value/state: "₹8,142 crore"

    # --- Source evidence (always present) ---
    doc_id: str
    doc_filename: str = ""
    page_number: int = 0
    source_quote: str = ""  # Exact text from document
    chunk_id: str = ""

    # --- Entity tags for normalization & pairing ---
    entities: list[str] = Field(default_factory=list)       # ["Delhivery", "Sahil Barua"]
    entity_types: list[str] = Field(default_factory=list)   # ["company", "person"]

    # --- Flexible attributes (evolving schema) ---
    attributes: dict[str, Any] = Field(default_factory=dict)
    # Examples:
    #   {"value": 8142, "unit": "₹ crore", "period": "FY2024"}
    #   {"role": "MD & CEO", "status": "active", "as_of": "2022"}
    #   {"address_line": "...", "city": "Gurugram", "state": "Haryana"}

    category: str = "general"   # financial, personnel, operational, geographic, ...
    confidence: float = 0.0     # 0–1, LLM self-assessed

    # --- Embedding (populated later, not persisted in JSON) ---
    embedding: list[float] | None = Field(default=None, exclude=True)


# ---------------------------------------------------------------------------
# Fact Relationship
# ---------------------------------------------------------------------------

class FactRelationship(BaseModel):
    """
    A discovered relationship between two facts from different documents.
    """
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    fact_a_id: str
    fact_b_id: str
    relationship_type: RelationshipType
    explanation: str = ""       # LLM-generated reasoning citing source evidence
    confidence: float = 0.0     # 0–1


# ---------------------------------------------------------------------------
# Pipeline results
# ---------------------------------------------------------------------------

class ExtractionResult(BaseModel):
    """Result of processing a single document."""
    document: Document
    facts: list[Fact] = Field(default_factory=list)
    chunk_count: int = 0


class ReconciliationResult(BaseModel):
    """Result of cross-document reconciliation."""
    relationships: list[FactRelationship] = Field(default_factory=list)
    pairs_evaluated: int = 0


class CaseExample(BaseModel):
    """One example of a required case for the submission."""
    case_number: int                    # 1–4
    case_label: str                     # "Corroborated Fact", etc.
    fact_a: Fact
    fact_b: Fact | None = None          # None for case 4 (extraction failure)
    relationship: FactRelationship | None = None
    explanation: str = ""
