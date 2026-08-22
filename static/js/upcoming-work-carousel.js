"use strict";
const REDUCED_MOTION_QUERY = '(prefers-reduced-motion: reduce)';
function initializeCarousel(carousel) {
    const previousButton = carousel.querySelector('[data-carousel-previous]');
    const nextButton = carousel.querySelector('[data-carousel-next]');
    const track = carousel.querySelector('[data-carousel-track]');
    const cards = Array.from(carousel.querySelectorAll('[data-carousel-card]'));
    const reducedMotionQuery = window.matchMedia(REDUCED_MOTION_QUERY);
    if (!previousButton || !nextButton || !track || cards.length < 2) {
        return;
    }
    let isTransitioning = false;
    const commitTrackPosition = () => {
        // Forces the reordered, no-transition state to render before the next slide begins.
        void track.offsetWidth;
    };
    const resetTrack = (reorderCards) => {
        const finish = () => {
            track.style.transition = 'none';
            reorderCards();
            carousel.dataset.carouselIndex = '0';
            commitTrackPosition();
            track.style.transition = '';
            isTransitioning = false;
        };
        if (reducedMotionQuery.matches) {
            finish();
            return;
        }
        track.addEventListener('transitionend', finish, { once: true });
    };
    previousButton.addEventListener('click', () => {
        if (isTransitioning) {
            return;
        }
        isTransitioning = true;
        track.style.transition = 'none';
        track.prepend(track.lastElementChild);
        carousel.dataset.carouselIndex = '1';
        commitTrackPosition();
        track.style.transition = '';
        carousel.dataset.carouselIndex = '0';
        resetTrack(() => undefined);
    });
    nextButton.addEventListener('click', () => {
        if (isTransitioning) {
            return;
        }
        isTransitioning = true;
        carousel.dataset.carouselIndex = '1';
        resetTrack(() => track.append(track.firstElementChild));
    });
    carousel.dataset.carouselIndex = '0';
}
document.querySelectorAll('[data-carousel]').forEach(initializeCarousel);
