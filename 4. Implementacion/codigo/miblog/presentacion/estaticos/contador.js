// Contador de caracteres restantes (rnf 4.1, RNF15).
// Es el único JavaScript de MiBlog (RNF31): no valida, no envía nada y no decide
// nada. La validación de verdad la hace el servidor (rnf 4.2).
//
// Cada <textarea data-limite="N" data-contador="id"> actualiza el elemento con ese
// id mostrando cuántos caracteres le quedan, y le agrega la clase contador--excedido
// cuando se pasó del límite. El límite viene escrito en la página por el servidor,
// así que el número no está repetido acá.
document.querySelectorAll("textarea[data-limite]").forEach(function (campo) {
  var contador = document.getElementById(campo.dataset.contador);
  if (contador === null) {
    return;
  }
  var limite = parseInt(campo.dataset.limite, 10);

  function actualizar() {
    // Array.from cuenta caracteres reales (un emoji cuenta 1), igual que len() en
    // Python. La propiedad .length de JavaScript cuenta un emoji como 2.
    var restantes = limite - Array.from(campo.value).length;
    contador.textContent = String(restantes);
    // Solo cambia el aspecto (la clase está en estilos.css). Que el mensaje se pase
    // no bloquea nada acá: el servidor es el que rechaza el texto (rnf 4.2).
    contador.classList.toggle("contador--excedido", restantes < 0);
  }

  campo.addEventListener("input", actualizar);
  actualizar();
});