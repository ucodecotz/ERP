ror_calculator = () => {
    let b_price, s_price, p_price, ror_val;
    b_price = $('.b_price').val();
    s_price = $('.s_price').val();
    p_price = s_price - b_price;
    ror_val = ((p_price / b_price) * 100);
    $('.p_price').html(p_price);
    if (ror_val < 45) {
        $('.ror_percent').html(`<span class="label label-lg bg-danger-400">` + ror_val + ` %</span>`);
    } else if (ror_val >= 45 && ror_val <= 59) {
        $('.ror_percent').html(`<span class="label bg-slate-400">` + ror_val + ` %</span>`);
    } else if (ror_val >= 60 && ror_val <= 79) {
        $('.ror_percent').html(`<span class="label bg-info-400">` + ror_val + ` %</span>`);
    } else if (ror_val >= 80 && ror_val <= 99) {
        $('.ror_percent').html(`<span class="label bg-primary-400">` + ror_val + ` %</span>`);
    } else if (ror_val >= 100) {
        $('.ror_percent').html(`<span class="label bg-success-400">` + ror_val + ` %</span>`);
    } else {
        $('.ror_percent').html(`<span class="label bg-danger-400">0 %</span>`);
    }

    if (ror_val < 45) {
        $('.ror_remarks').html(`<span class="label bg-danger-400">bad</span>`);
    } else if (ror_val >= 45 && ror_val <= 59) {
        $('.ror_remarks').html(`<span class="label bg-slate-400">average </span>`);
    } else if (ror_val >= 60 && ror_val <= 79) {
        $('.ror_remarks').html(`<span class="label bg-info-400">good</span>`);
    } else if (ror_val >= 80 && ror_val <= 99) {
        $('.ror_remarks').html(`<span class="label bg-primary-400">very good</span>`);
    } else if (ror_val >= 100) {
        $('.ror_remarks').html(`<span class="label bg-success-400">excellent</span>`);
    } else {
        $('.ror_remarks').html(`<span class="label bg-danger-400">null</span>`);
    }
}
$(function () {
    ror_calculator()
});
$(document).on('keyup', '.ror_form', function () {
    ror_calculator()
});

$(document).on("submit", ".ror_form", function (e) {
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
            console.log(data.status);
            if (data.status) {
                call_notify(String(data.message), "success", "topCenter");
                setTimeout(function () {
                    window.location.href = "/ror_calculator/";
                }, 1000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            call_notify("Failed to submit please check data and submit again", "warning", "topCenter");
        }
    })
});

$(document).on("submit", ".edit_ror_form", function (e) {
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
                    window.location.href = "/ror_calculator/";
                }, 1000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            call_notify("Failed to submit please check data and submit again", "warning", "topCenter");
        }
    })
});

$(document).on("click", ".delete_ror_commodity", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Delete ROR Commodity",
        closeIcon: true,
        content: "Are you sure you want to delete this ROR Commodity?..",
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
            window.location.href = "/ror_calculator/";
        }
    });
});
