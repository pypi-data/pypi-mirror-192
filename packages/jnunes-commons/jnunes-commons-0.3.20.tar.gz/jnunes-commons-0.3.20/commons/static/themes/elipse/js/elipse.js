/* check/nocheck checkbox */
$('tbody :checkbox').change(function () {
    $(this).closest('tr').toggleClass('selected-row', this.checked);
});

$('thead :checkbox').change(function () {
    $('tbody :checkbox').prop('checked', this.checked).trigger('change');
});

/*show/hide menu*/
$('#menu-button').click(function () {
    $('#menu').toggleClass('hide mobile');
});



// add asterisk to required fields
document.querySelectorAll('input[required]').forEach(e => {
    e ? e.parentElement.classList.add('required-input') : null;
})

// add phone mask
document.querySelector('.phone-mask')
    .addEventListener('keyup', e => e.target.value = formatPhoneNumber(e.target.value))

document.querySelector('.phone-mask')
    .addEventListener('change', e => e.target.value = formatPhoneNumber(e.target.value))

function formatPhoneNumber(value) {
    value = value.replace(/\D/g, "");
    value = value.replace(/^(\d{2})(\d)/g, "($1) $2");
    return value.replace(/(\d)(\d{4})$/, "$1-$2");
}