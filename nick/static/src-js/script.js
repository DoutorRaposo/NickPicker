//This is the original file with comments, which are excluded from the front-end script by babel
'use strict';

// This global const is used in tandem with the transition in CSS to show up and hide questions
const transitionTime = 250;

// When the content loads, the start button initializes the quiz
document.addEventListener("DOMContentLoaded", () => {

  document.querySelector(".start-button").addEventListener('click', (e) => fetchQuiz(e));

});

// This function gets the quiz info and starts the function that mounts the questions
function fetchQuiz(e) {
  const appdiv = e.target.parentElement.parentElement;
  fetch('questions/')
    .then(response => response.json())
    .then(response => {
      document.querySelector(".index-welcome").style.opacity = '0';
      setTimeout(() => {
        document.querySelector(".index-welcome").style.display = "none";
      }, transitionTime)
      initializeQuiz(response, appdiv);
    })
}

// This function mounts the questions and the functions of the next and back buttons
function initializeQuiz(questions, target) {
  const quizWrapper = initializeQuestions(questions);
  target.append(quizWrapper)
  const question_total = questions.questions.length;

  setNextButton(question_total);

  setBackButton();

  // This is the first question showing up!
  document.querySelector(`#question-0`).style.display = "block";
  setTimeout(() => {
    document.querySelector(`#question-0`).style.opacity = '1';
  }, transitionTime)
}

//This function sets up the back button to hide the current question and show the next one
function setBackButton() {
  const prevButtons = document.querySelectorAll(".back-btn");
  prevButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const current_question = e.target.parentElement.parentElement;
      const index = Number(current_question.dataset.question_id);
      current_question.style.opacity = '0';
      setTimeout(() => {
        current_question.style.display = "none";
      }, transitionTime);

      if (0 <= (index - 1)) {
        setTimeout(() => {
          document.querySelector(`#question-${index - 1}`).style.display = 'block';
          document.querySelector(`#question-${index - 1}`).style.opacity = '1';
        }, transitionTime);
      }
    });
  });
}

// This function sets up the next button to hide current question and show the next one
function setNextButton(question_total) {
  const nextButtons = document.querySelectorAll(".next-btn");
  nextButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const current_question = e.target.parentElement;
      const index = Number(current_question.dataset.question_id);

      current_question.style.opacity = '0';
      setTimeout(() => {
        current_question.style.display = "none";
      }, transitionTime);

      if (question_total > (index + 1)) {
        document.querySelector(`#question-${index + 1}`).style.display = "block";
        setTimeout(() => {
          document.querySelector(`#question-${index + 1}`).style.opacity = '1';
        }, transitionTime);
      }
      // If the question is the last one, then we will start to check the results server-side
      else {
        getResults(question_total);
      }
    });
  });
}

function getResults(question_total) {
  const answers_list = document.querySelectorAll(".selected");
  let answers_obj = {};
  // Check every "selected" class as answers and collects to object that we'll use for the results
  for (let i = 0; i < answers_list.length; i++) {
    if (answers_list[i].dataset.relation === "xor" || answers_list[i].dataset.relation === "img") {
      answers_obj[answers_list[i].dataset.question_id] = answers_list[i].dataset.answer_id;
    }
    else if (answers_list[i].dataset.relation === "and") {
      if (answers_obj[answers_list[i].dataset.question_id] == undefined) {
        answers_obj[answers_list[i].dataset.question_id] = [answers_list[i].dataset.answer_id];
      }
      else {
        answers_obj[answers_list[i].dataset.question_id].push(answers_list[i].dataset.answer_id);
      }
    }
  }
  // If the user managed to select none of the answers by any means, we set it to false
  for (let i = 0; i < question_total; i++) {
    if (answers_obj[i] == undefined) {
      answers_obj[i] = "false";
    }
  }
  // This is the object we will send in POST!!
  console.log(answers_obj);
}

