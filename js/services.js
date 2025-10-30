    // Anime Recommendation Function (used in the services section)
    function getRecommendation() {
        const animeInput = document.getElementById('animeInput').value;
        if (animeInput.trim() === '') {
            alert('Please enter an anime name!');
            return;
        }
        
        // Simulate recommendation process
        alert(`🎯 Analyzing "${animeInput}"...\n\n✨ Our AI is processing the genre, themes, and characteristics of this anime to find perfect matches for you!\n\n🎉 Your personalized recommendations will be generated based on:\n• Genre similarities\n• Theme analysis\n• Community ratings\n• Viewing patterns\n\nThank you for using AniMatch's recommendation service!`);
        
        // Here you would typically make an API call to your backend
        // This is currently a placeholder
    }
fetch('navbar.html')
.then(response => response.text())
.then(data => {
document.getElementById('navbar-container').innerHTML = data;
});