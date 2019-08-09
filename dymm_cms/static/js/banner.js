$(document).ready(function () {

    /*=========================================================================
    Import Modules
    =========================================================================*/
    let _f = $.base.method,
        _u = $.base.url,
        _loadingImg = $("img.loading"),
        _bannerListEle = $("div#bx-banner-list"),
        _bannerDetailEle = $("div#bx-banner-detail");

    /*=========================================================================
    Private methods for Tag Application
    =========================================================================*/
    let _banner = {
        list: function () {
        },
        detail: function () {
        }
    };

    _banner.list.prototype.uploadOptSelected = function (currEle) {
        let _form = _bannerListEle.find("form.file-form"),
            _option = currEle.find("option:selected").val(),
            _uri = _u.api.banner + "/import/{0}".format(_option);
        _form.attr("action", _uri);
    };
    _banner.list.prototype.upLoadSingleFile = function (currEle) {
        let _form = currEle.parent();
        _loadingImg.show();
        _form.ajaxSubmit(function () {
            location.reload();
            return false;
        });
    };
    _banner.list.prototype.tableRowTapped = function (currEle) {
        let _bannerId = currEle.data("id");
        _f.toggleTableOfRows(
            currEle, _u.api.banner + '/' + _bannerId + '/sub'
        );
        _banner.detail.prototype.getDetailFormWithValue(_bannerId);
    };
    _banner.list.prototype.optionSelected = function (currEle) {
        let _uri = '',
            _bannerId = _bannerListEle.find(".picked-item").data("id"),
            _option = currEle.find("option:selected").val();
        if (_bannerId === undefined) {
            _uri = _u.api.banner + "/export/" + _option
        } else {
            _uri = _u.api.banner + "/" + _bannerId + "/export/" + _option
        }
        _bannerListEle.find("a").attr("href", _uri);
    };
    _banner.detail.prototype.getDetailFormWithValue = function (bannerId) {
        $.get(_u.api.banner + "/" + bannerId + "/form")
            .done(function (response, textStatus, jqXHR) {
                _bannerDetailEle.html(response);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _banner.detail.prototype.resetBtnTapped = function (currEle) {
        if (currEle.is(".new")) {
            _bannerDetailEle.load(_u.api.banner + "/form");
        } else if (currEle.is(".selected")) {
            let _bannerId = _bannerDetailEle.find(".delegate-item").data("id");
            _banner.detail.prototype.getDetailFormWithValue(_bannerId)
        }
    };
    _banner.detail.prototype.createBtnTapped = function () {
        let _form = _bannerDetailEle.find("form").serialize();
        $.post(_u.api.banner + "/form", _form)
            .done(function (response, textStatus, jqXHR) {
                alert(response.message);
                location.reload();
            })
            .fail(function (response) {
                _f.htmlFailResponse(response,
                    _bannerDetailEle.find("div.message-fail"));
            });
    };
    _banner.detail.prototype.updateBtnTapped = function () {
        let _bannerId = _bannerDetailEle.find("div.delegate-item").data("id"),
            _form = _bannerDetailEle.find("form").serializeIncludeDisabled();
        $.put(_u.api.banner + "/" + _bannerId + "/form", _form)
            .done(function (response, textStatus, jqXHR) {
                alert(response.message);
                location.reload();
            })
            .fail(function (response) {
                _f.htmlFailResponse(response,
                    _bannerDetailEle.find(".message-fail"));
            });
    };
    _banner.detail.prototype.deleteBtnTapped = function () {
        let _bannerId = _bannerDetailEle.find(".delegate-item").data("id"),
            _del_key = _bannerDetailEle.find("input#delete_key").val(),
            _param = $.param({del_key: _del_key});
        $.delete(_u.api.banner + "/" + _bannerId, _param)
            .done(function (response, textStatus, jqXHR) {
                location.reload();
            })
            .fail(function (response) {
                _f.htmlFailResponse(response,
                    _bannerDetailEle.find("div.message-fail"));
            });
    };
    _banner.detail.prototype.newBtnTapped = function () {
        $.get(_u.api.banner + "/form")
            .done(function (response, textStatus, jqXHR) {
                _bannerDetailEle.html(response)
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };

    /*=========================================================================
    Event delegation map
    =========================================================================*/
    _bannerListEle.on(
        "click",
        "div.tr, .btn-submit",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is("div.tr")) {
                _banner.list.prototype.tableRowTapped(_currEle)
            } else if (_currEle.is(".btn-submit")) {
                _banner.list.prototype.upLoadSingleFile(_currEle)
            }
        });
    _bannerListEle.on(
        "change",
        ".select-option, .select-upload",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is(".select-option")) {
                _banner.list.prototype.optionSelected(_currEle)
            } else if (_currEle.is(".select-upload")) {
                _banner.list.prototype.uploadOptSelected(_currEle)
            }
        });
    _bannerDetailEle.on(
        "click",
        ".bt-create, .bt-update, .bt-delete, .bt-new, .bt-reset",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is(".bt-create")) {
                _banner.detail.prototype.createBtnTapped()
            } else if (_currEle.is(".bt-update")) {
                _banner.detail.prototype.updateBtnTapped()
            } else if (_currEle.is(".bt-delete")) {
                _banner.detail.prototype.deleteBtnTapped()
            } else if (_currEle.is(".bt-new")) {
                _banner.detail.prototype.newBtnTapped()
            } else if (_currEle.is(".bt-reset")) {
                _banner.detail.prototype.resetBtnTapped(_currEle)
            }
        });
});