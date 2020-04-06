import {criteria} from "./criteria-list.js";
import {render} from './renderView.js';
import {GOOD_TOTAL_POINTS} from "./criteria-list.js";


window.onload = function () {
  document.querySelector('.start').addEventListener("click", function (e) {
    e.stopPropagation();
    if (e.target.parentElement.tagName === "SECTION") e.target.parentElement.style.display = "none";
  });

  const header = document.querySelector('header');
  const offsetTop = header.offsetTop;

  window.onscroll = () => stickyHeader();

  function stickyHeader() {
    if (window.pageYOffset > offsetTop + GOOD_TOTAL_POINTS) {
      header.classList.add("sticky");
    } else {
      header.classList.remove("sticky");
    }
  }

  render(criteria);
};
