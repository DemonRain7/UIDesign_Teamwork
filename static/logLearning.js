$(function() {
    let prevBtn = $("#prev_button");
    let nextBtn = $("#next_button");

    // Progress bar
    $("#learn_progress_label").text(`Lesson ${LESSON_ID} of ${TOTAL_LESSONS}`);
    $("#learn_progress_fill").css("width", `${(LESSON_ID / TOTAL_LESSONS) * 100}%`);

    // Navigation
    if (LESSON_ID <= 1) {
        prevBtn.prop('disabled', true);
    } else {
        prevBtn.click(function() { window.location.href = `/learn/${LESSON_ID - 1}`; });
    }

    if (LESSON_ID >= TOTAL_LESSONS) {
        nextBtn.addClass('learn_btn_quiz')
               .click(function() { window.location.href = '/quiz/3'; });
    } else {
        nextBtn.click(function() { window.location.href = '/quiz/2'; });
    }

    // Title + subtitle
    $("#learning_title_container").text(learningContents.title);
    $("#learning_beginning_container").text(learningContents.beginning);

    // Table
    let tableData = learningContents.table;
    let headers = Object.keys(tableData[0]);
    let headerRow = headers.map(h => `<th>${h}</th>`).join("");
    let bodyRows = tableData.map(row =>
        `<tr>${headers.map(h => {
            const cls = h === 'Chinese' ? ' class="learn_chinese_cell"' : '';
            return `<td${cls}>${row[h]}</td>`;
        }).join("")}</tr>`
    ).join("");
    $("#learing_table_container").html(
        `<table class="learn_table">
            <thead><tr>${headerRow}</tr></thead>
            <tbody>${bodyRows}</tbody>
        </table>`
    );

    // Image cards
    [0, 1, 2, 3].forEach(i => {
        $(`#learning_image_${i}_container`).html(
            `<div class="learn_image_card">
                <img src="${learningContents.images[i]}" alt="${learningContents.captions[i]}">
                <div class="learn_image_caption">${learningContents.captions[i]}</div>
            </div>`
        );
    });
});
