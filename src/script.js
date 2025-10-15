const TOAST_SHOW_DURATION = 2600;

function getOrCreateToast() {
  let toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  return toast;
}

function showToast(message) {
  const toast = getOrCreateToast();
  toast.textContent = message;
  toast.classList.add('visible');
  clearTimeout(showToast._timer);
  showToast._timer = setTimeout(() => {
    toast.classList.remove('visible');
  }, TOAST_SHOW_DURATION);
}

async function shareUrl(imagePath) {
  const absoluteUrl = new URL(imagePath, window.location.href).toString();

  if (navigator.share) {
    try {
      await navigator.share({
        url: absoluteUrl,
        title: document.title,
        text: 'Syzygy Gallery — Physics of Faith Visual Archive'
      });
      showToast('Shared via native dialog');
      return;
    } catch (error) {
      if (error.name !== 'AbortError') {
        console.warn('Share failed, falling back to clipboard.', error);
      } else {
        return;
      }
    }
  }

  try {
    await navigator.clipboard.writeText(absoluteUrl);
    showToast('Link copied to clipboard');
  } catch (error) {
    console.warn('Clipboard write failed', error);
    const promptFallback = window.prompt('Copy this link:', absoluteUrl);
    if (promptFallback !== null) {
      showToast('Link ready to share');
    }
  }
}

function wireShareButtons() {
  const buttons = document.querySelectorAll('.share-button[data-share]');
  buttons.forEach(button => {
    button.addEventListener('click', async () => {
      button.disabled = true;
      try {
        await shareUrl(button.dataset.share);
      } finally {
        button.disabled = false;
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  wireShareButtons();
});
