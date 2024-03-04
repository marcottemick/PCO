import Modal from "../../Elements/Modal";

import { sanitizedData } from "../../Elements/utils";

// affiche du CRO et des détails extraits
const ModalCRO = ({ setIsOpen, detailCRO, idCRO, setIdCRO }) => {

    // réinitialise les variables d'ouverture et id pour permettre la réouverture sur le même id CRO
    const handleClick = (bool) => {
        setIsOpen(bool);
        setIdCRO("");
    };

    return (
        <Modal
            setIsOpen={handleClick}
            titre={`CRO numéro ${idCRO}`}
            valeurBouton="Fermer le CRO">
            <div>
                <div id='modal-ul-datas'>
                    <ul>
                        <li>Numéro de sécurité social: {detailCRO.nir}</li>
                        <li>Patient(e): {detailCRO.name_patient}</li>
                        <li>Adresse: {detailCRO.address}</li>
                        <li>Date de naissance: {detailCRO.birthday}</li>
                    </ul>
                    <ul>
                        <li>Anatomopathologiste: {detailCRO.name_med}</li>
                        <li>Diagnostic: {detailCRO.diagnostic}</li>
                        <li>Model LLM: {detailCRO.source}</li>
                     </ul>
                </div>
                <div id='modal-CRO' dangerouslySetInnerHTML={sanitizedData(detailCRO.CRO.replaceAll('\n', '<br/>'))} />
            </div>
        </Modal>
    );
};

export default ModalCRO