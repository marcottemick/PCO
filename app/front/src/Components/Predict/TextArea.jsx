// élément qui récupère le CRO à analyser
const Textarea = ({ CRO, setCRO, handleClickCRO }) => {
    // récupère le CRO à analyser
    const handleChangementTextarea = (event) => {
        setCRO(event.target.value);
    };

    return (
        <div id='container-textarea'>
            <div>
                <textarea
                    id="textarea"
                    value={CRO}
                    onChange={handleChangementTextarea}
                    placeholder="Copier votre CRO ici ..."
                />
            </div>
            <div>
                <button
                    // bouton qui permet de valider le CRO et de lancer l'analyse
                    className="btn"
                    onClick={handleClickCRO}>
                    <div>
                        <span class="material-symbols-outlined">search</span>
                        Analyser le CRO
                    </div>
                </button>
            </div>
        </div>
    );
};

export default Textarea;