// Constructs all questions and answers elements
function initializeQuestions(questions) {
  const quizWrapper = document.createElement('div');
  quizWrapper.className = "quiz-wrapper";

  questions.questions.forEach((question, index) => {
    const questionBox = document.createElement('div');
    questionBox.className = 'question-box';
    questionBox.id = `question-${index}`;
    questionBox.dataset.question_id = `${index}`;

    const titleWrapper = document.createElement('div');
    titleWrapper.className = 'question-wrapper';
    const title = document.createElement('div');
    title.className = 'question-wrapper__question-title';
    title.innerHTML = `${index + 1}. ${question.Title}`;
    titleWrapper.append(title);

    // Subtitles are only for multiple choice questions
    if (question.Select === "and") {
      const subtitle = document.createElement('div');
      subtitle.className = "question-wrapper__question-subtitle";
      subtitle.innerHTML = "Multiple answers are possible";
      titleWrapper.append(subtitle);
    }
    questionBox.append(titleWrapper);

    // If answers are big list, spread'em out
    const answers = document.createElement('ul');
    if (question.Options.length < 12) {
      answers.className = "option-box";
    }
    else {
      answers.className = "option-box big";
    }
  
    answers.dataset.relation = question.Select;
    question.Options.forEach((option, option_index) => {
      const li = document.createElement('li');

      // If the type is image, we don't need the checkbox, but otherwise we add it
      if (question.Select === "img") {
        const divGif = document.createElement('div');
        divGif.className = 'gif-container';
        const imgGif = document.createElement('img')
        imgGif.className = 'gif-container__img';
        imgGif.src = `${option[1]}`;
        const spanText = document.createElement('span');
        spanText.className = 'gif-container__title';
        spanText.innerHTML = `${option[0]}`;
        divGif.append(imgGif, spanText);
        li.append(divGif);
      }
      else {
        const icon = document.createElement('i')
        icon.className = "fa-regular fa-square"

        const textSpan = document.createElement('span');
        textSpan.innerHTML = `${option[1]}`;
        li.append(icon, textSpan);
      }

      li.dataset.answer_id = `${option[0]}`;
      li.dataset.question_id = `${index}`;
      li.dataset.relation = question.Select;
      li.className = 'option-box__li unselected';
      li.id = `answer-question-${index}`
      createAnswers(question, li, index, option_index);
      answers.append(li);
    });
    questionBox.append(answers);

    // Back button don't exist for the first question
    if (index != 0) {
      const backButton = document.createElement('div')
      backButton.className = "back-btn-wrapper";
      backButton.id = `wrapper-back-btn-${index}`;
      const spanButton = document.createElement('span')
      spanButton.innerHTML = "< Back";
      spanButton.className = "back-btn";
      spanButton.id = `back-btn-${index}`;
      backButton.append(spanButton);
      questionBox.append(backButton);
    };

    const nextButton = document.createElement('div');
    nextButton.className = "next-btn";
    nextButton.id = `next-btn-${index}`;
    if (index + 1 === questions.questions.length) {
      nextButton.innerHTML = "Check Results";
    }
    else {
      nextButton.innerHTML = "Next";
    }
    nextButton.style.display = "none";
    nextButton.style.opacity = "0";
    nextButton.dataset.question_id = `${index}`

    questionBox.append(nextButton)
    questionBox.style.display = "none";
    questionBox.style.opacity = '0';
    quizWrapper.append(questionBox);
  });
  return quizWrapper;
}

// Builds every answers for every question
function createAnswers(question, li, index, option_index) {

  // For every type of question, a different path in building
  if (question.Select === "xor") {
    li.addEventListener('click', () => {
      const other_answers = document.querySelectorAll(`#${li.id}`);
      other_answers.forEach(element => {
        element.className = 'option-box__li unselected';
        element.querySelector('i').className = "fa-regular fa-square";
      }

      );
      li.className = 'option-box__li selected';
      li.querySelector('i').className = "fa-regular fa-square-check";

      setTimeout(() => {
        document.querySelector(`#next-btn-${index}`).style.display = "block";
        document.querySelector(`#next-btn-${index}`).style.opacity = '1';
      }, transitionTime / 2);
    });
  }
  else if (question.Select === "img") {
    li.addEventListener('click', () => {
      const other_answers = document.querySelectorAll(`#${li.id}`);
      other_answers.forEach(element => {
        element.className = 'option-box__li unselected';
      }

      );
      li.className = 'option-box__li selected';

      setTimeout(() => {
        document.querySelector(`#next-btn-${index}`).style.display = "block";
        document.querySelector(`#next-btn-${index}`).style.opacity = '1';
      }, transitionTime / 2);
    });
  }
  else if (question.Select === "and") {
    li.addEventListener('click', () => {
      if (option_index == 0) {
        const other_answers = document.querySelectorAll(`#${li.id}`);
        other_answers.forEach(element => {
          element.className = 'option-box__li unselected';
          element.querySelector('i').className = "fa-regular fa-square";
        });
      }
      else {
        document.querySelectorAll(`#${li.id}`)[0].className = 'option-box__li unselected';
        document.querySelectorAll(`#${li.id}`)[0].querySelector('i').className = "fa-regular fa-square";
      }

      if (li.className === 'option-box__li selected') {
        li.className = 'option-box__li unselected';
        li.querySelector('i').className = "fa-regular fa-square";
      }
      else {
        li.className = 'option-box__li selected';
        li.querySelector('i').className = "fa-regular fa-square-check";
      }

      setTimeout(() => {
        document.querySelector(`#next-btn-${index}`).style.display = "block";
        document.querySelector(`#next-btn-${index}`).style.opacity = '1';
      }, transitionTime / 2);

    }
    );
  }
}

