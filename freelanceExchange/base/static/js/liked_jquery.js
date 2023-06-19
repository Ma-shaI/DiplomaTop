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
      data: { task_id: task_id, action: action },
      success: function (response) {
        console.log('OK');
      },
      error: function (xhr, errmsg, err) {
        console.log(xhr.status + ': ' + xhr.responseText);
      },
    });
  });
});
