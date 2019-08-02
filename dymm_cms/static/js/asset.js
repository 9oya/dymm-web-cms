$(document).ready(function () {

    /*=========================================================================
    Import Modules
    =========================================================================*/
    let _f = $.base.method,
        _u = $.base.url,
        _imgListEle = $("div#bx-asset-list");

    /*=========================================================================
    Private methods for Tag Application
    =========================================================================*/
    let _asset = {
        list: function () {
        }
    };

    _asset.list.prototype.getAssets = function (dirname) {
        $.get(_u.api.asset + "/" + dirname)
            .done(function (response, textStatus, jqXHR) {
                _imgListEle.html(response)
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _asset.list.prototype.renameAsset = function (currEle) {
        let _dirSelect = _imgListEle.find("select#dir_select"),
            _dirname = _dirSelect.find("option:selected").val(),
            _oldName = currEle.parent().data("name").split(".")[0],
            _newName = currEle.val().split(".")[0],
            _uri = "{0}/{1}/{2}/rename/{3}".format(_u.api.asset, _dirname,
                _oldName, _newName);
        $.put(_uri)
            .done(function (response, textStatus, jqXHR) {
                _asset.list.prototype.getAssets(_dirname);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _asset.list.prototype.upLoadSingleFile = function (currEle, target) {
        let _form = currEle.parent(),
            _dirSelect = _imgListEle.find("select#dir_select"),
            _dirname = _dirSelect.find("option:selected").val(),
            _name = currEle.parent().parent().data("name").split(".")[0],
            _tagId = _name.split("-")[1],
            _uri = _u.api.asset + "/import/{0}/{1}/{2}".format(_dirname,
                target, _tagId);
        if (_dirname !== 'category') {
            _uri = _u.api.asset + "/import/{0}/{1}/{2}".format(_dirname,
                target, _name);
        }
        _form.attr("action", _uri);
        _form.ajaxSubmit(function () {
            _asset.list.prototype.getAssets(_dirname);
            return false;
        });
    };
    _asset.list.prototype.upLoadMultiFiles = function (currEle, target) {
        let _form = currEle.parent(),
            _dirSelect = _imgListEle.find("select#dir_select"),
            _dirname = _dirSelect.find("option:selected").val(),
            _uri = _u.api.asset + "/import/{0}/{1}".format(_dirname, target);
        if (_dirname === 'category') {
            alert("Use tag-set-api when upload category images.");
            return false;
        }
        _form.attr("action", _uri);
        _form.ajaxSubmit(function () {
            _asset.list.prototype.getAssets(_dirname);
            return false;
        });
    };
    _asset.list.prototype.deleteAsset = function (currEle, target) {
        let _dirSelect = _imgListEle.find("select#dir_select"),
            _dirname = _dirSelect.find("option:selected").val(),
            _filename = currEle.parent().prev().data("name").split(".")[0];
        $.delete(_u.api.asset + "/{0}/{1}/del/{2}".format(_dirname, _filename,
            target))
            .done(function (response, textStatus, jqXHR) {
                _asset.list.prototype.getAssets(_dirname);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _asset.list.prototype.dirSelectChanged = function (currEle) {
        let _dirname = currEle.val();
        _asset.list.prototype.getAssets(_dirname);
    };
    _asset.list.prototype.pathSelectChanged = function (currEle) {
        let _dirSelect = _imgListEle.find("select#dir_select"),
            _oldDir = _dirSelect.find("option:selected").val(),
            _newDir = currEle.val(),
            _filename = currEle.parent().parent().prev().data("name")
                .split(".")[0];
        if (_newDir === 'category' || _newDir === 'archive') {
            alert("Dir you select is not allowed to move any file.\n" +
                "Use 'Archive.x' button when create zip file.\n" +
                "Use tag-set-api when upload category images.");
            return false;
        }
        $.put(_u.api.asset + "/{0}/{1}/move/{2}".format(_oldDir, _filename,
            _newDir))
            .done(function (response, textStatus, jqXHR) {
                _asset.list.prototype.getAssets(_oldDir);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _asset.list.prototype.archiveBtnTapped = function (currEle, target) {
        let _dirSelect = _imgListEle.find("select#dir_select"),
            _dirname = _dirSelect.find("option:selected").val();
        $.post("{0}/zip/{1}/{2}".format(_u.api.asset, _dirname, target))
            .done(function (response, textStatus, jqXHR) {
                _asset.list.prototype.getAssets('archive');
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };

    /*=========================================================================
    Event delegation map
    =========================================================================*/
    _imgListEle.on(
        "click",
        ".up-pdf, .up-svg, .up-imgs, .del-all, .del-svg, .del-pdf, .del-zip, " +
        ".zip-png, .zip-svg, .zip-pdf",
        function (event) {
            let _currEle = $(this);
            if (_currEle.is(".up-pdf")) {
                _asset.list.prototype.upLoadSingleFile(_currEle, "pdf")
            } else if (_currEle.is(".up-svg")) {
                _asset.list.prototype.upLoadSingleFile(_currEle, "svg")
            } else if (_currEle.is(".up-imgs")) {
                _asset.list.prototype.upLoadMultiFiles(_currEle, "files")
            } else if (_currEle.is(".del-all")) {
                _asset.list.prototype.deleteAsset(_currEle, "all")
            } else if (_currEle.is(".del-svg")) {
                _asset.list.prototype.deleteAsset(_currEle, "svg")
            } else if (_currEle.is(".del-pdf")) {
                _asset.list.prototype.deleteAsset(_currEle, "pdf")
            } else if (_currEle.is(".del-zip")) {
                _asset.list.prototype.deleteAsset(_currEle, "zip")
            } else if (_currEle.is(".zip-png")) {
                _asset.list.prototype.archiveBtnTapped(_currEle, 'png')
            } else if (_currEle.is(".zip-svg")) {
                _asset.list.prototype.archiveBtnTapped(_currEle, 'svg')
            } else if (_currEle.is(".zip-pdf")) {
                _asset.list.prototype.archiveBtnTapped(_currEle, 'pdf')
            }
        });
    _imgListEle.on(
        "change",
        "select#dir_select, select#path_select",
        function (event) {
            let _currEle = $(this);
            if (_currEle.is("select#dir_select")) {
                _asset.list.prototype.dirSelectChanged(_currEle);
            } else if (_currEle.is("select#path_select")) {
                _asset.list.prototype.pathSelectChanged(_currEle);
            }
        });
    _imgListEle.on(
        "keypress",
        ".asset-name",
        function (event) {
            let _currEle = $(this);
            if (_currEle.is(".asset-name")) {
                let _keyCode = (event.keyCode ? event.keyCode : event.which);
                if (_keyCode === 13) {
                    _asset.list.prototype.renameAsset(_currEle);
                }
            }
        });
});