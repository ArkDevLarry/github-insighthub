async function fetchStats() {
    let username = document.getElementById("username").value;
    let response = await fetch(`/github/${username}`);
    let data = await response.json();

    if (data.error) {
        document.getElementById("summary").innerText = "User not found!";
        return;
    }

    document.getElementById("summary").innerText = data.summary;
    document.getElementById("suggestions").innerText = data.suggestions;

    let repos = data.info.repositories.nodes.map(repo => repo.name);
    let stars = data.info.repositories.nodes.map(repo => repo.stargazers.totalCount);
    let forks = data.info.repositories.nodes.map(repo => repo.forks.totalCount);

    let chartData = [
        {
            x: repos,
            y: stars,
            name: 'Stars',
            type: 'bar'
        },
        {
            x: repos,
            y: forks,
            name: 'Forks',
            type: 'bar'
        }
    ];

    Plotly.newPlot('chart', chartData);
}
