document.getElementById('menu-toggle').addEventListener('click', function() {
    var navMenu = document.getElementById('nav-menu');
    var menuToggle = document.getElementById('menu-toggle');
    var cancelToggle = document.getElementById('cancel-toggle');
  
    navMenu.classList.toggle('show');
    menuToggle.style.display = 'none';
    cancelToggle.style.display = 'block';
  });
  
  document.getElementById('cancel-toggle').addEventListener('click', function() {
    var navMenu = document.getElementById('nav-menu');
    var menuToggle = document.getElementById('menu-toggle');
    var cancelToggle = document.getElementById('cancel-toggle');
  
    navMenu.classList.remove('show');
    menuToggle.style.display = 'flex';
    cancelToggle.style.display = 'none';
  });



  document.addEventListener('DOMContentLoaded', function () {
    var swiper = new Swiper('.swiper-container', {
      slidesPerView: 3, // Show 3 slides at a time
      spaceBetween: 30, // Space between slides in px
      loop: true,
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      autoplay: {
        delay: 2500,
        disableOnInteraction: false,
      },
    });
  });

  document.getElementById('dropdown-icon').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent the click event from bubbling up
    var dropdownContent = document.getElementById('dropdown-content');
    dropdownContent.classList.toggle('show');
});

// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function(event) {
    var dropdownContent = document.getElementById('dropdown-content');
    if (!event.target.matches('.fa-caret-down')) {
        dropdownContent.classList.remove('show');
    }
});
