// document.getElementById("demo").innerHTML = "value";
API_BASE_URL = "http://127.0.0.1:7000";
log = console.log

function update() {
    var e = document.getElementById("base_currency_selector");
    var baseCurr = e.options[e.selectedIndex].text;
    e = document.getElementById("compare_currency_selector");
    var compareCurr = e.options[e.selectedIndex].text;

    document.getElementById("stat_curr_1").text = baseCurr;
    document.getElementById("stat_curr_2").text = compareCurr;
    document.getElementById("result_box").value = ''

    var statsUrl = `${API_BASE_URL}/stats/${baseCurr}/${compareCurr}?start_date=${document.getElementById("start_date_input").value}`
    fetch(statsUrl, 
        {headers: {
            "Access-Control-Allow-Origin": "*",
        }})
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
              }
              return response.json();
        })
        .then((data) => updateStats(data))
        .catch((error) => console.error("Fetch error:", error));

    var chartUrl = `${API_BASE_URL}/chart/${baseCurr}/${compareCurr}?start_date=${document.getElementById("start_date_input").value}`
    fetch(chartUrl, 
        {headers: {
            "Access-Control-Allow-Origin": "*",
        }})
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
              }
              return response.json();
        })
        .then((data) => {
            log(data);
            document.getElementById("chart_img").src = data["chart_url"];
        })
        .catch((error) => console.error("Fetch error:", error));
    
}

function convert() {
    var e = document.getElementById("base_currency_selector");
    var baseCurr = e.options[e.selectedIndex].text;
    e = document.getElementById("compare_currency_selector");
    var compareCurr = e.options[e.selectedIndex].text;
    fetch(`${API_BASE_URL}/convert`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({
            "amount": parseFloat(document.getElementById("amount_input").value),
            "curr_source": baseCurr,
            "curr_result": compareCurr
        }),
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
              }
              return response.json();
        })
        .then((result) => {
            document.getElementById("result_box").value = parseFloat(result["converted_amount"]).toFixed(2);
            }
        )
        .catch((error) => console.error("Fetch error:", error));
}

function updateStats(stats) {
    document.getElementById("current_rate").textContent = stats["current_rate"];
    document.getElementById("min_rate").textContent = stats["min_rate"];
    document.getElementById("max_rate").textContent = stats["max_rate"];
    document.getElementById("mean_rate").textContent = stats["mean_rate"];

}