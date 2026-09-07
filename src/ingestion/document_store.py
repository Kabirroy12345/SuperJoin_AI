import sqlite3
import logging
from typing import List, Optional

from src.schemas import Document, Chunk, ChunkType

logger = logging.getLogger(__name__)

class DocumentStore:
    """SQLite-based store for Documents and Chunks."""

    def __init__(self, db_path: str = 'knowledge.db'):
        """
        Initializes the DocumentStore and creates tables if they do not exist.
        
        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Returns a new SQLite connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Creates the necessary tables."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    upload_time TEXT NOT NULL,
                    page_count INTEGER NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    doc_id TEXT NOT NULL,
                    doc_filename TEXT NOT NULL,
                    page_number INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    chunk_type TEXT NOT NULL,
                    token_estimate INTEGER NOT NULL,
                    FOREIGN KEY(doc_id) REFERENCES documents(id)
                )
            ''')
            conn.commit()

    def add_document(self, doc: Document, chunks: List[Chunk]):
        """
        Inserts a document and its associated chunks into the database.
        
        Args:
            doc: The Document metadata.
            chunks: The list of Chunks associated with the document.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO documents (id, filename, upload_time, page_count) VALUES (?, ?, ?, ?)",
                (doc.id, doc.filename, doc.upload_time, doc.page_count)
            )
            
            chunk_data = [
                (
                    chunk.id, chunk.doc_id, chunk.doc_filename, 
                    chunk.page_number, chunk.text, 
                    chunk.chunk_type.value if hasattr(chunk.chunk_type, 'value') else str(chunk.chunk_type), 
                    chunk.token_estimate
                ) for chunk in chunks
            ]
            
            cursor.executemany(
                "INSERT INTO chunks (id, doc_id, doc_filename, page_number, text, chunk_type, token_estimate) VALUES (?, ?, ?, ?, ?, ?, ?)",
                chunk_data
            )
            conn.commit()

    def get_document(self, doc_id: str) -> Optional[Document]:
        """Retrieves a document by its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
            row = cursor.fetchone()
            
            if row:
                return Document(
                    id=row['id'],
                    filename=row['filename'],
                    upload_time=row['upload_time'],
                    page_count=row['page_count']
                )
            return None

    def get_all_documents(self) -> List[Document]:
        """Retrieves all documents."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents")
            rows = cursor.fetchall()
            
            return [
                Document(
                    id=row['id'],
                    filename=row['filename'],
                    upload_time=row['upload_time'],
                    page_count=row['page_count']
                ) for row in rows
            ]

    def get_chunks(self, doc_id: str) -> List[Chunk]:
        """Retrieves all chunks for a specific document ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chunks WHERE doc_id = ?", (doc_id,))
            rows = cursor.fetchall()
            
            chunks = []
            for row in rows:
                # Handle Enum if it's an enum, otherwise fallback string
                try:
                    ctype = ChunkType(row['chunk_type'])
                except ValueError:
                    # In case string matches Enum member name instead of value
                    ctype = getattr(ChunkType, row['chunk_type'], row['chunk_type'])

                chunks.append(Chunk(
                    id=row['id'],
                    doc_id=row['doc_id'],
                    doc_filename=row['doc_filename'],
                    page_number=row['page_number'],
                    text=row['text'],
                    chunk_type=ctype,
                    token_estimate=row['token_estimate']
                ))
            return chunks

    def document_exists(self, filename: str) -> bool:
        """Checks if a document with the given filename already exists."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM documents WHERE filename = ?", (filename,))
            return cursor.fetchone() is not None
