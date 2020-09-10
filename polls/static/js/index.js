
  $("#btn-del").click(function(){
          const useId = $(this).attr("data-id");
          let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
      console.log(csrftoken)
      // const action = confirm("Are you sure you want to delete this user?");
      console.log(useId)
        // if(action){
            $.ajax(
        {
            type:"post",
            url: "/"+useId+"/delete/",
            headers: {'X-CSRFToken': csrftoken},
            data:{
                'user_id':useId,
            },
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            message:'Success',
        })
      // }
  });


