<script>
    import { books } from "../stores/book";
    import { derived } from "svelte/store";
    const reading = derived(books, ($books) => {
        return $books.filter((x) => x.state === "reading");
    });
</script>

<div class="box">
    {#each $reading as book}
        {#if book.state === "reading"}
            <span class="tag reading is-info is-large mx-1 my-1">
                {book.title}
            </span>
        {/if}
    {:else}
        <em>None! Time to go pick up a book.</em>
    {/each}
</div>
