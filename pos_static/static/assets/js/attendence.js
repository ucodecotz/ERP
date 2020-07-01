$(document).on("click", ".attendence-btn", function (e) {
    e.preventDefault();
    $.confirm({
        title: "Save Attendence",
        closeIcon: true,
        type: "green",
        content: "You are about to Save Attendence?",
        onContentReady: function () {
            let self = this;
            $(document).on("submit", ".attendence-form", function (e) {
                e.preventDefault();
                self.showLoading();
                let attent_list = [];
                let time_list = [];
                let staff_list = [];
                let comment_list = [];
                $(".attend").each((index, value) => {
                    attent_list.push(value.checked);
                });
                $(".arrive_time").each((index, value) => {
                    time_list.push(value.value);
                });
                $(".staff").each((index, value) => {
                    staff_list.push(value.value);
                });
                $(".comment").each((index, value) => {
                    comment_list.push(value.value);
                });
                console.log(staff_list);
                $.post($(this).attr("action"), {
                    "attend_list": JSON.stringify(attent_list),
                    "time_list": JSON.stringify(time_list),
                    "staff_list": JSON.stringify(staff_list),
                    "comment_list": JSON.stringify(comment_list),
                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
                }, function (response) {
                    self.hideLoading();
                    let data = JSON.parse(response)[0];
                    if (data.status) {
                        self.setType("green");
                        self.setContent(data.message);
                        self.$$save.hide();
                        setInterval(() => {
                            window.location.reload();
                        }, 1000);
                    } else {
                        self.setType("red");
                        self.setContent(data.message);
                    }
                });
            });
        },
        buttons: {
            save: {
                text: "save",
                btnClass: "btn-green",
                action: function () {
                    $(".attendence-form").submit();
                    return false;
                }
            }
        },
        onClose: function () {
            window.location.reload();
        }
    })
});

$(document).ready(function () {
    let $link = $(".pickadate");
    $.get($link.data("href"), {"date": $link.val()}, function (response) {
        $(".attendence_form_div").html(response);
    });
});

$(document).on("change", ".pickadate", function (e) {
    e.preventDefault();
    let $link = $(this);
    $.get($link.data("href"), {"date": $link.val()}, function (response) {
        $(".attendence_form_div").html(response);
    });
})