const apiUrl = 'http://localhost:5000/portfolio';
const portfolioBody = document.getElementById('portfolioBody');
const portfolioInfoElement = document.getElementById('portfolio-info');
const networthChartElement = document.getElementById('networth-chart'); // Add an element to hold the chart

document.addEventListener('DOMContentLoaded', () => getAssets());

async function getAssets() {
    // Fetch portfolio data from the backend
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const portfolioContainer = document.getElementById('portfolio-container');
            portfolioContainer.innerHTML = '';
            data.portfolio.forEach(asset => {
                const assetDiv = document.createElement('div');
                assetDiv.innerHTML = `
                    <h2>${asset[3]}</h2>
                    <p>Amount Holding: ${asset[4]}</p>
                    <p>Profit: $${data.profit[asset[3]]}</p>
                    <div>
                        <input type="text" id="buyAmount${asset[0]}" value=0>
                        <button onclick="transaction(${asset[0]}, 'BUY')">Buy</button>
                    </div>
                    <div>
                        <input type="text" id="sellAmount${asset[0]}" value=0>
                        <button onclick="transaction(${asset[0]}, 'SELL')">Sell</button>
                    </div>
                `;
                portfolioContainer.appendChild(assetDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
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
        console.log(data.message);
        if (data.message) {
            console.log(data.message);
        } else if (data.error) {
            console.log(data.error);
        }
    } catch(error) {
        console.error('Network error creating asset:', error);
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

async function transaction(id, transaction_type) {
    console.log("transaction");
    let transaction_amount = 0;
    if (transaction_type == "BUY") {
        transaction_amount = document.getElementById(`buyAmount${id}`).value;
    } else {
        transaction_amount = document.getElementById(`sellAmount${id}`).value;
    }
    fetch(`${apiUrl}/${id}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Latest Price:', data.nearest_price);
                    transaction_price = data.nearest_price;
                })
                .catch(error => {
                    console.error('Error fetching latest price:', error);
                });
    const transactionData = {
        transaction_type: transaction_type, 
        transaction_amount: transaction_amount,
        transaction_price: transaction_price, // need to get price from API
        transaction_datetime: new Date().toISOString(),
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
            console.log(data.error);
        }
        getAssets();
    } catch(error) {
        console.error('Network error buying/selling asset:', error);
    }
}