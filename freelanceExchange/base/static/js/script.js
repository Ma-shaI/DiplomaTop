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
      if (selected.length > 0) {
        chosenEl.innerHTML = selected.join(', ');
      } else {
        chosenEl.innerHTML = 'Здесь будут отображены, выбранные вами услуги';
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const formFields = document.querySelectorAll('.exp');
  const submitButton = document.querySelector('#experience_btn');
  function checkFormFields() {
    var isValid = true;
    for (var i = 0; i < formFields.length; i++) {
      if (formFields[i].value === '') {
        isValid = false;
        break;
      }
    }
    return isValid;
  }
  for (var i = 0; i < formFields.length; i++) {
    formFields[i].addEventListener('change', function () {
      if (checkFormFields()) {
        submitButton.disabled = false;
      } else {
        submitButton.disabled = true;
      }
    });
  }
  submitButton.disabled = true;
});

document.addEventListener('DOMContentLoaded', function () {
  const items = this.document.querySelectorAll('.btn_service');
  items.forEach((item) => {
    item.addEventListener('mouseenter', function () {
      item.classList.add('active');
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  let likeBtns = document.querySelectorAll('.like-btn');

  likeBtns.forEach(function (likeBtn) {
    likeBtn.addEventListener('click', function () {
      likeBtn.classList.toggle('liked');
    });
  });
});
$(document).ready(function () {

   $('.my-form').submit(function (event) {

     event.preventDefault();
     var form = $(this);
     var url = form.attr('action');
     var csrf_token = $('input[name="csrfmiddlewaretoken"]', form).val();
     var task_id = $('input[name="task_id"]', form).val();
     var button = $(event.target);
     var action = button.attr('name') + '=' + button.attr('value');
     $.ajax({
      type: 'POST',
      url: url,
      headers: { 'X-CSRFToken': csrf_token },
       data: {'task_id': task_id, 'action': action},
       success: function (response) { console.log('OK');
      },
       error: function (xhr, errmsg, err) { console.log(xhr.status + ': ' + xhr.responseText); } }); }); });
