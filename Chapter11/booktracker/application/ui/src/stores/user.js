import { writable } from "svelte/store";

const nullUser = {};

function createCurrentUser() {
    const { subscribe, set, update } = writable(nullUser);
    return {
        subscribe,
        set,
        update,
        logout: () => {
            set(nullUser);
        },
        login: (response) => {
            console.log(`Logged in as...`, response);
            set({
                ...response,
            });
        },
    };
}

const currentUser = createCurrentUser();
export { currentUser };
