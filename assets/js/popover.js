(function () {
  var openPopover = null;
  var openButton = null;
  var hoverTimer = null;
  var popoverCounter = 0;

  function closePopover() {
    if (openPopover) {
      openPopover.remove();
      openPopover = null;
    }
    if (openButton) {
      openButton.setAttribute('aria-expanded', 'false');
      openButton.removeAttribute('aria-describedby');
      openButton = null;
    }
  }

  function showPopover(btn) {
    closePopover();

    var note = btn.getAttribute('data-note');
    if (!note) return;

    var id = 'info-popover-' + (++popoverCounter);
    var pop = document.createElement('div');
    pop.className = 'info-popover';
    pop.id = id;
    pop.setAttribute('role', 'tooltip');
    pop.textContent = note;

    // Position relative to the document, anchored below-right of the button
    document.body.appendChild(pop);
    var rect = btn.getBoundingClientRect();
    var scrollX = window.pageXOffset || document.documentElement.scrollLeft;
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;
    pop.style.left = (rect.left + scrollX) + 'px';
    pop.style.top = (rect.bottom + scrollY + 4) + 'px';

    btn.setAttribute('aria-expanded', 'true');
    btn.setAttribute('aria-describedby', id);

    openPopover = pop;
    openButton = btn;
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Delegated click: toggle popover on button click
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('.info-toggle');
      if (btn) {
        e.stopPropagation();
        if (openButton === btn) {
          closePopover();
        } else {
          showPopover(btn);
        }
        return;
      }
      // Click outside closes any open popover
      closePopover();
    });

    // Escape key closes popover
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        closePopover();
      }
    });

    // Hover: show on mouseenter, hide on mouseleave (with small delay to allow
    // moving the cursor from button to popover without it closing)
    document.addEventListener('mouseover', function (e) {
      var btn = e.target.closest('.info-toggle');
      if (btn) {
        clearTimeout(hoverTimer);
        if (openButton !== btn) {
          showPopover(btn);
        }
      }
    });

    document.addEventListener('mouseout', function (e) {
      var btn = e.target.closest('.info-toggle');
      if (btn) {
        hoverTimer = setTimeout(function () {
          // Only close if the cursor didn't move to the popover
          if (openPopover && !openPopover.matches(':hover')) {
            closePopover();
          }
        }, 150);
      }
    });
  });
})();
