<script>
  export let queryParams;
  import Fuse from "fuse.js";
  import foods from "./food-scores.js";

  let results = [];

  const levels = new Map([
    [
      9,
      {
        label: "Very High",
        tag: "very-high",
        lightColor: "#EF89A4",
      },
    ],
    [7, { label: "High", tag: "high", lightColor: "#e7aa90" }],
    [
      5,
      {
        label: "Moderate",
        tag: "moderate",
        lightColor: "#f8fae0",
      },
    ],
    [3, { label: "Low", tag: "low", lightColor: "#deefe0" }],
    [
      1,
      {
        label: "Very low",
        tag: "very-low",
        lightColor: "#c2d7e8",
      },
    ],
  ]);

  const resultTags = new Map([
    [0, "first-result"],
    [1, "second-result"],
    [2, "third-result"],
    [3, "fourth-result"],
    [4, "fifth-result"],
  ]);

  let searchString =
    queryParams.get("food") == null ? "" : queryParams.get("food");

  const fuse = new Fuse(foods, {
    isCaseSensitive: false,
    includeScore: true,
    keys: ["name"],
  });
  search();

  $: {
    if (searchString === "") {
      queryParams.delete("food");
      window.history.replaceState({}, "", `${location.pathname}`);
    } else {
      queryParams.set("food", searchString);
      window.history.replaceState(
        {},
        "",
        `${location.pathname}?${queryParams.toString()}`
      );
    }
    search();
  }

  function search() {
    results = fuse
      .search(searchString)
      .splice(0, 5)
      .filter((result) => result.score < 0.4);
    if (results.length > 0) {
      document.body.style.backgroundColor = levels.get(
        results[0].item.score
      ).lightColor;
    } else {
      document.body.style.backgroundColor = "white";
    }
    console.log(results);
  }
</script>

<main>
  <div class="prompt">
    <h3 class="prompt-text prompt-text-left">Is</h3>
    <input
      class="prompt-text prompt-input"
      bind:value={searchString}
      autofocus
    />
    <h3 class="prompt-text prompt-text-right">high in salicylates?</h3>
  </div>
  {#if searchString !== "" && results.length == 0}
    <p>Sorry, no results were found.</p>
  {/if}
  {#each results as result, i}
    <div class="result {levels.get(result.item.score).tag} {resultTags.get(i)}">
      {result.item.name}: {levels.get(result.item.score).label}
    </div>
  {/each}
  <small>
    The content on this website is not intended to be a substitute for
    professional medical advice, diagnosis or treatment. The data source is <a
      href="https://atpscience.com/salicylate-foods-sensitivity-intolerances-and-food-list/"
      >just stuff on the internet</a
    >. Questions?
    <a href="https://twitter.com/hbradio">Message me on Twitter.</a>
  </small>
</main>

<style>
  main {
    padding: 1em;
    max-width: 600px;
    margin: 0 auto;
  }

  .result {
    margin-bottom: 1em;
    border-radius: 10px;
    padding: 0.2em;
  }

  .first-result {
    font-size: 2.441em;
    margin-block-start: 0;
    box-shadow: 10px 10px 5px rgba(0, 0, 0, 0.3);
  }
  .second-result {
    font-size: 1.953em;
  }

  .very-high {
    color: white;
    background-color: #8d1333;
  }
  .high {
    color: white;
    background-color: #dd855f;
  }
  .moderate {
    background-color: #f4f7c6;
  }
  .low {
    background-color: #9bd0a2;
  }
  .very-low {
    color: white;
    background-color: #4078a6;
  }

  .prompt {
    margin-bottom: 2em;
  }

  .prompt-text {
    display: inline;
  }

  .prompt-text-left {
    margin-right: 0.5em;
  }

  .prompt-text-right {
    margin-left: 0.5em;
  }

  .prompt-input {
    font-size: 1.953rem;
    width: 6em;
  }
</style>
