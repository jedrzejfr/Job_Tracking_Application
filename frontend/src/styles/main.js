async function fetchJobs() {
    try {
        const response = await fetch('http://localhost:5000/jobs');
        const jobs = await response.json();
        displayJobs(jobs);
    } catch (error) {
        console.error('Error fetching jobs:', error);
    }
}

function displayJobs(jobs) {
    const jobListings = document.getElementById('job-listings');
    jobListings.innerHTML = ''; // Clear existing content

    jobs.forEach(job => {
        const jobCard = document.createElement('div');
        jobCard.classList.add('job-card');

        jobCard.innerHTML = `
            <h2>${job.title}</h2>
            <p><strong>Company:</strong> ${job.company}</p>
            <p><strong>Location:</strong> ${job.location}</p>
            <p><strong>Salary:</strong> ${job.salary}</p>
            <p><strong>Type:</strong> ${job.type}</p>
            <p><strong>Posted:</strong> ${job.date_listed}</p>
            <p><strong>Link:</strong> <a href="${job.link}" target="_blank">Apply Here</a></p>
            <p><strong>Source:</strong> ${job.source}</p>
        `;

        jobListings.appendChild(jobCard);
    });
}

document.addEventListener('DOMContentLoaded', fetchJobs);