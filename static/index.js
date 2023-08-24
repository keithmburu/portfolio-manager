const apiUrl = 'http://localhost:5000/portfolio';
const portfolioBody = document.getElementById('portfolioBody');
const portfolioInfoElement = document.getElementById('portfolio-info');
const networthChartElement = document.getElementById('networth-chart'); // Add an element to hold the chart

document.addEventListener('DOMContentLoaded', () => getStocks());
document.addEventListener('DOMContentLoaded', () => displayNetWorth());
document.addEventListener('DOMContentLoaded', () => chartNetWorth());

async function getStocks() {
    try {
        // Fetch portfolio data from the backend
        const response = await fetch(apiUrl);
        const data = await response.json();

        const portfolioContainer = document.getElementById('portfolio-container');
        portfolioContainer.innerHTML = '';

        // Create table element
        const table = document.createElement('table');
        table.className = 'custom-table';

        // Create table header row
        const headerRow = document.createElement('tr');
        ['Stock Ticker', 'Stock Name', 'Amount Holding', 'Cost', 'Profit', 'Action'].forEach(headerText => {
            const headerCell = document.createElement('th');
            headerCell.textContent = headerText;
            headerRow.appendChild(headerCell);
        });
        table.appendChild(headerRow);

        data.portfolio.forEach(stock => {
            // Create table row
            const row = document.createElement('tr');

            // Stock Ticker
            const stockTickerCell = document.createElement('td');
            stockTickerCell.textContent = stock[1];
            row.appendChild(stockTickerCell);

            // Stock Name
            const stockNameCell = document.createElement('td');
            stockNameCell.textContent = stock[2];
            row.appendChild(stockNameCell);

            // Amount Holding
            const amountHoldingCell = document.createElement('td');
            amountHoldingCell.textContent = stock[3];
            row.appendChild(amountHoldingCell);

            // Cost
            const costCell = document.createElement('td');
            costCell.textContent = `$${stock[6]}`;
            row.appendChild(costCell);

            // Profit
            const profitCell = document.createElement('td');
            profitCell.textContent = `$${data.profit[stock[2]].toFixed(2)}`;
            row.appendChild(profitCell);

            // Action
            const actionCell = document.createElement('td');
            const buyInput = document.createElement('input');
            buyInput.type = 'text';
            buyInput.id = `buyAmount${stock[0]}`;
            buyInput.value = 0;
            const buyButton = document.createElement('button');
            buyButton.textContent = 'Buy';
            buyButton.onclick = () => transaction(stock[0], 'BUY',stock);
            const sellInput = document.createElement('input');
            sellInput.type = 'text';
            sellInput.id = `sellAmount${stock[0]}`;
            sellInput.value = 0;
            const sellButton = document.createElement('button');
            sellButton.textContent = 'Sell';
            sellButton.onclick = () => transaction(stock[0], 'SELL',stock);
            buyButton.style.marginRight = '10px';
            actionCell.appendChild(buyInput);
            actionCell.appendChild(buyButton);
            actionCell.appendChild(sellInput);
            actionCell.appendChild(sellButton);
            row.appendChild(actionCell);

            table.appendChild(row);
        });

        // Append table to container
        portfolioContainer.appendChild(table);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function newStock() {
    toggleFormVisibility();
    const stockData = {
        stock_ticker: document.getElementById("stockTicker").value,                         
        stock_name: document.getElementById("stockName").value, 
        amount_holding: document.getElementById("amountHolding").value,
        buy_datetime: new Date().toISOString(),
    };
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(stockData)
        });
        const data = await response.json();
        if (data.message) {
            console.log(data.message);
            getStocks();
            displayNetWorth();
        } else if (data.error) {
            window.alert(data.error);
        }
    } catch(error) {
        window.alert('Error creating stock:', data.error);
        console.error('Error creating stock:', error);
    }
}

function toggleFormVisibility() {
    const form = document.getElementById("newStockForm");
    if (form.style.visibility == "visible") {
        form.style.visibility = "hidden";
    } else {
        form.style.visibility = "visible";
    }
}

async function transaction(id, transaction_type, stockData) {
    console.log("transaction");
    
    let transaction_amount = 0;
    if (transaction_type == "BUY") {
        transaction_amount = document.getElementById(`buyAmount${id}`).value;
    } else {
        transaction_amount = document.getElementById(`sellAmount${id}`).value;
    }
    let transaction_price = await fetch(`${apiUrl}/${id}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Latest Price:', data.nearest_price);
                    return data.nearest_price;
                })
                .catch(error => {
                    console.error('Error fetching latest price:', error);
                });

    const currentDateTime = new Date().toISOString();
    const transactionData = {
        transaction_type: transaction_type, 
        transaction_amount: transaction_amount,
        transaction_price: transaction_price, 
        transaction_datetime: currentDateTime,
    };
    try {
        const response = await fetch(`${apiUrl}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(transactionData)
        });
        const data = await response.json();
        if (data.message) {
            console.log(data.message)
        } else if (data.error) {
            window.alert(data.error);
        }
    } catch(error) {
        console.error('Error buying/selling stock:', error);
    }
}

async function chartNetWorth() {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        const dates = data.networth.map(entry => entry[1].slice(5,-13));
        const networth = data.networth.map(entry => entry[2]);
        let networthChartElement = document.getElementById('networth-chart');
        const networthChart = new Chart(networthChartElement, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Net Worth',
                    data: networth,
                    fill:true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)'
                }]
            },
            options: {
                responsive: true,
            }       
        });
    } catch(error) {
        console.error('Error fetching data:', error);
    }
}
async function displayNetWorth() {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();

        const networthContainer = document.getElementById('networth-container');
        networthContainer.innerHTML = '';

        const currentDate = new Date().toISOString().substr(0, 10);

        let currentNetWorth = 0;
        for (const entry of data.networth) {
            entryDate = new Date(entry[1]).toISOString().substr(0, 10);
            if (entryDate === currentDate) {
                currentNetWorth = entry[2];
                console.log(currentNetWorth);
                break;
            }
        }
        const networthText = document.createElement('p');
        networthText.textContent = `Current Net Worth: $${currentNetWorth.toFixed(2)}`;
        networthContainer.appendChild(networthText);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

