$(document).ready(function () {

    /*=========================================================================
    Import Modules
    =========================================================================*/
    let _f = $.base.method,
        _u = $.base.url,
        _loadingImg = $("img.loading"),
        _avatarListEle = $("div#bx-avatar-list"),
        _avatarDetailEle = $("div#bx-avatar-detail");

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
        let _form = _avatarListEle.find("form.file-form"),
            _option = currEle.find("option:selected").val(),
            _uri = _u.api.avatar + "/import/{0}".format(_option);
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
            _avatarId = _avatarListEle.find(".picked-item").data("id"),
            _option = currEle.find("option:selected").val();
        if (_avatarId === undefined) {
            _uri = _u.api.avatar + "/export/" + _option
        } else {
            _uri = _u.api.avatar + "/" + _avatarId + "/export/" + _option
        }
        _avatarListEle.find("a").attr("href", _uri);
    };
    _avatar.detail.prototype.getDetailFormWithValue = function (avatarId) {
        $.get(_u.api.avatar + "/" + avatarId + "/form")
            .done(function (response, textStatus, jqXHR) {
                _avatarDetailEle.html(response);
                if (_avatarDetailEle.is(".off")) {
                    _avatarDetailEle.show();
                    _avatarDetailEle.removeClass("off").addClass("on");
                }
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _avatar.detail.prototype.resetBtnTapped = function (currEle) {
        if (currEle.is(".new")) {
            _avatarDetailEle.load(_u.api.avatar + "/form");
        } else if (currEle.is(".selected")) {
            let _avatarId = _avatarDetailEle.find(".delegate-item").data("id");
            _avatar.detail.prototype.getDetailFormWithValue(_avatarId)
        }
    };
    _avatar.detail.prototype.updateBtnTapped = function () {
        let _avatarId = _avatarDetailEle.find("div.delegate-item").data("id"),
            _form = _avatarDetailEle.find("form").serializeIncludeDisabled();
        $.put(_u.api.avatar + "/" + _avatarId + "/form", _form)
            .done(function (response, textStatus, jqXHR) {
                alert(response.message);
                location.reload();
            })
            .fail(function (response) {
                _f.htmlFailResponse(response,
                    _avatarDetailEle.find(".message-fail"));
            });
    };
    _avatar.detail.prototype.deleteBtnTapped = function () {
        let _avatarId = _avatarDetailEle.find(".delegate-item").data("id"),
            _del_key = _avatarDetailEle.find("input#delete_key").val(),
            _param = $.param({del_key: _del_key});
        $.delete(_u.api.avatar + "/" + _avatarId, _param)
            .done(function (response, textStatus, jqXHR) {
                location.reload();
            })
            .fail(function (response) {
                _f.htmlFailResponse(response,
                    _avatarDetailEle.find("div.message-fail"));
            });
    };

    /*=========================================================================
    Event delegation map
    =========================================================================*/
    _avatarListEle.on(
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
    _avatarListEle.on(
        "change",
        ".select-option, .select-upload",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is(".select-option")) {
                _avatar.list.prototype.optionSelected(_currEle)
            } else if (_currEle.is(".select-upload")) {
                _avatar.list.prototype.uploadOptSelected(_currEle)
            }
        });
    _avatarDetailEle.on(
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