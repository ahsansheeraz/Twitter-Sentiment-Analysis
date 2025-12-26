function fetchTrends() {
    const analyzeButton = document.querySelector('#trendsAnalysis button');
    analyzeButton.classList.add('loading');  // Add loading class to show loading state

    var country = document.getElementById('country').value;
    var trendsCount = document.getElementById('trendsCount').value;
    const trendsResult = document.getElementById('trendsResult');

    // Initially hide trendsResult and remove the border
    trendsResult.style.display = 'none';
    trendsResult.style.border = 'none';

    // Perform AJAX request to the backend (Flask) to fetch trends
    fetch('/analyze_trends', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            country: country,
            limit: trendsCount,
        }),
    })
    .then((response) => response.json())  // Parse the response as JSON
    .then((data) => {
        analyzeButton.classList.remove('loading');  // Remove loading state after response

        if (data.error) {
            trendsResult.innerHTML = data.error;
            trendsResult.style.display = 'block';  // Show the result div
            trendsResult.style.border = '1px solid #ccc';  // Add the border
            return;
        }

        // Display trends
        let trendsHTML = "<h3>Top Trends:</h3>";
        data.trends.forEach((trend) => {
            trendsHTML += `<div class="trend">
                               <h4>${trend.name}</h4>
                               <p>${trend.description ? trend.description : "No Description"}</p>
                           </div>`;
        });
        trendsResult.innerHTML = trendsHTML;

        // Display the bar and line charts
        document.getElementById('trendsBarChart').src = `data:image/png;base64,${data.bar_img}`;
        document.getElementById('trendsLineChart').src = `data:image/png;base64,${data.line_img}`;

        // Show the images
        document.getElementById('trendsBarChart').style.display = 'block';
        document.getElementById('trendsLineChart').style.display = 'block';

        // Show the result div and add the border
        trendsResult.style.display = 'block';
        trendsResult.style.border = '1px solid #ccc';
    })
    .catch((error) => {
        analyzeButton.classList.remove('loading');  // Remove loading state if there's an error
        trendsResult.innerHTML = "Error fetching trends.";
        trendsResult.style.display = 'block';  // Show the result div
        trendsResult.style.border = '1px solid #ccc';  // Add the border
        console.error("Error fetching trends:", error);  // Log the error for debugging
    });
}
