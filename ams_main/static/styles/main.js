document.addEventListener('DOMContentLoaded', function () {
	const sidebarToggle = document.getElementById('sidebar-toggle');
	const hamburgerIcon = document.querySelector('.hamburger-icon');
  
	// Add event listener to the hamburger icon
	hamburgerIcon.addEventListener('click', function () {
	  sidebarToggle.checked = !sidebarToggle.checked; // Toggle the checked state
	});
  });
  