$(document).on("submit", ".add-customer-form", function (e) {
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
                    window.location.href = "/auth/users/";
                }, 1000);
            } else {
                call_notify(String(data.message), "warning", "topCenter");
                setTimeout(function () {
                    window.location.href = "/auth/users/";
                }, 3000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            call_notify("Failed to submit please check data and submit again make sure that phone number and email used does not exists", "warning", "topCenter");
        }
    })
});

$(document).on("click", ".edit-customer-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "EDIT CUSTOMER INFORMATIONS",
        titleClass: "text-center",
        columnClass: "large",
        closeIcon: true,
        content: "url:" + $link.data("href"),
        onContentReady: function () {
            var self = this;
            $(document).on("submit", ".edit-customer-form", function (e) {
                e.preventDefault();
                var $form = $(this);
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
                            self.$$cancel.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        } else {
                            call_notify(String(data.message), "warning", "topCenter");
                            setTimeout(function () {
                                window.location.href = "/auth/users/";
                            }, 3000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                });
            });
        },
        buttons: {
            cancel: {
                text: "cancel",
                btnClass: "btn btn-danger",
                action: function () {
                    self.close();
                }
            },
            save: {
                text: "UPDATE",
                btnClass: "btn btn-success",
                action: function () {
                    $(".edit-customer-form").trigger("submit");
                    return false;
                }
            },
        },
        onOpenBefore: function () {
            $("body").css("overflow", "hidden");
        },
        onClose: function () {
            window.location.reload();
        }
    });
});


$(document).on("click", ".block-customer-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Block customer",
        closeIcon: true,
        content: "Are you sure you want to block this customer?!.",
        buttons: {
            confirm: {
                text: "Yes",
                btnClass: "btn btn-warning",
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
                            self.setType("red");
                            self.setContent(response);
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
    })
});

$(document).on("click", ".unblock-customer-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "Unblock customer",
        closeIcon: true,
        content: "Are you sure you want to unblock this customer?!.",
        buttons: {
            confirm: {
                text: "Yes",
                btnClass: "btn btn-green",
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
                            self.setType("red");
                            self.setContent(response);
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
    })
});

$(document).on("click", ".delete-customer-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Delete Customer",
        closeIcon: true,
        content: "Are you sure you want to delete this Customer?..",
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

$(document).on("submit", ".add-supplier-form", function (e) {
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
                    window.location.href = "/auth/users/";
                }, 1000);
            } else {
                call_notify(String(data.message), "warning", "topCenter");
                setTimeout(function () {
                    window.location.href = "/auth/users/";
                }, 3000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            call_notify("Failed to submit please check data and submit again make sure that phone number and email used does not exists", "warning", "topCenter");
        }
    })
});

$(document).on("click", ".edit-supplier-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "EDIT SUPPLIER INFORMATIONS",
        titleClass: "text-center",
        columnClass: "large",
        closeIcon: true,
        content: "url:" + $link.data("href"),
        onContentReady: function () {
            var self = this;
            $(document).on("submit", ".edit-supplier-form", function (e) {
                e.preventDefault();
                var $form = $(this);
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
                            self.$$cancel.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        } else {
                            call_notify(String(data.message), "warning", "topCenter");
                            setTimeout(function () {
                                window.location.href = "/auth/users/";
                            }, 2000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                });
            });
        },
        buttons: {
            cancel: {
                text: "cancel",
                btnClass: "btn btn-danger",
                action: function () {
                    self.close();
                }
            },
            save: {
                text: "UPDATE",
                btnClass: "btn btn-success",
                action: function () {
                    $(".edit-supplier-form").trigger("submit");
                    return false;
                }
            },
        },
        onOpenBefore: function () {
            $("body").css("overflow", "hidden");
        },
        onClose: function () {
            window.location.reload();
        }
    });
});

$(document).on("click", ".block-supplier-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Block Supplier",
        closeIcon: true,
        content: "Are you sure you want to block this supplier?!.",
        buttons: {
            confirm: {
                text: "Yes",
                btnClass: "btn btn-warning",
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
                            self.setType("red");
                            self.setContent(response);
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
    })
});

$(document).on("click", ".unblock-supplier-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "Unblock supplier",
        closeIcon: true,
        content: "Are you sure you want to unblock this supplier?!.",
        buttons: {
            confirm: {
                text: "Yes",
                btnClass: "btn btn-green",
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
                            self.setType("red");
                            self.setContent(response);
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
    })
});

