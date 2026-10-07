const skillFilter = document.getElementById("skillFilter");
const jobCards = document.querySelectorAll(".job-card");
const resultCount = document.getElementById("resultCount");
const searchForm = document.querySelector(".search-box form");
const searchButton = searchForm
    ? searchForm.querySelector("button")
    : null;


// ------------------------------------
// Skill Filter
// ------------------------------------

if (skillFilter) {

    skillFilter.addEventListener("input", function () {

        const searchSkill = skillFilter.value
            .toLowerCase()
            .trim();

        let visibleCount = 0;

        jobCards.forEach(function (card) {

            const skills = card.dataset.skills || "";

            if (
                searchSkill === "" ||
                skills.includes(searchSkill)
            ) {

                card.style.display = "block";
                visibleCount++;

            } else {

                card.style.display = "none";

            }

        });


        // Update result count

        if (resultCount) {

            resultCount.textContent = visibleCount;

        }

    });

}


// ------------------------------------
// Search Button Loading State
// ------------------------------------

if (searchForm && searchButton) {

    searchForm.addEventListener("submit", function () {

        searchButton.disabled = true;

        searchButton.textContent = "🔎 Searching...";

    });

}