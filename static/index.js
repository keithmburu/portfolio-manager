const apiUrl = 'http://localhost:5000/portfolio';
const portfolioBody = document.getElementById('portfolioBody');
const portfolioInfoElement = document.getElementById('portfolio-info');
const networthChartElement = document.getElementById('networth-chart'); // Add an element to hold the chart

document.addEventListener('DOMContentLoaded', () => {getAssets(); chartNetWorth();});

async function getAssets() {
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
        ['Asset Name', 'Asset Type', 'Amount Holding', 'Cost', 'Profit', 'Action'].forEach(headerText => {
            const headerCell = document.createElement('th');
            headerCell.textContent = headerText;
            headerRow.appendChild(headerCell);
        });
        table.appendChild(headerRow);

        data.portfolio.forEach(asset => {
            // Create table row
            const row = document.createElement('tr');

            // Asset Name
            const assetNameCell = document.createElement('td');
            assetNameCell.textContent = asset[3];
            row.appendChild(assetNameCell);

            // Asset type
            const assetTypeCell = document.createElement('td');
            assetTypeCell.textContent = asset[1];
            row.appendChild(assetTypeCell);

            // Amount Holding
            const amountHoldingCell = document.createElement('td');
            amountHoldingCell.textContent = asset[4];
            row.appendChild(amountHoldingCell);

            // Cost
            const costCell = document.createElement('td');
            costCell.textContent = `$${asset[9]}`;
            row.appendChild(costCell);

            // Profit
            const profitCell = document.createElement('td');
            profitCell.textContent = `$${data.profit[asset[3]]}`;
            row.appendChild(profitCell);

            // Action
            const actionCell = document.createElement('td');
            const buyInput = document.createElement('input');
            buyInput.type = 'text';
            buyInput.id = `buyAmount${asset[0]}`;
            buyInput.value = 0;
            const buyButton = document.createElement('button');
            buyButton.textContent = 'Buy';
            buyButton.onclick = () => transaction(asset[0], 'BUY',asset);
            const sellInput = document.createElement('input');
            sellInput.type = 'text';
            sellInput.id = `sellAmount${asset[0]}`;
            sellInput.value = 0;
            const sellButton = document.createElement('button');
            sellButton.textContent = 'Sell';
            sellButton.onclick = () => transaction(asset[0], 'SELL',asset);
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

/* 
To be embedded in html:
<div id="assets">
    <button onclick="toggleFormVisibility()">Add asset</button>
</div>
<form id="newAssetForm" style="visibility:hidden" onsubmit="newAsset()" >
    <p>Select Asset Type</p>
    <select id="assetType">
        <option value="Stock" selected>Stock</option>
        <option value="Bond">Bond</option>
        <option value="Cash">Cash</option>
    </select>
    <p>Enter Asset Ticker</p><input type="text" id="assetTicker">
    <p>Enter Asset Name</p><input type="text" id="assetName">
    <p>Enter Amount</p><input type="text" id="amountHolding">
    <p>Enter Maturity Date</p>
    <input type="datetime-local" id="matureDateTime">
    <p>Select Currency</p>
    <select id="currency">
        <option value="USD" selected>USD</option>
        <option value="CAD">CAD</option>
    </select>
    <br><br>
    <button type="submit">Submit</button>
</form>
*/

async function newAsset() {
    toggleFormVisibility();
    const assetData = {
        asset_type: document.getElementById("assetType").value, 
        asset_ticker: document.getElementById("assetTicker").value,                         
        asset_name: document.getElementById("assetName").value, 
        amount_holding: document.getElementById("amountHolding").value,
        buy_datetime: new Date().toISOString(),
        mature_datetime: document.getElementById("matureDateTime").value, 
        currency: document.getElementById("currency").value
    };
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(assetData)
        });
        const data = await response.json();
        if (data.message) {
            console.log(data.message);
        } else if (data.error) {
            window.alert(data.error);
        }
    } catch(error) {
        console.error('Error creating asset:', error);
    }
}

function toggleFormVisibility() {
    const form = document.getElementById("newAssetForm");
    if (form.style.visibility == "visible") {
        form.style.visibility = "hidden";
    } else {
        document.getElementById("matureDateTime").value = new Date().toISOString();
        form.style.visibility = "visible";
    }
}

async function transaction(id, transaction_type, assetData) {
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
            getAssets();
        } else if (data.error) {
            window.alert(data.error);
        }
    } catch(error) {
        console.error('Error buying/selling asset:', error);
    }
}

async function chartNetWorth() {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        console.log(data.networth[0]);
        const dates = data.networth.map(entry => entry[1].slice(5,-13));
        const networth = data.networth.map(entry => entry[2]);
        console.log(dates, networth);
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