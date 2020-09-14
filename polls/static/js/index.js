


$(document).ready(function (){
    deleteUser()
})

function  deleteUser(){
    $('#btn-delete').click(function (){
    $.ajax({
        type:"POST",
        dataType:'json',
        beforeSend: function (){
            $('#exampleModal').modal("show")
            }
        })
    })
 }

$("#modal-submit").on('click',function (){
    let csrfToken = $('input[name=csrfmiddlewaretoken]').val()
    const userId = $(this).data('id')
        $.ajax({
        url:$('#modal-submit').data('url'),
        type:"POST",
        data: {
            csrfmiddlewaretoken: csrfToken,
            id:userId,
            action:"DELETE"
        },
        dataType:'json',
        success:function (data){
            $('.user-info').html(data.html_view)
            $('#exampleModal').modal("hide")
            }
        })
    })


// updating the user
$('#update-btn').click(function (){
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val()
        const  userId = $(this).data('id')
        console.log(userId)
        console.log(csrfToken)
        $.ajax({
            url: $('#update-btn').data("url"),
            type:"POST",
            data: {
                csrfmiddlewaretoken: csrfToken,
                id:userId,
                action:"EDIT"
            },
            dataType: "json",
            success: function (data){
                $('#signup-form').html(data.html_view)
            }
        });
    }
    )
