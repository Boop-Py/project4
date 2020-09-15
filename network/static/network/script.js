var last_form = null;
document.addEventListener('DOMContentLoaded', function () {

    // when heart is clicked, call the like_and_dislike function
    document.querySelectorAll('.heart').forEach(div => {
        div.onclick = function() {
            like_and_dislike(this);
        };
    });
    
    // shows edit form when button is pressed
    document.querySelectorAll("[id^='edit_post']").forEach(a => {
        a.onclick = function () {
            if (last_form != null) {
                hideForm(last_form);
            }
            last_form = this;
            let p = document.querySelector('#post_text_' + this.dataset.id);
            let form = document.querySelector('#frm_edit_' + this.dataset.id);
            p.style.display = 'none';
            form.querySelector('#id_post_edit_text').value = p.innerHTML;
            form.style.display = '';
        };
    });
    
    //Close the post editing form by clicking the close button.
    document.querySelectorAll("[id^='btn_close_']").forEach(a => {
        a.onclick = function () {
            hideForm(this);
        };

    });
    if (document.getElementById("follow_button")) {
        document.querySelector('#follow_button').addEventListener("click", function (event) {
            fetch(`/follow/${this.dataset.id}`)
                .then(response => response.json())
                .then(data => {
                    document.querySelector('#sp_followers').innerHTML = data.total_followers;
                    if (data.result == "follow") {
                        this.innerHTML = "Following";
                        this.className = "ui orange button";
                    } else {
                        this.innerHTML = "Follow";
                        this.className = "ui orange button";
                    }
                });

        })

        // show 'unfollow' on the button when needed
        document.querySelector('#follow_button').addEventListener("mouseover", function (event) {
            if (this.className == "ui orange button") {
                this.innerHTML = "Unfollow"
            }
        });

        // show 'follow' on the button when needed
        document.querySelector('#follow_button').addEventListener("mouseleave", function (event) {
            if (this.className == "ui orange button") {
                this.innerHTML = "Following"
            }
        });

    }
    //It receives an element and makes the asynchronous call of the like method.
    async function like_and_dislike(element) {
        await fetch(`/like/${element.dataset.id}`)
            .then(response => response.json())
            .then(data => {
                element.className = data.css_class;
                element.querySelector('small').innerHTML = data.total_likes;
            });
    }
    //Receive an element and hide the post editing form.
    function hideForm(element) {
        let p = document.querySelector('#post_text_' + element.dataset.id);
        let form = document.querySelector('#frm_edit_' + element.dataset.id);
        p.style.display = '';
        form.querySelector('#id_post_edit_text').value = p.innerHTML;
        form.style.display = 'none';
    }
    //Displays the alert message according to the return (success or error).
    function alertMessage(data, alert, id) {
        let div = document.createElement('div');
        let sucess = false;
        div.setAttribute('role', 'alert');
        div.setAttribute('id', 'alert_message');
        if (document.getElementById('alert_message') == null) {
            if (data.error) {
                if (data.error.id_post_edit_text) {
                    div.innerHTML = data.error.id_post_edit_text.join();
                } else {
                    div.innerHTML = data.error;
                }
                div.className = 'alert alert-dismissible fade alert-danger in show';
            } else {
                sucess = true;
                document.querySelector('#post_text_' + id).innerHTML = data.text;
                div.innerHTML = "Post changed successfully!";
                div.className = 'alert alert-dismissible fade alert-success in show';
            }
        }
        alert.appendChild(div);
        var alert_message = document.getElementById('alert_message');
        setTimeout(function () {
            if (alert_message != null) {
                $(alert_message).fadeOut("fast");
                alert_message.remove();
                if (sucess) {
                    document.querySelector('#frm_edit_' + id).style.display = 'none';
                    document.querySelector('#post_text_' + id).style.display = '';
                }
            }
        }, 1000);
    }
});