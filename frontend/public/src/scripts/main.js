async function fetchJobs() {
    try {
        console.log('Fetching jobs...');  // Debugging
        const response = await fetch('http://localhost:5000/jobs');
        console.log('Response:', response);  // Debugging
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const jobs = await response.json();
        console.log('Jobs:', jobs);  // Debugging
        displayJobs(jobs);
    } catch (error) {
        console.error('Error fetching jobs:', error);
    }
}

function displayJobs(jobs) {
    console.log('Displaying jobs:', jobs);  // Debugging
    const jobListings = document.getElementById('job-listings');
    if (!jobListings) {
        console.error('Element with id "job-listings" not found!');
        return;
    }
    jobListings.innerHTML = ''; // Clear existing content

    jobs.forEach(job => {
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

document.addEventListener('DOMContentLoaded', fetchJobs);