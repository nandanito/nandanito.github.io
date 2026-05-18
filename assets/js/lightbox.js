// Image lightbox for /writing/ and /writing/notes/ post pages.
// Conditionally loaded by _includes/scripts.html — present only on
// pages whose category is "writing" or "notes". Wraps every <figure>
// image with a click handler that opens it inside the native <dialog>
// element. ESC-to-close, focus trap, and modal a11y come from the
// browser's <dialog> implementation. No third-party dependencies.

(function () {
  'use strict';

  var figures = document.querySelectorAll('article figure img');
  if (figures.length === 0) return;

  // Build the dialog once and reuse it across all image opens.
  var dialog = document.createElement('dialog');
  dialog.className = 'lightbox';
  dialog.setAttribute('aria-label', 'Enlarged image');
  dialog.innerHTML =
    '<button class="lightbox-close" type="button" aria-label="Close enlarged image">&times;</button>' +
    '<img class="lightbox-image" alt="">' +
    '<figcaption class="lightbox-caption"></figcaption>';
  document.body.appendChild(dialog);

  var lbImage = dialog.querySelector('.lightbox-image');
  var lbCaption = dialog.querySelector('.lightbox-caption');
  var lbClose = dialog.querySelector('.lightbox-close');

  function openLightbox(img) {
    lbImage.src = img.currentSrc || img.src;
    lbImage.alt = img.alt || '';
    var fig = img.closest('figure');
    var cap = fig ? fig.querySelector('figcaption') : null;
    if (cap && cap.textContent.trim()) {
      lbCaption.textContent = cap.textContent.trim();
      lbCaption.style.display = '';
    } else {
      lbCaption.textContent = '';
      lbCaption.style.display = 'none';
    }
    if (typeof dialog.showModal === 'function') {
      dialog.showModal();
    } else {
      // Very old browser fallback — open the image in a new tab.
      window.open(img.src, '_blank', 'noopener,noreferrer');
    }
  }

  // Open on click.
  figures.forEach(function (img) {
    img.addEventListener('click', function () {
      openLightbox(img);
    });
    // Also keyboard-trigger: make images focusable via tab so users
    // pressing Enter/Space can open them.
    img.setAttribute('tabindex', '0');
    img.setAttribute('role', 'button');
    img.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openLightbox(img);
      }
    });
  });

  // Close on backdrop click (clicking the dialog element itself, not
  // its children). The image and caption stop propagation so clicks
  // inside don't close.
  dialog.addEventListener('click', function (e) {
    if (e.target === dialog) dialog.close();
  });
  lbImage.addEventListener('click', function (e) { e.stopPropagation(); });
  lbCaption.addEventListener('click', function (e) { e.stopPropagation(); });

  // Close button.
  lbClose.addEventListener('click', function () { dialog.close(); });
})();
