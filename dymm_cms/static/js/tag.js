$(document).ready(function () {

    /*=========================================================================
    Import Modules
    =========================================================================*/
    let _f = $.base.method,
        _u = $.base.url,
        _loadingImg = $("img.loading"),
        _tagListEle = $("div#bx-tag-list"),
        _tagDetailEle = $("div#bx-tag-detail"),
        _tagStepEle = $("div#bx-tag-step"),
        _tagSetEle = $("div#bx-tag-set"),
        _tagAddEle = $("div#bx-tag-add");

    /*=========================================================================
    Private methods for Tag Application
    =========================================================================*/
    let _tag = {
        list: function () {
        },
        detail: function () {
        },
        step: function () {
        },
        set: function () {
        },
        add: function () {
        }
    };

    _tag.list.prototype.uploadOptSelected = function (currEle) {
        let _form = _tagListEle.find("form.file-form"),
            _option = currEle.find("option:selected").val(),
            _uri = _u.api.tag + "/import/{0}".format(_option);
        _form.attr("action", _uri);
    };
    _tag.list.prototype.upLoadSingleFile = function (currEle) {
        let _form = currEle.parent();
        _loadingImg.show();
        _form.ajaxSubmit(function () {
            location.reload();
            return false;
        });
    };
    _tag.list.prototype.getPickTagTemplate = function (tagId) {
        let _pickedEle = _tagListEle.find(".picked-item");
        $.get(_u.api.tag + "/pick/" + tagId)
            .done(function (response, textStatus, jqXHR) {
                _pickedEle.replaceWith(response)
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.list.prototype.tableRowTapped = function (currEle) {
        let _tagId = currEle.data("id");
        _f.toggleTableOfRows(
            currEle, _u.api.tag + '/' + _tagId + '/sub'
        );
        _tag.list.prototype.getPickTagTemplate(_tagId);
        _tag.detail.prototype.getDetailFormWithValue(_tagId);
        _tag.set.prototype.getSetOfTags(_tagId);
        _tag.step.prototype.closeBtnTapped();
    };
    _tag.list.prototype.resetBtnTapped = function () {
        let _tableHeader = _tagListEle.find("section.tb > header");
        $.get(_u.api.tag)
            .done(function (response, textStatus, jqXHR) {
                _tableHeader.nextAll().remove();
                _tableHeader.after(response);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.list.prototype.optionSelected = function (currEle) {
        let _uri = '',
            _tagId = _tagListEle.find(".picked-item").data("id"),
            _option = currEle.find("option:selected").val();
        if (_tagId === undefined) {
            _uri = _u.api.tag + "/export/" + _option
        } else {
            _uri = _u.api.tag + "/" + _tagId + "/export/" + _option
        }
        _tagListEle.find("a").attr("href", _uri);
    };
    _tag.detail.prototype.getDetailFormWithValue = function (tagId) {
        $.get(_u.api.tag + "/" + tagId + "/form")
            .done(function (response, textStatus, jqXHR) {
                _tagDetailEle.html(response);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.detail.prototype.resetBtnTapped = function (currEle) {
        if (currEle.is(".new")) {
            _tagDetailEle.load(_u.api.tag + "/form");
        } else if (currEle.is(".selected")) {
            let _tagId = _tagDetailEle.find(".delegate-item").data("id");
            _tag.detail.prototype.getDetailFormWithValue(_tagId)
        }
    };
    _tag.detail.prototype.createBtnTapped = function () {
        let _form = _tagDetailEle.find("form").serialize();
        $.post(_u.api.tag + "/form", _form)
            .done(function (response, textStatus, jqXHR) {
                alert(response.message);
                location.reload();
            })
            .fail(function (response) {
                _f.htmlFailResponse(response,
                    _tagDetailEle.find("div.message-fail"));
            });
    };
    _tag.detail.prototype.updateBtnTapped = function () {
        let _tagId = _tagDetailEle.find("div.delegate-item").data("id"),
            _form = _tagDetailEle.find("form").serializeIncludeDisabled();
        $.put(_u.api.tag + "/" + _tagId + "/form", _form)
            .done(function (response, textStatus, jqXHR) {
                alert(response.message);
                location.reload();
            })
            .fail(function (response) {
                _f.htmlFailResponse(response,
                    _tagDetailEle.find(".message-fail"));
            });
    };
    _tag.detail.prototype.deleteBtnTapped = function () {
        let _tagId = _tagDetailEle.find(".delegate-item").data("id"),
            _del_key = _tagDetailEle.find("input#delete_key").val(),
            _param = $.param({del_key: _del_key});
        $.delete(_u.api.tag + "/" + _tagId, _param)
            .done(function (response, textStatus, jqXHR) {
                location.reload();
            })
            .fail(function (response) {
                _f.htmlFailResponse(response,
                    _tagDetailEle.find("div.message-fail"));
            });
    };
    _tag.detail.prototype.newBtnTapped = function () {
        $.get(_u.api.tag + "/form")
            .done(function (response, textStatus, jqXHR) {
                _tagDetailEle.html(response)
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.detail.prototype.class1Selected = function (currEle) {
        let _class1Id = currEle.val(),
            _division1SelectEle = _tagDetailEle.find("#division1_select");
        _tagDetailEle.find("input#class1").val(_class1Id);
        $.get(_u.api.tag + "/" + _class1Id + "/division1")
            .done(function (response, textStatus, jqXHR) {
                _division1SelectEle.html(response);
                if (_class1Id === "0") {
                    _tagDetailEle.find("input#division1").val(0);
                    _tagDetailEle.find("select#division1_select")
                        .trigger("change");
                }
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.detail.prototype.division1Selected = function (currEle) {
        let _class1Id = _tagDetailEle.find("input#class1").val(),
            _division1Id = currEle.val(),
            _division2SelectEle = _tagDetailEle.find(
                "select#division2_select");
        _tagDetailEle.find("input#division1").val(_division1Id);
        $.get(_u.api.tag + "/" + _class1Id + "/" + _division1Id +
            "/division2")
            .done(function (response, textStatus, jqXHR) {
                _division2SelectEle.html(response);
                if (_division1Id === "0") {
                    _tagDetailEle.find("input#division2").val(0);
                    _tagDetailEle.find("select#division2_select")
                        .trigger("change");
                }
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.detail.prototype.division2Selected = function (currEle) {
        let _class1Id = _tagDetailEle.find("input#class1").val(),
            _division1Id = _tagDetailEle.find("input#division1").val(),
            _division2Id = currEle.val(),
            _division3SelectEle = _tagDetailEle.find("select#division3_select");
        _tagDetailEle.find("input#division2").val(_division2Id);
        $.get(_u.api.tag + "/" + _class1Id + "/" + _division1Id +
            "/" + _division2Id + "/division3")
            .done(function (response, textStatus, jqXHR) {
                _division3SelectEle.html(response);
                if (_division2Id === "0") {
                    _tagDetailEle.find("input#division3").val(0);
                    _tagDetailEle.find("select#division3_select")
                        .trigger("change");
                }
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.detail.prototype.division3Selected = function (currEle) {
        let _class1Id = _tagDetailEle.find("input#class1").val(),
            _division1Id = _tagDetailEle.find("input#division1").val(),
            _division2Id = _tagDetailEle.find("input#division2").val(),
            _division3Id = currEle.val(),
            _division4SelectEle = _tagDetailEle.find("select#division4_select");
        _tagDetailEle.find("input#division3").val(_division3Id);
        $.get(_u.api.tag + "/" + _class1Id + "/" + _division1Id +
            "/" + _division2Id + "/" + _division3Id + "/division4")
            .done(function (response, textStatus, jqXHR) {
                _division4SelectEle.html(response);
                if (_division3Id === "0") {
                    _tagDetailEle.find("input#division4").val(0);
                    _tagDetailEle.find("select#division4_select")
                        .trigger("change");
                }
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.detail.prototype.division4Selected = function (currEle) {
        let _division4Id = currEle.val();
        _tagDetailEle.find("input#division4").val(_division4Id);
        if (_division4Id === "0") {
            _tagDetailEle.find("input#division5").val(0);
        }
    };
    _tag.step.prototype.logStep = function () {
        let _tagId = _tagSetEle.find(".delegate-item").data("id");
        $.get(_u.api.tag + "/step/" + _tagId)
            .done(function (response, textStatus, jqXHR) {
                _tagStepEle.find(".wrap-step").append(response);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
        if (_tagStepEle.is(".off")) {
            _tagStepEle.show();
            _tagStepEle.removeClass("off").addClass("on");
        }
    };
    _tag.step.prototype.itemBtnTapped = function (currEle) {
        let _tagId = currEle.data("id"),
            _sortType = _tagSetEle.find("select#sort_select").val();
        _tag.set.prototype.getSetOfTags(_tagId, _sortType);
        _tag.detail.prototype.getDetailFormWithValue(_tagId);
        currEle.nextAll().remove();
        currEle.remove();
    };
    _tag.step.prototype.closeBtnTapped = function () {
        _tagStepEle.find(".bt-close").nextAll().remove();
        if (_tagStepEle.is(".on")) {
            _tagStepEle.hide();
            _tagStepEle.removeClass("on").addClass("off");
        }
    };
    _tag.set.prototype.getSetOfTags = function (superId, sortType) {
        sortType = sortType || "priority";
        $.get(_u.api.tag + "/" + superId + "/set/" + sortType)
            .done(function (response, textStatus, jqXHR) {
                _tagSetEle.html(response);
                if (_tagSetEle.is(".off")) {
                    _tagSetEle.show();
                    _tagSetEle.removeClass("off").addClass("on");
                }
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.set.prototype.tableRowNameTapped = function (currEle) {
        let _tagId = currEle.parent().data("tagId");
        _tag.step.prototype.logStep();
        _tag.detail.prototype.getDetailFormWithValue(_tagId);
        _tag.set.prototype.getSetOfTags(_tagId);
    };
    _tag.set.prototype.closeBtnTapped = function () {
        if (_tagSetEle.is(".on")) {
            _tagSetEle.hide();
            _tagSetEle.removeClass("on").addClass("off");
        }
    };
    _tag.set.prototype.resetBtnTapped = function () {
        let _tagFactId = _tagSetEle.find(".delegate-item").data("id");
        _tag.set.prototype.getSetOfTags(_tagFactId);
    };
    _tag.set.prototype.searchBtnTapped = function () {
        let _tableHeader = _tagAddEle.find("section.tb > header");
        $.get(_u.api.tag + "/add")
            .done(function (response, textStatus, jqXHR) {
                _tableHeader.nextAll().remove();
                _tableHeader.after(response);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
        if (_tagAddEle.is(".off")) {
            _tagAddEle.show();
            _tagAddEle.removeClass("off").addClass("on");
        }
    };
    _tag.set.prototype.delBtnTapped = function (currEle) {
        let _del_key = _tagSetEle.find("#delete_key2").val(),
            _superId = _tagSetEle.find(".delegate-item").data("id"),
            _tagSetId = currEle.parent().data("id"),
            _param = $.param({del_key: _del_key}),
            _url ="{0}/{1}/{2}".format(_u.api.tag, "set", _tagSetId);
        $.delete(_url, _param)
            .done(function (response, textStatus, jqXHR) {
                _tag.set.prototype.getSetOfTags(_superId);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.set.prototype.sortSelected = function (currEle) {
        let _superId = _tagSetEle.find(".delegate-item").data("id"),
            _sortType = currEle.val();
        _tag.set.prototype.getSetOfTags(_superId, _sortType);
    };
    _tag.set.prototype.setTagSetScore = function (tagSetId, priority) {
        let _superId = _tagSetEle.find(".delegate-item").data("id"),
            _sortType = _tagSetEle.find("select#sort_select").val(),
            _uri = _u.api.tag + "/set/" + tagSetId + "/priority";
        if (priority >= 0 && priority !== undefined) {
            _uri = _u.api.tag + "/set/" + tagSetId + "/priority/" + priority
        }
        $.put(_uri)
            .done(function (response, textStatus, jqXHR) {
                _tag.set.prototype.getSetOfTags(_superId, _sortType);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.set.prototype.swapTagSetScores = function (upperId, lowerId) {
        let _superId = _tagSetEle.find(".delegate-item").data("id"),
            _sortType = _tagSetEle.find("select#sort_select").val();
        $.put(_u.api.tag + "/set/" + upperId + "/" + lowerId + "/priority/swap")
            .done(function (response, textStatus, jqXHR) {
                _tag.set.prototype.getSetOfTags(_superId, _sortType);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.set.prototype.upBtnTapped = function (currEle) {
        let _superId = _tagSetEle.find(".delegate-item").data("id"),
            _selected = currEle.parent(),
            _lowerId = _selected.data("id"),
            _upperId = _selected.prev().data("id");
        if (_upperId === undefined) {
            _tag.set.prototype.setTagSetScore(_superId, _lowerId);
            return
        }
        _tag.set.prototype.swapTagSetScores(_upperId, _lowerId);
    };
    _tag.set.prototype.downBtnTapped = function (currEle) {
        let _selected = currEle.parent(),
            _upperId = _selected.data("id"),
            _lowerId = _selected.next().data("id");
        if (_lowerId === undefined) {
            return
        }
        _tag.set.prototype.swapTagSetScores(_upperId, _lowerId);
    };
    _tag.set.prototype.setBtnTapped = function (currEle) {
        let _tagSetId = currEle.parent().data("id");
        _tag.set.prototype.setTagSetScore(_tagSetId);
    };
    _tag.set.prototype.priorityBtnTapped = function (currEle) {
        let _tagSetId = currEle.parent().data("id");
        _tag.set.prototype.setTagSetScore(_tagSetId, 0);
    };
    _tag.set.prototype.tableRowDivisionTapped = function (currEle) {
        let _tagId = currEle.parent().data("tagId"),
            _tableHeader = _tagAddEle.find("section.tb > header");
        $.get(_u.api.tag + "/" + _tagId + "/sub/add")
            .done(function (response, textStatus, jqXHR) {
                _tableHeader.nextAll().remove();
                _tableHeader.after(response);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
        if (_tagAddEle.is(".off")) {
            _tagAddEle.show();
            _tagAddEle.removeClass("off").addClass("on");
        }
    };
    _tag.set.prototype.upImgBtnTapped = function (currEle, dirname, target) {
        let _superId = _tagSetEle.find(".delegate-item").data("id"),
            _form = currEle.parent(),
            _tagId = currEle.parent().parent().parent().data("tagId"),
            _uri = _u.api.asset + "/import/{0}/{1}/{2}".format(dirname,
                target, _tagId);
        _form.attr("action", _uri);
        _form.ajaxSubmit(function () {
            _tag.set.prototype.getSetOfTags(_superId);
            return false;
        });
    };
    _tag.set.prototype.boolBtnTapped = function (currEle, target) {
        let _superId = _tagSetEle.find(".delegate-item").data("id"),
            _tableRow = currEle.parent(),
            _tagSetId = _tableRow.data("id");
        $.put(_u.api.tag + "/set/" + _tagSetId + "/" + target)
            .done(function (response, textStatus, jqXHR) {
                _tag.set.prototype.getSetOfTags(_superId);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.set.prototype.delAllBtnTapped = function () {
        let _del_key = _tagSetEle.find("#delete_key2").val(),
            _superId = _tagSetEle.find(".delegate-item").data("id"),
            _param = $.param({del_key: _del_key}),
            _url = "{0}/{1}/{2}".format(_u.api.tag, _superId, "set");
        $.delete(_url, _param)
            .done(function (response, textStatus, jqXHR) {
                _tag.set.prototype.getSetOfTags(_superId);
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.add.prototype.flipBtnTapped = function (currEle) {
        let _tableRow = currEle.parent(),
            _tagId = _tableRow.data("id");
        _f.toggleTableOfRows(
            _tableRow, _u.api.tag + '/' + _tagId + '/sub/add'
        );
    };
    _tag.add.prototype.addBtnTapped = function (currEle) {
        let _superId = _tagSetEle.find(".delegate-item").data("id"),
            _subId = currEle.parent().data("id"),
            _sortType = _tagSetEle.find("select#sort_select").val();
        $.post(_u.api.tag + "/set/" + _superId + "/" + _subId)
            .done(function (response, textStatus, jqXHR) {
                _tag.set.prototype.getSetOfTags(_superId, _sortType);
                _f.coloringTableOfARow(currEle.parent(),
                    "thistle", "paleturquoise")
            })
            .fail(function (response) {
                _f.alertFailResponse(response);
            });
    };
    _tag.add.prototype.closeBtnTapped = function () {
        if (_tagAddEle.is(".on")) {
            _tagAddEle.hide();
            _tagAddEle.removeClass("on").addClass("off");
        }
    };
    _tag.add.prototype.resetBtnTapped = function () {
        _tagSetEle.find("li.bt-search").trigger("click");
    };

    /*=========================================================================
    Event delegation map
    =========================================================================*/
    _tagListEle.on(
        "click",
        "div.tr, .bt-reset, .btn-submit",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is("div.tr")) {
                _tag.list.prototype.tableRowTapped(_currEle)
            } else if (_currEle.is(".bt-reset")) {
                _tag.list.prototype.resetBtnTapped()
            } else if (_currEle.is(".btn-submit")) {
                _tag.list.prototype.upLoadSingleFile(_currEle)
            }
        });
    _tagListEle.on(
        "change",
        ".select-option, .select-upload",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is(".select-option")) {
                _tag.list.prototype.optionSelected(_currEle)
            } else if (_currEle.is(".select-upload")) {
                _tag.list.prototype.uploadOptSelected(_currEle)
            }
        });
    _tagDetailEle.on(
        "click",
        ".bt-create, .bt-update, .bt-delete, .bt-new, .bt-reset",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is(".bt-create")) {
                _tag.detail.prototype.createBtnTapped()
            } else if (_currEle.is(".bt-update")) {
                _tag.detail.prototype.updateBtnTapped()
            } else if (_currEle.is(".bt-delete")) {
                _tag.detail.prototype.deleteBtnTapped()
            } else if (_currEle.is(".bt-new")) {
                _tag.detail.prototype.newBtnTapped()
            } else if (_currEle.is(".bt-reset")) {
                _tag.detail.prototype.resetBtnTapped(_currEle)
            }
        });
    _tagDetailEle.on(
        "change",
        "select#class1_select, select#division1_select, " +
        "select#division2_select, select#division3_select, " +
        "select#division4_select",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is("select#class1_select")) {
                _tag.detail.prototype.class1Selected(_currEle);
            } else if (_currEle.is("select#division1_select")) {
                _tag.detail.prototype.division1Selected(_currEle);
            } else if (_currEle.is("select#division2_select")) {
                _tag.detail.prototype.division2Selected(_currEle);
            } else if (_currEle.is("select#division3_select")) {
                _tag.detail.prototype.division3Selected(_currEle);
            } else if (_currEle.is("select#division4_select")) {
                _tag.detail.prototype.division4Selected(_currEle);
            }
        });
    _tagStepEle.on(
        "click",
        ".bt-item, .bt-close",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is(".bt-item")) {
                _tag.step.prototype.itemBtnTapped(_currEle);
            } else if (_currEle.is(".bt-close")) {
                _tag.step.prototype.closeBtnTapped();
            }
        });
    _tagSetEle.on(
        "click",
        ".tr-name, .bt-close, .bt-reset, .bt-search, .tr-del, " +
        ".tr-up, .tr-down, .tr-set, .tr-priority, .tr-division, " +
        ".up-img, .is-active, .bt-del",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is(".tr-name")) {
                _tag.set.prototype.tableRowNameTapped(_currEle);
            } else if (_currEle.is(".bt-close")) {
                _tag.set.prototype.closeBtnTapped();
            } else if (_currEle.is(".bt-reset")) {
                _tag.set.prototype.resetBtnTapped();
            } else if (_currEle.is(".bt-search")) {
                _tag.set.prototype.searchBtnTapped();
            } else if (_currEle.is(".tr-del")) {
                _tag.set.prototype.delBtnTapped(_currEle);
            } else if (_currEle.is(".tr-up")) {
                _tag.set.prototype.upBtnTapped(_currEle);
            } else if (_currEle.is(".tr-down")) {
                _tag.set.prototype.downBtnTapped(_currEle);
            } else if (_currEle.is(".tr-set")) {
                _tag.set.prototype.setBtnTapped(_currEle);
            } else if (_currEle.is(".tr-priority")) {
                _tag.set.prototype.priorityBtnTapped(_currEle);
            } else if (_currEle.is(".tr-division")) {
                _tag.set.prototype.tableRowDivisionTapped(_currEle);
            } else if (_currEle.is(".up-img")) {
                _tag.set.prototype.upImgBtnTapped(_currEle, 'category', 'png');
            } else if (_currEle.is(".is-active")) {
                _tag.set.prototype.boolBtnTapped(_currEle, "is-active");
            } else if (_currEle.is(".bt-del")) {
                _tag.set.prototype.delAllBtnTapped();
            }
        });
    _tagSetEle.on(
        "change",
        "select#sort_select",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is("select#sort_select")) {
                _tag.set.prototype.sortSelected(_currEle);
            }
        });
    _tagAddEle.on(
        "click",
        ".tr-flip, .tr-add, .bt-close, .bt-reset",
        function (e) {
            let _currEle = $(this);
            if (_currEle.is(".tr-flip")) {
                _tag.add.prototype.flipBtnTapped(_currEle);
            } else if (_currEle.is(".tr-add")) {
                _tag.add.prototype.addBtnTapped(_currEle);
            } else if (_currEle.is(".bt-close")) {
                _tag.add.prototype.closeBtnTapped();
            } else if (_currEle.is(".bt-reset")) {
                _tag.add.prototype.resetBtnTapped();
            }
        });
});