import sqlite3
import json
from typing import List, Optional
import logging
from src.schemas import Fact

logger = logging.getLogger(__name__)

class FactStore:
    """Store for managing extracted facts using SQLite."""

    def __init__(self, db_path: str = 'knowledge.db'):
        """
        Initialize the FactStore and create tables if they don't exist.
        
        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Create the facts table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS facts (
                    id TEXT PRIMARY KEY,
                    claim TEXT,
                    subject TEXT,
                    predicate TEXT,
                    object_value TEXT,
                    entities TEXT,
                    entity_types TEXT,
                    attributes TEXT,
                    category TEXT,
                    confidence REAL,
                    source_quote TEXT,
                    doc_id TEXT,
                    doc_filename TEXT,
                    page_number INT,
                    chunk_id TEXT
                )
            ''')
            conn.commit()

    def add_facts(self, facts: List[Fact]):
        """
        Add a list of facts to the store.
        
        Args:
            facts: List of Fact objects to store.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for fact in facts:
                cursor.execute('''
                    INSERT OR REPLACE INTO facts (
                        id, claim, subject, predicate, object_value, 
                        entities, entity_types, attributes, category, 
                        confidence, source_quote, doc_id, doc_filename, 
                        page_number, chunk_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    fact.id,
                    fact.claim,
                    fact.subject,
                    fact.predicate,
                    fact.object_value,
                    json.dumps(fact.entities),
                    json.dumps(fact.entity_types),
                    json.dumps(fact.attributes),
                    fact.category,
                    fact.confidence,
                    fact.source_quote,
                    fact.doc_id,
                    fact.doc_filename,
                    fact.page_number,
                    fact.chunk_id
                ))
            conn.commit()

    def _row_to_fact(self, row: tuple) -> Fact:
        """Convert a database row to a Fact object."""
        return Fact(
            id=row[0],
            claim=row[1],
            subject=row[2],
            predicate=row[3],
            object_value=row[4],
            entities=json.loads(row[5]),
            entity_types=json.loads(row[6]),
            attributes=json.loads(row[7]),
            category=row[8],
            confidence=row[9],
            source_quote=row[10],
            doc_id=row[11],
            doc_filename=row[12],
            page_number=row[13],
            chunk_id=row[14]
        )

    def get_facts(self, doc_id: Optional[str] = None) -> List[Fact]:
        """
        Get facts, optionally filtered by doc_id.
        
        Args:
            doc_id: Optional document ID to filter by.
            
        Returns:
            List of Fact objects.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if doc_id:
                cursor.execute('SELECT * FROM facts WHERE doc_id = ?', (doc_id,))
            else:
                cursor.execute('SELECT * FROM facts')
            
            rows = cursor.fetchall()
            return [self._row_to_fact(row) for row in rows]

    def get_all(self, exclude_doc: Optional[str] = None) -> List[Fact]:
        """
        Get all facts, optionally excluding a specific document.
        
        Args:
            exclude_doc: Optional document ID to exclude.
            
        Returns:
            List of Fact objects.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if exclude_doc:
                cursor.execute('SELECT * FROM facts WHERE doc_id != ?', (exclude_doc,))
            else:
                cursor.execute('SELECT * FROM facts')
                
            rows = cursor.fetchall()
            return [self._row_to_fact(row) for row in rows]

    def get_fact(self, fact_id: str) -> Optional[Fact]:
        """
        Get a specific fact by ID.
        
        Args:
            fact_id: The ID of the fact to retrieve.
            
        Returns:
            The Fact object if found, otherwise None.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM facts WHERE id = ?', (fact_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_fact(row)
            return None

    def count(self) -> int:
        """
        Count the total number of facts in the store.
        
        Returns:
            Integer count of facts.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM facts')
            return cursor.fetchone()[0]
