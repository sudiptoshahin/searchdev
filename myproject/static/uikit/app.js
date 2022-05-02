// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});


let alertWrapper = document.querySelector('.alert');
let alertClose = document.querySelector('.alert__close');

function alertDisplay() {
    console.log('Alert wrapper clicked!');
    alertWrapper.style.display = 'none';
}

if (alertWrapper) {
    alertClose.addEventListener('click', alertDisplay, false);
}