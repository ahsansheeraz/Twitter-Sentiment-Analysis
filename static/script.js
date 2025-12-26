// Typing effect for the headline
const text = "Welcome to X(Twitter) Sentiment Analyzer!";
const typingSpeed = 100; // Adjust speed for typing
let index = 0;

function typeHeadline() {
    const headline = document.getElementById('headline');

    // Condition to replace 'Twitter' with 'X' after typing 'Welcome to Twitter'
    if (text.substring(0, index) === "Welcome to Twitter") {
        headline.innerHTML = "Welcome to X";
    } else {
        headline.innerHTML = text.substring(0, index); 
    }

    if (index < text.length) {
        index++;
        setTimeout(typeHeadline, typingSpeed);
    } else {
        // Show the paragraph with fade-in effect once typing is complete
        const paragraph = document.getElementById('intro-text');
        paragraph.classList.remove('hidden');
        paragraph.classList.add('show');
    }
}

// Start the typing effect when the page loads
window.onload = function() {
    typeHeadline();
};


async function analyzeText() {
    const analyzeButton = document.querySelector('#textAnalysis button');
    analyzeButton.classList.add('loading'); // Add loading effect to button

    const text = document.getElementById('textInput').value;

    if (text.trim() === "") {
        // If the input is empty, clear the result and hide the border
        textResult.textContent = ""; 
        textResult.style.border = "none"; 
        textResult.style.display = "none"; // Hide the result box
        analyzeButton.classList.remove('loading'); // Remove loading effect
        return;
    }

    const response = await fetch('/analyze_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `text=${encodeURIComponent(text)}`,
    });
    const result = await response.json();
    analyzeButton.classList.remove('loading'); // Remove loading effect when done
      // Display the result with a dynamic border
    textResult.innerHTML = `Sentiment: <span class="${getSentimentClass(result.sentiment)}">${result.sentiment}</span>`;
    textResult.style.border = "1px solid #ccc"; // Add border
    textResult.style.display = "block"; // Make the result visible
}
// user tweets by username
async function analyzeAccount() {
    const analyzeButton = document.querySelector('#accountAnalysis button');
    analyzeButton.classList.add('loading');

    const accountId = document.getElementById('accountInput').value;
    const count = document.getElementById('accountCount').value;

    const response = await fetch('/account_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `account_id=${encodeURIComponent(accountId)}&count=${count}`,
    });

    analyzeButton.classList.remove('loading');

    if (response.ok) {
        const result = await response.json();
        const resultContainer = document.getElementById('accountResult');

        // Clear the previous results
        resultContainer.innerHTML = '';

        // Create table structure for tweets and sentiments
        const table = document.createElement('table');
        table.style.width = '100%';
        table.style.borderCollapse = 'collapse';

        result.forEach(tweet => {
            const row = document.createElement('tr');
            row.style.borderBottom = '1px solid #ccc';

            // Tweet Text Column
            const textCell = document.createElement('td');
            textCell.style.padding = '10px';
            textCell.style.width = '70%';
            textCell.textContent = tweet.text;

            // Sentiment Column
            const sentimentCell = document.createElement('td');
            sentimentCell.style.padding = '10px';
            sentimentCell.style.width = '30%';
            sentimentCell.style.textAlign = 'center';
            sentimentCell.textContent = tweet.sentiment;

            // Add cells to the row
            row.appendChild(textCell);
            row.appendChild(sentimentCell);

            // Add the row to the table
            table.appendChild(row);
        });

        // Append the table to the result container
        resultContainer.appendChild(table);
    } else {
        document.getElementById('accountResult').innerHTML = `<p style="color:red;">Failed to analyze account. Please try again.</p>`;
    }
}

/*async function analyzeHashtag() {
    const analyzeButton = document.querySelector('#hashtagAnalysis button');
    analyzeButton.classList.add('loading'); // Add loading effect to button

    const hashtag = document.getElementById('hashtag').value;
    const count = document.getElementById('hashtagCount').value;
    const response = await fetch('/hashtag_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `hashtag=${encodeURIComponent(hashtag)}&count=${count}`,
    });

    const result = await response.json();
    analyzeButton.classList.remove('loading'); // Remove loading effect when done
    if (result.error) {
        document.getElementById('hashtagResult').innerHTML = `<p>Error: ${result.error}</p>`;
    } else {
        document.getElementById('hashtagResult').innerHTML = result.map(tweet => 
            `<p>${tweet.text} - Sentiment: ${tweet.sentiment}</p>`).join('');
    }
}*/
async function analyzeHashtag() {
    const analyzeButton = document.querySelector('#hashtagAnalysis button');
    analyzeButton.classList.add('loading');

    const hashtag = document.getElementById('hashtag').value;
    const count = document.getElementById('hashtagCount').value;
    const hashtagResult = document.getElementById('hashtagResult');

    // Hide results and visualizations initially
    hashtagResult.style.border = 'none';
    hashtagResult.style.display = 'none';
    document.querySelector('.charts-section').style.display = 'none';
    document.querySelector('.wordcloud-section').style.display = 'none';

    const response = await fetch('/hashtag_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `hashtag=${encodeURIComponent(hashtag)}&count=${count}`,
    });

    const result = await response.json();
    analyzeButton.classList.remove('loading');

    if (result.error) {
        hashtagResult.innerHTML = `<p>Error: ${result.error}</p>`;
        hashtagResult.style.border = '1px solid #ccc';
        hashtagResult.style.display = 'block';
    } else {
        hashtagResult.innerHTML = result.map(tweet =>
            `<p>${tweet.text} - Sentiment: <span class="${getSentimentClass(tweet.sentiment)}">${tweet.sentiment}</span></p>`
        ).join('');
        hashtagResult.style.border = '1px solid #ccc';
        hashtagResult.style.display = 'block';

        // Update chart and word cloud images
        document.getElementById('hashtagPieChart').src = 'static/hashtag_pie_chart.png?' + new Date().getTime();
        document.getElementById('hashtagBarChart').src = 'static/hashtag_bar_chart.png?' + new Date().getTime();
        document.getElementById('hashtagWordCloud').src = 'static/hashtag_wordcloud.png?' + new Date().getTime();

        // Show charts and word cloud
        document.querySelector('.charts-section').style.display = 'block';
        document.querySelector('.wordcloud-section').style.display = 'block';
    }
}

// Function to determine sentiment class
function getSentimentClass(sentiment) {
    switch (sentiment.toLowerCase()) {
        case 'negative':
            return 'negative-sentiment';
        case 'positive':
            return 'positive-sentiment';
        case 'neutral':
            return 'neutral-sentiment';
        default:
            return '';
    }
}

/*async function fetchTrends() {
    const count = document.getElementById('trendsCount').value;
    const response = await fetch('/trends_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `count=${count}`,
    });
    const trends = await response.json();
    const trendsResult = trends.map(trend => `<h3>${trend.trend}</h3>` + trend.tweets.map(tweet => `<p>${tweet.text} - Sentiment: ${tweet.sentiment}</p>`).join('')).join('');
    document.getElementById('trendsResult').innerHTML = trendsResult;
}*/
