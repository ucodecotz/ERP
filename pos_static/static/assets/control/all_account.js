$(document).on("click",".add-account-link",function(e){
    e.preventDefault();
    let $link = $(this);
    $.confirm({
        type: "green",
        columnClass: "medium",
        title: "CREATE ACCOUNT",
        titleClass: "text-center",
        closeIcon: true,
        content: "url:" + $link.data("href"),
        onContentReady: function(){
            var self = this;
            $("input[type='number']").val(0);
            $(document).on("submit", ".add-account-form", function (e) {
                e.preventDefault();
                let $form = $(this);
                self.showLoading();
                $.ajax({
                    url: $form.attr("action"),
                    type: $form.attr("method"),
                    data: $form.serializeArray(),
                }).done(function (response) {
                    self.hideLoading();
                    try {
                        let data = JSON.parse(response)[0];
                        if (data.status) {
                            self.setType("green");
                            self.setContent(data.message);
                            self.$$save.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                })
            });
        },
        buttons: {
            save: {
                text: "Save",
                btnClass: "btn btn-success",
                action: function(){
                    $(".add-account-form").trigger("submit");
                    return false
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

$(document).on("click",".edit-account-link",function(e){
    e.preventDefault();
    let $link = $(this);
    $.confirm({
        type: "green",
        columnClass: "medium",
        title: "EDIT ACCOUNT",
        titleClass: "text-center",
        closeIcon: true,
        content: "url:" + $link.data("href"),
        onContentReady: function(){
            var self = this;
            $(document).on("submit", ".edit-account-form", function (e) {
                e.preventDefault();
                let $form = $(this);
                self.showLoading();
                $.ajax({
                    url: $form.attr("action"),
                    type: $form.attr("method"),
                    data: $form.serializeArray(),
                }).done(function (response) {
                    self.hideLoading();
                    try {
                        let data = JSON.parse(response)[0];
                        if (data.status) {
                            self.setType("green");
                            self.setContent(data.message);
                            self.$$save.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                })
            });
        },
        buttons: {
            save: {
                text: "Update",
                btnClass: "btn btn-success",
                action: function(){
                    $(".edit-account-form").trigger("submit");
                    return false
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

$(document).on("click",".account-deposit-link",function(e){
    e.preventDefault();
    let $link = $(this);
    $.confirm({
        type: "green",
        columnClass: "medium",
        title: "DEPOSIT FUND",
        titleClass: "text-center",
        closeIcon: true,
        content: "url:" + $link.data("href"),
        onContentReady: function(){
            $("input[type='number']").val('');
            var self = this;
            $(document).on("submit", ".account-deposit-form", function (e) {
                e.preventDefault();
                let $form = $(this);
                self.showLoading();
                $.ajax({
                    url: $form.attr("action"),
                    type: $form.attr("method"),
                    data: $form.serializeArray(),
                }).done(function (response) {
                    self.hideLoading();
                    try {
                        let data = JSON.parse(response)[0];
                        if (data.status) {
                            self.setType("green");
                            self.setContent(data.message);
                            self.$$save.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                })
            });
        },
        buttons: {
            save: {
                text: "Deposit",
                btnClass: "btn btn-success",
                action: function(){
                    $(".account-deposit-form").trigger("submit");
                    return false
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

$(document).on("click", ".delete-account-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Delete Account",
        closeIcon: true,
        content: "Are you sure you want to delete this account informations?..",
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

$(document).on("click",".account-transfer-link",function(e){
    e.preventDefault();
    let $link = $(this);
    $.confirm({
        type: "green",
        columnClass: "medium",
        title: "TRANSFER FUND",
        titleClass: "text-center",
        closeIcon: true,
        content: "url:" + $link.data("href"),
        onContentReady: function(){
            var self = this;
            $(document).on("submit", ".account-transfer-form", function (e) {
                e.preventDefault();
                let $form = $(this);
                self.showLoading();
                $.ajax({
                    url: $form.attr("action"),
                    type: $form.attr("method"),
                    data: $form.serializeArray(),
                }).done(function (response) {
                    self.hideLoading();
                    try {
                        let data = JSON.parse(response)[0];
                        if (data.status) {
                            self.setType("green");
                            self.setContent(data.message);
                            self.$$save.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                })
            });
        },
        buttons: {
            save: {
                text: "Confirm transfer",
                btnClass: "btn btn-success",
                action: function(){
                    $(".account-transfer-form").trigger("submit");
                    return false
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



$(document).on("click",".cash-collection-transfer-link",function(e){
    e.preventDefault();
    let $link = $(this);
    $.confirm({
        type: "green",
        columnClass: "large",
        title: "TRANSFER FUND",
        titleClass: "text-center",
        closeIcon: true,
        content: "url:" + $link.data("href"),
        onContentReady: function(){
            var self = this;
            $(document).on("submit", ".cash-collection-transfer-form", function (e) {
                e.preventDefault();
                let $form = $(this);
                self.showLoading();
                $.ajax({
                    url: $form.attr("action"),
                    type: $form.attr("method"),
                    data: $form.serializeArray(),
                }).done(function (response) {
                    self.hideLoading();
                    try {
                        let data = JSON.parse(response)[0];
                        if (data.status) {
                            self.setType("green");
                            self.setContent(data.message);
                            self.$$save.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                })
            });
        },
        buttons: {
            save: {
                text: "Confirm transfer",
                btnClass: "btn btn-success",
                action: function(){
                    $(".cash-collection-transfer-form").trigger("submit");
                    return false
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