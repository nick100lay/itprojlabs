
import { useState } from 'react';
import Button from 'react-bootstrap/Button';

import MatchList from './MatchList';
import useCurrentMatches from './api/currentMatches';
import SettingResultModal from './SettingResultModal';
import MatchCreationModal from './MatchCreationModal'


function MatchView(props) {
    const [modalShow, setModalShow] = useState(false);
    const [selectedMatch, setSelectedMatch] = useState(null);

    if (props.isLoading) {
        return (
            <>
                <span>Загрузка</span>
            </>
        )
    } else if (props.matches !== null) {
        return (
            <>
                <Button variant="primary" onClick={() => setModalShow(true)}>Зарегистрировать матч</Button>
                <MatchList matches={props.matches} setResult={(match) => setSelectedMatch(match)} />
                <SettingResultModal
                    show={selectedMatch !== null}
                    onHide={() => setSelectedMatch(null)}
                    selectedMatch={selectedMatch}
                    postResults={props.matchesMethods.postResults}
                />
                <MatchCreationModal
                    show={modalShow}
                    onHide={() => setModalShow(false)}
                    postMatches={props.matchesMethods.post}
                />
            </>
        )
    } else {
        return (
            <>
                <span>Ошибка: {props.matchesError.message}</span>
            </>
        )
    }
}


function MatchesPage() {

    const [matches, matchesMethods, matchesError, isLoading] = useCurrentMatches();

    return (
        <>
            <header>
                <h1>
                    Список матчей
                </h1>
            </header>

            <MatchView matches={matches} matchesMethods={matchesMethods} matchesError={matchesError} isLoading={isLoading} />

        </>
    );
}


export default MatchesPage;