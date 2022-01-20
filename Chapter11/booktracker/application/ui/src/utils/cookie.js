function getCookie(name) {
    var match = document.cookie.match(
        RegExp("(?:^|;\\s*)" + name + "=([^;]*)")
    );
    return match ? match[1] : null;
}
function deleteCookie(name, path, domain) {
    if (
        document.cookie.split(";").some((c) => c.trim().startsWith(name + "="))
    ) {
        document.cookie =
            name +
            "=" +
            (path ? ";path=" + path : "") +
            (domain ? ";domain=" + domain : "") +
            ";expires=Thu, 01 Jan 1970 00:00:01 GMT";
    }
}
export { getCookie, deleteCookie };
