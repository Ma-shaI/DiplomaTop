console.log('JavaScript code is loaded!');
document.addEventListener('DOMContentLoaded', () => {
  const checkbox = document.getElementById('id_4-work_here');

  // get a reference to the end_work div
  const endWorkDiv = document.querySelectorAll('.end_work');

  // hide the end_work div by default

  // add a change event listener to the checkbox
  if (checkbox) {
    checkbox.addEventListener('change', () => {
      if (checkbox.checked) {
        // if the checkbox is checked, hide the end_work div
        endWorkDiv.forEach((div) => {
          div.style.display = 'none';
        });
      } else {
        endWorkDiv.forEach((div) => {
          div.style.display = 'inline-block';
        });
      }
    });
  } else {
    console.log('hi');
  }
});
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('id_name');
  const divs = document.querySelectorAll('.hidden');
  if (form) {
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
  } else {
    console.error('Form element not found');
  }
});

document.addEventListener('DOMContentLoaded', function (event) {
  const items = document.querySelectorAll('.has-children');
  items.forEach((item) => {
    item.addEventListener('mouseenter', function (event) {
      const menu = document.getElementById(this.getAttribute('data-menu'));
      const menus = document.querySelectorAll('.submenu-container');
      menus.forEach((m) => {
        m.style.display = 'none';
      });
      menu.style.display = 'block';
    });
    item.addEventListener('mouseleave', function (event) {
      const menus = document.querySelectorAll('.submenu-container');
      menus.forEach((m) => {
        m.style.display = 'none';
      });
    });
  });
});
