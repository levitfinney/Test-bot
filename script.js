async function ask() {
    let q = document.getElementById("q").value;
    let chat = document.getElementById("chat");

    if (!q) return;

    chat.innerHTML += `<p><b>You:</b> ${q}</p>`;

    let res = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ q })
    });

    let data = await res.json();

    chat.innerHTML += `<p><b>AI:</b> ${data.r}</p>`;

    chat.scrollTop = chat.scrollHeight;
    document.getElementById("q").value = "";
}
