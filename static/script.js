const descMap = {
    caesar_encrypt: "Caesar Cipher shifts characters by a fixed key.",
    caesar_decrypt: "Reverses Caesar Cipher using the same shift.",
    base64_encrypt: "Encodes text into Base64 format.",
    base64_decrypt: "Decodes Base64 encoded text.",
    aes_encrypt: "AES is a secure symmetric encryption algorithm.",
    aes_decrypt: "Decrypts AES encrypted data using the same key."
};

function runAlgo(algo) {
    desc.innerText = descMap[algo];

    fetch("/process", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            text: text.value,
            key: key.value,
            algorithm: algo
        })
    })
    .then(r => r.json())
    .then(d => result.innerText = d.result);
}

function copyText() {
    navigator.clipboard.writeText(result.innerText);
}

text.addEventListener("input", () => {
    let s = 0, v = text.value;
    if (v.length >= 6) s++;
    if (/[A-Z]/.test(v)) s++;
    if (/[0-9]/.test(v)) s++;
    if (/[^A-Za-z0-9]/.test(v)) s++;

    strength.style.width = `${s*25}%`;
    strength.style.background =
        ["#ef4444","#f97316","#facc15","#22c55e"][s-1] || "transparent";
});

function toggleTheme() {
    const body = document.body;
    const icon = document.getElementById("themeIcon");

    body.classList.toggle("light");

    if (body.classList.contains("light")) {
        icon.textContent = "☀️";  // light mode
    } else {
        icon.textContent = "🌙";  // dark mode
    }
}

