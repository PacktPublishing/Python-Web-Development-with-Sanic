async function sleep(seconds = 1) {
    await new Promise((resolve) => setTimeout(resolve, seconds * 1000));
}
export { sleep };
