<script>
    export let baseURL;

    import Footer from "./layouts/Footer.svelte";
    import Header from "./layouts/Header.svelte";
    import Main from "./layouts/Main.svelte";
    import Nav from "./layouts/Nav.svelte";
    import AuthCode from "./components/AuthCode.svelte";

    const urlSearchParams = new URLSearchParams(window.location.search);
    const authCode = urlSearchParams.get("code");
</script>

<main>
    <Nav {authCode} {baseURL} />
    <Header />
    {#if authCode}
        <AuthCode {authCode} {baseURL} />
    {:else}
        <Main {baseURL} />
    {/if}
    <Footer />
</main>
