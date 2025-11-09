document.getElementById('quizForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Collect class, subject and API keys
    const classInput = document.getElementById('class').value;
    const subject = document.getElementById('subject').value;
    const apiKey1 = document.getElementById('apiKey1').value;
    const apiKey2 = document.getElementById('apiKey2').value;
    const apiKey3 = document.getElementById('apiKey3').value;

    // Determine whether to use pre-made or generated based on API keys
    document.getElementById('result').innerText = 'Fetching questions...';
    let questions = [];

    if (!classInput || !subject) {
      alert('Please enter class (10th or 12th) and subject');
      return;
    }

    if (apiKey1 || apiKey2 || apiKey3) {
      // Use live generation
      let res = await fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({subject, keys: [apiKey1, apiKey2, apiKey3].filter(Boolean)})
      });
      questions = await res.json();
    } else {
      // Use pre-made
      let res = await fetch('/premade', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({class: classInput, subject: subject})
      });
      questions = await res.json();
    }

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
