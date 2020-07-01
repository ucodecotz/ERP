$(document).on("click",".update-profile-information-link",function(e){
    e.preventDefault();
    $.confirm({
        type: "green",
        title: "UPDATE PROFILE INFORMATIONS",
        titleClass: "text-center",
        closeIcon: true,
        content: "Are you sure you want to update your informations?..",
        onContentReady: function(){
            var self = this;
            $(document).on("submit",".update-profile-info-form",function(e){
                e.preventDefault();
                var $form = $(this);
                self.showLoading();
                $.ajax({
                    url: $form.attr("action"),
                    type: $form.attr("method"),
                    data: $form.serializeArray(),
                }).done(function(response){
                    self.hideLoading();
                    try {
                        let data = JSON.parse(response)[0];
                        if(data.status){
                            self.setType("green");
                            self.setContent(data.message);
                            self.$$save.hide();
                            setTimeout(function(){
                                self.close();
                            },1000)
                        }else{
                            self.setType("red");
                            self.setContent(data.message);
                        }
                    } catch (error) {
                        call_notify("Profile failed to update", "failure", "topCenter");
                    }
                })
            });
        },
        buttons: {
            save: {
                text: "UPDATE",
                btnClass: "btn btn-success",
                action: function(){
                    $(".update-profile-info-form").trigger("submit");
                    return false;
                }
            }
        },
        onOpenBefore: function(){
            $("body").css("overflow","hidden");
        },
        onClose: function(){
            window.location.reload();
        }
    });
});

$(document).on("click",".change-password-link",function(e){
    e.preventDefault();
    $.confirm({
        type: "red",
        title: "CHANGE PASSWORD",
        titleClass: "text-center",
        closeIcon: true,
        content: "Are you sure you want to change your password?..",
        onContentReady: function(){
            var self = this;
            $(document).on("submit",".change-password-form",function(e){
                e.preventDefault();
                var $form = $(this);
                self.showLoading();
                $.ajax({
                    url: $form.attr("action"),
                    type: $form.attr("method"),
                    data: $form.serializeArray(),
                }).done(function(response){
                    self.hideLoading();
                    try {
                        let data = JSON.parse(response)[0];
                        if(data.status){
                            self.setType("green");
                            self.setContent(data.message);
                            self.$$save.hide();
                            setTimeout(function(){
                                self.close();
                            },1000)
                        }else{
                            self.setType("red");
                            self.setContent(data.message);
                        }
                    } catch (error) {
                        call_notify("Profile failed to update", "failure", "topCenter");
                    }
                })
            });
        },
        buttons: {
            save: {
                text: "Confirm",
                btnClass: "btn btn-warning",
                action: function(){
                    $(".change-password-form").trigger("submit");
                    return false;
                }
            }
        },
        onOpenBefore: function(){
            $("body").css("overflow","hidden");
        },
        onClose: function(){
            window.location.reload();
        }
    });
});