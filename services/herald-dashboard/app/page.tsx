"use client";

import { useState, useEffect } from 'react';
import PitchMap from './components/PitchMap';

export default function Home() {
    const [matches, setMatches] = useState([]);
    const [selectedMatchId, setSelectedMatchId] = useState(null);
    const [events, setEvents] = useState([]);

    useEffect(() => {
        fetch(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: '{ matches { matchId homeTeam awayTeam date } }' }),
        })
            .then(res => res.json())
            .then(data => {
                if (data.data && data.data.matches && data.data.matches.length > 0) {
                    setMatches(data.data.matches);
                    setSelectedMatchId(data.data.matches[0].matchId);
                }
            })
            .catch(err => console.error(err));
    }, []);

    useEffect(() => {
        if (!selectedMatchId) return;

        fetch(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: `{ events(matchId: ${selectedMatchId}) { type details } }`
            }),
        })
            .then(res => res.json())
            .then(data => {
                if (data.data && data.data.events) {
                    const parsedEvents = data.data.events.map((e: any) => {
                        try {
                            const details = JSON.parse(e.details);
                            return { ...e, ...details };
                        } catch (err) {
                            return e;
                        }
                    }).filter((e: any) => e.x !== undefined && e.y !== undefined);
                    setEvents(parsedEvents);
                }
            })
            .catch(err => console.error(err));
    }, [selectedMatchId]);

    return (
        <main style={{ padding: '2rem' }}>
            <h1>Project Olympian: Herald Dashboard</h1>
            <div style={{ display: 'flex', gap: '2rem' }}>
                <div style={{ width: '300px' }}>
                    <h2>Matches</h2>
                    <ul>
                        {matches.map((m: any) => (
                            <li
                                key={m.matchId}
                                onClick={() => setSelectedMatchId(m.matchId)}
                                style={{ cursor: 'pointer', fontWeight: selectedMatchId === m.matchId ? 'bold' : 'normal' }}
                            >
                                {m.homeTeam} vs {m.awayTeam}
                            </li>
                        ))}
                    </ul>
                </div>
                <div style={{ flex: 1 }}>
                    <h2>Tactical Map</h2>
                    <PitchMap data={events} />
                </div>
            </div>
        </main>
    )
}
