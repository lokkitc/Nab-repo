'use strict';



/**
 * add event on element
 */

const addEventOnElem = function (elem, type, callback) {
  if (!elem) return;
  
  if (NodeList.prototype.isPrototypeOf(elem)) {
    elem.forEach(element => {
      element.addEventListener(type, callback);
    });
  } else {
    elem.addEventListener(type, callback);
  }
}



/**
 * navbar toggle
 */

const navTogglers = document.querySelectorAll("[data-nav-toggler]");
const navbar = document.querySelector("[data-navbar]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");
const overlay = document.querySelector("[data-overlay]");

const toggleNavbar = function () {
  navbar.classList.toggle("active");
  overlay.classList.toggle("active");
}

addEventOnElem(navTogglers, "click", toggleNavbar);

const closeNavbar = function () {
  navbar.classList.remove("active");
  overlay.classList.remove("active");
}

addEventOnElem(navbarLinks, "click", closeNavbar);



/**
 * header sticky & back top btn active
 */

const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

const headerActive = function () {
  if (window.scrollY > 150) {
    header.classList.add("active");
    backTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    backTopBtn.classList.remove("active");
  }
}

addEventOnElem(window, "scroll", headerActive);

let lastScrolledPos = 0;

const headerSticky = function () {
  if (lastScrolledPos >= window.scrollY) {
    header.classList.remove("header-hide");
  } else {
    header.classList.add("header-hide");
  }

  lastScrolledPos = window.scrollY;
}

addEventOnElem(window, "scroll", headerSticky);

function submitSearch() {
  const searchValue = document.querySelector('input[name="name"]').value;
  const categoryValue = document.querySelector('select[name="category"]').value;
  window.location.href = `{% url 'product:catalog' %}?name=${searchValue}&category=${categoryValue}`;
}

/**
 * scroll reveal effect
 */

const sections = document.querySelectorAll("[data-section]");

const scrollReveal = function () {
  for (let i = 0; i < sections.length; i++) {
    console.log('Section:', sections[i]);
    console.log('Position:', sections[i].getBoundingClientRect().top);
    console.log('Window height:', window.innerHeight / 2);
    
    if (sections[i].getBoundingClientRect().top < window.innerHeight / 2) {
      sections[i].classList.add("active");
      console.log('Added active class to:', sections[i]);
    }
  }
}

scrollReveal();

addEventOnElem(window, "scroll", scrollReveal);