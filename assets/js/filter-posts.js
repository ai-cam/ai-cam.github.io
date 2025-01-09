document.addEventListener('DOMContentLoaded', function() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const posts = document.querySelectorAll('.posts__item');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');

            const category = btn.dataset.category;

            posts.forEach(post => {
                if (category === 'all') {
                    post.style.display = 'block';
                } else {
                    const postCategories = post.dataset.categories.split(',');
                    post.style.display = postCategories.includes(category) ? 'block' : 'none';
                }
            });
        });
    });
}); 