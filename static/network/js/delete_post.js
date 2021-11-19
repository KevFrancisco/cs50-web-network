function delete_post(id) {
    if (confirm('Are you sure you want to delete this post?\nThis action is irreversible')) {
        // Init vars for easier handling *huff!*
        let csrftoken = Cookies.get('csrftoken');
        let url = 'post/delete';
        let data = {
                'id':id,
            }

        // Fetchy fetch!
        fetch(url, {
            method: "PUT",
            headers: { "X-CSRFToken": csrftoken },
            body: JSON.stringify(data)
            })
        .then(Response => Response.json())
        .then(result => {
            console.log(result);
            
            // Delete the card element
            let card_id = 'post-card-' + id;
            let card_el = document.getElementById(card_id);
                card_el.remove();
        
                // Reinitialize the masonry Grid after removing the post
            $(function () {
                $('.grid').masonry({
                    itemSelector: '.grid-item', // use a separate class for itemSelector, other than .col-
                    columnWidth: '.grid-sizer',
                    percentPosition: true
                    });
            });
        });
    }
};