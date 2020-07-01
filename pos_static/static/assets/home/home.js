let sales_list_rows = $('.sales_list_table tbody').children().length;
$('.sales_list_badge').html(sales_list_rows);

let expenses_list_rows = $('.expenses_table tbody').children().length;
$('.expenses_badge').html(expenses_list_rows);

$(document).on("click", ".sale-aprove-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "APPROVE SALE",
        titleClass: "text-center",
        closeIcon: true,
        content: "Are you sure you want to Approve this sale?..",
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
            window.location.reload();
        }
    });
});

$(document).on('click', '.remove-expense', function (e) {
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
                action: function () {
                    let self = this;
                    $.get($link.data("href"), function (response) {
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
        onOpenBefore: function () {
            $("body").addClass("no-scroll");
        },
        onClose: function () {
            $("body").removeClass("no-scroll");
            window.location.reload();
        },
    });
});
$(document).on("click", ".expense-details", function (e) {
    $.confirm({
        title: "Expense Details",
        type: "green",
        content: "url: " + $(this).data("href"),
        closeIcon: true,
        columnClass: "medium",
        buttons: {
            btn: {
                text: "btn",
                isHidden: true
            }
        },
        onOpenBefore: function () {
            $("body").addClass("no-scroll");
        },
        onClose: function () {
            $("body").removeClass("no-scroll");
            window.location.reload();
        },
    });
});