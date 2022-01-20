<script>
    export let baseURL;
    import { createBook } from "../utils/actions";
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    async function addBook() {
        await createBook(
            baseURL,
            "xxdMkXiurxTKkZaiWNJs3F0D",
            "xxdlvO0xjwsrUbooypcZwkJl",
            null,
            true,
            true,
            false
        );
        dispatch("bookCreated");
    }
</script>

<button class="button is-sanic" on:click={addBook}>
    <span class="icon">
        <i class="fas fa-plus" />
    </span>
    <span>Add <strong>PyWebDev w/ Sanic</strong></span>
</button>
