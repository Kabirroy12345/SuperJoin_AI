import logging
from typing import List
import uuid
from src.schemas import Fact, Chunk
from src.llm.adapter import LLMAdapter

logger = logging.getLogger(__name__)

class FactExtractor:
    """Extracts facts from text chunks using an LLM."""

    def __init__(self, llm_adapter: LLMAdapter):
        self.llm = llm_adapter
        self.system_prompt = (
            "You are a precise fact extraction system. Your task is to extract objective, atomic facts from text. "
            "A fact is a self-contained statement representing a single relationship or piece of information.\n\n"
            "Extract facts as a JSON array, where each object has the following keys:\n"
            "- claim: A full sentence stating the fact.\n"
            "- subject: The main entity the fact is about.\n"
            "- predicate: The relationship or action.\n"
            "- object_value: The target entity or value.\n"
            "- entities: A list of named entities involved.\n"
            "- entity_types: A list of corresponding types for the entities (e.g. Person, Organization, Location, Metric).\n"
            "- attributes: A dictionary of additional structured data (e.g., value, unit, period, role, status).\n"
            "- category: The category of the fact (e.g., financial, personnel, operational, geographic, legal).\n"
            "- confidence: A float between 0.0 and 1.0 indicating your confidence.\n"
            "- source_quote: The exact text from the chunk supporting the fact.\n\n"
            "Examples:\n"
            "Text: 'Acme Corp reported $5M revenue in Q3.'\n"
            "Output: [{\"claim\": \"Acme Corp reported $5M revenue in Q3.\", \"subject\": \"Acme Corp\", \"predicate\": \"reported revenue\", \"object_value\": \"$5M\", \"entities\": [\"Acme Corp\"], \"entity_types\": [\"Organization\"], \"attributes\": {\"period\": \"Q3\", \"currency\": \"USD\", \"value\": 5000000}, \"category\": \"financial\", \"confidence\": 0.95, \"source_quote\": \"Acme Corp reported $5M revenue in Q3.\"}]\n\n"
            "Text: 'Dr. John Smith joined the hospital as Chief of Surgery in 2021.'\n"
            "Output: [{\"claim\": \"Dr. John Smith joined the hospital as Chief of Surgery in 2021.\", \"subject\": \"Dr. John Smith\", \"predicate\": \"joined as\", \"object_value\": \"Chief of Surgery\", \"entities\": [\"Dr. John Smith\", \"Chief of Surgery\"], \"entity_types\": [\"Person\", \"Role\"], \"attributes\": {\"year\": 2021}, \"category\": \"personnel\", \"confidence\": 0.98, \"source_quote\": \"Dr. John Smith joined the hospital as Chief of Surgery in 2021.\"}]\n\n"
            "Text: 'The Nile is located in Africa.'\n"
            "Output: [{\"claim\": \"The Nile is located in Africa.\", \"subject\": \"The Nile\", \"predicate\": \"is located in\", \"object_value\": \"Africa\", \"entities\": [\"The Nile\", \"Africa\"], \"entity_types\": [\"Location\", \"Continent\"], \"attributes\": {}, \"category\": \"geographic\", \"confidence\": 0.99, \"source_quote\": \"The Nile is located in Africa.\"}]\n\n"
            "Ensure the output is ONLY a valid JSON array and contains no other text."
        )

    def extract(self, chunks: List[Chunk]) -> List[Fact]:
        """
        Extract facts from a list of chunks in sequence.
        
        Args:
            chunks: A list of Chunk objects to process.
            
        Returns:
            A list of Fact objects extracted from the chunks.
        """
        all_facts = []
        
        # Process in single batches iteratively for simplicity and rate limit friendliness
        for chunk in chunks:
            prompt = f"Extract facts from the following text:\n\n{chunk.text}"
            
            try:
                extracted_data = self.llm.call_json(prompt, system_prompt=self.system_prompt)
                
                if not isinstance(extracted_data, list):
                    logger.warning(f"Expected a JSON list from LLM, got {type(extracted_data)}")
                    continue
                    
                for item in extracted_data:
                    try:
                        fact_id = str(uuid.uuid4())
                        fact = Fact(
                            id=fact_id,
                            claim=item.get("claim", ""),
                            subject=item.get("subject", ""),
                            predicate=item.get("predicate", ""),
                            object_value=item.get("object_value", ""),
                            entities=item.get("entities", []),
                            entity_types=item.get("entity_types", []),
                            attributes=item.get("attributes", {}),
                            category=item.get("category", ""),
                            confidence=float(item.get("confidence", 0.0)),
                            source_quote=item.get("source_quote", ""),
                            doc_id=chunk.doc_id,
                            doc_filename=chunk.doc_filename,
                            page_number=chunk.page_number,
                            chunk_id=chunk.id
                        )
                        all_facts.append(fact)
                    except Exception as e:
                        logger.error(f"Failed to create Fact object from item {item}: {e}")
                        
            except Exception as e:
                logger.error(f"Fact extraction failed for chunk {chunk.id}: {e}")
                continue
                
        return all_facts
