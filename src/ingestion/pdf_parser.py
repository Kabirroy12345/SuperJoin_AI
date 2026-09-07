import logging
import uuid
import datetime
from pathlib import Path
from typing import List, Tuple, Union
import pdfplumber

from src.schemas import Document, Chunk, ChunkType

logger = logging.getLogger(__name__)

class PDFParser:
    """Parses PDF documents into text and table chunks using pdfplumber."""

    def __init__(self):
        pass

    def parse(self, pdf_path: Union[str, Path]) -> Tuple[Document, List[Chunk]]:
        """
        Parses a PDF file and extracts text and tables as separate chunks.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            A tuple containing the Document metadata and a list of Chunks.
        """
        path = Path(pdf_path)
        doc_id = str(uuid.uuid4())
        filename = path.name
        chunks: List[Chunk] = []

        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {path}")

        try:
            with pdfplumber.open(str(path)) as doc_plumber:
                page_count = len(doc_plumber.pages)

                document = Document(
                    id=doc_id,
                    filename=filename,
                    page_count=page_count
                )

                for page_num, page_plumber in enumerate(doc_plumber.pages):
                    try:
                        # 1. Extract plain text
                        text = page_plumber.extract_text() or ""
                        clean_text = text.strip()

                        if clean_text:
                            text_chunk = Chunk(
                                id=str(uuid.uuid4()),
                                doc_id=doc_id,
                                doc_filename=filename,
                                page_number=page_num + 1,
                                text=clean_text,
                                chunk_type=ChunkType.TEXT,
                                token_estimate=len(clean_text) // 4
                            )
                            chunks.append(text_chunk)

                        # 2. Extract structured tables
                        tables = page_plumber.extract_tables()
                        for table in tables:
                            md_table = self._table_to_markdown(table)
                            if md_table:
                                table_chunk = Chunk(
                                    id=str(uuid.uuid4()),
                                    doc_id=doc_id,
                                    doc_filename=filename,
                                    page_number=page_num + 1,
                                    text=md_table,
                                    chunk_type=ChunkType.TABLE,
                                    token_estimate=len(md_table) // 4
                                )
                                chunks.append(table_chunk)

                    except Exception as e:
                        logger.warning(f"Error processing page {page_num + 1} of {filename}: {e}")
                        continue

        except Exception as e:
            logger.error(f"Failed to open or parse PDF {filename}: {e}")
            raise

        return document, chunks

    def _table_to_markdown(self, table: List[List[Union[str, None]]]) -> str:
        """Converts a parsed table into a markdown string."""
        if not table or not table[0]:
            return ""

        # Filter out completely empty rows
        filtered_rows = []
        for row in table:
            clean_row = [str(cell).replace('\n', ' ').strip() if cell is not None else "" for cell in row]
            if any(cell for cell in clean_row):
                filtered_rows.append(clean_row)

        if not filtered_rows:
            return ""

        # Pad rows to maximum column length
        max_cols = max(len(r) for r in filtered_rows)
        md_rows = []
        for i, row in enumerate(filtered_rows):
            padded_row = row + [""] * (max_cols - len(row))
            md_rows.append("| " + " | ".join(padded_row) + " |")

            # Add header separator after the first row
            if i == 0:
                separator = "| " + " | ".join(["---"] * max_cols) + " |"
                md_rows.append(separator)

        return "\n".join(md_rows)
