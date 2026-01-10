function filterBooks(category) {
  const sections = document.querySelectorAll("section");

  sections.forEach(section => {
    section.style.display =
      category === "all" || section.dataset.category === category
        ? "block"
        : "none";
  });
}
