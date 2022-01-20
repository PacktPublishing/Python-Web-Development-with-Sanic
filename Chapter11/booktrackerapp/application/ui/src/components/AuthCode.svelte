<script>
    export let authCode;
    export let baseURL;

    import Clipboard from "./Clipboard.svelte";

    let authCodeUsed = false;
    let error = false;

    const curlCode = `curl ${baseURL}/api/v1/auth -X POST \\
    -H "Authorization: Code ${authCode}"`;

    const doLogin = async () => {
        authCodeUsed = true;
        const response = await fetch(`${baseURL}/api/v1/auth`, {
            method: "POST",
            headers: {
                authorization: `Code ${authCode}`,
            },
        });
        if (response.status === 200) {
            window.location.href = baseURL;
        } else {
            console.log({ response });
            error = true;
        }
    };
</script>

<section class="section is-large">
    <div class="container">
        <div class="notification is-primary">
            Your GitHub authorization code: <strong>{authCode}</strong>
            <Clipboard value={authCode} />
        </div>
        <div class="block">
            You can either enter the web portal:

            <span class="has-addons">
                {#if authCodeUsed}
                    <button class="button" disabled>
                        Authorization code used
                    </button>
                {:else}
                    <button class="button is-link" on:click={doLogin}>
                        <span>Continue</span>
                        <span class="icon is-small">
                            <i class="fas fa-arrow-alt-circle-right" />
                        </span>
                    </button>
                {/if}
            </span>
        </div>
        <div class="block">
            Or, use the authorization code to retrieve an access token for the
            API:
            <Clipboard value={curlCode} />
            <pre>
                <code>{curlCode}</code>
            </pre>
        </div>
        {#if error}
            <div class="notification is-danger">
                An error occurred while trying to verify your authorization
                code.
                <a
                    href={`${baseURL}/api/v1/auth/github`}
                    class="button is-small"
                >
                    Try again
                </a>
            </div>
        {/if}
    </div>
</section>

<style>
    button,
    .button {
        vertical-align: baseline;
    }
</style>
