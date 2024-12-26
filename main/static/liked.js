<script>
    let isLiked = false;  // Track whether the song is liked or not.

    function toggleLike() {
        const heartIcon = document.getElementById('heart-icon');
        const likeForm = document.getElementById('like-form');

        if (isLiked) {
            // If already liked, remove 'text-danger' and add 'text-muted' to change color to white
            heartIcon.classList.remove('text-danger');
            heartIcon.classList.add('text-muted');
            isLiked = false;

            // Optionally, you can prevent the form from being submitted immediately, until re-liked
            likeForm.querySelector('button[type="submit"]').disabled = true;
        } else {
            // If not liked, add 'text-danger' to turn the heart red
            heartIcon.classList.remove('text-muted');
            heartIcon.classList.add('text-danger');
            isLiked = true;

            // Enable the submit button
            likeForm.querySelector('button[type="submit"]').disabled = false;
        }
    }
</script>