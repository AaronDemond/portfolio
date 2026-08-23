"use strict";

const previewDialog = document.querySelector('[data-screenshot-preview]');

if (previewDialog instanceof HTMLDialogElement) {
    const previewImage = previewDialog.querySelector('[data-screenshot-preview-image]');
    const previewCaption = previewDialog.querySelector('[data-screenshot-preview-caption]');
    const closeButton = previewDialog.querySelector('[data-screenshot-preview-close]');

    if (
        previewImage instanceof HTMLImageElement
        && previewCaption instanceof HTMLElement
        && closeButton instanceof HTMLButtonElement
    ) {
        document.querySelectorAll('[data-screenshot-preview-trigger]').forEach((trigger) => {
            trigger.addEventListener('click', () => {
                const image = trigger.querySelector('img');
                const caption = trigger.closest('figure')?.querySelector('figcaption');

                if (!(image instanceof HTMLImageElement)) {
                    return;
                }

                previewImage.src = image.currentSrc || image.src;
                previewImage.alt = image.alt;
                previewCaption.textContent = caption?.textContent ?? '';
                previewDialog.showModal();
            });
        });

        closeButton.addEventListener('click', () => previewDialog.close());

        previewDialog.addEventListener('click', (event) => {
            if (event.target === previewDialog) {
                previewDialog.close();
            }
        });

        previewDialog.addEventListener('close', () => {
            previewImage.removeAttribute('src');
            previewImage.alt = '';
            previewCaption.textContent = '';
        });
    }
}
