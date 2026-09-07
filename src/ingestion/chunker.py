import uuid
import logging
from typing import List
from src.schemas import Chunk, ChunkType

logger = logging.getLogger(__name__)

class Chunker:
    """Splits raw page-level chunks into LLM-friendly chunks."""

    def __init__(self, target_tokens: int = 800, overlap_tokens: int = 100):
        self.target_tokens = target_tokens
        self.overlap_tokens = overlap_tokens
        # Estimate 1 token ≈ 4 chars
        self.target_chars = target_tokens * 4
        self.overlap_chars = overlap_tokens * 4

    def chunk(self, raw_chunks: List[Chunk]) -> List[Chunk]:
        """
        Splits a list of raw chunks into smaller chunks of target size.
        
        Args:
            raw_chunks: A list of raw Chunk objects (e.g., from PDFParser).
            
        Returns:
            A list of processed Chunk objects.
        """
        processed_chunks: List[Chunk] = []

        for chunk in raw_chunks:
            if chunk.chunk_type == ChunkType.TABLE:
                # Tables are not split
                processed_chunks.append(chunk)
            elif chunk.chunk_type == ChunkType.TEXT:
                split_chunks = self._split_text_chunk(chunk)
                processed_chunks.extend(split_chunks)
            else:
                logger.warning(f"Unknown chunk type: {chunk.chunk_type}. Keeping as is.")
                processed_chunks.append(chunk)

        return processed_chunks

    def _split_text_chunk(self, chunk: Chunk) -> List[Chunk]:
        """Splits a single text chunk into multiple chunks preserving paragraphs."""
        text = chunk.text
        if not text:
            return []

        if len(text) <= self.target_chars:
            return [chunk]

        paragraphs = text.split('\n\n')
        new_chunks = []
        current_text = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If a single paragraph is too large, split it by segments with overlap
            if len(para) > self.target_chars:
                # If current_text is not empty, save it first
                if current_text:
                    new_chunks.append(self._create_new_chunk(chunk, current_text))
                    current_text = ""
                
                # Split large paragraph by arbitrary chunks with overlap
                start = 0
                step = max(1, self.target_chars - self.overlap_chars)
                while start < len(para):
                    end = min(start + self.target_chars, len(para))
                    segment = para[start:end]
                    new_chunks.append(self._create_new_chunk(chunk, segment))
                    start += step
                    
            elif len(current_text) + len(para) + 2 <= self.target_chars:
                if current_text:
                    current_text += "\n\n" + para
                else:
                    current_text = para
            else:
                # Create a new chunk from current_text
                new_chunks.append(self._create_new_chunk(chunk, current_text))
                
                # Calculate overlap string from the end of current_text
                overlap_text = ""
                if self.overlap_chars > 0 and len(current_text) > self.overlap_chars:
                    overlap_text = current_text[-self.overlap_chars:]
                elif self.overlap_chars > 0:
                    overlap_text = current_text
                
                current_text = overlap_text + "\n\n" + para if overlap_text else para

        if current_text:
            new_chunks.append(self._create_new_chunk(chunk, current_text))

        return new_chunks

    def _create_new_chunk(self, original_chunk: Chunk, text: str) -> Chunk:
        """Helper to create a new Chunk based on an original chunk with new text."""
        return Chunk(
            id=str(uuid.uuid4()),
            doc_id=original_chunk.doc_id,
            doc_filename=original_chunk.doc_filename,
            page_number=original_chunk.page_number,
            text=text,
            chunk_type=original_chunk.chunk_type,
            token_estimate=len(text) // 4
        )
