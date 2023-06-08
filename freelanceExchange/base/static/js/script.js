document.addEventListener('DOMContentLoaded', () => {
  const checkbox = document.getElementById('id_4-work_here');
  const endWorkDiv = document.querySelectorAll('.end_work');
  if (checkbox) {
    checkbox.addEventListener('change', () => {
      if (checkbox.checked) {
        endWorkDiv.forEach((div) => {
          div.style.display = 'none';
        });
      } else {
        endWorkDiv.forEach((div) => {
          div.style.display = 'inline-block';
        });
      }
    });
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

document.addEventListener('DOMContentLoaded', () => {
  const checkboxes = document.querySelectorAll('input[name="service"]');
  const chosenEl = document.querySelector('.chosen_el');

  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
      let selected = [];

      checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
          selected.push(checkbox.nextSibling.textContent.trim());
        }
      });

      chosenEl.innerHTML = selected.join(', ');
    });
  });
});
