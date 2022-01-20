<script>
    import { derived, writable } from "svelte/store";

    export let text;
    export let icon;
    export let placeholder;
    export let searchFunction;
    export let display;
    export let prop;
    export let enabled = false;
    export let selectedItem;
    export let onReset;
    import { onMount } from "svelte";

    import debounce from "../utils/debounce";

    let inputValue;
    let items;
    let inputElement;
    const isLoading = writable(false);
    const isOpen = writable(false);
    const isEnabled = writable(enabled);
    const allowed = writable(true);
    const canType = derived([isEnabled, allowed], ([$isEnabled, $allowed]) => {
        return $isEnabled && $allowed;
    });

    onMount(() => {
        selectedItem.subscribe((item) => {
            if (
                item.ready === undefined &&
                item[prop] === undefined &&
                item.eid === undefined
            ) {
                reset();
            }
            if (
                item[prop] &&
                item[prop] !== inputValue &&
                inputElement !== document.activeElement
            ) {
                console.log(
                    "Setting in onMount",
                    inputElement,
                    document.activeElement
                );
                inputValue = item[prop];
            }
        });
    });
    const handleBlur = (e) => {
        if (!inputValue || (inputValue && $selectedItem.eid)) {
            isOpen.set(false);
        }
    };
    const handleSearch = async (e) => {
        isLoading.set(true);
        items = await searchFunction(inputValue);
        isOpen.set(true);
        selectedItem.update((x) => {
            x[prop] = inputValue;
            return x;
        });
        isLoading.set(false);
    };

    const selectItem = (item) => {
        selectedItem.update((x) => {
            x.eid = item.eid;
            x.ready = true;
            x.item = item;
            return x;
        });
        if (item.eid) {
            allowed.set(false);
        }
        if (item[prop]) {
            console.log("Setting in selectItem");
            inputValue = item[prop];
        }
        isOpen.set(false);
    };

    const reset = () => {
        console.log("reset");
        isOpen.set(false);
        allowed.set(true);
        inputValue = "";
        selectedItem.set({
            eid: null,
            ready: null,
            [prop]: null,
        });
        if (onReset) {
            onReset();
        }
    };
    $: {
        isEnabled.set(enabled);
    }
</script>

<div class="field has-addons">
    <div
        class="control has-icons-left is-relative is-expanded"
        class:is-loading={$isLoading}
    >
        <input
            class="input"
            type="text"
            id="input"
            {placeholder}
            bind:this={inputElement}
            bind:value={inputValue}
            on:keyup={debounce(handleSearch, 250)}
            on:keydown={() => ($selectedItem.ready = false)}
            on:blur={handleBlur}
            disabled={!$canType}
        />
        {#if icon}
            <span class="icon is-small is-left">
                {#if $selectedItem.ready}
                    <i class="fas fa-check" />
                {:else}
                    <i class={icon} />
                {/if}
            </span>
        {/if}
        {#if items}
            <div class="list" class:is-open={$isOpen}>
                {#each items as item}
                    <div
                        class="list-item is-clickable"
                        on:click={() => selectItem(item)}
                    >
                        <div class="list-item-title">{display(item)}</div>
                    </div>
                {/each}
                <div
                    class="list-item is-clickable has-background-grey-lighter"
                    on:click={() => selectItem({ eid: null })}
                >
                    <div class="list-item-title has-text-grey">{text}</div>
                </div>
            </div>
        {/if}
    </div>
    <div class="control">
        <button
            class="button is-dark"
            disabled={!inputValue || !$isEnabled}
            on:click={reset}
        >
            <i class="fas fa-times" /></button
        >
    </div>
</div>

<style>
    .list {
        display: none;
        position: absolute;
        background-color: #ffffff !important;
        width: 100%;
    }
    .list.is-open {
        display: block;
        z-index: 9;
    }
    .list-item-title {
        color: #2a2a2a;
    }
    .list-item:hover {
        background-color: #ededed;
    }
</style>
