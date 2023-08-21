/* 
To be embedded in html:
<div id="assets">
    <button onclick="toggleFormVisibility(0)">Add asset</button>
</div>
<form id="assetForm0" style="visibility:hidden" onSubmit=newAsset()>
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
    if (data.message) {
        window.alert(data.message);
        const assetInfoDiv = document.createElement('div'); 
        const assetFormDiv = document.createElement('div'); 
        assetInfoDiv.id = `assetInfo${id}`; 
        assetFormDiv.id = `assetForm${id}`;
        assetInfoDiv.innerHTML = `
            <p><strong> ${assetData.asset_name} ${assetData.asset_ticker? assetData.asset_ticker: ""}</strong></p>
            <p>${assetData.asset_type != "Stock"? assetData.currency : ""} ${assetData.amount_holding} ${assetData.asset_type == "Stock"? "shares" : ""}</p>
            <button onclick="toggleFormVisibility(${id})">Update asset</button>
        `
        assetFormDiv.innerhtml = `
            <form id="assetForm${id}" style="visibility:hidden" onSubmit=updateAsset(${id})>
                <select id="assetType${id}">
                    <option value="Asset Type">Asset Type</option>
                    <option value="Stock">Stock</option>
                    <option value="Bond">Bond</option>
                    <option value="Cash">Cash</option>
                </select>
                <input type="text" id="assetTicker${id}">Asset Ticker</input>
                <input type="datetime-local" id="matureDateTime${id}">Maturity Date</input>
                <select id="currency${id}">
                    <option value="Currency" selected>Currency</option>
                    <option value="USD">USD</option>
                    <option value="CAD">CAD</option>
                </select>
                <input type="submit">Submit</input>
            </form>
        `; 
        document.getElementById(`assetType${id}`).value = assetData.asset_type
        const assets = document.getElementById('assets')
        assets.appendChild(assetInfoDiv);
        assets.appendChild(assetFormDiv);
    } else if (data.error) {
        window.alert(data.error);
    }
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
    if (data.message) {
        window.alert(data.message)
        const assetInfoDiv = document.getElementById(`assetInfo${id}`); 
        assetInfoDiv.innerHTML = `
            <p><strong> ${assetData.asset_name} ${assetData.asset_ticker? assetData.asset_ticker: ""}</strong></p>
            <p>${assetData.asset_type != "Stock"? assetData.currency : ""} ${assetData.amount_holding} ${assetData.asset_type == "Stock"? "shares" : ""}</p>
            <button onclick="toggleFormVisibility(${id})">Update asset</button>
        `
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