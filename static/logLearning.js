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

    if (LEARN_ONLY) {
        if (LESSON_ID >= TOTAL_LESSONS) {
            nextBtn.text('Back to Home →')
                   .click(function() { window.location.href = '/'; });
        } else {
            nextBtn.click(function() { window.location.href = `/learn/${LESSON_ID + 1}`; });
        }
    } else if (LESSON_ID >= TOTAL_LESSONS) {
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
    const skipKeys = new Set(['Image', 'Caption']);
    let headers = Object.keys(tableData[0]).filter(h => !skipKeys.has(h));
    let headerRow = headers.map(h => `<th>${h}</th>`).join("") + '<th></th>';
    let bodyRows = tableData.map((row, i) => {
        const hasImage = row['Image'] && row['Image'].trim();
        const viewCell = hasImage
            ? `<td><button class="view_pic_btn" data-index="${i}">View Picture</button></td>`
            : '<td><span class="view_pic_none">—</span></td>';
        return `<tr>${headers.map(h => {
            const cls = h === 'Chinese' ? ' class="learn_chinese_cell"' : '';
            return `<td${cls}>${row[h] ?? ''}</td>`;
        }).join("")}${viewCell}</tr>`;
    }).join("");
    $("#learing_table_container").html(
        `<table class="learn_table">
            <thead><tr>${headerRow}</tr></thead>
            <tbody>${bodyRows}</tbody>
        </table>`
    );

    let currentIndex = 0;

    // Single image card
    function showCard(index) {
        currentIndex = Math.max(0, Math.min(index, tableData.length - 1));
        const row = tableData[currentIndex];
        const img = row['Image'] || '';
        const cap = row['Caption'] || '';
        if (img) {
            $('#learning_image_container').html(
                `<div class="learn_image_card">
                    <img src="${img}" alt="${cap}">
                    <div class="learn_image_caption">${cap}</div>
                </div>`
            );
        } else {
            $('#learning_image_container').html(
                `<div class="learn_image_empty">No image available</div>`
            );
        }
        $('.view_pic_btn').removeClass('active');
        $(`.view_pic_btn[data-index="${currentIndex}"]`).addClass('active');
        // Highlight selected row
        $('tbody tr').removeClass('learn_row_selected');
        $('tbody tr').eq(currentIndex).addClass('learn_row_selected');
    }

    showCard(0);

    $(document).on('click', '.view_pic_btn', function() {
        showCard(parseInt($(this).data('index')));
    });

    // Arrow key navigation between rows
    $(document).on('keydown', function(e) {
        var tag = (e.target && e.target.tagName) ? e.target.tagName.toUpperCase() : '';
        if (tag === 'INPUT' || tag === 'TEXTAREA') return;
        if (e.key === 'ArrowDown') { e.preventDefault(); showCard(currentIndex + 1); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); showCard(currentIndex - 1); }
    });
});
