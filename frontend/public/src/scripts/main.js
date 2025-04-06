let allJobs = []; // This will store all jobs fetched from the API
let filteredJobs = []; // This will store the filtered jobs
let currentPage = 1;
const jobsPerPage = 10;

// Initialize a blank histogram
function initializeBlankHistogram() {
    const ctx = document.getElementById('histogramChart').getContext('2d');

    // Create a chart with empty data
    window.histogramChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [], // No labels initially
            datasets: [{
                label: 'Number of Listings',
                data: [], // No data initially
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Allow custom sizing
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Listings'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

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
        renderHistogram(); // Render the histogram with the fetched data
        renderSalaryHistogram(); // For salary distribution histogram
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

            // Render the histogram if the "Posting Date Analysis" tab is clicked
            if (tab.getAttribute('href') === '#Posting-Date-Analysis') {
                renderHistogram();
            }
        });
    });
}

// Apply filters based on checkbox selections
function applyFilters() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const filterByDate = document.getElementById('filter-by-date').checked;
    const filterBySalary = document.getElementById('filter-by-salary').checked;

    filteredJobs = allJobs.filter(job => {
        const hasDate = job.date_listed !== "Date not provided";
        const hasSalary = job.salary !== "No salary range listed";
        const matchesSearch = job.title.toLowerCase().includes(searchTerm);

        // Apply search term and checkbox filters
        if (filterByDate && filterBySalary) {
            return matchesSearch && hasDate && hasSalary;
        } else if (filterByDate) {
            return matchesSearch && hasDate;
        } else if (filterBySalary) {
            return matchesSearch && hasSalary;
        } else {
            return matchesSearch;
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

// Render the histogram based on user selections
function renderHistogram() {
    const granularity = document.getElementById('granularity').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    // Filter jobs by date range
    const jobsInRange = allJobs.filter(job => {
        if (job.date_listed === "Date not provided") return false;

        const [day, month, year] = job.date_listed.split('/');
        const jobDate = new Date(`${year}-${month}-${day}`);

        const start = startDate ? new Date(startDate) : null;
        const end = endDate ? new Date(endDate) : null;

        return (!start || jobDate >= start) && (!end || jobDate <= end);
    });

    // Group jobs by the selected granularity
    const groupedData = {};
    jobsInRange.forEach(job => {
        const [day, month, year] = job.date_listed.split('/');
        const jobDate = new Date(`${year}-${month}-${day}`);

        let label;
        if (granularity === 'day') {
            label = jobDate.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
        } else if (granularity === 'week') {
            const weekStart = new Date(jobDate);
            weekStart.setDate(jobDate.getDate() - jobDate.getDay()); // Start of the week (Sunday)
            label = `Week of ${weekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`;
        } else if (granularity === 'month') {
            label = jobDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
        }

        if (!groupedData[label]) {
            groupedData[label] = 0;
        }
        groupedData[label]++;
    });

    // Sort labels chronologically
    const sortedLabels = Object.keys(groupedData).sort((a, b) => {
        return new Date(a) - new Date(b);
    });

    // Prepare data for Chart.js
    const labels = sortedLabels;
    const data = sortedLabels.map(label => groupedData[label]);

    // Get the canvas element
    const ctx = document.getElementById('histogramChart').getContext('2d');

    // Destroy the existing chart if it exists
    if (window.histogramChart) {
        window.histogramChart.destroy();
    }

    // Create the chart
    window.histogramChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Listings',
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Allow custom sizing
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Listings'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Initialize salary distribution histogram
function initializeSalaryHistogram() {
    const ctx = document.getElementById('salaryHistogramChart').getContext('2d');

    window.salaryHistogramChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Number of Jobs',
                data: [],
                backgroundColor: 'rgba(153, 102, 255, 0.5)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Jobs'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Salary Range'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.parsed.y} jobs`;
                        },
                        title: function(context) {
                            return context[0].label;
                        }
                    }
                }
            }
        }
    });
}

// Extract numerical salary from string (handles formats like "$50,000 - $70,000")
function extractSalaryValue(salaryStr) {
    if (!salaryStr || salaryStr === "No salary range listed") return null;

    // Handle different salary formats
    const match = salaryStr.match(/\$?([0-9,]+)/);
    if (!match) return null;

    // Take the first number found (for ranges, this will be the lower bound)
    return parseInt(match[1].replace(/,/g, ''), 10);
}

// Render salary distribution histogram
function renderSalaryHistogram() {
    const binSize = parseInt(document.getElementById('salary-bin-size').value, 10);

    // Extract salaries and filter out nulls
    const salaries = allJobs
        .map(job => extractSalaryValue(job.salary))
        .filter(val => val !== null);

    if (salaries.length === 0) {
        console.log("No salary data available");
        return;
    }

    // Find min and max salary
    const minSalary = Math.min(...salaries);
    const maxSalary = Math.max(...salaries);

    // Create bins
    const bins = {};
    const start = Math.floor(minSalary / binSize) * binSize;
    const end = Math.ceil(maxSalary / binSize) * binSize;

    // Initialize bins
    for (let i = start; i < end; i += binSize) {
        const rangeLabel = `$${i.toLocaleString()} - $${(i + binSize).toLocaleString()}`;
        bins[rangeLabel] = 0;
    }

    // Count salaries in each bin
    salaries.forEach(salary => {
        const binIndex = Math.floor(salary / binSize);
        const rangeStart = binIndex * binSize;
        const rangeLabel = `$${rangeStart.toLocaleString()} - $${(rangeStart + binSize).toLocaleString()}`;
        bins[rangeLabel]++;
    });

    // Prepare data for chart
    const labels = Object.keys(bins);
    const data = Object.values(bins);

    // Update chart
    if (window.salaryHistogramChart) {
        window.salaryHistogramChart.data.labels = labels;
        window.salaryHistogramChart.data.datasets[0].data = data;
        window.salaryHistogramChart.update();
    }
}


// Add event listener for the "Update Histogram" button
document.getElementById('update-histogram').addEventListener('click', renderHistogram);
document.getElementById('update-salary-histogram').addEventListener('click', renderSalaryHistogram);

// Add event listeners for checkboxes
document.getElementById('filter-by-date').addEventListener('change', applyFilters);
document.getElementById('filter-by-salary').addEventListener('change', applyFilters);

// Add event listener for search button
document.getElementById('search-input').addEventListener('input', applyFilters);

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    initializeBlankHistogram(); // Initialize a blank histogram
    initializeSalaryHistogram();
    fetchJobs(); // Fetch jobs and render the histogram
    setupTabs(); // Set up tab navigation
});
