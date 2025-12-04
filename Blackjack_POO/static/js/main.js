document.addEventListener("DOMContentLoaded", () => {
    const clickSfx = document.getElementById("sfx-click");
    const cardSfx  = document.getElementById("sfx-card");
    const winSfx   = document.getElementById("sfx-win");
    const loseSfx  = document.getElementById("sfx-lose");
    const bgMusic  = document.getElementById("music-bg");

    const body = document.body;
    const resultRaw = (body.dataset.result || "").toLowerCase();

    // Petit helper pour jouer un son sans erreur
    const playSafe = (audioEl) => {
        if (!audioEl) return;
        try {
            audioEl.currentTime = 0;
            audioEl.play();
        } catch (e) {
            // les navigateurs peuvent bloquer l'autoplay, on ignore l'erreur
        }
    };

    // On démarre la musique de fond au premier clic (pour éviter le blocage autoplay)
    let bgStarted = false;

    const startBgMusic = () => {
        if (!bgStarted && bgMusic) {
            playSafe(bgMusic);
            bgStarted = true;
        }
    };

    // Sons selon le résultat de la manche
    if (resultRaw === "victoire") {
        playSafe(winSfx);
    } else if (resultRaw === "défaite" || resultRaw === "defaite") {
        playSafe(loseSfx);
    }

    // Sons sur les boutons
    const buttons = document.querySelectorAll(".btn");
    buttons.forEach((btn) => {
        btn.addEventListener("click", () => {
            startBgMusic(); // on lance la musique à la première interaction

            const soundType = btn.dataset.sound || "click";

            if (soundType === "card") {
                playSafe(cardSfx);
            } else {
                playSafe(clickSfx);
            }
        });
    });
});
