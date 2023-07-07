document
  .getElementById('lang-form')
  .addEventListener('submit', function (event) {
    event.preventDefault();
    const form = event.target;

    const data = new FormData(form);

    data.append('return_url', window.location.pathname);

    fetch(form.action, {
      method: form.method,
      body: data,
      credentials: 'same-origin',
    })
      .then(function (response) {
        if (response.ok) {
          const modal = document.getElementById('myModal');
          const modalDialog = modal.getElementsByClassName('modal-dialog');
          modalDialog[0].classList.remove('modal-dialog-scrollable');
          modal.style.display = 'none';
          modal.removeAttribute('aria-modal');
          modal.setAttribute('aria-hidden', 'true');
          document.body.classList.remove('modal-open');
          document.body.removeAttribute('style');
          document.getElementsByClassName('modal-backdrop')[0].remove();
          window.location.reload();
        } else {
          console.error('Ошибка при отправке формы', response);
        }
      })
      .catch(function (error) {
        console.error(error);
      });
  });
