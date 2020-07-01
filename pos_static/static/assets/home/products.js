$(document).on("submit", ".add-product-form", function (e) {
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
                    window.location.href = "/products/";
                }, 1000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            call_notify("Failed to submit please check data and submit again make sure that product does your adding not exists", "warning", "topCenter");
        }
    })
});

// $(document).on("click", ".hello", function (e) {
//     call_notify("hello", "success", "topRight");
// });

$(document).on("submit", ".edit-product-form", function (e) {
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
                    window.location.href = "/products/";
                }, 1000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            call_notify("Failed to submit please check data and submit again make sure that product does your adding not exists", "warning", "topCenter");
        }
    })
});

$(document).on("click", ".delete-product-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Delete product",
        closeIcon: true,
        content: "Are you sure you want to delete this product?..",
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
            window.location.href = "/products/";
        }
    });
});

$(document).on("click", ".block-product-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Block product",
        closeIcon: true,
        content: "Are you sure you want to block this product?. you will never be able to use this product during purchase and seles creation..",
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
            window.location.href = "/products/";
        }
    });
});

$(document).on("click", ".unblock-product-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "Unblock Product",
        closeIcon: true,
        content: "Are you sure you want to unblock this product?..",
        buttons: {
            confirm: {
                text: "yes",
                btnClass: "btn btn-success",
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
            window.location.href = "/products/";
        }
    });
});

let product_list_rows = $('.product_list_table tbody').children().length;
$('.product_badge').html(product_list_rows);

$('.product_list_table tbody').change(function () {
    let product_list_rows = $('.product_list_table tbody').children().length;
    $('.product_badge').html(product_list_rows);
})