window.addEventListener('DOMContentLoaded', function() {
    // Get the current URL path
    var currentPath = window.location.pathname;

    // Function to disable beforeunload event listener
    function disableBeforeUnload() {
        window.removeEventListener('beforeunload', handleBeforeUnload);
    }

    // Function to handle the beforeunload event
    function handleBeforeUnload(e) {
        e.preventDefault();
        e.returnValue = '';
    }

    // Check if the current URL matches the create or update pages
    if (currentPath === '/create/' || currentPath.startsWith('/update/')) {
        // Add the beforeunload event listener
        window.addEventListener('beforeunload', handleBeforeUnload);

        // Select the form element and listen for the submit event
        var form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', disableBeforeUnload);
        }
    }
});
