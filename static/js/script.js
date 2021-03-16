let englishToYoruba;

window.onload = () => {
  // Submit event listener
  document.getElementById('word-submit').addEventListener('click', getResultsFromServer);

  // Add tones
  createAndDisplayYorubaTones();
  
  // Global mode event listener
  document.getElementById('mode').addEventListener('change', changeGlobalDictMode);

  // Sets the global dictionary mode. If false, mode is Yoruba to english.
  englishToYoruba = true;
}

function getResultsFromServer(){
  if (englishToYoruba) {
    getEnglishWordFromServer();
  } else {
    getYorubaWordFromServer();
  }
}

function changeGlobalDictMode() {
  const modeElement = document.getElementById('mode');
  if (modeElement.selectedIndex == 0) {
    englishToYoruba = true;
    console.log(englishToYoruba);
  } else if (modeElement.selectedIndex == 1){
    englishToYoruba = false;
    console.log(englishToYoruba);
  }
}

function createAndDisplayYorubaTones() {
  const toneList = document.getElementById("tone-buttons");

  const toneCodes = [
    '224', '225', // low tone a, high tone a
    '232', '233', // low tone e, high tone e
    '7865', // e with dot below
    ['7865', '768'], // low tone e with dot below
    ['7865', '769'], // high tone e with dot below
    '236', '237', // low tone i, high tone i
    '242', '243', // low tone o, high tone o
    '7885', // o with dot below
    ['7885', '768'], //low tone o with dot below
    ['7885', '769'], // high tone o with dot below
    '7779', // s with dot below
    '249', '250', // low tone u, high tone u
  ]

  // Create the button each code and assign the event listener,
  // which adds the designated code to the input
  toneCodes.forEach((code) => {
    const el = document.createElement('button');
    // Handles combined underdots
    if (typeof code == 'object') {
      el.innerText = String.fromCharCode(code[0], code[1]);
    } else {
      el.innerText = String.fromCharCode(code);
    }
    
    el.addEventListener('click', () => {
       // Handles combined underdots
      if (typeof code == 'object'){
        document.getElementById('word-input').value += String.fromCharCode(code[0], code[1]);
        return
      } else {
      document.getElementById('word-input').value += String.fromCharCode(code);
      }
    })
    toneList.appendChild(el);
  })

}

function getEnglishWordFromServer() {
  const englishWord = getWordFromHTML();
  fetchEnglish(englishWord);
}

function getYorubaWordFromServer() {
  const yorubaWord = getWordFromHTML();
  fetchYoruba(yorubaWord);
}

function getWordFromHTML() {
  return document.getElementById('word-input').value;
}

function fetchYoruba(word) {
  // Fetches the Yoruba from the python server
  fetch(`/get-yoruba/${word}`)
    .then((response) => {
      return response.json();
    }).then((json) => {
      displayResultsFromServer(json);
    })
}

function fetchEnglish(word) {
  // Fetches the Yoruba from the python server
  fetch(`/get-english/${word}`)
    .then((response) => {
      return response.json();
    }).then((json) => {
      console.log(json);
      displayResultsFromServer(json);
    })
}

function displayResultsFromServer(json) {
  clearPastResults();
  showResultHeader();
  createElsForEachResult(json);
}

function clearPastResults() {
  const childNodes = document.getElementById('each-result').childNodes;
  childNodes.forEach(div => {
    div.innerHTML = '';
  })
}

function showResultHeader() {
  const resultDiv = document.getElementById('result-area');

  // If the results have already beeen gotten at least once
  if (resultDiv.firstChild.innerText == 'Matches:') {
    console.log('here');
    return;
  }
  const resultHeader = document.createElement('h3');
  resultHeader.innerText = "Matches:";

  // Add to the front of the div
  resultDiv.insertBefore(resultHeader, resultDiv.firstChild);
}

function createElsForEachResult(array){
  const definitionDiv = document.getElementById('opposite-definition');
  const partOfSpeechDiv = document.getElementById('part-of-speech');
  const esDiv = document.getElementById('english-sentence');
  const ysDiv = document.getElementById('yoruba-sentence');

  const oppositeDef = array[0];
  const alternativeOppositeDef = array[1];
  const partOfSpeech = array[2];
  const englishSentence = array[3];
  const yorubaSentence = array[4];

  const definitionEl = document.createElement('h3');
  //definitionEl.setAttribute('class', 'result')
  definitionEl.innerText = `Definition(s): ${oppositeDef} ${alternativeOppositeDef}`;

  const partOfSpeechEl = document.createElement('p');
  //partOfSpeechEl.setAttribute('class', 'result');
  partOfSpeechEl.innerText = `Part of Speech: ${partOfSpeech}`;

  const englishSentenceEl = document.createElement('p');
  englishSentenceEl.innerText = `English sentence: ${englishSentence}`;

  const yorubaSentenceEl = document.createElement('p');
  yorubaSentenceEl.innerText = `Yoruba sentence: ${yorubaSentence}`;

  definitionDiv.append(definitionEl);
  partOfSpeechDiv.append(partOfSpeechEl);
  esDiv.append(englishSentenceEl);
  ysDiv.append(yorubaSentenceEl);

  // array.forEach((item) => {
  //   const element = document.createElement('p');
  //   element.setAttribute('class', 'result');
  //   element.innerText = item;
    
  //   resultDiv.append(element);
  // })
}