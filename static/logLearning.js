/*
learningContents format example:

{
"title": "Lesson 1",
"beginning": "beginning words",
"table": [
{"Cooking Method": "Stir-fried", "Chinese": "爆炒", "Texture Outcome": "Savory, quick wok toss, lightly charred"},
{"Cooking Method": "Braised", "Chinese": "炖", "Texture Outcome": "Fall-apart tender, rich in liquid"}
],
"images": ["www.image.com/image0", "www.image.com/image1", "www.image.com/image2", "www.image.com/image3"]
}
*/

$( function() {
    let leaningTitleContainerElem = $("#learning_title_container");
    let learningBeginningContainerElem = $("#learning_beginning_container");
    let learningTableContainerElem = $("#learing_table_container");
    let learningImage0ContainerElem = $("#learning_image_0_container");
    let learningImage1ContainerElem = $("#learning_image_1_container");
    let learningImage2ContainerElem = $("#learning_image_2_container");
    let learningImage3ContainerElem = $("#learning_image_3_container");

    if (!learningContents) {
        leaningTitleContainerElem.html("<h1>No contents for this lesson!</h1>");
    } else {
        leaningTitleContainerElem.html(`<h1>${learningContents.title}</h1>`);
        learningBeginningContainerElem.html(`<p>${learningContents.beginning}</p>`);

        const tableData = JSON.parse(learningContents.table);
        const headers = Object.keys(tableData[0]);
        const headerRow = headers.map(h => `<th scope="col">${h}</th>`).join("");
        const bodyRows = tableData.map(row =>
            `<tr>${headers.map(h => `<td>${row[h]}</td>`).join("")}</tr>`
        ).join("");
        learningTable = `<table class="table"><thead><tr>${headerRow}</tr></thead><tbody>${bodyRows}</tbody></table>`;
        learningTableContainerElem.html(learningTable);

        learningImage0ContainerElem.html(`<img src="${learningContents.images[0]}">`);
        learningImage1ContainerElem.html(`<img src="${learningContents.images[1]}">`);
        learningImage2ContainerElem.html(`<img src="${learningContents.images[2]}">`);
        learningImage3ContainerElem.html(`<img src="${learningContents.images[3]}">`);
    }
})