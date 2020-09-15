


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
        const formData = $('#signup-form').serializeArray();
        const  formAll = JSON.stringify(formData)
        const url = $(this).data("url")
        console.log(url)
        $.ajax({
            url: $(this).data("url"),
            type:"POST",
            data: {
                csrfmiddlewaretoken: csrfToken,
                id:userId,
                action:"EDIT",
                formData:formAll,
            },
            dataType: "json",
            success: function (data){
                $('#signup-form').html(data.table_view)
            }
        });
    }
    )
