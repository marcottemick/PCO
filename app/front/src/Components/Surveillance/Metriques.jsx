import './Surveillance.css';

import { useEffect, useState } from 'react';

// extension de génération de graphique
import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { Line } from "react-chartjs-2";
import { fetchGetMetriques } from '../../Hooks/getMetriques';
import Chargement from '../../Elements/Chargement';

Chart.register(CategoryScale);

// affichage des métriques des tests du modèle
const Metriques = () => {
    // stocke les métriques
    const [chartData, setChartData] = useState({});
    // surveille le chargement des données
    const [isLoading, setIsloading] = useState(false);
    // gère les erreurs
    const [isError, setIsError] = useState(false);

    // chargement des métriques
    useEffect(() => {
        setIsloading(true);
        fetchGetMetriques()
            .then(response =>
                setChartData(response.response)
            )
            .catch(e => {
                console.error(e.message);
                setIsloading(() => false);
                setIsError(true);
            })
            .finally(() => setIsloading(false));
    }, []);

    console.log('isLoading', isLoading, 'isError', isError)


    // constantes pour génération des graphiques
    const labels_ner = ['ents', 'DATE', 'DIAG', 'LOC', 'PER']
    const colors_label = ['blue', 'violet', 'yellow', 'green', 'orange']
    const metrics = ['precision', 'rappel', 'scoref1']

    const renderMetrics = () => {
        return (
            <div id='container-graph'>
                {/* première boucle => les métriques */}
                {metrics.map(metric =>
                    <div style={{ width: '1000px' }}>
                        <Line
                            data={{
                                // seconde boucle => les différents labels surveillés
                                labels: chartData.remarque.map(rq => rq.substring(0, 7)),
                                datasets:
                                    labels_ner.map((label_ner, index) => ({
                                        label: `${label_ner}_${metric}`,
                                        data: chartData[`${label_ner}_${metric}`],
                                        backgroundColor: colors_label,
                                        borderColor: colors_label[index],
                                        borderWidth: 2,
                                        yAxisID: `y`,
                                    }))
                            }}
                            options={{
                                plugins: {
                                    title: {
                                        display: true,
                                        text: metric
                                    }
                                }
                            }}
                        />
                    </div>

                )}
            </div>
        );
    };

    if (!isLoading && Object.keys(chartData).length !== 0) {
        return renderMetrics();
    }
    else if (!isLoading && isError) {
        return <Chargement texte='Une erreur est survenue durant le chargement des données !' />
    }
    else if (isLoading) {
        return <Chargement texte='Métriques en cours de chargement...' />
    }

};

export default Metriques;