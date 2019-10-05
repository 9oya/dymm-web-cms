$(document).ready(function () {
    /*=========================================================================
    Javascript Extensions
    =========================================================================*/
    String.prototype.format = function () {
        let formatted = this;
        for (let arg in arguments) {
            formatted = formatted.replace("{" + arg + "}", arguments[arg]);
        }
        return formatted;
    };

    /*=========================================================================
    jQuery Extensions
    =========================================================================*/
    $.each(["put", "delete"], function (i, method) {
        $[method] = function (url, data, callback, type) {
            if ($.isFunction(data)) {
                type = type || callback;
                callback = data;
                data = undefined;
            }
            return $.ajax({
                url: url,
                type: method,
                dataType: type,
                data: data,
                success: callback
            });
        };
    });
    $.fn.serializeIncludeDisabled = function () {
        let disabled = this.find(":input:disabled").removeAttr("disabled");
        let serialized = this.serialize();
        disabled.attr("disabled", "disabled");
        return serialized;
    };

    /*=========================================================================
    Public properties
    =========================================================================*/
    let _url = {
            api: {
                admin: "/api/admin",
                asset: "/api/asset",
                avatar: "/api/avatar",
                tag: "/api/tag",
                banner: "/api/banner"
            },
            view: {
                home: "/home",
                signIn: "/admin/sign-in",
                signUp: "/admin/sign-up",
                tag: "/tag"
            }
        },
        _message = {
            error: {
                notFound: "The requested resource is not available: 404",
                methodErr: "405 Method Not Allowed",
                server: "Internal server error: 500",
                network: "Network with server failed. \nPleas check your " +
                    "Wi-Fi or network status."
            }
        },
        _code = {
            expiredToken: "expired-token"
        },
        _alertFailResponse = function (response) {
            if (response.status === 400) {
                alert(response.responseJSON.message);
            } else if (response.status === 401) {
                alert(response.responseJSON.message);
            } else if (response.status === 403) {
                if (response.responseJSON.code === _code.expiredToken) {
                    location.assign(_url.view.signIn);
                    return
                }
                alert(response.responseJSON.message);
            } else if (response.status === 404) {
                alert(_message.error.notFound);
            } else if (response.status === 405) {
                alert(_message.error.methodErr);
            } else if (response.status === 500) {
                alert(_message.error.server);
            } else {
                alert(_message.error.network);
            }
        },
        _htmlFailResponse = function (response, msgEle) {
            if (response.status === 400) {
                msgEle.text(JSON.stringify(
                    response.responseJSON.message, null, "\t")
                );
            } else if (response.status === 401) {
                msgEle.text(JSON.stringify(
                    response.responseJSON.message, null, "\t")
                );
            } else if (response.status === 403) {
                if (response.responseJSON.code === _code.expiredToken) {
                    location.assign(_url.view.signIn);
                    return
                }
                msgEle.text(JSON.stringify(
                    response.responseJSON.message, null, "\t")
                );
            } else if (response.status === 404) {
                alert(_message.error.notFound);
            } else if (response.status === 405) {
                alert(_message.error.methodErr);
            } else if (response.status === 500) {
                alert(_message.error.server);
            } else {
                alert(_message.error.network);
            }
        },
        _coloringTableOfARow = function (targetEle, before, after) {
            targetEle.prevAll(".selected").removeClass("selected").css(
                "background-color", before);
            targetEle.nextAll(".selected").removeClass("selected").css(
                "background-color", before);
            if (targetEle.not(".selected")) {
                targetEle.addClass("selected");
                targetEle.css("background-color", after);
            }
        },
        _foldSubRowsRecursively = function (targetEle) {
            $.each(targetEle, function (i, subEle) {
                subEle = $(subEle);
                if (subEle.is(".off")) {
                    return;
                }
                let subElsSuperId = subEle.data("id"),
                    subSubEle = subEle.nextAll(".super" + subElsSuperId);
                _foldSubRowsRecursively(subSubEle);
                subEle.find("div.tr-flip").text("Spread");
                subEle.removeClass("on").addClass("off");
            });
            targetEle.hide();
        },
        _loadSubRows = function (tappedEle, url, subElesColor, superId) {
            $.get(url)
                .done(function (response, textStatus, jqXHR) {
                    let subEles = $(response).addClass("super" + superId);
                    subEles.addClass("sub");
                    subEles.css("background-color", subElesColor);
                    tappedEle.after(subEles);
                    console.log("LoadAfter Complete.");
                })
                .fail(function (response) {
                    _alertFailResponse(response);
                });
            tappedEle.addClass("tapped");
        },
        _toggleTableOfRows = function (tappedEle, url, subElesColor) {
            subElesColor = subElesColor || "beige";
            tappedEle.css("background-color", "paleturquoise");
            if (tappedEle.data("hasSub") !== "True") {
                console.log("Current Element has any sub-entities.");
                return false;
            }
            let _superId = tappedEle.data("id");
            if (tappedEle.is(".off")) {
                if (tappedEle.is(".tapped")) {
                    tappedEle.nextAll(".super" + _superId).show();
                } else {
                    _loadSubRows(tappedEle, url, subElesColor, _superId)
                }
                tappedEle.find("div.tr-flip").text("Fold");
                tappedEle.removeClass("off").addClass("on");
            } else if (tappedEle.is(".on")) {
                let _subEls = tappedEle.nextAll(".super" + _superId);
                _foldSubRowsRecursively(_subEls);
                tappedEle.find("div.tr-flip").text("Spread");
                tappedEle.removeClass("on").addClass("off");
            }
        };
    $.base = {
        url: _url,
        message: _message,
        code: _code,
        method: {
            alertFailResponse: _alertFailResponse,
            htmlFailResponse: _htmlFailResponse,
            coloringTableOfARow: _coloringTableOfARow,
            toggleTableOfRows: _toggleTableOfRows
        }
    };
});