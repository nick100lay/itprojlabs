
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import { useForm } from 'react-hook-form';


function SettingResultModal(props) {

    const { register, handleSubmit, reset, formState: { errors }, setError } = useForm();
    const onSuccess = () => {
        reset();
        props.onHide();
    }
    const onSubmit = matchResult => {
        props.postResults([{matchId: props.selectedMatch.id, ...matchResult}])
            .then(() => onSuccess())
            .catch(() => setError("post", {}, { shouldFocus: false }));
    }

    if (props.selectedMatch === null) {
        return <></>
    }
    return (
        <Modal
            {...props}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            <Form onSubmit={handleSubmit(onSubmit)}>
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Выберите победителя
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    { errors.post && <Form.Text className="text-danger">
                        Не удалось огласить итоги матча
                    </Form.Text> }
                    <Form.Select { ...register("winner") } aria-label="Default select example">
                        <option value="1">{props.selectedMatch.firstPlayer.firstName + " " + props.selectedMatch.firstPlayer.secondName}</option>
                        <option value="2">{props.selectedMatch.secondPlayer.firstName + " " + props.selectedMatch.secondPlayer.secondName}</option>
                        <option value="0">Ничья</option>
                    </Form.Select>
                </Modal.Body>
                <Modal.Footer>
                    <Button type="submit">Огласить результаты</Button>
                    <Button variant='secondary' onClick={props.onHide}>Закрыть</Button>
                </Modal.Footer>
            </Form>
        </Modal>
    );
}


export default SettingResultModal;