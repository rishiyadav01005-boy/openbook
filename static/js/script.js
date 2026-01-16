// Dashboard category filter (corrected & safe)

function filterBooks(category) {
  const titles = document.querySelectorAll(".category-title");

  titles.forEach(title => {
    const grid = title.nextElementSibling; // book-grid
    const categoryName = title.textContent.trim().toLowerCase();

    if (category === "all" || categoryName === category.toLowerCase()) {
      title.style.display = "block";
      if (grid) grid.style.display = "grid";
    } else {
      title.style.display = "none";
      if (grid) grid.style.display = "none";
    }
  });
}
