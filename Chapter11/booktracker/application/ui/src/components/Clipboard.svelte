<script>
    import { tick } from "svelte";

    let valueCopy = null;
    export let value = null;
    let areaDom;
    let message = null;
    let icon = "fa-copy";

    async function copy() {
        valueCopy = value;
        await tick();
        areaDom.focus();
        areaDom.select();
        message = "Copied";
        try {
            const successful = document.execCommand("copy");
            if (!successful) {
                message = "Oops, unable to copy";
                icon = "fa-times";
            } else {
                icon = "fa-check";
                setTimeout(() => {
                    message = null;
                    icon = "fa-copy";
                }, 5000);
            }
        } catch (err) {
            message = "Oops, unable to copy";
            icon = "fa-times";
        }

        valueCopy = null;
    }
</script>

{#if valueCopy != null}
    <textarea bind:this={areaDom}>{valueCopy}</textarea>
{/if}
<span class="icon" on:click={copy} title="Copy to clipboard">
    <i class={`fas ${icon}`} />
</span>
{#if message}
    <em>{message}</em>
{/if}

<style>
    textarea {
        position: fixed;
        top: 0;
        left: 0;
        width: 2em;
        height: 2em;
        padding: 0;
        border: none;
        outline: none;
        box-shadow: none;
        background: transparent;
    }

    span {
        cursor: pointer;
    }
</style>
