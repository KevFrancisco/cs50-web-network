function follow_user(id) {
    // Init vars for easier handling *huff!*
    let csrftoken = Cookies.get('csrftoken');
    let url = '../user/follow';
    let data = {
            'to_follow_id':id,
        };
    
    fetch(url, {
        method: "PUT",
        headers: { "X-CSRFToken": csrftoken },
        body: JSON.stringify(data)
        })
    .then(Response => Response.json())
    .then(result => {
        console.log(result);

        if (result["new_follow"]) {
            let follow_btn = document.getElementById('user-follow-' + id);
                follow_btn.classList.remove('btn-warning');
                follow_btn.classList.add('btn-danger');
                document.getElementById('user-follow-span-' + id).innerText = 'Unfollow';

                // Show the popover, then hide after delay
                $(function () {
                    let pop = $(follow_btn);
                    pop.popover("show") 
                    pop.on('shown.bs.popover',function() { 
                        setTimeout(function() {
                        pop.popover("hide")}, 1500); 
                    })
                })
        } else {
            let follow_btn = document.getElementById('user-follow-' + id);
                follow_btn.classList.remove('btn-danger');
                follow_btn.classList.add('btn-warning');
                document.getElementById('user-follow-span-' + id).innerText = 'Follow';
                
                // Show the popover, then hide after delay
                $(function () {
                    let pop = $(follow_btn);
                    pop.popover("show") 
                    pop.on('shown.bs.popover',function() { 
                        setTimeout(function() {
                        pop.popover("hide")}, 1500); 
                    })
                });

        };


    });

};