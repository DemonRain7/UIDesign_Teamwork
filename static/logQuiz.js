// Quiz client-side behaviour — Yu Qiu / Alice
$(function () {
    var isMulti = $('.option-card.multi').length > 0;

    if (isMulti) {
        // Checkbox: toggle individual cards
        $('.option-card.multi').on('click', function () {
            var cb = $(this).find('input[type="checkbox"]');
            cb.prop('checked', !cb.prop('checked'));
            $(this).toggleClass('selected', cb.prop('checked'));
        });
        // Prevent double-toggle when clicking directly on the checkbox
        $('.option-card.multi input[type="checkbox"]').on('click', function (e) {
            e.stopPropagation();
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
