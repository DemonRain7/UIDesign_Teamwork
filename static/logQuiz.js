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

    // Keyboard shortcuts: A/B/C/D pick an option, Enter submits.
    // Skip when the user is typing in a real input/textarea.
    $(document).on('keydown', function (e) {
        var tag = (e.target && e.target.tagName) ? e.target.tagName.toUpperCase() : '';
        if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
        if (e.ctrlKey || e.metaKey || e.altKey) return;

        var key = (e.key || '').toUpperCase();
        if (['A', 'B', 'C', 'D'].indexOf(key) !== -1) {
            var $card = $('.option-card').filter(function () {
                return $(this).find('.option-key').text().trim().toUpperCase() === key;
            }).first();
            if (!$card.length) return;
            e.preventDefault();
            if (isMulti) {
                var $cb = $card.find('input[type="checkbox"]');
                $cb.prop('checked', !$cb.prop('checked')).trigger('change');
            } else {
                $('.option-card').removeClass('selected');
                $card.addClass('selected');
                $card.find('input[type="radio"]').prop('checked', true);
            }
        } else if (key === 'ENTER') {
            if ($('#quiz_form').length && $('input[name="answer"]:checked').length) {
                e.preventDefault();
                $('#quiz_form').trigger('submit');
            }
        }
    });
});