$(document).on("click", ".delete-supplier-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Delete supplier",
        closeIcon: true,
        content: "Are you sure you want to delete this Supplier?..",
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


$(document).on("submit", ".add-borrower-form", function (e) {
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
                    window.location.href = "/auth/users/";
                }, 1000);
            } else {
                call_notify(String(data.message), "warning", "topCenter");
                setTimeout(function () {
                    window.location.href = "/auth/users/";
                }, 3000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            call_notify("Failed to submit please check data and submit again make sure that phone number and email used does not exists", "warning", "topCenter");
        }
    })
});

$(document).on("click", ".edit-borrower-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "EDIT BORROWER INFORMATIONS",
        titleClass: "text-center",
        columnClass: "large",
        closeIcon: true,
        content: "url:" + $link.data("href"),
        onContentReady: function () {
            var self = this;
            $(document).on("submit", ".edit-borrower-form", function (e) {
                e.preventDefault();
                var $form = $(this);
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
                            self.$$cancel.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        } else {
                            call_notify(String(data.message), "warning", "topCenter");
                            setTimeout(function () {
                                window.location.href = "/auth/users/";
                            }, 3000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                });
            });
        },
        buttons: {
            cancel: {
                text: "cancel",
                btnClass: "btn btn-danger",
                action: function () {
                    self.close();
                }
            },
            save: {
                text: "UPDATE",
                btnClass: "btn btn-success",
                action: function () {
                    $(".edit-borrower-form").trigger("submit");
                    return false;
                }
            },
        },
        onOpenBefore: function () {
            $("body").css("overflow", "hidden");
        },
        onClose: function () {
            window.location.reload();
        }
    });
});

$(document).on("click", ".block-borrower-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Block Borrower",
        closeIcon: true,
        content: "Are you sure you want to block this borrower?!.",
        buttons: {
            confirm: {
                text: "Yes",
                btnClass: "btn btn-warning",
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
                            self.setType("red");
                            self.setContent(response);
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
    })
});

$(document).on("click", ".unblock-borrower-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "Unblock Borrower",
        closeIcon: true,
        content: "Are you sure you want to unblock this borrower?!.",
        buttons: {
            confirm: {
                text: "Yes",
                btnClass: "btn btn-green",
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
                            self.setType("red");
                            self.setContent(response);
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
    })
});

$(document).on("click", ".delete-borrower-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Delete Borrower",
        closeIcon: true,
        content: "Are you sure you want to delete this Borrower?..",
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


$(document).on("submit", ".add-staff-form", function (e) {
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
                    window.location.href = "/auth/users/";
                }, 1000);
            } else {
                call_notify(String(data.message), "warning", "topCenter");
                setTimeout(function () {
                    window.location.href = "/auth/users/";
                }, 3000);
            }
        } catch (error) {
            $('.someBlock').preloader('remove');
            call_notify("Failed to submit please check data and submit again make sure that phone number and email used does not exists", "warning", "topCenter");
        }
    })
});

$(document).on("click", ".edit-staff-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "EDIT STAFF INFORMATIONS",
        titleClass: "text-center",
        columnClass: "large",
        closeIcon: true,
        content: "url:" + $link.data("href"),
        onContentReady: function () {
            var self = this;
            $(document).on("submit", ".edit-staff-form", function (e) {
                e.preventDefault();
                var $form = $(this);
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
                            self.$$cancel.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        } else {
                            call_notify(String(data.message), "warning", "topCenter");
                            setTimeout(function () {
                                window.location.href = "/auth/users/";
                            }, 3000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                });
            });
        },
        buttons: {
            cancel: {
                text: "cancel",
                btnClass: "btn btn-danger",
                action: function () {
                    self.close();
                }
            },
            save: {
                text: "UPDATE",
                btnClass: "btn btn-success",
                action: function () {
                    $(".edit-staff-form").trigger("submit");
                    return false;
                }
            },
        },
        onOpenBefore: function () {
            $("body").css("overflow", "hidden");
        },
        onClose: function () {
            window.location.reload();
        }
    });
});

