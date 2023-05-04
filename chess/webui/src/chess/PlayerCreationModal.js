

import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import { useForm } from 'react-hook-form';


function PlayerCreationModal(props) {
    const { register, handleSubmit, reset, formState: { errors }, setError } = useForm();
    const onSuccess = () => {
        reset();
        props.onHide();
    }
    const onSubmit = player => {
        props.postPlayers([player])
            .then(() => onSuccess())
            .catch(() => setError("post", {}, { shouldFocus: false }));
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
                        Зарегистрировать участника
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    { errors.post && <Form.Text className="text-danger">
                        Не удалось зарегистрировать участника
                    </Form.Text> }
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Label>Имя</Form.Label>
                        <Form.Control type="text" placeholder="Имя" 
                            { ...register("firstName", { 
                                required: true, 
                                minLength: 2,
                                maxLength: 20
                            })} 
                        />
                        { errors.firstName && <Form.Text className="text-danger">
                            { errors.firstName.type === "required" && "Требуется указать имя" }
                            { errors.firstName.type === "minLength" && "Имя слишком короткое" }
                            { errors.firstName.type === "maxLength" && "Имя слишком длинное" }
                        </Form.Text> }
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicPassword">
                        <Form.Label>Фамилия</Form.Label>
                        <Form.Control type="text" placeholder="Фамилия" 
                            { ...register("secondName", {
                                required: true,
                                minLength: 2,
                                maxLength: 20
                            })}
                        />
                        { errors.secondName && <Form.Text className="text-danger">
                            { errors.secondName.type === "required" && "Требуется указать фамилию" }
                            { errors.secondName.type === "minLength" && "Фамилия слишком короткая" }
                            { errors.secondName.type === "maxLength" && "Фамилия слишком длинная" }
                        </Form.Text> }
                    </Form.Group>
                </Modal.Body>
                <Modal.Footer>
                    <Button type="submit">Зарегистрировать</Button>
                    <Button variant='secondary' onClick={props.onHide}>Закрыть</Button>
                </Modal.Footer>
            </Form>
        </Modal>
    );
}


export default PlayerCreationModal;