<script>
    export let baseURL;
    export let eid;
    export let state;
    import { get, writable, derived } from "svelte/store";
    import { books } from "../stores/book";
    import { setBookState } from "../utils/actions";

    const states = ["unread", "reading", "read"];
    const current = writable(states.indexOf(state));

    function titleCase(str) {
        if (!str) return "";
        return str
            .toLowerCase()
            .split(" ")
            .map(function (word) {
                return word.charAt(0).toUpperCase() + word.slice(1);
            })
            .join(" ");
    }

    async function move() {
        let newState;
        const idx = get(current);
        let next = idx + 1;
        if (next >= states.length) {
            next = 0;
        }
        current.set(next);

        books.update((x) => {
            x.forEach((y, xidx) => {
                if (y.eid === eid) {
                    newState = states[next];
                    x[xidx].state = newState;
                }
            });
            return x;
        });

        await setBookState(baseURL, eid, newState);
    }

    const display = derived(current, ($current) => {
        const displayState = states[$current];
        return {
            state: titleCase(displayState),
            class:
                $current === 2
                    ? "is-success"
                    : $current === 1
                    ? "is-info"
                    : "is-black",
            icon:
                $current === 2
                    ? "fas fa-check-circle"
                    : $current === 1
                    ? "fas fa-circle"
                    : "far fa-circle",
        };
    });
</script>

<div class="tags has-addons is-clickable" on:click={move}>
    <span class="tag is-dark">{$display.state}</span>
    <span class={`tag ${$display.class}`}><i class={$display.icon} /></span>
</div>

<style>
    .tag.is-dark:hover {
        background-color: #4a4a4a;
    }
</style>
