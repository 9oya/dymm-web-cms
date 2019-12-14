$(document).ready(function () {

    /*=========================================================================
    Import Modules
    =========================================================================*/
    let _f = $.base.method,
        _u = $.base.url,
        _loadingImg = $("img.loading"),
        _avtListEle = $("div#bx-avatar-list"),
        _avtDetailEle = $("div#bx-avatar-detail");

    /*=========================================================================
    Private methods for Tag Application
    =========================================================================*/
    let _avatar = {
        list: function () {
        },
        detail: function () {
        }
    };

    _avatar.list.prototype.uploadOptSelected = function (currEle) {
        let _form = _avtListEle.find("form.file-form"),
            _option = currEle.find("option:selected").val(),
            _uri = _u.api.avatar + "/import/{0}".format(_option);
        if (_option === 'del-avatar') {
            let del_key = _avtListEle.find("input#delete_key").val();
            if (del_key === undefined || del_key === "") {
                alert("You need to fill in the del_key input.");
                location.reload();
                return
            }
            _uri += ("/" + del_key)
        }
        _form.attr("action", _uri);
    };
    _avatar.list.prototype.upLoadSingleFile = function (currEle) {
        let _form = currEle.parent();
        _loadingImg.show();
        _form.ajaxSubmit(function () {
            location.reload();
            return false;
        });
    };
    _avatar.list.prototype.tableRowTapped = function (currEle) {
        let _avatarId = currEle.data("id");
        _avatar.detail.prototype.getDetailFormWithValue(_avatarId);
    };
    _avatar.list.prototype.optionSelected = function (currEle) {
        let _uri = '',
            _avatarId = _avtListEle.find(".picked-item").data("id"),
            _option = currEle.find("option:selected").val();
        if (_avatarId === undefined) {
            _uri = _u.api.avatar + "/export/" + _option
        } else {
            _uri = _u.api.avatar + "/" + _avatarId + "/export/" + _option
        }
        _avtListEle.find("a").attr("href", _uri);
    };
    _avatar.list.prototype.searchOptionSelected = function (currEle) {
        let _option = currEle.find("option:selected").val();
        if (_option === 'admin' || _option === 'inactive' ||
            _option === 'block' || _option === 'unconf') {
            let _tableHeader = _avtListEle.find("section.tb > header"),
                _select_url = "{0}/{1}/{2}".format(_u.api.avatar, "select",
                    _option),
                _export_url = "{0}/{1}/{2}/{3}".format(_u.api.avatar, "export",
                    "select", _option);
            $.get(_select_url)
                .done(function (response, textStatus, jqXHR) {
                    _tableHeader.nextAll().remove();
                    _tableHeader.after(response);
                })
                .fail(function (response) {
                    _f.alertFailResponse(response);
                });
            _avtListEle.find("a").attr("href", _export_url);
        }
    };
    _avatar.list.prototype.searchEnterKeyTapped = function (currEle) {
        let _tableHeader = _avtListEle.find("section.tb > header"),
            _keyword = currEle.val(),
            _option = $(".wrap-search").find("option:selected").val(),
            _search_url = "{0}/{1}/{2}/{3}".format(_u.api.avatar, "search",
                _keyword, _option),
            _export_url = "{0}/{1}/{2}/{3}/{4}".format(_u.api.avatar, "export",
                "search", _keyword, _option);
        $.get(_search_url)
            .done(function (response, textStatus, jqXHR) {
                _tableHeader.nextAll().remove();
                _tableHeader.after(response);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
        _avtListEle.find("a").attr("href", _export_url);
    };
    _avatar.detail.prototype.getDetailFormWithValue = function (avatarId) {
        $.get(_u.api.avatar + "/" + avatarId + "/form")
            .done(function (response, textStatus, jqXHR) {
                _avtDetailEle.html(response);
                if (_avtDetailEle.is(".off")) {
                    _avtDetailEle.show();
                    _avtDetailEle.removeClass("off").addClass("on");
                }
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _avatar.detail.prototype.resetBtnTapped = function (currEle) {
        if (currEle.is(".new")) {
            _avtDetailEle.load(_u.api.avatar + "/form");
        } else if (currEle.is(".selected")) {
            let _avatarId = _avtDetailEle.find(".delegate-item").data("id");
            _avatar.detail.prototype.getDetailFormWithValue(_avatarId)
        }
    };
    _avatar.detail.prototype.updateBtnTapped = function () {
        let _avatarId = _avtDetailEle.find("div.delegate-item").data("id"),
            _form = _avtDetailEle.find("form").serializeIncludeDisabled();
        $.put(_u.api.avatar + "/" + _avatarId + "/form", _form)
            .done(function (response, textStatus, jqXHR) {
                alert(response.message);
                location.reload();
            })
            .fail(function (response) {
                _f.htmlFailResponse(response,
                    _avtDetailEle.find(".message-fail"));
            });
    };
    _avatar.detail.prototype.deleteBtnTapped = function () {
        let _avatarId = _avtDetailEle.find(".delegate-item").data("id"),
            _del_key = _avtDetailEle.find("input#delete_key").val(),
            _param = $.param({del_key: _del_key});
        $.delete(_u.api.avatar + "/" + _avatarId, _param)
            .done(function (response, textStatus, jqXHR) {
                location.reload();
            })
            .fail(function (response) {
                _f.htmlFailResponse(response,
                    _avtDetailEle.find("div.message-fail"));
            });
    };

    /*=========================================================================
    Event delegation map
    =========================================================================*/
    _avtListEle.on(
        "click",
        "div.tr, .btn-submit",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is("div.tr")) {
                _avatar.list.prototype.tableRowTapped(_currEle)
            } else if (_currEle.is(".btn-submit")) {
                _avatar.list.prototype.upLoadSingleFile(_currEle)
            }
        });
    _avtListEle.on(
        "change",
        ".select-option, .select-upload, .select-search",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is(".select-option")) {
                _avatar.list.prototype.optionSelected(_currEle)
            } else if (_currEle.is(".select-upload")) {
                _avatar.list.prototype.uploadOptSelected(_currEle)
            } else if (_currEle.is(".select-search")) {
                _avatar.list.prototype.searchOptionSelected(_currEle)
            }
        });
    _avtListEle.on("keypress", ".search-avatar", function (event) {
        let _currEle = $(this);
        if (_currEle.is(".search-avatar")) {
            let _keyCode = (event.keyCode ? event.keyCode : event.which);
            if (_keyCode === 13) {
                _avatar.list.prototype.searchEnterKeyTapped(_currEle);
            }
        }
    });
    _avtDetailEle.on(
        "click",
        ".bt-update, .bt-delete, .bt-reset",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is(".bt-update")) {
                _avatar.detail.prototype.updateBtnTapped()
            } else if (_currEle.is(".bt-delete")) {
                _avatar.detail.prototype.deleteBtnTapped()
            } else if (_currEle.is(".bt-reset")) {
                _avatar.detail.prototype.resetBtnTapped(_currEle)
            }
        });
});