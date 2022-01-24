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
    results = fuse.search(searchString).splice(0, 5).filter(result => result.score < 0.4);
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
  <input bind:value={searchString} />
  {#if searchString !== "" && results.length == 0}
    <p>Sorry, no results were found.</p>
  {/if}
  {#each results as result, i}
    <div class="result {levels.get(result.item.score).tag} {resultTags.get(i)}">
      {result.item.name}: {levels.get(result.item.score).label}
    </div>
  {/each}
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 720px;
    margin: 0 auto;
  }

  .result {
    padding: 0.2em;
  }

  .first-result {
    font-size: 3em;
    font-weight: bold;
    margin-block-start: 0;
  }
  .second-result {
    font-size: 2em;
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
</style>
