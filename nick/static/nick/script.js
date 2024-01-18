'use strict';

function App() {
  const [count, setCount] = React.useState(0);
  function updateCount() {
    setCount(count + 1);
  }
  return React.createElement("div", null, React.createElement("h1", null, count), React.createElement("button", {
    onClick: updateCount
  }, "Count"));
}
document.addEventListener("DOMContentLoaded", () => ReactDOM.render(React.createElement(App, null), document.querySelector("#app")));
