"use strict";

$(document).on("change", "select[name=product]", function(e) {
    e.preventDefault();
    console.log($(this).val());
    $.get("/product/" + $(this).val() + "/short_name/", function(response) {
        let data = JSON.parse(response)[0];
        if (data.status) {
            $(".product-short").html(data.unit);
        }
    });
});

$(document).on("click", ".add-purchase", function(e) {
    e.preventDefault();
    $.confirm({
        title: "",
        type: "green",
        closeIcon: true,
        content: "You are about to submit Purchase??",
        onContentReady: function() {
            var self = this;
            $(document).on("submit", ".purchase-form", function(e) {
                e.preventDefault();
                self.showLoading();
                self.$$yes.hide();
                self.$$no.hide();
                let $formData = new FormData($(this)[0]);
                $('.someBlock').preloader({
                    text: 'Please wait the form is submitting',
                    percent: 100,
                    duration: 5000,
                    zIndex: '99999999999',
                    // setRelative: true
                });
                $.ajax({
                    url: $(this).attr("action"),
                    method: "POST",
                    data: $formData,
                    processData: false,
                    contentType: false,
                }).done(function(response) {
                    self.hideLoading();
                    $('.someBlock').preloader('remove');
                    try {
                        let data = JSON.parse(response)[0];
                        if (data.status) {
                            self.setContent("Successfully Submitted");
                            call_notify(String(data.message), "success", "topCenter");
                            setTimeout(function() {
                                if (($("input[name=last]").val() == "0")) {
                                    window.location.reload();
                                } else {
                                    window.location.href = "/purchases/" + data.last + "/";
                                }
                            }, 1000);
                        }
                    } catch (error) {
                        call_notify("Failed to submit please check data and submit again", "warning", "topCenter");
                    }
                });
            });
        },
        buttons: {
            yes: {
                text: "Yes",
                btnClass: "btn-green",
                isHidden: true,
                action: function() {
                    var self = this;
                    self.setContent("There is another Purchased Item");
                    $("input[name=last]").val(1);
                    $(".purchase-form").submit();
                    return false;
                }
            },
            no: {
                text: "Submit",
                btnClass: "btn-green",
                action: function() {
                    var self = this;
                    $("input[name=last]").val(0);
                    
                    $(".purchase-form").submit();
                    return false;
                }
            }
        }
    })

});

$(document).on('click', '.remove-purchase', function(e) {
    e.preventDefault();
    let $link = $(this);
    $.confirm({
        title: "Remove Confirmation",
        type: "red",
        closeIcon: true,
        content: "Are you sure?",
        buttons: {
            remove: {
                text: "Remove",
                btnClass: "btn-danger",
                action: function() {
                    let self = this;
                    $.get($link.data("href"), function(response) {
                        let data = JSON.parse(response)[0];
                        if (data.status) {
                            self.setContent(data.message);
                            self.setType("green");
                            self.$$remove.hide();
                            setInterval(() => {
                                self.close();
                            }, 1000);
                        } else {
                            self.setContent(data.message);
                            self.setType("red");
                        }
                    });
                    return false;
                }
            }
        },
        onOpenBefore: function() {
            $("body").addClass("no-scroll");
        },
        onClose: function() {
            $("body").removeClass("no-scroll");
            window.location.reload();
        },
    });
});

$(document).on("submit", ".add-purchase-form", function(e) {
    e.preventDefault();
    let $formData = new FormData($(this)[0]);
    $.ajax({
        url: $(this).attr("action"),
        method: "POST",
        data: $formData,
        processData: false,
        contentType: false,
    }).done(function(response) {
        try {
            let data = JSON.parse(response)[0];
            if (data.status) {
                call_notify(String(data.message), "success", "topCenter");
                setTimeout(function() {
                    window.location.reload();
                }, 1000);
            }
        } catch (error) {
            $(".purchase-form").html(response);
        }
    });
});
$(document).on('click', '.remove-purchase-item', function(e) {
    e.preventDefault();
    let $link = $(this);
    $.confirm({
        title: "Remove Confirmation",
        type: "red",
        closeIcon: true,
        content: "Are you sure?",
        buttons: {
            remove: {
                text: "Remove",
                btnClass: "btn-danger",
                action: function() {
                    let self = this;
                    $.get($link.data("href"), function(response) {
                        let data = JSON.parse(response)[0];
                        if (data.status) {
                            self.setContent(data.message);
                            self.setType("green");
                            self.$$remove.hide();
                            setInterval(() => {
                                self.close();
                            }, 1000);
                        } else {
                            self.setContent(data.message);
                            self.setType("red");
                        }
                    });
                    return false;
                }
            }
        },
        onOpenBefore: function() {
            $("body").addClass("no-scroll");
        },
        onClose: function() {
            $("body").removeClass("no-scroll");
            window.location.reload();
        },
    });
});