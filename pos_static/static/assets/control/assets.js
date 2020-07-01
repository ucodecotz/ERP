$(document).on("submit", ".add-asset-form", function (e) {
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
                    window.location.href = "/control/assets/";
                }, 1000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            call_notify("Failed to submit please check data and submit again", "warning", "topCenter");
        }
    })
});

$(document).on("submit", ".edit-asset-form", function (e) {
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
                    window.location.href = "/control/assets/";
                }, 1000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            call_notify("Failed to submit please check data and submit again", "warning", "topCenter");
        }
    })
});

$(document).on("click", ".delete-asset-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Delete Asset",
        closeIcon: true,
        content: "Are you sure you want to delete this Asset?..",
        buttons: {
            confirm: {
                text: "yes",
                btnClass: "btn btn-danger",
                action: function () {
                    var self = this;
                    self.showLoading();
                    $.ajax({
                        url: $link.data("href"),
                        type: "GET",
                    }).done(function (response) {
                        self.hideLoading();
                        try {
                            let data = JSON.parse(response)[0];
                            if (data.status) {
                                self.setType("green");
                                self.setContent(data.message);
                                self.$$confirm.hide();
                                setTimeout(function () {
                                    self.close();
                                }, 1000);
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
        onOpenBefore: function () {
            $("body").css('overflow', 'hidden');
        },
        onClose: function () {
            window.location.href = "/control/assets/";
        }
    });
});