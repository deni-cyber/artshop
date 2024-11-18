function toggleMenu() {
    const menu = document.querySelector('.collapsible');
    menu.classList.toggle('show');
}

function closeMenu() {
    const menu =document.querySelector('.collapsible');
    menu.classList.remove('show');
}

document.addEventListener('click', function (event) {
    const menu = document.querySelector('.navlistbox');
    const menuButton = document.querySelector('.menu-button');

    if (!menu.contains(event.target) && event.target !== menuButton) {
        menu.classList.remove('show'); // Close the menu if clicked outside
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('.navlistbox a');
    const currentUrl = window.location.href;

    navLinks.forEach(link => {
        if (link.href === currentUrl) {
            link.classList.add('active');
        }
    });
});