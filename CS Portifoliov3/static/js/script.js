const navLinks = document.querySelectorAll(".nav-link");
const sections = document.querySelectorAll("section");

window.addEventListener("scroll", function () {
  const scrollPosition = document.documentElement.scrollTop;

  sections.forEach(function (section) {
    if (section.offsetTop <= scrollPosition + 60 && section.offsetTop + section.offsetHeight > scrollPosition + 60) {
      navLinks.forEach(function (link) {
        link.classList.remove("active");
        if (section.getAttribute("id") === link.getAttribute("href").substring(1)) {
          link.classList.add("active");
        }
      });
    }
  });
});

navLinks.forEach(function (link) {
  link.addEventListener("click", function (event) {
    event.preventDefault();
    const targetSection = document.querySelector(link.getAttribute("href"));
    targetSection.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });
});

new TypeIt('.typeit', {
  cursor: true,
  cursorSpeed: 1000,
  lifeLike: true,
  breakLines: false,
  loop: false,
  startDelay: 500,
  nextStringDelay: 500
}).go();

const circle = document.querySelector('.circle');
      let x = 0;
      let y = 0;

      function updatePosition(event) {
        x = event.clientX;
        y = event.clientY;
        circle.style.left = `${x - 15}px`;
        circle.style.top = `${y - 15}px`;
      }

document.addEventListener('mousemove', updatePosition);
      document.addEventListener('click', event => {
        if (event.target.tagName === 'A' || event.target.tagName === 'BUTTON') {
          circle.classList.add('fill');
        } else {
          circle.classList.remove('fill');
        }
      });

const projectsButton = document.getElementById("projects-button");

projectsButton.addEventListener("click", function() {
  window.location.href = "/projects";
});
