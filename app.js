document.getElementById('quizForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Collect API keys and subject
    const subject = document.getElementById('subject').value;
    const apiKey1 = document.getElementById('apiKey1').value;
    const apiKey2 = document.getElementById('apiKey2').value;
    const apiKey3 = document.getElementById('apiKey3').value;
    if (!apiKey1) { alert('At least one Gemini API key is required'); return; }

    // Send data to backend via fetch
    document.getElementById('result').innerText = 'Generating questions...';
    let res = await fetch('/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({subject, keys: [apiKey1, apiKey2, apiKey3].filter(Boolean)})
    });
    let questions = await res.json();
    document.getElementById('result').innerText = questions.join('\n\n');
    document.getElementById('saveDoc').style.display = 'block';
});

// Save .doc
function saveDocFile(questions) {
    const content = questions.join('\n\n');
    const blob = new Blob([content], {type: 'application/msword'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'cbse-quiz.doc';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// On Save
let generatedQuestions = [];
document.getElementById('saveDoc').addEventListener('click', function() {
    let text = document.getElementById('result').innerText.trim();
    let questions = text.split('\n\n');
    saveDocFile(questions);
});
