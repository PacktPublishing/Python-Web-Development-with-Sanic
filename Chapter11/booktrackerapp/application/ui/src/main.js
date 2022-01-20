import App from "./App.svelte";

const app = new App({
    target: document.body,
    props: { baseURL: "http://localhost:7777" },
});

export default app;
