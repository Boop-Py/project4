var last_form = null;
document.addEventListener('DOMContentLoaded', function () {

    // when heart is clicked, call the like_and_dislike function
    document.querySelectorAll('.heart').forEach(div => {
        console.log("heart clicked")
        div.onclick = function() {
            like_and_dislike(this);
        };
    });
    
    // when follow button is clicked, call the follow function
    document.querySelectorAll('.follow').forEach(div => {
        console.log("folo clicked")
        div.onclick = function() {
            follow_unfollow(this);
        };
    }); 
    
    document.querySelectorAll("[id^='edit_form']").forEach(form => {
        form.onsubmit = function (e) {
            e.preventDefault();
            this.querySelector('#div_buttons').style.display = "none";
            if (this.querySelector('#alert_message') != null) {
                this.querySelector('#alert_message').remove();
            }
            let alert = this.querySelector('#post_text_alert_' + this.dataset.id);

            let input = this.querySelector('div>textarea');
            if (input.value.trim().length == 0) {
                alert_message({
                    'error': 'This field is required.'
                }, alert, this.dataset.id);
                this.querySelector('#div_buttons').style.display = "";
                return 0;
            }
            var form_data = $(this).serialize();
            let csrftoken = this.querySelector("input[name='csrfmiddlewaretoken']").value;
            fetch(`/stronk/editpost/${this.dataset.id}`, {
                    method: 'POST',
                    headers: {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        "X-CSRFToken": csrftoken
                    },
                    body: form_data
                })
                .then(response => response.json())
                .then(data => {
                    alert_message(data, alert, this.dataset.id);
                    this.querySelector('#div_buttons').style.display = 'none';
                    form.style.display = 'none'; 
                    document.querySelector('#post_content' + this.dataset.id).innerHTML = data.text;
                    
                }).catch((error) => {
                    console.log(error)

                    this.querySelector('#div_buttons').style.display = "";
                });
        }
    });
   
    // shows edit form when button clicked
    document.querySelectorAll("[id^='edit_post']").forEach(a => {
        a.onclick = function () {
            if (last_form != null) {
                hide_form(last_form);
            }
            last_form = this;
            let p = document.querySelector('#post_content' + this.dataset.id);
            let form = document.querySelector('#edit_form' + this.dataset.id);
            document.querySelector('#div_buttons').style.display = 'block';
            p.style.display = 'none';
            form.querySelector('#id_edit_text').value = p.innerHTML;
            form.style.display = '';
        };
    });
    
    // close edit form
    document.querySelectorAll("[id^='close_edit_button']").forEach(a => {
        console.log("close button")
        a.onclick = function () {
            hide_form(this);
        };
    });

    if (document.getElementById("follow_button")) {
        document.querySelector('#follow_button').addEventListener("click", function (event) {
            console.log("follow button clicked")
            console.log(this.dataset)
            fetch(`/stronk/follow/${this.dataset.id}`)
                .then(response => response.json())
                .then(data => {
                    document.querySelector('h4').innerHTML = data.total_followers;
                    if (data.result == "follow") {
                        this.innerHTML = "Following";
                        this.className = "ui button";
                    }                    
                    else {
                        this.innerHTML = "Follow";
                        this.className = "ui basic button";
                    }
                });
        })

        // show 'unfollow' on the button
        document.querySelector('#follow_button').addEventListener("mouseover", function (event) {
            if (this.className == "ui button") {
                this.innerHTML = "Unfollow"
            }
        });

        // show 'following' on the button
        document.querySelector('#follow_button').addEventListener("mouseleave", function (event) {
            if (this.className == "ui button") {
                this.innerHTML = "Following"
            }
        });
    }
    
     // asynchronous like function
    async function like_and_dislike(element) {
        console.log("like function reached")
        await fetch(`/stronk/like/${element.dataset.id}`)
            .then(response => response.json())
            .then(data => {
               element.querySelector('span').innerHTML = data.total_likes;
            });
    }
    
    // hide the edit form
    function hide_form(element) {
        let p = document.querySelector('#post_content' + element.dataset.id);
        let form = document.querySelector('#edit_form' + element.dataset.id);
        p.style.display = '';
        form.querySelector('#id_edit_text').value = p.innerHTML;
        form.style.display = 'none';
    } 
    
    // show alert
    function alert_message(data, alert, id) {
        console.log("Do I  get here?");
        let div = document.createElement('div');
        let sucess = false;
        div.setAttribute('role', 'alert');
        div.setAttribute('id', 'alert_message');
        if (document.getElementById('alert_message') == null) {
            if (data.error) {
                if (data.error.id_edit_text) {
                    div.innerHTML = data.error.id_edit_text.join();
                } else {
                    div.innerHTML = data.error;
                }
                div.className = 'ui alert';
            } else {
                sucess = true;
                document.querySelector('#post_content' + id).innerHTML = data.text;
                div.innerHTML = "Post changed successfully!";
                div.className = 'ui alert';
            }
        }
        alert.appendChild(div);
        var alert_message = document.getElementById('alert_message');
        setTimeout(function () {
            if (alert_message != null) {
                $(alert_message).fadeOut("fast");
                alert_message.remove();
                if (sucess) {
                    document.querySelector('#edit_form' + id).style.display = 'none';
                    document.querySelector('#post_content' + id).style.display = '';
                }
            }
        }, 1000);
    }  
});