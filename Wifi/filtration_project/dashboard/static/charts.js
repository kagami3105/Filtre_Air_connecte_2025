document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("section.card").forEach(card => {
    const id = card.dataset.id;
    const ctx = document.getElementById(`chart-${id}`);
    const rawData = document.getElementById(`data-${id}`);
    if (!ctx || !rawData) return;

    const parsed = JSON.parse(rawData.textContent);

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: parsed.labels.reverse(),
        datasets: [
          {
            label: 'Température (°C)',
            data: parsed.temperature.reverse(),
            borderColor: '#e74c3c',
            backgroundColor: 'rgba(231, 76, 60, 0.2)',
            tension: 0.3,
            fill: true
          },
          {
            label: 'Humidité (%)',
            data: parsed.humidity.reverse(),
            borderColor: '#3498db',
            backgroundColor: 'rgba(52, 152, 219, 0.2)',
            tension: 0.3,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  });
});