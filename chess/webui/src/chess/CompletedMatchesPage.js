

import MatchList from './MatchList';
import useCompletedMatches from './api/completedMatches';


function MatchView(props) {
    if (props.isLoading) {
        return (
            <>
                <span>Загрузка</span>
            </>
        )
    } else if (props.matches !== null) {
        return (
            <>
                <MatchList matches={props.matches} />
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


function CompletedMatchesPage() {

    const [matches, , matchesError, isLoading] = useCompletedMatches();

    return (
        <>
            <header>
                <h1>
                    Итоги матчей
                </h1>
            </header>

            <MatchView matches={matches} matchesError={matchesError} isLoading={isLoading} />

        </>
    );
}


export default CompletedMatchesPage;