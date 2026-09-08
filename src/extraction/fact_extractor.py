import logging
import re
from typing import List, Optional
import uuid
from src.schemas import Fact, Chunk
from src.llm.adapter import LLMAdapter

logger = logging.getLogger(__name__)

class FactExtractor:
    """Extracts high-signal facts from text chunks using an LLM with rigorous filtering."""

    def __init__(self, llm_adapter: LLMAdapter):
        self.llm = llm_adapter
        self.system_prompt = (
            "You are an expert fact extraction engine. Your objective is to extract high-signal, self-contained, "
            "objective facts from corporate, regulatory, and economic documents.\n\n"
            "CRITICAL QUALITY RULES:\n"
            "1. EXTRACT SUBSTANTIVE FACTS: Financial metrics (revenue, EBITDA, profits), operational numbers (volume, "
            "network reach, pin codes), governance/personnel changes, and strategic milestones.\n"
            "2. REJECT BOILERPLATE: NEVER extract generic statutory phrases or legal disclaimers (e.g., 'pursuant to the "
            "Companies Act 2013', 'rules framed thereunder', 'secretarial standards'). These are boilerplate, not facts.\n"
            "3. REJECT UNPARSED TABLE DUMPS: NEVER extract lines that are just sequences of numbers or percentages "
            "(e.g., 'Total 77 0 0% 28 36.36%'). A fact requires a defined metric and meaning.\n"
            "4. REJECT BARE HEADERS: A header or role title without an entity or relationship is not a fact "
            "(e.g., 'Chief Financial Officer' alone is not a fact; 'X serves as Chief Financial Officer' is a fact).\n"
            "5. ATOMIC & GROUNDED: Each fact must be self-contained and grounded by an exact verbatim quote.\n\n"
            "Extract facts as a JSON array where each object has:\n"
            "- claim: A clear, self-contained sentence stating the fact.\n"
            "- subject: The entity or subject the fact is about.\n"
            "- predicate: The relationship, action, or metric property.\n"
            "- object_value: The stated value, figure, or target entity.\n"
            "- entities: List of named entities (e.g. ['Acme Corp', 'Jane Doe']).\n"
            "- entity_types: Corresponding types (e.g. ['Organization', 'Person', 'Metric']).\n"
            "- attributes: Structured key-values (e.g., {'value': 1500, 'unit': 'million', 'period': '2024'}).\n"
            "- category: One of 'financial', 'operational', 'personnel', 'geographic', 'strategic'.\n"
            "- confidence: Float between 0.0 and 1.0.\n"
            "- source_quote: Verbatim exact snippet from the text supporting the claim.\n\n"
            "Examples:\n"
            "Text: 'Acme Logistics reported revenue from operations of $1,500 million in 2024.'\n"
            "Output: [{\"claim\": \"Acme Logistics reported revenue from operations of $1,500 million in 2024.\", "
            "\"subject\": \"Acme Logistics\", \"predicate\": \"reported revenue from operations\", \"object_value\": \"$1,500 million\", "
            "\"entities\": [\"Acme Logistics\"], \"entity_types\": [\"Organization\"], "
            "\"attributes\": {\"period\": \"2024\", \"value\": 1500, \"unit\": \"$ million\"}, "
            "\"category\": \"financial\", \"confidence\": 0.98, "
            "\"source_quote\": \"Acme Logistics reported revenue from operations of $1,500 million in 2024.\"}]\n\n"
            "Ensure output is ONLY a valid JSON array and contains no commentary."
        )

    def _is_valid_fact(self, fact: Fact) -> bool:
        """Filter out noisy boilerplate, unparsed table dumps, and incomplete fragments."""
        claim = fact.claim.strip()
        if len(claim) < 20:
            return False

        # Reject bare numeric / table row sequences
        if re.search(r'^\s*total\s+[\d\s.%]+$', claim, re.IGNORECASE):
            return False
        if len(re.findall(r'\b\d+(?:\.\d+)?%?\b', claim)) >= 4 and len(re.findall(r'[a-zA-Z]{3,}', claim)) < 3:
            return False

        # Reject legal boilerplate fragments
        boilerplate_terms = [
            "the companies act, 2013",
            "rules framed thereunder",
            "secretarial standards",
            "pursuant to section",
            "table of contents",
            "forward-looking statements",
            "safe harbor",
        ]
        claim_lower = claim.lower()
        if any(term in claim_lower for term in boilerplate_terms) and not any(m in claim_lower for m in ["crore", "revenue", "profit", "ebitda", "million", "billion", "appointed", "joined", "resigned"]):
            return False

        # Reject facts where subject or object is missing
        if not fact.subject or len(fact.subject.strip()) < 2:
            return False
        if not fact.object_value or len(fact.object_value.strip()) < 2:
            return False

        return True

    def extract(self, chunks: List[Chunk], batch_size: int = 3) -> List[Fact]:
        """
        Extract high-signal facts from a list of chunks using efficient batching.
        Batches multiple chunks into single LLM queries to maximize speed and stay
        comfortably within rate-limits.
        
        Args:
            chunks: A list of Chunk objects to process.
            batch_size: Number of chunks to batch per LLM call (default 3).
            
        Returns:
            A list of high-signal Fact objects extracted from the chunks.
        """
        all_facts = []
        valid_chunks = [c for c in chunks if len(c.text.strip()) >= 30]

        for i in range(0, len(valid_chunks), batch_size):
            batch = valid_chunks[i:i + batch_size]
            chunk_map = {c.id: c for c in batch}

            prompt_lines = ["Extract objective, substantive facts from the following text chunk(s) as a JSON array:\n"]
            for idx, c in enumerate(batch, 1):
                prompt_lines.append(f"--- CHUNK {idx} (Page {c.page_number}, Chunk ID: {c.id}) ---\n{c.text}\n")

            prompt_lines.append(
                "For each fact, output a JSON object with:\n"
                "- claim: Full substantive sentence\n"
                "- subject: Main entity or metric subject\n"
                "- predicate: Relationship, metric, or action\n"
                "- object_value: Value, state, or target\n"
                "- entities: List of named entities involved\n"
                "- entity_types: List of corresponding types\n"
                "- attributes: Structured key-values (e.g., {'value': 1500, 'unit': 'million', 'period': '2024'})\n"
                "- category: One of 'financial', 'operational', 'personnel', 'geographic', 'strategic'\n"
                "- confidence: Float between 0.0 and 1.0\n"
                "- source_quote: Verbatim exact snippet from the text supporting the claim\n"
                "- chunk_id: The exact Chunk ID from which this fact was extracted\n"
                "- page_number: The exact Page number from which this fact was extracted\n\n"
                "Output ONLY a valid JSON array and no other text."
            )
            prompt = "\n".join(prompt_lines)

            try:
                extracted_data = self.llm.call_json(prompt, system_prompt=self.system_prompt)
                if not isinstance(extracted_data, list):
                    continue

                for item in extracted_data:
                    try:
                        c_id = item.get("chunk_id")
                        ref_chunk = chunk_map.get(c_id, batch[0])

                        # Robust page number extraction
                        raw_page = item.get("page_number")
                        if raw_page is not None:
                            page_match = re.search(r'\d+', str(raw_page))
                            page_num = int(page_match.group(0)) if page_match else ref_chunk.page_number
                        else:
                            page_num = ref_chunk.page_number

                        # Robust confidence parsing
                        raw_conf = item.get("confidence", 0.90)
                        try:
                            if isinstance(raw_conf, str) and "%" in raw_conf:
                                confidence = float(raw_conf.replace("%", "").strip()) / 100.0
                            else:
                                confidence = float(raw_conf)
                        except (ValueError, TypeError):
                            confidence = 0.90

                        fact_id = str(uuid.uuid4())
                        fact = Fact(
                            id=fact_id,
                            claim=item.get("claim", "").strip(),
                            subject=item.get("subject", "").strip(),
                            predicate=item.get("predicate", "").strip(),
                            object_value=item.get("object_value", "").strip(),
                            entities=item.get("entities", []),
                            entity_types=item.get("entity_types", []),
                            attributes=item.get("attributes", {}),
                            category=item.get("category", "operational"),
                            confidence=confidence,
                            source_quote=item.get("source_quote", "").strip(),
                            doc_id=ref_chunk.doc_id,
                            doc_filename=ref_chunk.doc_filename,
                            page_number=page_num,
                            chunk_id=ref_chunk.id
                        )

                        if self._is_valid_fact(fact):
                            all_facts.append(fact)
                        else:
                            logger.debug(f"Filtered out low-signal fact: {fact.claim[:60]}")
                    except Exception as e:
                        logger.error(f"Failed to create Fact: {e}")

            except Exception as e:
                logger.error(f"Batch extraction failed for batch starting at {i}: {e}")
                continue

        return all_facts