$(document).on("click", ".recover-staff-password-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        closeIcon: true,
        title: "Recovering Staff Passwords",
        content: "By Confirming, new password and Username will be generated.",
        type: "green",
        onContentReady: function () {

        },
        buttons: {
            recover: {
                text: "Confirm",
                btnClass: "btn-green",
                action: function () {
                    let self = this;
                    self.showLoading();
                    self.$$recover.hide();
                    $.get($link.data("href"), function (response) {
                        self.hideLoading();
                        self.setContent(response);
                        self.setType("green");
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

$(document).on("click", ".block-staff-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Block Staff",
        closeIcon: true,
        content: "Are you sure you want to block this staff?!.",
        buttons: {
            confirm: {
                text: "Yes",
                btnClass: "btn btn-warning",
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
                            self.setType("red");
                            self.setContent(response);
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
    })
});

$(document).on("click", ".unblock-staff-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "green",
        title: "Unblock Staff",
        closeIcon: true,
        content: "Are you sure you want to unblock this staff?!.",
        buttons: {
            confirm: {
                text: "Yes",
                btnClass: "btn btn-green",
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
                            self.setType("red");
                            self.setContent(response);
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
    })
});

$(document).on("click", ".delete-staff-link", function (e) {
    e.preventDefault();
    var $link = $(this);
    $.confirm({
        type: "red",
        title: "Delete Staff",
        closeIcon: true,
        content: "Are you sure you want to delete this staff?..",
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

$(document).on("click", ".bad-debt", function (e) {
    e.preventDefault();
    let $link = $(this);
    $.confirm({
        type: 'blue',
        closeIcon: false,
        columnClass: 'large',
        title: 'CREATE BAD DEBT',
        titleClass: 'text-center',
        content: 'url:' + $link.data('href'),
        onContentReady: function () {
            let self = this;
            $(document).on("change", ".debt_type", function (e) {
                if ($(".debt_type").val() == "Expense") {
                    $(".staff-selection").hide();
                } else if ($(".debt_type").val() == "Staff") {
                    $(".staff-selection").show();
                } else {
                    $(".staff-selection").hide();
                }
            });
            $(document).on("submit", ".customer-bad-debt-form", function (e) {
                e.preventDefault();
                var $form = $(this);
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
                            self.$$cancel.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                });
            });
        },
        buttons: {
            cancel: {
                text: 'Cancel',
                btnClass: 'btn btn-danger',
            },
            save: {
                text: 'Save',
                btnClass: 'btn-success btn',
                action: function () {
                    $('.customer-bad-debt-form').trigger('submit');
                    return false
                }
            },
        },
        onOpenBefore: function () {
            $("body").css('overflow', 'hidden');
        },
        onClose: function () {
            window.location.reload();
        }

    })
});
$(function () {
    // Setting datatable defaults
    $.extend($.fn.dataTable.defaults, {
        autoWidth: true,
        columnDefs: [{
            orderable: false,
            width: '100px',
            targets: [5]
        }],
        dom: '<"datatable-header"fBl><"datatable-scroll-wrap"t><"datatable-footer"ip>',
        language: {
            search: '<span>Filter:</span> _INPUT_',
            searchPlaceholder: 'Type to filter...',
            lengthMenu: '<span>Show:</span> _MENU_',
            paginate: {
                'first': 'First',
                'last': 'Last',
                'next': '&rarr;',
                'previous': '&larr;'
            }
        },
        drawCallback: function () {
            $(this).find('tbody tr').slice(-1).find('.dropdown, .btn-group').addClass('dropup');
        },
        preDrawCallback: function () {
            $(this).find('tbody tr').slice(-1).find('.dropdown, .btn-group').removeClass('dropup');
        }
    });

    // Basic datatable
    $('.customers_table').DataTable({
        order: [],
        buttons: {
            buttons: [
                {
                    extend: 'excelHtml5',
                    className: 'btn btn-primary',
                    exportOptions: {
                        columns: [0, 1, 2, 3, 4]
                    }
                },
            ]
        }
    });
    $('.suppliers_table').DataTable({
        order: [],
        // buttons: {
        //     buttons: [
        //         {
        //             extend: 'excelHtml5',
        //             className: 'btn btn-primary',
        //             exportOptions: {
        //                 columns: [0, 1, 2, 3, 4]
        //             }
        //         },
        //     ]
        // }
    });
    $('.borrowers_table').DataTable({
        order: [],
        // buttons: {
        //     buttons: [
        //         {
        //             extend: 'excelHtml5',
        //             className: 'btn btn-primary',
        //             exportOptions: {
        //                 columns: [0, 1, 2, 3, 4]
        //             }
        //         },
        //     ]
        // }
    });
    $('.staff_table').DataTable({
        order: [],
        // buttons: {
        //     buttons: [
        //         {
        //             extend: 'excelHtml5',
        //             className: 'btn btn-primary',
        //             exportOptions: {
        //                 columns: [0, 1, 2, 3, 4]
        //             }
        //         },
        //     ]
        // }
    });
})
