
import { useState } from 'react';
import Button from 'react-bootstrap/Button';

import PlayerList from './PlayerList';
import usePlayers from './api/players';
import PlayerCreationModal from './PlayerCreationModal';


function PlayersView(props) {
    const [modalShow, setModalShow] = useState(false);

    if (props.isLoading) {
        return (
            <>
                <span>Загрузка</span>
            </>
        )
    } else if (props.players !== null) {
        return (
            <>
                <Button variant="primary" onClick={() => setModalShow(true)}>Зарегистрировать участника</Button>
                <PlayerList players={props.players} />
                <PlayerCreationModal
                    show={modalShow}
                    onHide={() => setModalShow(false)}
                    postPlayers={props.playerMethods.post}
                />
            </>
        )
    } else {
        return (
            <>
                <span>Ошибка: {props.playersError.message}</span>
            </>
        )
    }
}


function PlayersPage() {

    const [players, playerMethods, playersError, isLoading] = usePlayers();

    return (
        <>
            <header>
                <h1>
                    Список участников
                </h1>
            </header>

            <PlayersView players={players} playerMethods={playerMethods} playersError={playersError} isLoading={isLoading} />

        </>
    );
}


export default PlayersPage;