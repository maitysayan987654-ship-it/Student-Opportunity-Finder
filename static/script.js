const skillFilter = document.getElementById("skillFilter");
const jobCards = document.querySelectorAll(".job-card");
const resultCount = document.getElementById("resultCount");

if (skillFilter) {

    skillFilter.addEventListener("input", function () {

        const searchSkill = skillFilter.value.toLowerCase().trim();

        let visibleCount = 0;

        jobCards.forEach(function (card) {

            const skills = card.dataset.skills || "";

            if (searchSkill === "" || skills.includes(searchSkill)) {

                card.style.display = "block";
                visibleCount++;

            } else {

                card.style.display = "none";

            }

        });

        if (resultCount) {
            resultCount.textContent =
                "Showing " + visibleCount + " opportunities";
        }

    });

}