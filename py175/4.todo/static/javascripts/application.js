// https://launchschool.com/lessons/7131ac4b/assignments/9bfe69ac
"use strict";

document.addEventListener("DOMContentLoaded", function () {
    let forms = document.querySelectorAll("form.delete, form.complete_all");
    forms.forEach(form => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            event.stopPropagation();

            if (confirm("Are you sure? This cannot be undone!")) {
                event.target.submit();
            }
        });
    });
});