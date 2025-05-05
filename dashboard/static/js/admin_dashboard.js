document.addEventListener("DOMContentLoaded", function () {
    // Fetch data from the API
    fetch("/dashboard/api/chart-data/")
        .then(response => response.json())
        .then(data => {
            // Update User Growth Chart
            const userGrowthCtx = document.getElementById("userGrowthChart").getContext("2d");
            new Chart(userGrowthCtx, {
                type: "line",
                data: {
                    labels: data.user_growth.map(item => item.date),
                    datasets: [{
                        label: "User Growth",
                        data: data.user_growth.map(item => item.count),
                        borderColor: "#007bff",
                        backgroundColor: "rgba(0, 123, 255, 0.2)",
                        fill: true,
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                },
            });

            // Update User Distribution Chart
            const userDistributionCtx = document.getElementById("userDistributionChart").getContext("2d");
            new Chart(userDistributionCtx, {
                type: "doughnut",
                data: {
                    labels: ["Doctors", "Patients", "Admins"],
                    datasets: [{
                        data: [
                            data.user_distribution.doctors,
                            data.user_distribution.patients,
                            data.user_distribution.admins,
                        ],
                        backgroundColor: ["#28a745", "#ffc107", "#17a2b8"],
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                },
            });

            // Update Activity Overview Chart
            const activityOverviewCtx = document.getElementById("activityOverviewChart").getContext("2d");
            new Chart(activityOverviewCtx, {
                type: "bar",
                data: {
                    labels: ["Active Users", "Inactive Users"],
                    datasets: [{
                        label: "Activity Overview",
                        data: [
                            data.activity_overview.active_users,
                            data.activity_overview.inactive_users,
                        ],
                        backgroundColor: ["#007bff", "#dc3545"],
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                },
            });
        })
        .catch(error => console.error("Error fetching chart data:", error));
});