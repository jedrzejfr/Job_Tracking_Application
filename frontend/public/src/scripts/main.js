// Sample data (replace with your API fetch logic)
let allJobs = []; // This will store all jobs fetched from the API
let currentPage = 1;
const jobsPerPage = 10;

// Fetch jobs from the API
async function fetchJobs() {
    try {
        const response = await fetch('http://localhost:5000/jobs');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        allJobs = await response.json();
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
    const jobsToDisplay = allJobs.slice(startIndex, endIndex);

    jobsToDisplay.forEach(job => {
        const jobCard = document.createElement('div');
        jobCard.classList.add('job-card');

        jobCard.innerHTML = `
            <h2>${job.title}</h2>
            <p><strong>Company:</strong> ${job.company}</p>
            <p><strong>Location:</strong> ${job.location}</p>
            <p><strong>Salary:</strong> ${job.salary}</p>
            <p><strong>Link:</strong> <a href="${job.link}" target="_blank">Apply Here</a></p>
            <p><strong>Posted:</strong> ${job.date_listed}</p>
            <p><strong>Source:</strong> ${job.source}</p>
        `;

        jobListings.appendChild(jobCard);
    });
}

// Set up pagination buttons
function setupPagination() {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = ''; // Clear existing buttons

    const totalPages = Math.ceil(allJobs.length / jobsPerPage);

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

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    fetchJobs();
    setupTabs();
});