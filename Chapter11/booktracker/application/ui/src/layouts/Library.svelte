<script>
    import { onMount } from "svelte";
    export let baseURL;
    import AddBook from "../components/AddBook.svelte";
    import { fetchBooks } from "../utils/actions";
    import { books } from "../stores/book";
    import BookState from "../components/BookState.svelte";
    import Love from "../components/Love.svelte";
    import Reading from "../components/Reading.svelte";
    import AddPyWebDev from "../components/AddPyWebDev.svelte";

    let getBooks;

    const doFetchBooks = () => {
        getBooks = fetchBooks(baseURL);
    };

    onMount(doFetchBooks);
</script>

<h2 class="title is-2">My Library</h2>
<div class="columns">
    <div class="column is-half">
        <h3 class="title is-4">Books I have</h3>
        <div class="container">
            <AddBook {baseURL} on:bookCreated={doFetchBooks} />
            <AddPyWebDev {baseURL} on:bookCreated={doFetchBooks} />
        </div>
        <div class="list has-visible-pointer-controls has-overflow-ellipsis">
            {#await getBooks}
                loading
            {:then}
                {#each $books as book}
                    <div class="list-item">
                        <Love
                            {baseURL}
                            isLoved={book.is_loved}
                            eid={book.eid}
                        />
                        <div class="list-item-content">
                            <div class="list-item-title" title={book.title}>
                                {book.title}
                                {#if book.series}
                                    <small>{book.series.name}</small>
                                {/if}
                            </div>
                            <div class="list-item-description">
                                By {book.author.name}
                            </div>
                        </div>
                        <div class="list-item-controls">
                            <BookState
                                {baseURL}
                                state={book.state}
                                eid={book.eid}
                            />
                        </div>
                    </div>
                {/each}
            {/await}
        </div>
    </div>
    <div class="column is-half">
        <h3 class="title is-4">Books I am reading</h3>
        <Reading />
    </div>
</div>

<style>
    .list {
        min-height: 400px;
        overflow-y: auto;
    }
    .list-item-title small {
        font-weight: 200;
        color: #7a7a7a;
    }
</style>
