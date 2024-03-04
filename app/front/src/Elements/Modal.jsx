import './Modal.css'; 

//contenant modal => props.children
const Modal = ({children, setIsOpen, titre, valeurBouton}) => {

    return (
        <>
            <div className='darkBG' onClick={() => setIsOpen(false)} />
            <div className='centered'>
                <div className='modal'>
                    <div className='modalHeader'>
                        <h5 className='heading'>{titre}</h5>
                    </div>
                 <button className='closeBtn' onClick={() => setIsOpen(false)}>
                        <p>x</p>
                    </button>
                    <div className='modalContent'>
                        {children}
                    </div>
                    <div className='modalActions'>
                        <div className='actionsContainer'>
                         <button className='btn' onClick={() => setIsOpen(false)}>
                                {valeurBouton}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Modal;