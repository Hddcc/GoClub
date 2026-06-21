(function () {
  var menu = document.querySelector("aside .book-menu-content nav")
    || document.querySelector("aside .book-menu-content");

  if (!menu) return;

  addEventListener("beforeunload", function () {
    localStorage.setItem("menu.scrollTop", menu.scrollTop);
  });

  menu.scrollTop = localStorage.getItem("menu.scrollTop");
})();
