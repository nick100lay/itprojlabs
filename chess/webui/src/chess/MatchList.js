import { Button } from 'react-bootstrap';
import Table from 'react-bootstrap/Table';


function MatchList(props) {
    
    const renderTableRows = (matches, setResult) => {
        return matches.map((match) => {
            let winner;
            if (match.result !== null) {
                winner = (
                    <>
                        {match.result.winner !== null ? match.result.winner.firstName + " " + match.result.winner.secondName : "Ничья"}
                    </>
                )
            } else {
                winner = (
                    <Button variant='primary' onClick={() => setResult(match)}>
                        Огласить результаты
                    </Button>
                )
            }
            return (<tr key={match.id}>
                <td>{match.firstPlayer.firstName + " " + match.firstPlayer.secondName}</td>
                <td>{match.secondPlayer.firstName + " " + match.secondPlayer.secondName}</td>
                <td>{winner}</td>
            </tr>);
        });
    };

    return (
        <Table striped bordered hover size="sm">
            <thead>
                <tr>
                    <th>Первый игрок</th>
                    <th>Второй игрок</th>
                    <th>Победитель</th>
                </tr>
            </thead>
            <tbody>
                {renderTableRows(props.matches, props.setResult)}
            </tbody>
        </Table>
    );
}

export default MatchList;