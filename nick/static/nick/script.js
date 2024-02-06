'use strict';

document.addEventListener("DOMContentLoaded", () => {

  document.querySelector(".start-button").addEventListener('click', (e) => startQuiz(e));

});


function startQuiz(e) {
  const appdiv = e.target.parentElement.parentElement;
  fetch('questions/')
    .then(response => response.json())
    .then(response => {
      document.querySelector(".index-welcome").style.display = "none"
      mountQuestions(response, appdiv);
    })
}

function mountQuestions(questions, target) {
  const quizWrapper = document.createElement('div');
  quizWrapper.className = "quiz-wrapper"

  questions.questions.forEach((question, index) => {
    const questionBox = document.createElement('div');
    questionBox.className = 'question-box';
    questionBox.id = `question-${index}`;

    const titleWrapper = document.createElement('div')
    titleWrapper.className = 'question-wrapper'
    const title = document.createElement('div');
    title.className = 'question-wrapper__question-title';
    title.innerHTML = `${index + 1}. ${question.Title}`;
    titleWrapper.append(title)
    

    if (question.Select === "or") {
      const subtitle = document.createElement('div');
      subtitle.className = "question-wrapper__question-subtitle"
      subtitle.innerHTML = "Multiple answers are possible";
      titleWrapper.append(subtitle)
    }
    questionBox.append(titleWrapper)

    const answers = document.createElement('ul')
    answers.className = "option-box"
    question.Options.forEach(option => {
      const li = document.createElement('li')
      li.innerHTML = `${option}`
      li.className = 'option-box__li'
      answers.append(li)
    });
    questionBox.append(answers);

    quizWrapper.append(questionBox);
  })
  target.append(quizWrapper)
}