$(document).on("submit",".add-group-form",function(e){
    e.preventDefault();
    var $form = $(this);
    $('.someBlock').preloader({
        text: 'Please wait the form is submitting',
        percent: 100,
        duration: 5000,
        zIndex: '99999999999',
        // setRelative: true
    });
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
                    window.location.href="/auth/user_groups/";
                },1000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            $(".add-group-form").html(response);
        }
    })
});

$(document).on("submit", ".edit-group-form", function (e) {
    e.preventDefault();
    var $form = $(this);
    $('.someBlock').preloader({
        text: 'Please wait the form is submitting',
        percent: 100,
        duration: 5000,
        zIndex: '99999999999',
        // setRelative: true
    });
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
                    window.location.href = "/auth/user_groups/";
                }, 1000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            $(".edit-group-form").html(response);
        }
    })
});

$(document).on("click",".delete-group-link",function(e){
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Delete Group",
        closeIcon: true,
        content: "Are you sure you want to delete this group?..",
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


$(document).on("click",".group-permissions-link",function(e){
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "USER PERMISSIONS",
        titleClass: "text-center",
        closeIcon: true,
        columnClass: "xlarge",
        content: function() {
            var self = this;
            $.ajax({
                url: $link.data("href"),
                type: "GET",
            }).done(function(response){
                self.setContent(response);
                self.$$ok.hide();
            }).fail(function(){
                self.setContent("something went wrong");
                self.$$ok.hide();
            });

        },
        onContentReady: function(){
            var self = this;
            $(document).on("click",".add-permission-link",function(e){
                e.preventDefault();
                let $add_link = $(this);
                $.ajax({
                    url: $add_link.data("href"),
                    type: "GET",
                }).done(function(response2){
                    $(".assigned-permission-div").html(response2);
                });
            });
            $(document).on("click",".remove-permission-link",function(e){
                e.preventDefault();
                let $remove_link = $(this);
                $.ajax({
                    url: $remove_link.data("href"),
                    type: "GET",
                }).done(function(response3){
                    $(".not-assigned-permission-div").html(response3);
                });
            });
        },
        buttons: {
            ok: {
                text: "",
                action: function(){
                    return false;
                }
            }
        },
        onOpenBefore: function(){
            $("body").css("overflow","hidden");
        },
        onClose: function() {
            window.location.reload();
        }
    });
});

$(document).on("click",".staff-available-link",function(e){
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "GROUP STAFF(s)",
        titleClass: "text-center",
        closeIcon: true,
        columnClass: "xlarge",
        content: function() {
            var self = this;
            $.ajax({
                url: $link.data("href"),
                type: "GET",
            }).done(function(response){
                self.setContent(response);
                self.$$ok.hide();
            }).fail(function(){
                self.setContent("something went wrong");
                self.$$ok.hide();
            });

        },
        onContentReady: function(){
            var self = this;
            $(document).on("click",".add-staff-group-link",function(e){
                e.preventDefault();
                let $add_link = $(this);
                $.ajax({
                    url: $add_link.data("href"),
                    type: "GET",
                }).done(function(response2){
                    $(".staff-assigned-permission-div").html(response2);
                });
            });
            $(document).on("click",".remove-staff-group-link",function(e){
                e.preventDefault();
                let $remove_link = $(this);
                $.ajax({
                    url: $remove_link.data("href"),
                    type: "GET",
                }).done(function(response3){
                    $(".staff-not-assigned-permission-div").html(response3);
                });
            });
        },
        buttons: {
            ok: {
                text: "",
                action: function(){
                    return false;
                }
            }
        },
        onOpenBefore: function(){
            $("body").css("overflow","hidden");
        },
        onClose: function() {
            window.location.reload();
        }
    });
});