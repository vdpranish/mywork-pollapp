// creating an html element
const  modal = document.createElement("div");


$(".btn-delete").click(
    function (){
        const userId = $(this).attr("data-id")
        const userName = $(this).attr("data-name")
        // adding modal into created element
        modal.innerHTML = `
            <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog" role="document">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Delete Confirmation</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                        </button>
                      </div>
                      <div class="modal-body">
                        <p>Please Confirm for Delete ${userName}</p>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button id="del-confirm" type="submit" class="btn btn-primary" data-id=${userId}>Delete</button>
                      </div>
                    </div>
                  </div>
            </div>
`
        console.log(userId)
        console.log(userName)

        // modal appdending

        document.querySelector(".user-info").appendChild(modal);
        $("#del-confirm").click(function(){
          const useId = $(this).attr("data-id");
        console.log(useId)
            // creating csrf token
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
            const csrftoken = getCookie('csrftoken');
        // ajax request for deleting user
        $.ajax(
            {
            type:"POST",
            url: "/"+useId+"/delete/",
            headers: {'X-CSRFToken': csrftoken},
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: window.location.href = "/adminview",
            });
        })
    }
)











// updating the user
$('#update-btn').click(
    function (){
        const  userId = $(this).attr("data-id");
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        console.log('Clicked')
        console.log(`user id :${userId}`)
        $.ajax({
            type:"POST",
            url: "/"+userId+"/edit/",
            headers: {'X-CSRFToken': csrftoken},
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: window.location.href = "/adminview"
        });
        console.log('Success')
    }
    )


