import React from 'react';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';

const PITCH_WIDTH = 55; // meters
const PITCH_LENGTH = 91.4; // meters

const INITIAL_VIEW_STATE = {
    target: [PITCH_WIDTH / 2, PITCH_LENGTH / 2, 0],
    zoom: 18,
    pitch: 0,
    bearing: 0
};

export default function PitchMap({ data }: { data: any[] }) {
    const layers = [
        new ScatterplotLayer({
            id: 'players',
            data,
            getPosition: (d: any) => [d.x, d.y],
            getFillColor: [255, 0, 0],
            getRadius: 0.5,
        })
    ];

    return (
        <div style={{ position: 'relative', height: '500px', width: '100%', border: '1px solid #ccc' }}>
            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={true}
                layers={layers}
                style={{ position: 'absolute' }}
            >
            </DeckGL>
        </div>
    );
}
