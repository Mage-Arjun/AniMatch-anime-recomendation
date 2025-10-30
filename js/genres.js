// Add interactivity to genre cards
document.querySelectorAll('.genre-card').forEach(card => {
    card.addEventListener('click', function() {
        const genre = this.querySelector('h3').textContent;
        alert(`You selected ${genre}! This would show anime recommendations for this genre.`);
    });
})
fetch('navbar.html')
  .then(response => response.text())
  .then(data => {
    document.getElementById('navbar-container').innerHTML = data;
  });