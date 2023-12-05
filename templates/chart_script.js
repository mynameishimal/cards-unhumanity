document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM Content Loaded");
    const pastScoresData = JSON.parse(document.getElementById('pastScoresData').textContent);
    console.log("Past Scores Data: ", pastScoresData);

    const ctx = document.getElementById('past-scores-chart').getContext('2d');
    console.log("Context: ", ctx);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from(Array(pastScoresData.length), (_, i) => i + 1),
            datasets: [{
                label: 'Past Scores',
                data: pastScoresData,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});