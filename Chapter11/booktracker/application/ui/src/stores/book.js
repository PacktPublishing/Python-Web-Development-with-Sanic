import { writable } from "svelte/store";

const books = writable([]);
export { books };
