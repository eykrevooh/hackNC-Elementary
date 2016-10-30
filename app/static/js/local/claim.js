function claim (event){
    var link = $(event.relatedTarget);
    var question = link.data('question');
    var user = link.data('user');
    var modal = $(this);

    $.ajax({
        url: "/claim/",
        data: {user : user, question : question},
        type: "POST",
        success: function(data){
            return 0;
            },
        error: function(){
            console.log("Error");
            }
        });
    });
