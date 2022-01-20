import { get } from "svelte/store";
import { currentUser } from "../stores/user";
import jwt_decode from "jwt-decode";
import { deleteCookie, getCookie } from "./cookie";

let refreshInterval;

const me = async (baseURL, cookie, skipVerify = false) => {
    const user = get(currentUser);
    if (cookie) {
        if (!skipVerify) {
            const response = await verify(baseURL);
            if (response.status !== 200) {
                const refreshResponse = await refresh(baseURL);
                if (refreshResponse.status !== 200) {
                    deleteCookie("access_token");
                    window.location.href = baseURL;
                }
            }
        }
        if (!user.me) {
            const decoded = jwt_decode(cookie);
            const ttl = (decoded.exp - (Date.now() / 1000))  * 0.75
            if (!refreshInterval) {
                setInterval(refresh, ttl * 1000, baseURL)
            }
            if (decoded.user) {
                currentUser.login({ me: decoded.user });
            }
        }
        return currentUser.me;
    } else {
        await refresh(baseURL);
    }
    return null;
};

const refresh = async (baseURL) => {
    const response = await fetch(`${baseURL}/api/v1/auth/refresh`, {
        method: "POST",
    });
    if (response.status === 200) {
        await me(baseURL, getCookie("access_token"), true);
    } else {
        if (refreshInterval) {
            clearInterval(refreshInterval)
        }
    }
    return response;
};

const verify = async (baseURL) => {
    return await fetch(`${baseURL}/api/v1/auth/verify`);
};

export { me };
