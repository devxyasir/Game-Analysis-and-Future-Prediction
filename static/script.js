window.onload = function() {
    const predictions = document.querySelectorAll('.prediction');
    predictions.forEach((pred, index) => {
        setTimeout(() => {
            pred.style.opacity = 1;
            pred.style.transform = 'translateY(0)';
        }, index * 200); // Stagger the animations
    });
};
