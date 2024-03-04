// nettoie tous éléments qui pourraient introduire des données malveillantes.
import DOMPurify from 'dompurify';

export const sanitizedData = (text) => ({
    // transforme un texte en élément HTML
    __html: DOMPurify.sanitize(text)
    }
);