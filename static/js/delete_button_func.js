document.getElementById("cancel-button").addEventListener("click", function (e) {
    e.preventDefault();
    let previousUrl = document.referrer;
    if (previousUrl) {
        window.location.href = previousUrl;
    } else {
        window.location.href = "{% url 'modules:moderator_page' %}";
    }
});