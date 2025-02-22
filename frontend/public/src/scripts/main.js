let allJobs = []; // This will store all jobs fetched from the API
let filteredJobs = []; // This will store the filtered jobs
let currentPage = 1;
const jobsPerPage = 10;

// Fetch jobs from the API
async function fetchJobs() {
    try {
        console.log("Fetching jobs...");
        const response = await fetch('http://localhost:5000/jobs');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Jobs data:", data);  // Log the fetched data

        allJobs = data;
        filteredJobs = allJobs; // Initialize filteredJobs with all jobs

        displayJobs(currentPage);
        setupPagination();
    } catch (error) {
        console.error('Error fetching jobs:', error);
    }
}

// Display jobs for the current page
function displayJobs(page) {
    const jobListings = document.getElementById('job-listings');
    jobListings.innerHTML = ''; // Clear existing content

    const startIndex = (page - 1) * jobsPerPage;
    const endIndex = startIndex + jobsPerPage;
    const jobsToDisplay = filteredJobs.slice(startIndex, endIndex);

    jobsToDisplay.forEach(job => {
        const jobCard = document.createElement('div');
        jobCard.classList.add('job-card');

        // Parse the date in "DD/MM/YYYY" format
        let formattedDate = "Date not provided";
        if (job.date_listed && job.date_listed !== "Date not provided") {
            const [day, month, year] = job.date_listed.split('/'); // Split the string into day, month, year
            const dateObj = new Date(`${year}-${month}-${day}`); // Create a valid Date object
            if (!isNaN(dateObj)) { // Check if the date is valid
                formattedDate = dateObj.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
            }
        }

        jobCard.innerHTML = `
            <h2>${job.title}</h2>
            <p><strong>Company:</strong> ${job.company}</p>
            <p><strong>Location:</strong> ${job.location}</p>
            <p><strong>Salary:</strong> ${job.salary}</p>
            <p><strong>Link:</strong> <a href="${job.link}" target="_blank">Apply Here</a></p>
            <p><strong>Posted:</strong> ${formattedDate}</p>
            <p><strong>Source:</strong> ${job.source}</p>
        `;

        jobListings.appendChild(jobCard);
    });

    // Scroll to the top of the job listings
    document.getElementById('current-jobs').scrollIntoView({ behavior: 'smooth' });
}

// Set up pagination buttons
function setupPagination() {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = ''; // Clear existing buttons

    const totalPages = Math.ceil(filteredJobs.length / jobsPerPage);

    // Previous Button
    const prevButton = document.createElement('button');
    prevButton.innerText = 'Previous';
    prevButton.disabled = currentPage === 1;
    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            displayJobs(currentPage);
            setupPagination();
        }
    });
    pagination.appendChild(prevButton);

    // Next Button
    const nextButton = document.createElement('button');
    nextButton.innerText = 'Next';
    nextButton.disabled = currentPage === totalPages;
    nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            displayJobs(currentPage);
            setupPagination();
        }
    });
    pagination.appendChild(nextButton);
}

// Tab Navigation
function setupTabs() {
    const tabs = document.querySelectorAll('nav ul li a');
    const sections = document.querySelectorAll('section');

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();

            // Remove active class from all tabs and sections
            tabs.forEach(t => t.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));

            // Add active class to the clicked tab and corresponding section
            tab.classList.add('active');
            const targetSection = document.querySelector(tab.getAttribute('href'));
            targetSection.classList.add('active');
        });
    });
}

// Apply filters based on checkbox selections
function applyFilters() {
    const filterByDate = document.getElementById('filter-by-date').checked;
    const filterBySalary = document.getElementById('filter-by-salary').checked;

    filteredJobs = allJobs.filter(job => {
        const hasDate = job.date_listed !== "Date not provided";
        const hasSalary = job.salary !== "No salary range listed";

        if (filterByDate && filterBySalary) {
            return hasDate && hasSalary; // Show jobs with both date and salary
        } else if (filterByDate) {
            return hasDate; // Show jobs with date
        } else if (filterBySalary) {
            return hasSalary; // Show jobs with salary
        } else {
            return true; // Show all jobs
        }
    });

    currentPage = 1; // Reset to the first page
    displayJobs(currentPage);
    setupPagination();
}

// Filter jobs by title based on search input
function searchJobs() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    filteredJobs = allJobs.filter(job => job.title.toLowerCase().includes(searchTerm));
    currentPage = 1; // Reset to the first page
    displayJobs(currentPage);
    setupPagination();
}

// Add event listeners for checkboxes
document.getElementById('filter-by-date').addEventListener('change', applyFilters);
document.getElementById('filter-by-salary').addEventListener('change', applyFilters);

// Add event listener for search button
document.getElementById('search-button').addEventListener('click', searchJobs);

// Add event listener for pressing Enter in the search input
document.getElementById('search-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        searchJobs();
    }
});

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    fetchJobs();
    setupTabs();
});