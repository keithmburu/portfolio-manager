/* 
Embed in html:
<form id="newAssetForm" onSubmit=newAsset()>
    <select id="assetType">
        <option value="Asset Type" selected>Asset Type</option>
        <option value="Stock">Stock</option>
        <option value="Bond">Bond</option>
        <option value="Cash">Cash</option>
    </select>
    <input type="text" id="assetTicker">Asset Ticker</input>
    <input type="datetime-local" id="matureDateTime">Maturity Date</input>
    <select id="currency">
        <option value="Currency" selected>Currency</option>
        <option value="USD">USD</option>
        <option value="CAD">CAD</option>
    </select>
    <input type="submit">Submit</input>
</form>

<form id="updateAssetForm1" onSubmit=updateAsset(0)>
    <select id="assetType1">
        <option value="Asset Type" selected>Asset Type</option>
        <option value="Stock">Stock</option>
        <option value="Bond">Bond</option>
        <option value="Cash">Cash</option>
    </select>
    <input type="text" id="assetTicker1">Asset Ticker</input>
    <input type="datetime-local" id="matureDateTime1">Maturity Date</input>
    <select id="currency1">
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
        asset_type: document.getElementById("assetType") , 
        asset_ticker: document.getElementById("assetTicker"),                         
        asset_name: document.getElementById("assetName"), 
        amount_holding: document.getElementById("amountHolding"),
        buy_datetime: Date(),
        mature_datetime: document.getElementById("matureDateTime"), 
        currency: document.getElementById("currency")
    };
    const response = await fetch('http://localhost:5000', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(assetData)
    });
    const data = await response.json();
    const assetDiv = document.createElement('div'); 
    assetDiv.id = `asset${id}`; 
    assetDiv.innerHTML = `
        <p><strong> ${assetData.asset_name} ${assetData.asset_ticker? assetData.asset_ticker: ""}</strong></p>
        <p>${assetData.amount_holding}</p>
    `; 
    document.getElementById('assetData').appendChild(assetDiv);
}

async function updateAsset(id) {
    const assetData = {
        asset_type: document.getElementById(`assetType${id}`) , 
        asset_ticker: document.getElementById(`assetTicker${id}`),                         
        asset_name: document.getElementById(`assetName${id}`), 
        amount_holding: document.getElementById(`amountHolding${id}`),
        buy_datetime: Date(),
        mature_datetime: document.getElementById(`matureDateTime${id}`),
        currency: document.getElementById(`currency${id}`)
    };
    const response = await fetch(`http://localhost:5000/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(assetData)
    });
    const data = await response.json();
    const assetDiv = document.getElementById(`asset${id}`); 
    assetDiv.innerHTML = `
        <p><strong> ${assetData.asset_name} ${assetData.asset_ticker? assetData.asset_ticker: ""}</strong></p>
        <p>${assetData.amount_holding}</p>
    `; 
}