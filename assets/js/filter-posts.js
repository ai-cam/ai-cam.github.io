document.addEventListener('DOMContentLoaded', function() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');

            const category = btn.dataset.category;
            
            // Get all posts except those in no-filter sections
            const posts = document.querySelectorAll('.posts__grid:not(.no-filter) .posts__item');
            const paginationContainer = document.querySelector('.posts__pagination');
            let visiblePosts = 0;

            posts.forEach(post => {
                if (category === 'all') {
                    post.style.display = 'block';
                    visiblePosts++;
                } else {
                    const postCategories = post.dataset.categories.split(',');
                    if (postCategories.includes(category)) {
                        post.style.display = 'block';
                        visiblePosts++;
                    } else {
                        post.style.display = 'none';
                    }
                }
            });

            // Hide pagination if filtering
            if (category !== 'all' && paginationContainer) {
                paginationContainer.style.display = 'none';
            } else if (paginationContainer) {
                paginationContainer.style.display = 'block';
            }
        });
    });
}); 