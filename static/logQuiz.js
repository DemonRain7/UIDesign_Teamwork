// Quiz client-side behaviour — Yu Qiu / Alice
$(function () {
    var isMulti = $('.option-card.multi').length > 0;

    if (isMulti) {
        // The card is a <label> wrapping a hidden checkbox, so the browser
        // toggles the checkbox automatically on label-click. We only need to
        // mirror that state into the .selected class for styling.
        $('.option-card.multi input[type="checkbox"]').on('change', function () {
            $(this).closest('.option-card').toggleClass('selected', $(this).prop('checked'));
        });
    } else {
        // Radio: single selection
        $('.option-card').on('click', function () {
            $('.option-card').removeClass('selected');
            $(this).addClass('selected');
            $(this).find('input[type="radio"]').prop('checked', true);
        });
    }

    $('#quiz_form').on('submit', function (e) {
        if (!$('input[name="answer"]:checked').length) {
            e.preventDefault();
            alert('Please select at least one option before submitting.');
        }
    });
});
