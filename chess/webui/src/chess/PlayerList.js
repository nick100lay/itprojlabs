import Table from 'react-bootstrap/Table';


function PlayerList(props) {
    
    const renderTableRows = (players, selectPlayer, filter) => {
        players = filter !== undefined ? players.filter(filter) : players
        return players.map((player) => (
            <tr onClick={() => selectPlayer && selectPlayer(player)} key={player.id}>
                <td>{player.firstName}</td>
                <td>{player.secondName}</td>
            </tr>
        ));
    };

    return (
        <Table striped bordered hover size="sm">
            <thead>
                <tr>
                    <th>Имя</th>
                    <th>Фамилия</th>
                </tr>
            </thead>
            <tbody>
                {renderTableRows(props.players, props.selectPlayer, props.filter)}
            </tbody>
        </Table>
    );
}

export default PlayerList;