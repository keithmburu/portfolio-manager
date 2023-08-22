/* 
To be embedded in html:
<div id="assets">
    <button onclick="toggleFormVisibility(0)">Add asset</button>
</div>
<form id="newAssetForm" style="visibility:hidden" onSubmit=newAsset()>
    <select id="assetType">
        <option value="Asset Type" selected>Asset Type</option>
        <option value="Stock">Stock</option>
        <option value="Bond">Bond</option>
        <option value="Cash">Cash</option>
    </select>
    <input type="text" id="assetTicker">Asset Ticker</input>
    <input type="text" id="assetName">Asset Name</input>
    <input type="datetime-local" id="matureDateTime">Maturity Date</input>
    <select id="currency">
        <option value="Currency" selected>Currency</option>
        <option value="USD">USD</option>
        <option value="CAD">CAD</option>
    </select>
    <input type="submit">Submit</input>
</form>

<script>
    document.getElementById("matureDateTime").value = Date();
</script>
*/

async function newAsset() {
    const assetData = {
        asset_type: document.getElementById("assetType").value, 
        asset_ticker: document.getElementById("assetTicker").value,                         
        asset_name: document.getElementById("assetName").value, 
        amount_holding: document.getElementById("amountHolding").value,
        buy_datetime: Date(),
        mature_datetime: document.getElementById("matureDateTime").value, 
        currency: document.getElementById("currency").value
    };
    const response = await fetch('http://localhost:5000', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(assetData)
    });
    const data = await response.json();
    if (data.message) {
        window.alert(data.message);
        const assetInfoDiv = document.createElement('div'); 
        const assetUpdateDiv = document.createElement('div'); 
        assetInfoDiv.id = `assetInfo${id}`;
        assetUpdateDiv.id = `assetUpdate${id}`; 
        assetInfoDiv.innerHTML = `
            <p><strong> ${assetData.asset_name} ${assetData.asset_ticker? 
            assetData.asset_ticker: ""}</strong></p>
            <p>${assetData.asset_type != "Stock"? assetData.currency : ""} 
            ${assetData.amount_holding} ${assetData.asset_type == "Stock"? "shares" : ""}</p>
        `
        assetUpdateDiv.innerhtml = `
            <div>
                <button onclick="transaction(${id}, 'BUY')">Buy</button>
                <input type="text" id="buyAmount${id}" value=0>Amount</input>
            </div>
            <div>
                <button onclick="transaction(${id}, 'SELL')">Sell</button>
                <input type="text" id="sellAmount${id}" value=0>Amount</input>
            </div>
        `; 
        document.getElementById(`assetType${id}`).value = assetData.asset_type
        const assets = document.getElementById('assets')
        assets.appendChild(assetInfoDiv);
        assets.appendChild(assetUpdateDiv);
    } else if (data.error) {
        window.alert(data.error);
    }
}

function toggleFormVisibility(id) {
    const form = document.getElementById(`assetForm${id}`)
    if (form.style.visibility == "visible") {
        form.style.visibility = "hidden";
    } else {
        form.style.visibility = "visible";
    }
}

async function transaction(id, transaction_type) {
    let transaction_amount = 0;
    if (transaction_type == "BUY") {
        transaction_amount = document.getElementById(`buyAmount${id}`).value;
    } else {
        transaction_amount = document.getElementById(`sellAmount${id}`).value;
    }
    const transactionData = {
        transaction_type: transaction_type, 
        transaction_amount: transaction_amount,
        transaction_price: transaction_amount, // need to get price from API
        transaction_datetime: Date(),
    };
    const response = await fetch(`http://localhost:5000/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(transactionData)
    });
    const data = await response.json();
    if (data.message) {
        window.alert(data.message)
        const assetInfoDiv = document.getElementById(`assetInfo${id}`); 
        assetInfoDiv.innerHTML = `
            <p><strong> ${assetData.asset_name} ${assetData.asset_ticker? 
            assetData.asset_ticker: ""}</strong></p>
            <p>${assetData.asset_type != "Stock"? assetData.currency : ""} 
            ${assetData.amount_holding} ${assetData.asset_type == "Stock"? "shares" : ""}</p>
        `
    } else if (data.error) {
        window.alert(data.error);
    }
}