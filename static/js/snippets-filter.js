document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('snippets-search');
  const searchCount = document.getElementById('search-count');
  const content = document.getElementById('snippets-content');

  if (!searchInput || !content) return;

  // Group snippets: each snippet is an H3 + all elements until next H3 or HR
  function getSnippets() {
    const snippets = [];
    const children = Array.from(content.children);
    let currentSnippet = null;

    children.forEach((element) => {
      if (element.tagName === 'H3') {
        // Start a new snippet
        if (currentSnippet) {
          snippets.push(currentSnippet);
        }
        currentSnippet = {
          title: element,
          elements: [element],
          text: element.textContent.toLowerCase()
        };
      } else if (element.tagName === 'HR') {
        // HR marks the end of a snippet
        if (currentSnippet) {
          currentSnippet.elements.push(element);
          snippets.push(currentSnippet);
          currentSnippet = null;
        }
      } else if (currentSnippet) {
        // Add element to current snippet
        currentSnippet.elements.push(element);
        currentSnippet.text += ' ' + element.textContent.toLowerCase();
      }
    });

    // Don't forget the last snippet if there's no trailing HR
    if (currentSnippet) {
      snippets.push(currentSnippet);
    }

    return snippets;
  }

  const snippets = getSnippets();
  const totalSnippets = snippets.length;

  // Update count display
  function updateCount(visibleCount) {
    if (visibleCount === totalSnippets) {
      searchCount.textContent = `Showing all ${totalSnippets} snippets`;
    } else {
      searchCount.textContent = `Showing ${visibleCount} of ${totalSnippets} snippets`;
    }
  }

  // Initial count
  updateCount(totalSnippets);

  // Filter function
  function filterSnippets() {
    const query = searchInput.value.toLowerCase().trim();
    let visibleCount = 0;

    snippets.forEach((snippet) => {
      const matches = !query || snippet.text.includes(query);

      snippet.elements.forEach((element) => {
        element.style.display = matches ? '' : 'none';
      });

      if (matches) {
        visibleCount++;
      }
    });

    updateCount(visibleCount);
  }

  // Listen to input events
  searchInput.addEventListener('input', filterSnippets);

  // Also listen to keyup for better responsiveness
  searchInput.addEventListener('keyup', filterSnippets);

  // Focus on search input when user presses '/' key (common shortcut)
  document.addEventListener('keydown', function(e) {
    if (e.key === '/' && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
    }
  });
});
