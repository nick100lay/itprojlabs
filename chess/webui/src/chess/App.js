

import { Routes, Route } from 'react-router-dom';
import Container from 'react-bootstrap/Container';


import NavPanel from './NavPanel';
import HomePage from './HomePage';
import PlayersPage from './PlayersPage';
import CurrentMatchesPage from './CurrentMatchesPage';
import CompletedMatchesPage from './CompletedMatchesPage'


function ChessApp() {
    return (
        <>
            <NavPanel />

            <Container>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/players" element={<PlayersPage />} />
                    <Route path="/current-matches" element={<CurrentMatchesPage />} />
                    <Route path="/match-results" element={<CompletedMatchesPage />} />
                </Routes>
            </Container>
        </>
    );
}


export default ChessApp;