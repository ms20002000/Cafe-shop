document.addEventListener("DOMContentLoaded", function() {
    const navBar = document.querySelector('.inner');
    const itemsCount = navBar.querySelectorAll('li').length;
    navBar.style.gridTemplateColumns = `repeat(${itemsCount}, 1fr)`;
});
