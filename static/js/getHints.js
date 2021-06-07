const base_url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`

const hintsPlaces = { "1": document.getElementById("first-hint"), "2": document.getElementById("second-hint") }

const hintsButtons = { "1": document.getElementById("first-btn"), "2": document.getElementById("second-btn") }

for (let i = 1; i <= Object.keys(hintsButtons).length; i++) {
    // console.log(i.toString())
    // console.log(hintsButtons[i.toString()])
    hintsButtons[i.toString()].addEventListener('click', () => getHint(i, hintsPlaces[i.toString()]))
}
// document.getElementById("first-btn").addEventListener('click', () => getHint(1, document.getElementById("first-hint")))
// document.getElementById("second-btn").addEventListener('click', () => getHint(2, document.getElementById("second-hint")))

async function getHint(number, hintObj) {
    const jsonData = await getData(`${base_url}/hints/${number}`)
    // const paragraph = document.createElement("div");
    if (jsonData["status"] === "OK") {
        hintObj.innerHTML = jsonData["content"];
        // hintObj.appendChild(paragraph);
    }
    else if (jsonData["status"] === "BAD" && "reason" in jsonData) {
        const errPar = document.createElement('p')
        errPar.classList = "is-size-3 has-text-danger-dark"
        errPar.innerText = jsonData["reason"]
        document.getElementById('hints-errors').appendChild(errPar)
    }
    else {
        alert("An error occurred 😥")
    }
}

async function getData(url) {
    return fetch(url).then(function (response) {
        if (response.ok) return response.json()
        throw new Error("Invalid data from server!")
    }, function (reason) { alert(reason) });
}