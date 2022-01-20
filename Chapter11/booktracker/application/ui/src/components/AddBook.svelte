<script>
    export let baseURL;
    import { createEventDispatcher } from "svelte";
    import Keydown from "svelte-keydown";
    import AutoComplete from "./Autocomplete.svelte";
    import { createBook } from "../utils/actions";
    import { derived, writable } from "svelte/store";

    let isActive = true;

    const text = {
        shouldCreateBook: "Book doesn't exist? Click to create a new one.",
        shouldCreateAuthor: "Author doesn't exist? Click to create a new one.",
        shouldCreateSeries:
            "Book series doesn't exist? Click to create a new one.",
    };
    const dispatch = createEventDispatcher();
    const selectedAuthor = writable({});
    const selectedSeries = writable({});
    const selectedBook = writable({});

    const savable = derived(
        [selectedBook, selectedAuthor],
        ([$selectedBook, $selectedAuthor]) => {
            return $selectedBook.ready && $selectedAuthor.ready;
        }
    );
    const continuable = derived(selectedBook, ($selectedBook) => {
        return !!$selectedBook.ready && !$selectedBook.eid;
    });

    async function searchBooks(keyword) {
        const url = `${baseURL}/api/v1/books?title=${keyword}`;
        const response = await fetch(url);
        return (await response.json()).books;
    }

    async function searchAuthors(keyword) {
        const url = `${baseURL}/api/v1/authors?name=${keyword}`;
        const response = await fetch(url);
        return (await response.json()).authors;
    }

    async function searchSeries(keyword) {
        const url = `${baseURL}/api/v1/books/series?name=${keyword}`;
        const response = await fetch(url);
        return (await response.json()).series;
    }

    async function handleCreateBook() {
        await createBook(
            baseURL,
            $selectedBook.eid ? $selectedBook.eid : $selectedBook.title,
            $selectedAuthor.eid ? $selectedAuthor.eid : $selectedAuthor.name,
            $selectedSeries.eid ? $selectedSeries.eid : $selectedSeries.name,
            !!$selectedBook.eid,
            !!$selectedAuthor.eid,
            !!$selectedSeries.eid
        );
        dispatch("bookCreated");
        reset();
    }
    selectedBook.subscribe((selected) => {
        if (selected.item && selected.item.author) {
            selectedAuthor.set({
                ...selected.item.author,
                ready: true,
            });
        }
    });

    function reset() {
        isActive = false;
        selectedBook.set({});
        selectedAuthor.set({});
        selectedSeries.set({});
    }
</script>

<Keydown paused={!isActive} on:Escape={() => (isActive = false)} />
<button class="button" on:click={() => (isActive = !isActive)}>
    <span class="icon">
        <i class="fas fa-plus" />
    </span>
    <span>Add a book</span>
</button>
<div class="modal" class:is-active={isActive}>
    <div class="modal-background" />
    <div class="modal-card">
        <header class="modal-card-head">
            <p class="modal-card-title">Add a book</p>
            <button
                class="delete"
                aria-label="close"
                on:click={() => (isActive = false)}
            />
        </header>
        <section class="modal-card-body">
            <div class="field">
                <label class="label required" for="bookName">Title</label>
                <AutoComplete
                    searchFunction={searchBooks}
                    selectedItem={selectedBook}
                    text={text.shouldCreateBook}
                    placeholder="Python Web Development with Sanic"
                    icon="fas fa-book"
                    prop="title"
                    display={(book) => `${book.title}`}
                    enabled={true}
                    onReset={() => {
                        selectedAuthor.set({});
                        selectedSeries.set({});
                    }}
                />
            </div>
            <div class="field">
                <label class="label required" for="authorName">Author</label>
                <AutoComplete
                    searchFunction={searchAuthors}
                    selectedItem={selectedAuthor}
                    text={text.shouldCreateAuthor}
                    placeholder="Adam Hopkins"
                    icon="fas fa-user"
                    prop="name"
                    display={(author) => `${author.name}`}
                    enabled={$continuable}
                />
            </div>
            <div class="field">
                <label class="label" for="seriesName">Series</label>
                <AutoComplete
                    searchFunction={searchSeries}
                    selectedItem={selectedSeries}
                    text={text.shouldCreateSeries}
                    icon="fas fa-list"
                    prop="name"
                    display={(series) => `${series.name}`}
                    enabled={$continuable}
                />
            </div>
        </section>
        <footer class="modal-card-foot">
            <button
                class="button is-success"
                on:click={handleCreateBook}
                disabled={!$savable}
            >
                Save
            </button>
            <button class="button" on:click={reset}> Cancel </button>
        </footer>
    </div>
</div>

<style>
    :global(.hide-arrow::after) {
        display: none !important;
    }
    :global(.autocomplete-clear-button) {
        color: #333;
    }
    :global(.autocomplete-list-item-create) {
        color: #999999;
        cursor: pointer;
    }
    .modal-card {
        max-height: initial;
        height: 500px;
    }
</style>
