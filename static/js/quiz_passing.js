        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function onClick(event) {
            let url = '{% url "quiz_bim:user_answer" progress_test_id %}'
            let data = {
                "answer_id": event.target.value,
            }
            fetch(url, {
                method: "post",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            })
        }

        function debounce(func, timeout = 300) {
            let timer;
            return (...args) => {
                clearTimeout(timer);
                timer = setTimeout(() => {
                    func.apply(this, args);
                }, timeout);
            };
        }

        function onLoad() {
            let radioButtons = document.getElementsByClassName("answer-radio");
            let debounceClick = debounce(onClick)

            for (let button of radioButtons) {
                button.addEventListener("click", debounceClick)
            }
        }

        // window.addEventListener("load", onLoad)

        document.addEventListener('htmx:afterRequest', onLoad)