'use strict';

const transitionTime = 250;

document.addEventListener("DOMContentLoaded", () => {

  document.querySelector(".start-button").addEventListener('click', (e) => fetchQuiz(e));

});


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

function initializeQuiz(questions, target) {
  const quizWrapper = initializeQuestions(questions);
  target.append(quizWrapper)
  const question_total = questions.questions.length;

  const nextButtons = document.querySelectorAll(".next-btn")
  nextButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const current_question = e.target.parentElement;
      const index = Number(current_question.dataset.question_id);
      

      current_question.style.opacity = '0';
      setTimeout(() => {
        current_question.style.display = "none";
      }, transitionTime)

      if (question_total > (index + 1)) {
        document.querySelector(`#question-${index + 1}`).style.display = "block";
        setTimeout(() => {
          document.querySelector(`#question-${index + 1}`).style.opacity = '1';
        }, transitionTime)
      }
      else {
        const answers_list = document.querySelectorAll(".selected");
        let answers_obj = {}
        for (let i = 0; i < answers_list.length; i++) {
          if (answers_list[i].dataset.relation === "xor" || answers_list[i].dataset.relation === "img") {
            answers_obj[answers_list[i].dataset.question_id] = answers_list[i].dataset.answer_id
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

        for (let i = 0; i < question_total; i++) {
          if (answers_obj[i] == undefined)
          {
            answers_obj[i] = "false";
          }
        }
        // This is the object we will send in POST!!
        console.log(answers_obj)
      }
    })
  });

  const prevButtons = document.querySelectorAll(".back-btn")
  prevButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const current_question = e.target.parentElement.parentElement;
      const index = Number(current_question.dataset.question_id);
      current_question.style.opacity = '0';
      setTimeout(() => {
        current_question.style.display = "none";
      }, transitionTime)

      if (0 <= (index - 1)) {
        document.querySelector(`#question-${index - 1}`).style.display = 'block';
        setTimeout(() => {
          document.querySelector(`#question-${index - 1}`).style.opacity = '1';
        }, transitionTime)
      }
    })
  });

  document.querySelector(`#question-0`).style.display = "block";
  setTimeout(() => {
    document.querySelector(`#question-0`).style.opacity = '1';
  }, transitionTime)
}

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

    if (question.Select === "and") {
      const subtitle = document.createElement('div');
      subtitle.className = "question-wrapper__question-subtitle";
      subtitle.innerHTML = "Multiple answers are possible";
      titleWrapper.append(subtitle);
    }
    questionBox.append(titleWrapper);

    const answers = document.createElement('ul');
    answers.className = "option-box";
    answers.dataset.relation = question.Select;
    question.Options.forEach((option, option_index) => {
      const li = document.createElement('li');
      
      const icon = document.createElement('i')
      icon.className = "fa-regular fa-square"

      const textSpan = document.createElement('span');
      textSpan.innerHTML = `${option[1]}`;

      li.append(icon, textSpan);

      li.dataset.answer_id = `${option[0]}`;
      li.dataset.question_id = `${index}`;
      li.dataset.relation = question.Select;
      li.className = 'option-box__li unselected';
      li.id = `answer-question-${index}`
      if (question.Select === "xor" || question.Select === "img") {
        li.addEventListener('click', () => {
          const other_answers = document.querySelectorAll(`#${li.id}`)
          other_answers.forEach(element => {
            element.className = 'option-box__li unselected';
            element.querySelector('i').className = "fa-regular fa-square"
          }

          )
          li.className = 'option-box__li selected';
          li.querySelector('i').className = "fa-regular fa-square-check"

          document.querySelector(`#next-btn-${index}`).style.display = "block";
        });
      }
      else if (question.Select === "and") {
        li.addEventListener('click', () => {
          if (option_index == 0) {
            const other_answers = document.querySelectorAll(`#${li.id}`)
            other_answers.forEach(element => {
              element.className = 'option-box__li unselected';
              element.querySelector('i').className = "fa-regular fa-square"
            })
          }
          else {
            document.querySelectorAll(`#${li.id}`)[0].className = 'option-box__li unselected';
            document.querySelectorAll(`#${li.id}`)[0].querySelector('i').className = "fa-regular fa-square"
          }

          if (li.className === 'option-box__li selected') {
            li.className = 'option-box__li unselected';
            li.querySelector('i').className = "fa-regular fa-square"
          }
          else {
            li.className = 'option-box__li selected';
            li.querySelector('i').className = "fa-regular fa-square-check"
          }


          document.querySelector(`#next-btn-${index}`).style.display = "block";
        }
        );
      }
      answers.append(li);
    });
    questionBox.append(answers);

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
    nextButton.dataset.question_id = `${index}`

    questionBox.append(nextButton)
    questionBox.style.display = "none";
    questionBox.style.opacity = '0';
    quizWrapper.append(questionBox);
  });
  return quizWrapper;
}
