$('.msg-form').submit(function (event) {
  event.preventDefault();
  var form = $(this);
  var url = form.attr('action');
  var csrf_token = $('input[name="csrfmiddlewaretoken"]', form).val();
  var msg = $('input[name="msg"]', form);
  var button = $(event.target);
  var action = button.attr('name') + '=' + button.attr('value');

  if (!msg.val()) {
    return;
  }

  $.ajax({
    type: 'POST',
    url: url,
    headers: { 'X-CSRFToken': csrf_token },
    data: { msg: msg.val(), action: action },
    success: function (response) {
      var chatMsg = $('<div>').addClass('chat__msg');
      var msgRecipient = $('<div>').addClass('msg__recipient');
      var chatMsgRecipient = $('<div>').addClass('chat__msg-recipient');
      var date = new Date();
      var msgText = $('input[name="msg"]', form).val();

      chatMsgRecipient.append($('<p>').text(response.recipient));
      chatMsgRecipient.append($('<p>').text(msgText));
      msgRecipient.append(chatMsgRecipient);
      chatMsg.append(msgRecipient);

      $('.chat__block').append(chatMsg);
      msg.val('');
    },
    error: function (xhr, errmsg, err) {
      console.log(xhr.status + ': ' + xhr.responseText);
    },
  });
});
