const form = document.getElementById('id_name');
const divs = document.querySelectorAll('.hidden');

form.addEventListener('change', function (event) {
  const selected = event.target.value;
  divs.forEach((div) => {
    if (div.id === selected) {
      div.style.display = 'block';
    } else {
      div.style.display = 'none';
    }
  });
});

document.addEventListener('DOMContentLoaded', function (event) {
  var items = document.querySelectorAll('.has-children');
  items.forEach((item) => {
    item.addEventListener('mouseenter', function (event) {
      var menu = document.getElementById(this.getAttribute('data-menu'));
      var menus = document.querySelectorAll('.submenu-container');
      menus.forEach((m) => {
        m.style.display = 'none';
      });
      menu.style.display = 'block';
    });
    item.addEventListener('mouseleave', function (event) {
      var menus = document.querySelectorAll('.submenu-container');
      menus.forEach((m) => {
        m.style.display = 'none';
      });
    });
  });
});
