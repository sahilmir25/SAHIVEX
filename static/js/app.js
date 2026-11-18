
document.addEventListener("DOMContentLoaded", function () {

    console.log("SAHIVEX Application Started!");

    const buttons = document.querySelectorAll("button");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            console.log("SAHIVEX Button Clicked!");
        });
    });

});
