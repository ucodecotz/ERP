$(document).on("submit",".add-user-type-form",function(e){
    e.preventDefault();
    var $form = $(this);
    $.ajax({
        url: $form.attr("action"),
        type: $form.attr("method"),
        data: $form.serializeArray(),
    }).done(function(response){
        try {
            let data = JSON.parse(response)[0];
            if (data.status) {
                call_notify(String(data.message),"success","topCenter");
                setTimeout(function(){
                    window.location.href="/control/user_types/";
                },1000);
            }
        } catch (error) {
            $(".add-user-type-form").html(response);
        }
    })
});

$(document).on("submit", ".edit-user-type-form", function (e) {
    e.preventDefault();
    var $form = $(this);
    $.ajax({
        url: $form.attr("action"),
        type: $form.attr("method"),
        data: $form.serializeArray(),
    }).done(function (response) {
        try {
            let data = JSON.parse(response)[0];
            if (data.status) {
                call_notify(String(data.message), "success", "topCenter");
                setTimeout(function () {
                    window.location.href = "/control/user_types/";
                }, 1000);
            }
        } catch (error) {
            $(".edit-user-type-form").html(response);
        }
    })
});

$(document).on("click",".delete-user-type-link",function(e){
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Delete user type",
        closeIcon: true,
        content: "Are you sure you want to delete this type?..",
        buttons: {
            confirm:{
                text: "yes",
                btnClass: "btn btn-danger",
                action: function(){
                    var self = this;
                    self.showLoading();
                    $.ajax({
                        url: $link.data("href"),
                        type: "GET",
                    }).done(function(response){
                        self.hideLoading();
                        try {
                            let data = JSON.parse(response)[0];
                            if (data.status) {
                                self.setType("green");
                                self.setContent(data.message);
                                self.$$confirm.hide();
                                setTimeout(function(){
                                    self.close();
                                },1000);
                            } else {
                                self.setType("red");
                                self.setContent(data.message);
                            }
                        } catch (error) {
                            self.setContent(response);
                            self.setType("red");
                        }
                    });
                    return false;
                }
            }
        },
        onOpenBefore: function(){
            $("body").css('overflow', 'hidden');
        },
        onClose: function(){
            window.location.reload();
        }
    });
});