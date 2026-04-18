// Quiz client-side behaviour — Yu Qiu / Alice
// Highlights the selected option card and guards submission.
$(function () {
    $('.option-card').on('click', function () {
        $('.option-card').removeClass('selected');
        $(this).addClass('selected');
        $(this).find('input[type="radio"]').prop('checked', true);
    });

    $('#quiz_form').on('submit', function (e) {
        if (!$('input[name="answer"]:checked').length) {
            e.preventDefault();
            alert('Please select an option before submitting.');
        }
    });
});
