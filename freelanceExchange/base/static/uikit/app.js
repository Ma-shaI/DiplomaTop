//function checkButton() {
//  if (document.getElementById('radio_freelancer').checked) {
//    return document.getElementById('radio_freelancer').checked;
//  } else if (document.getElementById('radio_client').checked) {
//    return document.getElementById('radio_client').checked;
//  } else {
//    console.log('ничего не выбрано');
//  }
//}
//let regBlock = document.querySelector('.register__block');
//let regBlockBtn = document.querySelector('.btn_reg');
//regBlockBtn.addEventListener('click', function () {
//  regBlock.style.display = 'none';
//});

function showHide(element_id) {
  //Если элемент с id-шником element_id существует
  if (document.getElementById(element_id)) {
    //Записываем ссылку на элемент в переменную obj
    let obj = document.getElementById(element_id);
    console.log(document.getElementById('radio_freelancer').checked);
    console.log(document.getElementById('radio_client').checked);
    //Если css-свойство display не block, то:
    if (obj.style.display != 'block') {
      obj.style.display = 'block'; //Показываем элемент
    } else obj.style.display = 'none'; //Скрываем элемент
  }
  //Если элемент с id-шником element_id не найден, то выводим сообщение
  else alert('Элемент с id: ' + element_id + ' не найден!');
}
