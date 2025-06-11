const totalViewChart =  document.getElementById('total-views-chart')
const revenueChart = document.getElementById('growth-rate')
const growthRatheChart = document.getElementById('growth-rate-chart')


new Chart (totalViewChart,{
    type: 'line',
    data: {
        labels: ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
        datasets: [{
            label: '# of Votes',
            data: [12545, 19512, 37897, 24574, 29564, 44547],
            borderWidth: 1
        
          }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
          }
    }     
})