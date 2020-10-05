var btn = document.getElementsByClassName('form__field-item-delete old-ingredient-delete')

for (var i = 0; i < btn.length; i++) {
  btn[i].addEventListener('click', function(e) {
    e.currentTarget.parentNode.remove();
  }, false);
}
