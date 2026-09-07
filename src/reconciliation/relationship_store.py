import sqlite3
from typing import List, Optional

from src.schemas import FactRelationship, RelationshipType

class RelationshipStore:
    """SQLite store for fact relationships."""
    
    def __init__(self, db_path: str = 'knowledge.db'):
        """Initializes the database connection and schema."""
        self.db_path = db_path
        self._init_db()
        
    def _get_connection(self) -> sqlite3.Connection:
        """Gets a database connection with row factory configured."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initializes the database schema if it doesn't exist."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fact_relationships (
                    id TEXT PRIMARY KEY,
                    fact_a_id TEXT NOT NULL,
                    fact_b_id TEXT NOT NULL,
                    relationship_type TEXT NOT NULL,
                    explanation TEXT,
                    confidence REAL
                )
            """)
            # Create indexes for faster queries on fact lookups
            conn.execute("CREATE INDEX IF NOT EXISTS idx_rel_fact_a ON fact_relationships(fact_a_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_rel_fact_b ON fact_relationships(fact_b_id)")
            conn.commit()

    def add_relationship(self, rel: FactRelationship):
        """Adds a single relationship to the store."""
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO fact_relationships 
                (id, fact_a_id, fact_b_id, relationship_type, explanation, confidence)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(rel.id), 
                    str(rel.fact_a_id), 
                    str(rel.fact_b_id), 
                    rel.relationship_type.value, 
                    rel.explanation, 
                    rel.confidence
                )
            )
            conn.commit()

    def add_relationships(self, rels: List[FactRelationship]):
        """Adds multiple relationships to the store in a batch."""
        if not rels:
            return
            
        with self._get_connection() as conn:
            conn.executemany(
                """
                INSERT OR REPLACE INTO fact_relationships 
                (id, fact_a_id, fact_b_id, relationship_type, explanation, confidence)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        str(r.id), 
                        str(r.fact_a_id), 
                        str(r.fact_b_id), 
                        r.relationship_type.value, 
                        r.explanation, 
                        r.confidence
                    ) for r in rels
                ]
            )
            conn.commit()

    def _row_to_model(self, row: sqlite3.Row) -> FactRelationship:
        """Converts a database row to a FactRelationship model."""
        return FactRelationship(
            id=row['id'],
            fact_a_id=row['fact_a_id'],
            fact_b_id=row['fact_b_id'],
            relationship_type=RelationshipType(row['relationship_type']),
            explanation=row['explanation'],
            confidence=row['confidence']
        )

    def get_relationships(self, type: Optional[str] = None) -> List[FactRelationship]:
        """Gets relationships, optionally filtering by relationship type."""
        with self._get_connection() as conn:
            if type:
                cursor = conn.execute(
                    "SELECT * FROM fact_relationships WHERE relationship_type = ?", 
                    (type,)
                )
            else:
                cursor = conn.execute("SELECT * FROM fact_relationships")
            return [self._row_to_model(row) for row in cursor.fetchall()]

    def get_all(self) -> List[FactRelationship]:
        """Gets all relationships from the store."""
        return self.get_relationships()

    def get_by_fact(self, fact_id: str) -> List[FactRelationship]:
        """Gets all relationships involving a specific fact.
        
        Args:
            fact_id: The ID of the fact to search for.
            
        Returns:
            A list of relationships where the given fact is either fact_a or fact_b.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM fact_relationships WHERE fact_a_id = ? OR fact_b_id = ?", 
                (str(fact_id), str(fact_id))
            )
            return [self._row_to_model(row) for row in cursor.fetchall()]

    def count(self) -> int:
        """Gets the total number of relationships in the store."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM fact_relationships")
            return cursor.fetchone()[0]
