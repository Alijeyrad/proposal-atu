// Open the offcanvas on large screens
function openOffcanvas(offcanvasInstance) {
    const bootstrapBreakpoint = getBootstrapBreakpoint();
    
    if (bootstrapBreakpoint === 'lg' || bootstrapBreakpoint === 'xl') {
    offcanvasInstance.show();
    }
}

// Close the offcanvas on smaller screens
function closeOffcanvas(offcanvasInstance) {
    const bootstrapBreakpoint = getBootstrapBreakpoint();
    
    if (bootstrapBreakpoint === 'xs' || bootstrapBreakpoint === 'sm' || bootstrapBreakpoint === 'md') {
    offcanvasInstance.hide();
    }
}

// Get the current Bootstrap breakpoint
function getBootstrapBreakpoint() {
    const windowWidth = window.innerWidth;
    if (windowWidth < 576) return 'xs';
    if (windowWidth >= 576 && windowWidth < 768) return 'sm';
    if (windowWidth >= 768 && windowWidth < 992) return 'md';
    if (windowWidth >= 992 && windowWidth < 1200) return 'lg';
    return 'xl';
}

// Open the offcanvas on page load
window.addEventListener('DOMContentLoaded', function() {
    const offcanvasInstance = new bootstrap.Offcanvas('#offcanvas');
    openOffcanvas(offcanvasInstance);

    // Close or open the offcanvas on window resize
    window.addEventListener('resize', function() {
    closeOffcanvas(offcanvasInstance);
    openOffcanvas(offcanvasInstance);
    });
});