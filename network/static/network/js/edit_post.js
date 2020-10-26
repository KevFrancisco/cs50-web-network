$(function () {
    $('[data-toggle="popover-edit-save"]').popover({
        content:'Saved!',
        container:'body',
        placement:'top',
        trigger:'manual',
    })
})

function edit_post(id) {
    let post_text_div = document.getElementById('post-text-' + id);
    let edit_textarea = document.createElement('textarea');
        edit_textarea.classList.add('w-100', 'form-control', 'form-control-sm');
        edit_textarea.id = 'post-textarea-' + id
        edit_textarea.style.height = post_text_div.clientHeight + "px";
        edit_textarea.innerHTML = post_text_div.innerText;

    post_text_div.innerHTML = '';
    post_text_div.append(edit_textarea);
    $(function() {
        $('#post-textarea-' + id).overlayScrollbars({resize: "vertical"});
    });

    // Reinitialize the masonry Grid after textarea replacement
    $(function () {
        $('.grid').masonry({
            itemSelector: '.grid-item', // use a separate class for itemSelector, other than .col-
            columnWidth: '.grid-sizer',
            percentPosition: true
            });
    })

    // Replace the Edit Button with save
    let edit_save_btn = document.getElementById('edit-save-btn-' + id);
        edit_save_btn.classList.remove('btn-warning');
        edit_save_btn.classList.add('btn-success');
        edit_save_btn.innerText = 'Save';
        edit_save_btn.onclick = function () {
            send_edited_post(id, edit_textarea.value);
        }
}

function send_edited_post(id, new_text) {
    // Remove Textarea and replace the div contents with plaintext
    let post_text_div = document.getElementById('post-text-' + id);
        post_text_div.innerHTML = '';
        post_text_div.innerText = new_text;
    
    // Replace the save button
    let edit_save_btn = document.getElementById('edit-save-btn-' + id);
        edit_save_btn.classList.remove('btn-success');
        edit_save_btn.classList.add('btn-warning');
        edit_save_btn.innerText = 'Edit';
        edit_save_btn.onclick = function () {
            edit_post(id);
        }

    // Show the popover, then hide after delay
    $(function () {
        var pop = $(edit_save_btn);
        pop.popover("show") 
        pop.on('shown.bs.popover',function() { 
            setTimeout(function() {
            pop.popover("hide")}, 1500); 
        })
    });

    // Reinitialize the masonry Grid after saving
    $(function () {
        $('.grid').masonry({
            itemSelector: '.grid-item', // use a separate class for itemSelector, other than .col-
            columnWidth: '.grid-sizer',
            percentPosition: true
            });
    })

    // Init vars for easier handling *huff!*
    let csrftoken = Cookies.get('csrftoken');
    let url = 'post/edit';
    let data = {
            'id':id,
            'text':new_text
        }

    fetch(url, {
        method: "PUT",
        headers: { "X-CSRFToken": csrftoken },
        body: JSON.stringify(data)
        })
    .then(Response => Response.json())
    .then(result => {
        console.log(result);
    });


};