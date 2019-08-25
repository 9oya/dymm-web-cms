$(document).ready(function () {
    let _adminFieldEle = $("div#admin-div"),
        _recentMail = Cookies.getJSON('dymm_admin_recent_mail');

    /*
    ===========================================================================
    Prototype properties for private methods
    ===========================================================================
    */
    let _admin = function () {};

    if (_recentMail !== undefined) {
        _adminFieldEle.find("input#email").val(_recentMail)
    }
    /*
    ===========================================================================
    Private methods for Admin
    ===========================================================================
    */
    _admin.prototype.signIn = function () {
        let _form = _adminFieldEle.find("form#admin-form").serialize(),
            _formEle = _adminFieldEle.find("form#admin-form"),
            _msgFail = _adminFieldEle.find("div.message-fail"),
            _loading = $("img.loading");
        _formEle.hide();
        _msgFail.hide();
        _loading.show();
        $.post("/api/admin/auth", _form)
            .done(function (response, textStatus, jqXHR) {
                if (jqXHR.status !== 200) {
                    alert(_msg.error.network);
                    return false;
                }
                Cookies.remove('dymm_admin');
                let _in30Minutes = 1 / 48;
                Cookies.set('dymm_url_token', response.data.url_token, {
                    expires: _in30Minutes
                });
                Cookies.set('dymm_admin', response.data.admin_info, {
                    expires: _in30Minutes
                });
                Cookies.set('dymm_admin_recent_mail',
                    response.data.admin_info.email,
                    {expires: 7});
                location.assign("/home");
            })
            .fail(function (response) {
                _loading.hide();
                _formEle.show();
                _msgFail.show();
                if (response.status === 400) {
                    _msgFail.text(
                        JSON.stringify(response.responseJSON.message,
                        null, "\t"));
                } else if (response.status === 401) {
                    _msgFail.text(
                        JSON.stringify(response.responseJSON.message,
                        null, "\t"));
                } else if (response.status === 403) {
                    _msgFail.text(
                        JSON.stringify(response.responseJSON.message,
                        null, "\t"));
                } else if (response.status === 500) {
                    alert(_msg.error.server);
                } else {
                    alert(_msg.error.network);
                }
            });
    };
    _admin.prototype.signUp = function () {
        let _form = $("form#admin-form").serialize();
        $.post("/api/admin/new", _form)
            .done(function (response, textStatus, jqXHR) {
                if (jqXHR.status !== 200) {
                    alert(_msg.error.network);
                    return false;
                }
                Cookies.remove('dymm_admin');
                let _in30Minutes = 1 / 48;
                Cookies.set('dymm_url_token', response.data.url_token, {
                    expires: _in30Minutes
                });
                Cookies.set('dymm_admin', response.data.admin_info, {
                    expires: _in30Minutes
                });
                Cookies.set('dymm_admin_recent_mail',
                    response.data.admin_info.email,
                    {expires: 7});
                location.assign("/home");
            })
            .fail(function (response) {
                if (response.status === 400) {
                    _adminFieldEle.find("div.message-fail").text(JSON.stringify(
                        response.responseJSON.message, null, "\t"));
                } else if (response.status === 401) {
                    _adminFieldEle.find("div.message-fail").text(JSON.stringify(
                        response.responseJSON.message, null, "\t"));
                } else if (response.status === 403) {
                    _adminFieldEle.find("div.message-fail").text(JSON.stringify(
                        response.responseJSON.message, null, "\t"));
                } else if (response.status === 500) {
                    alert(_msg.error.server);
                } else {
                    alert(_msg.error.network);
                }
            });
    };

    /*
    ===========================================================================
    Event delegation map
    ===========================================================================
    */
    _adminFieldEle.on("click", "div.bt-sign-in, div.bt-sign-up", function (e) {
        let _currEle = $(this);
        if (_currEle.is("div.bt-sign-in")) {
            _admin.prototype.signIn();
        } else if (_currEle.is("div.bt-sign-up")) {
            _admin.prototype.signUp();
        }
    });
    _adminFieldEle.on("keypress", "input#password", function (event) {
        let _currEle = $(this);
        if (_currEle.is("input#password")) {
            let _keyCode = (event.keyCode ? event.keyCode : event.which);
            if (_keyCode === 13) {
                _adminFieldEle.find("div.bt-sign-in").trigger("click");
            }
        }
    });
});