// nettoie tous éléments qui pourraient introduire des données malveillantes.
import DOMPurify from 'dompurify';

export const sanitizedData = (text) => ({
    // https://blog.logrocket.com/using-dangerouslysetinnerhtml-react-application/
    // transforme un texte en élément HTML
    __html: DOMPurify.sanitize(text)
    }
);