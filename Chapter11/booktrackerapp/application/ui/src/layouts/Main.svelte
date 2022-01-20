<script>
    export let baseURL;
    import { currentUser } from "../stores/user";
    import Library from "./Library.svelte";
</script>

<section class="section">
    <div class="container">
        {#if $currentUser.me}
            <Library {baseURL} />
        {/if}
    </div>
</section>
