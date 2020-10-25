// Initialize Popover for Bootstrap since feature is opt-in
// Add generic attr for all popovers, then only show for new likes
$(function () {
    $('[data-toggle="popover"]').popover({
        content:'Liked!',
        container:'body',
        placement:'top',
        trigger:'manual',
    })
})

function like_post(id) {
    let csrftoken = Cookies.get('csrftoken');
    let url = 'post/like';
    let data = {'id':id}

    fetch(url, {
        method: "PUT",
        headers: { "X-CSRFToken": csrftoken },
        body: JSON.stringify(data)
        })
    .then(Response => Response.json())
    .then(result => {
        console.log(result);
        
        let button_span_id = 'like-count-' + id;
        let button_span_el = document.getElementById(button_span_id)
        let liked_icon_id = 'liked-icon-' + id;
        let liked_icon_el = document.getElementById(liked_icon_id);
        let liked = result["new_like"];
        let like_num = button_span_el.innerText;
        
        // Make the popover
        let button_id = 'like-btn-' + id;
        $('button_id').popover({
            content:"Liked!",
            placement:"top",
            trigger:"focus"
        });
        // Get the el to popover
        let button_el = document.getElementById(button_id);
    
        if (liked == true) {
            button_span_el.innerText = parseInt(like_num + 1);

            button_el.classList.remove('btn-outline-secondary');
            button_el.classList.add('btn-warning');

            liked_icon_el.classList.remove('far');
            liked_icon_el.classList.add('fas');

            // Show the popover, then hide after delay
            $(function () {
                var pop = $(button_el);
                pop.popover("show") 
                pop.on('shown.bs.popover',function() { 
                    setTimeout(function() {
                    pop.popover("hide")}, 1500); 
                })
            })
        } else {
            button_span_el.innerText = parseInt(like_num - 1);
            
            button_el.classList.remove('btn-warning');
            button_el.classList.add('btn-outline-secondary');

            liked_icon_el.classList.remove('fas');
            liked_icon_el.classList.add('far');
        }
    });


};