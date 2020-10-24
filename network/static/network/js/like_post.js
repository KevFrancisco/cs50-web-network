function like_post(id) {
    let csrftoken = Cookies.get('csrftoken');

    let url = 'post/like';
    let data = {
        'id':id,
    }

    fetch(url, {
        method: "PUT",
        headers: { "X-CSRFToken": csrftoken },
        body: JSON.stringify(data)
    })
    .then(Response => Response.json())
    .then(result => {
        console.log(result);

        let button_id = 'like-count-' + id;
        let like_num = document.getElementById(button_id).innerText;

        if (result["new_like"] == true) {
            document.getElementById(button_id).innerText = parseInt(like_num + 1);
        } else {
            document.getElementById(button_id).innerText = parseInt(like_num - 1);
        }

    })
};