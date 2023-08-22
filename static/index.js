const apiUrl = 'http://localhost:5000';
const portfolioInfoElement = document.getElementById('portfolio-info');
const networthChartElement = document.getElementById('networth-chart'); // Add an element to hold the chart

// Function to fetch historical networth data
async function fetchNetworthData() {
    try {
        const response = await fetch(apiUrl+'/'); // Change the URL to match your backend API URL
        const data = await response.json();

        const networthData = data.networth;

        // Create arrays for chart data
        const networthDates = networthData.map(item => new Date(item.date)); // Convert date strings to Date objects
        const networthValues = networthData.map(item => item.networth);

        // Create the line chart
        const ctx = document.getElementById('networth-chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: networthDates,
                datasets: [{
                    label: 'Networth History',
                    data: networthValues,
                    borderColor: 'blue',
                    backgroundColor: 'rgba(0, 0, 255, 0.2)',
                    fill: true,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day'
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Networth'
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error('Error fetching networth data:', error);
    }
}

// Call the function to fetch and display networth data
fetchNetworthData();

