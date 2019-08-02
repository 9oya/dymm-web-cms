$(document).ready(function () {

    /*
    ===========================================================================
    Import Modules
    ===========================================================================
    */
    let _navItems = $("ul#navigation-bar > li > a"),
        _adminBtns = $("ul.wrap-admin-bt"),
        _pathName = $(location).attr('pathname').split('/')[1],
        _cookie = Cookies.getJSON('dymm_admin');

    if (_cookie === undefined) {
        location.assign('/admin/sign-in');
    }

    /*
    ===========================================================================
    Initializing navigation items and buttons for admin user.
    ===========================================================================
    */
    !(function (pathName, navItems) {
        $.each(navItems, function (i, item) {
            let _item = $(item);
            if (_item.data("path") === _pathName) {
                _item.css("background-color", "white");
                _item.css("color", "#2a557f");
            }
            _item.attr("href", "/" + _item.data('path'));
        });
        $("li.admin-name").text(_cookie.first_name);
    })(_pathName, _navItems);
    let expiration = _cookie.url_token_expiration;
    expiration = moment.tz(expiration, "UTC");
    $('#clock').countdown(expiration.toDate())
        .on('update.countdown', function (event) {
            var format = '%H:%M:%S';
            if (event.offset.minutes < 30) {
                $(this).css("color", "limegreen");
            }
            if (event.offset.minutes < 15) {
                $(this).css("color", "orange");
            }
            if (event.offset.minutes < 5) {
                $(this).css("color", "red");
            }
            $(this).html(event.strftime('%H:%M:%S'));
        })
        .on('finish.countdown', function (event) {
            $(this).text('00:00:00')
        });

    /*
    ===========================================================================
    Prototype properties for private methods
    ===========================================================================
    */
    let top = {
            nav: function () {},
            adminBtns: function () {}
        };

    /*
    ===========================================================================
    private methods for RDA
    ===========================================================================
    */
    top.nav.prototype.naviItempTapped = function () {
        if (Cookies.getJSON('dymm_admin') === undefined) {
            location.assign("/admin/sign-in");
        }
    };
    top.adminBtns.prototype.refreshBtnTapped = function (cookie) {
        let _param = $.param({email: _cookie.email});
        $.post("/api/admin/refresh", _param)
            .done(function (response, textStatus, jqXHR) {
                if (jqXHR.status === 400) {
                    alert(response.message);
                } else if (jqXHR.status === 401) {
                    alert(response.message);
                } else if (jqXHR.status === 200) {
                    Cookies.remove('dymm_admin');
                    let _in30Minutes = 1 / 48;
                    Cookies.set('dymm_url_token', response.data.url_token, {
                        expires: _in30Minutes
                    });
                    Cookies.set('dymm_admin', response.data.admin_info, {
                        expires: _in30Minutes
                    });
                    location.reload();
                } else {
                    alert("Unexpected status code");
                }
            });
    };
    top.adminBtns.prototype.signOutBtnTapped = function () {
        Cookies.remove('dymm_admin');
        Cookies.remove('dymm_url_token');
        location.assign("/admin/sign-in");
    };

    /*
    ===========================================================================
    Event delegation map
    ===========================================================================
    */
    _navItems.on("click", function (e) {
        top.nav.prototype.naviItempTapped();
    });
    _adminBtns.on("click", "li.bt-refresh, li.bt-sign-out",
        function (e) {
            let _currEle = $(this);
            _cookie = Cookies.getJSON('dymm_admin');
            if (_currEle.is("li.bt-refresh")) {
                if (_cookie === undefined) {
                    location.assign('/admin/sign-in');
                }
                top.adminBtns.prototype.refreshBtnTapped(_cookie);
            } else if (_currEle.is("li.bt-sign-out")) {
                top.adminBtns.prototype.signOutBtnTapped();
            }
        })
});