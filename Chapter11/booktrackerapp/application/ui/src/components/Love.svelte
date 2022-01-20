<script>
    export let baseURL;
    export let eid;
    export let isLoved;
    import { toggleLoveBook } from "../utils/actions";
    import { books } from "../stores/book";

    const onClick = async () => {
        books.update((x) => {
            x.forEach((y, xidx) => {
                if (y.eid === eid) {
                    console.log(y, isLoved);
                    x[xidx].is_loved = !y.is_loved;
                }
            });
            return x;
        });
        await toggleLoveBook(baseURL, eid);
    };
</script>

<div class="list-item-image is-clickable" on:click={onClick}>
    <i class="fa-heart" class:fas={isLoved} class:far={!isLoved} />
</div>

<style>
    .fas.fa-heart {
        color: #ff0d68;
    }
</style>
