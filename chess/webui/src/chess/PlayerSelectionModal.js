

import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import PlayerList from './PlayerList';
import usePlayers from './api/players';


function PlayersView(props) {

    if (props.isLoading) {
        return (
            <>
                <span>Загрузка</span>
            </>
        )
    } else if (props.players !== null) {
        return (
            <>
                <PlayerList players={props.players} selectPlayer={
                    player => { 
                        props.selectPlayer(player);
                        props.onHide();
                    }}
                    filter={props.filter} />
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


function PlayerSelectionModal(props) {

    const [players, , playersError, isLoading] = usePlayers();

    return (
        <Modal
            {...props}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            <header>
                <h1>
                    Выберите участника
                </h1>
            </header>

            <Modal.Body>
                <PlayersView players={players} playersError={playersError} isLoading={isLoading} onHide={props.onHide} selectPlayer={props.selectPlayer} filter={props.filter} />
            </Modal.Body>

            <Modal.Footer>
                <Button variant='secondary' onClick={props.onHide}>Закрыть</Button>
            </Modal.Footer>

        </Modal>
    );
}

export default PlayerSelectionModal;