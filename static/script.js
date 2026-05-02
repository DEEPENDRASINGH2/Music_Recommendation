// ===============================
// 🚀 RUN AFTER DOM LOAD (IMPORTANT)
// ===============================
document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("searchBox");
    const box = document.getElementById("suggestions");
    const form = document.getElementById("searchForm");

    // ===============================
    // 🎤 VOICE SEARCH
    // ===============================
    window.startVoice = function () {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "en-US";

        recognition.onresult = function (event) {
            input.value = event.results[0][0].transcript;
            form.submit(); // 🔥 auto search
        };

        recognition.start();
    };

    // ===============================
    // 🎯 MOOD SET (FIXED)
    // ===============================
    window.setMood = function (mood) {
        input.value = mood;
        form.submit(); // 🔥 auto search
    };

    // ===============================
    // ▶️ PLAY (YouTube)
    // ===============================
    window.playSong = function (song) {
        window.open("https://www.youtube.com/results?search_query=" + song, "_blank");
    };

    // ===============================
    // ▶ OPEN DIRECT VIDEO
    // ===============================
    window.openSong = function (url) {
        if (url) {
            window.open(url, "_blank");
        }
    };

    // ===============================
    // 🔍 SMART SEARCH (SAFE)
    // ===============================
    if (input && box) {
        input.addEventListener("input", function () {
            let q = input.value;

            if (q.length < 2) {
                box.innerHTML = "";
                return;
            }

            fetch(`/suggest?q=${q}`)
                .then(res => res.json())
                .then(data => {
                    box.innerHTML = "";

                    data.forEach(song => {
                        let div = document.createElement("div");
                        div.innerText = song;
                        div.classList.add("suggest-item");

                        div.onclick = () => {
                            input.value = song;
                            box.innerHTML = "";
                            form.submit(); // 🔥 auto search
                        };

                        box.appendChild(div);
                    });
                })
                .catch(() => {
                    box.innerHTML = "";
                });
        });
    }

    // ===============================
    // 🌌 PARTICLE BACKGROUND (OPTIMIZED)
    // ===============================
    const canvas = document.createElement("canvas");
    canvas.style.position = "fixed";
    canvas.style.top = 0;
    canvas.style.left = 0;
    canvas.style.zIndex = "-1";
    document.body.appendChild(canvas);

    const ctx = canvas.getContext("2d");

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    let particles = [];

    for (let i = 0; i < 50; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            r: Math.random() * 2,
            dx: (Math.random() - 0.5) * 0.4,
            dy: (Math.random() - 0.5) * 0.4
        });
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = "#00ffff";
            ctx.fill();

            p.x += p.dx;
            p.y += p.dy;

            if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
        });

        requestAnimationFrame(animateParticles);
    }

    animateParticles();

    // ===============================
    // ✨ MOUSE GLOW (SOFT)
    // ===============================
    const glow = document.createElement("div");
    glow.style.position = "fixed";
    glow.style.width = "180px";
    glow.style.height = "180px";
    glow.style.borderRadius = "50%";
    glow.style.pointerEvents = "none";
    glow.style.background =
        "radial-gradient(circle, rgba(0,255,255,0.15) 0%, transparent 70%)";
    glow.style.zIndex = "0";

    document.body.appendChild(glow);

    document.addEventListener("mousemove", (e) => {
        glow.style.left = e.clientX - 90 + "px";
        glow.style.top = e.clientY - 90 + "px";
    });

    // ===============================
    // 🎧 CARD HOVER (FIXED)
    // ===============================
    document.addEventListener("mouseover", (e) => {
        const card = e.target.closest(".neon-card");
        if (card) {
            card.style.boxShadow = "0 0 25px #0ff";
        }
    });

    document.addEventListener("mouseout", (e) => {
        const card = e.target.closest(".neon-card");
        if (card) {
            card.style.boxShadow = "0 0 10px #0ff2";
        }
    });

    // ===============================
    // 🚀 FLOATING EFFECT (SAFE)
    // ===============================
    const cards = document.querySelectorAll(".neon-card");

    cards.forEach((card, index) => {
        card.style.animation = `float ${4 + index * 0.2}s ease-in-out infinite`;
    });

    const style = document.createElement("style");
    style.innerHTML = `
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }`;
    document.head.appendChild(style);

});