import { books } from "../stores/book";
import { getCookie } from "../utils/cookie";

async function createBook(
    baseURL,
    title,
    author,
    series,
    titleIsEID,
    authorIsEID,
    seriesIsEID
) {
    const url = `${baseURL}/api/v1/books`;
    await fetch(url, {
        method: "POST",
        body: JSON.stringify({
            title,
            author,
            series,
            title_is_eid: titleIsEID,
            author_is_eid: authorIsEID,
            series_is_eid: seriesIsEID,
        }),
        headers: {
            "content-type": "application/json",
            "x-xsrf-token": getCookie("csrf_token"),
        },
        credentials: "same-origin",
    });
}

async function fetchBooks(baseURL) {
    const url = `${baseURL}/api/v1/books?current_user=true`;
    const response = await fetch(url, {
        headers: {
            "x-xsrf-token": getCookie("csrf_token"),
        },
        credentials: "same-origin",
    });
    const items = (await response.json()).books;
    books.update((x) => {
        const existing = x.map(y => y.eid)
        return [...x, ...items.filter(y => !existing.includes(y.eid))];
    });
}

async function toggleLoveBook(baseURL, bookEID) {
    const url = `${baseURL}/api/v1/books/${bookEID}/love`;
    await fetch(url, {
        method: "PUT",
        headers: {
            "x-xsrf-token": getCookie("csrf_token"),
        },
        credentials: "same-origin"
    });
}

async function setBookState(baseURL, bookEID, state) {
    const url = `${baseURL}/api/v1/books/${bookEID}/state`;
    await fetch(url, {
        method: "PUT",
        body: JSON.stringify({ state }),
        headers: {
            "content-type": "application/json",
            "x-xsrf-token": getCookie("csrf_token"),
        },
        credentials: "same-origin",
    });
}

export { createBook, fetchBooks, toggleLoveBook, setBookState };
