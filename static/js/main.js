function filterVideos(){let q=document.getElementById('search').value.toLowerCase();document.querySelectorAll('.card').forEach(c=>{c.style.display=c.dataset.title.includes(q)?'':'none'})}
