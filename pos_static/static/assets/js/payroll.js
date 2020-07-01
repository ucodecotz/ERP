"use strict";
$(document).on('click', '.pay_salaries', function () {
    let row_checked = $('.user-selected').parent().parent().find(".user-selected").is(':checked');
    let deduction_amount = $('.user-selected').parent().parent().find(".deduction").val();
    let $link = $(this);
    $.confirm({
        title: "Salary Payment",
        titleClass: "text-center",
        type: "green",
        closeIcon: true,
        content: " ",
        columnClass: "medium",
        onContentReady: function () {
            let self = this;
            self.showLoading();
            let user_selected_list = [];
            let deduction_list = [];
            let staff_list = [];
            $('input[type=checkbox]').each(function () {
                console.log($(this).val())
                if (this.checked) {
                    staff_list.push($(this).data("user"))
                    user_selected_list.push(true);
                    if ($(this).parent().parent().find('.deduction').val() == null) {
                        deduction_list.push(0);
                    } else {
                        deduction_list.push($(this).parent().parent().find('.deduction').val());
                    }
                }

            });
            $.get($link.data("href"), {
                "user_selected_list": JSON.stringify(user_selected_list),
                "deduction_list": JSON.stringify(deduction_list),
                "staff_list": JSON.stringify(staff_list),
                "month": $(".select-month").data("month")
            }, function (response) {
                self.hideLoading();
                self.setContent(response);
            });
            $(document).on("submit", ".salary-payment-form", function (e) {
                e.preventDefault();
                $.post($(this).attr("action"), {
                    "user_selected_list": JSON.stringify(user_selected_list),
                    "deduction_list": JSON.stringify(deduction_list),
                    "staff_list": JSON.stringify(staff_list),
                    "payment_type": $(".payment_type option:selected").val(),
                    "total": $(".total").val(),
                    "bank": $(".bank option:selected").val(),
                    "month": $(".select-month").data("month"),
                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
                }, function (response) {
                    console.log(response);
                    let data = JSON.parse(response)[0];
                    if (data.status) {
                        self.setType("green")
                        self.setContent(data.message);
                        self.$$pay.hide()
                        setInterval(() => {
                            window.location.reload();
                        }, 1000);
                    } else {
                        self.setType("red")
                        self.setContent(data.message);
                    }
                });
            });
        },
        buttons: {
            pay: {
                text: "Pay",
                btnClass: "btn-primary",
                action: function () {
                    let self = this;
                    $(".salary-payment-form").submit();
                    return false;
                }
            }
        },
        onClose: function () {
            window.location.reload();
        }
    });
});


$(document).on("click", ".select-month", function (e) {
    e.preventDefault();
    let $link = $(this);
    $.confirm({
        title: "Month",
        type: "green",
        closeIcon: true,
        content: "url: " + $link.data("href"),
        buttons: {
            select: {
                text: "Select",
                btnClass: "btn-success",
                action: function () {
                    window.location.href = "/control/payroll/?month=" + $(".months option:selected").val() + "&year=" + $(".year option:selected").val()
                    return false;
                }
            }
        },
        onClose: function () {
            window.location.reload();
        }
    });
});