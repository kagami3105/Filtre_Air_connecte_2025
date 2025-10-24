// function getCookie(name) {
//   const value = `; ${document.cookie}`;
//   const parts = value.split(`; ${name}=`);
//   if (parts.length === 2) return parts.pop().split(';').shift();
// }

// document.addEventListener('DOMContentLoaded', () => {
//   document.querySelectorAll('.card').forEach(card => {
//     const id = card.dataset.id;
//     const statusEl = card.querySelector('.status');
//     const speedEl = card.querySelector('.speed');

//     // Toggle On/Off
//     card.querySelector('.btn-toggle').addEventListener('click', () => {
//       fetch(`/filters/${id}/toggle/`, {
//         method: 'POST',
//         headers: {'X-CSRFToken': getCookie('csrftoken')}
//       }).then(r => r.json()).then(data => {
//         statusEl.textContent = data.status ? "Actif" : "Inactif";
//         statusEl.className = "status " + (data.status ? "on" : "off");
//         card.classList.add("pulse");
//         setTimeout(() => card.classList.remove("pulse"), 500);
//       });
//     });

//     // Vitesse
//     const setSpeed = (val) => {
//       const formData = new FormData();
//       formData.append('fan_speed', val);
//       fetch(`/filters/${id}/speed/`, {
//         method: 'POST',
//         headers: {'X-CSRFToken': getCookie('csrftoken')},
//         body: formData
//       }).then(r => r.json()).then(data => {
//         speedEl.textContent = data.fan_speed;
//         speedEl.style.color = "#4facfe";
//         setTimeout(() => speedEl.style.color = "", 800);
//       });
//     };

//     card.querySelector('.btn-speed-inc').addEventListener('click', () => {
//       setSpeed(parseInt(speedEl.textContent, 10) + 5);
//     });
//     card.querySelector('.btn-speed-dec').addEventListener('click', () => {
//       setSpeed(parseInt(speedEl.textContent, 10) - 5);
//     });
//   });
// });

// document.addEventListener("DOMContentLoaded", () => {
//   document.querySelectorAll(".card").forEach(card => {
//     const id = card.dataset.id;
//     const speedDisplay = card.querySelector(".speed");

//     card.querySelector(".btn-speed-inc").addEventListener("click", () => {
//       updateSpeed(+10);
//     });

//     card.querySelector(".btn-speed-dec").addEventListener("click", () => {
//       updateSpeed(-10);
//     });

//     function updateSpeed(delta) {
//       let current = parseInt(speedDisplay.textContent);
//       let newSpeed = Math.min(100, Math.max(0, current + delta));
//       fetch("/api/fan_speed/", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ speed: newSpeed })
//       })
//         .then(res => res.json())
//         .then(data => {
//           if (data.speed !== undefined) {
//             speedDisplay.textContent = data.speed;
//           }
//         })
//         .catch(err => console.error(err));
//     }
//   });
// });



document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".card").forEach(card => {
    const id = card.dataset.id;
    const speedEl = card.querySelector(".speed");
    const btnInc = card.querySelector(".btn-speed-inc");
    const btnDec = card.querySelector(".btn-speed-dec");

    const updateSpeed = (delta) => {
      let speed = parseInt(speedEl.textContent);
      speed = Math.min(100, Math.max(0, speed + delta));
      speedEl.textContent = speed;

      fetch("/api/fan_speed/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ fan_speed: speed })
      });
    };

    btnInc.addEventListener("click", () => updateSpeed(+10));
    btnDec.addEventListener("click", () => updateSpeed(-10));
  });
});
