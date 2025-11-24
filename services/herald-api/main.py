import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import psycopg2
import os
import json
from typing import List, Optional

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mercury:mercury_password@nexus:5432/mercury_db")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@strawberry.type
class Event:
    event_id: int
    match_id: int
    type: str
    timestamp: float
    details: str # JSON string

@strawberry.type
class Match:
    match_id: int
    home_team: str
    away_team: str
    date: str

@strawberry.type
class Query:
    @strawberry.field
    def matches(self) -> List[Match]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT match_id, home_team, away_team, date FROM matches")
        rows = cur.fetchall()
        matches = [Match(match_id=r[0], home_team=r[1], away_team=r[2], date=str(r[3])) for r in rows]
        conn.close()
        return matches

    @strawberry.field
    def events(self, match_id: int) -> List[Event]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT event_id, match_id, type, timestamp, details FROM events WHERE match_id = %s", (match_id,))
        rows = cur.fetchall()
        events = []
        for r in rows:
            # Ensure details is a string
            details_val = r[4]
            if isinstance(details_val, dict):
                details_val = json.dumps(details_val)
            events.append(Event(event_id=r[0], match_id=r[1], type=r[2], timestamp=r[3], details=details_val))
        conn.close()
        return events

schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.get("/health")
def health_check():
    return {"status": "ok"}
